import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the python file specified in the file_path attribute, constrained to the working directory. Arguments can be provided with the args attribute",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file that should be executed. Must be included and must be a python file. if not a python file or empty, error is returned",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="list of arguments that should be passed to the executable file",
                items=types.Schema(type=types.Type.STRING)
            )
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=[]) -> str:
    work_dir_abspath = os.path.abspath(working_directory)
    joined_abspath = os.path.abspath(os.path.join(working_directory, file_path))

    if not joined_abspath.startswith(work_dir_abspath):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(joined_abspath):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    output = ""
    try:
        args = ["python", joined_abspath] + args
        result = subprocess.run(args, capture_output=True, text=True, timeout=30, cwd=work_dir_abspath)
        print(args)

        if result.returncode > 0:
            output += f"Process exited with code {result.returncode}\n\n"

        if not result.stdout and not result.stderr:
            output += "No output produced\n"
        else:
            output += f"STDOUT: {result.stdout}\n\n"
            output += f"STDERR: {result.stderr}\n\n"


    except Exception as e:
        output += f"Error: executing Python file: {e}"

    return output
