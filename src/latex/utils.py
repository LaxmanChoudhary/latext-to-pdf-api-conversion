
def file_contains(filepath, text):
    with open(filepath, "r") as fp:
        data = fp.read()

    return data.__contains__(text)