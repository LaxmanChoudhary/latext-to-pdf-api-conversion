import uuid

from flask import Flask, request, send_file, jsonify
import subprocess
import os
from zipfile import ZipFile

app = Flask(__name__)

API_VERSION = "2.0"


def _compile_latex(file_path):
    fdir, _ = os.path.split(file_path)
    fname = os.path.splitext(os.path.basename(file_path))[0]
    output_filename = fname + "-" + str(uuid.uuid4())[:8]

    # rename input file, as tectonic don't have flag to name outputfile
    os.rename(file_path, os.path.join(fdir, output_filename+".tex"))

    # chdir to execute command
    os.chdir(fdir)
    app.logger.info(f"changed directory to {os.getcwd()} and running file {output_filename+'.tex'}")

    # Run Tectonic
    result = subprocess.run(['tectonic', output_filename+".tex"], capture_output=True, text=True)

    if result.returncode != 0:
        # If compilation failed, return the error message
        return None, (f"Tectonic runtime error | {result.stderr}", 500)

    full_output_path = os.path.join(fdir, output_filename + ".pdf")
    return full_output_path, None


def file_contains(filepath, text):
    with open(filepath, "r") as fp:
        data = fp.read()

    return data.__contains__(text)

def _unzip(zip_file_path):
    """
    Returns tuple (filepath, error), one of the value is None
    :param zip_file_path:
    :return:
    """
    tmp_dir = str(uuid.uuid4())[:4]
    zip_container_dir = os.path.join("/tmp", tmp_dir)
    os.makedirs(zip_container_dir)
    try:
        with ZipFile(zip_file_path, 'r') as fzip:
            fzip.extractall(path=zip_container_dir)
    except Exception as ex:
        app.logger.error(ex)
        return None, ("Error while unzipping.", 500)

    tex_file = None
    files = os.listdir(zip_container_dir)
    for filename in files:
        if filename.endswith(".tex") and file_contains(os.path.join(zip_container_dir, filename), "documentclass"):
            tex_file = filename
            break

    if not tex_file:
        return None, ("BAD REQUEST! No file with .tex extension found or no documentclass found", 400)

    return os.path.join(zip_container_dir, tex_file), None

@app.route("/convert", methods=["POST"])
def convert_latex():
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
        output_file, compile_error = _compile_latex(full_file_path)

        if compile_error:
            return compile_error

        return send_file(output_file)

    if extension == "zip":
        file_path, unzip_error = _unzip(full_file_path)

        if unzip_error:
            return unzip_error

        output_file, compile_error = _compile_latex(file_path)

        if compile_error:
            return compile_error

        return send_file(output_file)

    return "Something went wrong.", 500


@app.route('/version', methods=['GET'])
def get_version():
    return f"api version: {API_VERSION}"


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, host="0.0.0.0")
