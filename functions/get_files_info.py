import os
from google.genai import types


CURRENT_DIR = "."

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory: str, directory: str | None = '.') -> str:
    """

    Args:
        working_directory: a directory that the code is allowed to work in
        directory: a path to the target directory the function caller wants list

    Returns: a result string that can be fed to the llm

    """
    if not directory:
        return "Error: directory is empty"

    work_dir_abspath = os.path.abspath(working_directory)
    joined_abspath = os.path.abspath(os.path.join(working_directory, directory))

    if not joined_abspath.startswith(work_dir_abspath):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(joined_abspath):
        return f'Error: "{directory}" is not a directory'

    try:
        dir_items = os.listdir(joined_abspath)
        results = ""

        for item in dir_items:
            file_path = os.path.join(joined_abspath, item)
            results += f"- {item}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n"
    except Exception as e:
        return f"Error in the standard libary function: {e}"

    return results
