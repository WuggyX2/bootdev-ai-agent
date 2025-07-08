import os
from config import MAX_FILE_LENGTH


def get_file_content(working_directory: str, file_path: str) -> str:
    """

    Args:
        working_directory:
        file_path:

    Returns:

    """
    work_dir_abspath = os.path.abspath(working_directory)
    joined_abspath = os.path.abspath(os.path.join(working_directory, file_path))

    if not joined_abspath.startswith(work_dir_abspath):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(joined_abspath):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(joined_abspath, "r", encoding="utf-8") as file:
            file_content = file.read(MAX_FILE_LENGTH + 1)

            if len(file_content) > MAX_FILE_LENGTH:
                file_content += f'[...File "{file_path}" truncated at 10000 characters]'

        return file_content
    except Exception as e:
        return f"Error in the standard libary function: {e}"
