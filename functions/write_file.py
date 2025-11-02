import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Returns the content of a file specified in the file path attribute, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file where and which name the file should written with",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that should be stored to the file"
            )
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    work_dir_abspath = os.path.abspath(working_directory)
    joined_abspath = os.path.abspath(os.path.join(working_directory, file_path))

    if not joined_abspath.startswith(work_dir_abspath):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    directory = os.path.dirname(joined_abspath)

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


    with open(joined_abspath, "w", encoding="utf-8") as f:
        f.write(content)


    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
