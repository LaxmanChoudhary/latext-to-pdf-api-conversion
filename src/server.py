from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)


@app.route('/convert', methods=['POST'])
def convert_latex_to_pdf():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file and file.filename.endswith('.tex'):
        filename = file.filename
        file.save(filename)

        # Convert LaTeX to PDF
        subprocess.run(['pdflatex', filename])

        pdf_filename = filename.replace('.tex', '.pdf')

        # Send the PDF file
        return send_file(pdf_filename, as_attachment=True)

    return 'Invalid file type', 400


if __name__ == '__main__':
    app.run(host="0.0.0.0" ,debug=True)