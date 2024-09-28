import uuid
import os
from zipfile import ZipFile

from .utils import file_contains


def unzip(zip_file_path):
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
