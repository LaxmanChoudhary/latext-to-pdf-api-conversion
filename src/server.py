import jwt
from flask import Flask, request, send_file
import os

import psycopg2
from flask_cors import CORS

from latex import process, unzip
from auth.core import create_jwt
from middleware import auth_token_required

app = Flask(__name__)
CORS(app)

API_VERSION = os.environ.get("API_VERSION", "UNSET")


def _db():
    app.logger.info(os.environ.get("DB_HOST"))
    conn = psycopg2.connect(host=os.environ.get("DB_HOST"),
                            database=os.environ.get("DB_DB"),
                            user=os.environ.get("DB_USER"),
                            password=os.environ.get("DB_PASSWORD"))
    return conn

@app.route("/", methods=["GET"])
def hello():
    return "Hello! Yes api is up but you are supposed to use other endpoint for the purpose."

@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    cur = _db().cursor()
    cur.execute("SELECT email, password FROM \"user\" WHERE email=%s", (auth.username,))
    res = cur.fetchall()
    cur.close()
    _db().close()

    if len(res) > 0:
        # at least one row returned
        user_row = res[0]
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return create_jwt(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401


@app.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers['Authorization']
    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithms="HS256")
    except Exception as ex:
        app.logger.error(ex)
        return "not authorized", 401

    return decoded, 200


@app.route("/convert", methods=["POST"])
@auth_token_required
def convert_latex(*args, **kwargs):
    if len(request.files) == 0:
        return "Bad request! No file attached.", 400

    file = None
    for _ in request.files:
        file = request.files.get(_)
        break

    if not file:
        return "BAD REQUEST! Unable to retrieve file.", 400

    if file.filename == "":
        return "No file selected.", 400

    fname, extension = file.filename.rsplit(".", maxsplit=1)

    if extension not in ["tex", "zip"]:
        return f"Not Acceptable, files required are .tex and .zip", 406

    # save file
    dest = os.path.join("/tmp", file.filename)
    file.save(dst=dest)
    full_file_path = os.path.join("/tmp", file.filename)

    if extension == "tex":
        output_file, compile_error = process.compile_latex(full_file_path)

        if compile_error:
            return compile_error

        return send_file(output_file)

    if extension == "zip":
        file_path, unzip_error = unzip.unzip(full_file_path)

        if unzip_error:
            return unzip_error

        output_file, compile_error = process.compile_latex(file_path)

        if compile_error:
            return compile_error

        return send_file(output_file)

    return "Something went wrong.", 500


@app.route('/version', methods=['GET'])
def get_version():
    return f"api version: {API_VERSION}"


if __name__ == '__main__':
    app.run(debug=os.environ.get("DEBUG", False), host="0.0.0.0")
