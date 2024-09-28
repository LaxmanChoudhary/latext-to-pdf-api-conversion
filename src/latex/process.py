import os
import subprocess
import uuid


def compile_latex(file_path):
    fdir, _ = os.path.split(file_path)
    fname = os.path.splitext(os.path.basename(file_path))[0]
    output_filename = fname + "-" + str(uuid.uuid4())[:8]

    # rename input file, as tectonic don't have flag to name outputfile
    os.rename(file_path, os.path.join(fdir, output_filename+".tex"))

    # chdir to execute command
    os.chdir(fdir)

    # Run Tectonic
    result = subprocess.run(['tectonic', output_filename+".tex"], capture_output=True, text=True)

    if result.returncode != 0:
        # If compilation failed, return the error message
        return None, (f"Tectonic runtime error | {result.stderr}", 500)

    full_output_path = os.path.join(fdir, output_filename + ".pdf")
    return full_output_path, None
