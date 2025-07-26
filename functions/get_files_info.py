import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    try:
        path = working_directory
        if directory:
            path = os.path.join(working_directory, directory)
        path = os.path.abspath(path)
        working_directory = os.path.abspath(working_directory)
        if not path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        if not os.path.isdir(path):
            return f'Error: "{directory}" is not a directory\n'

        files_info = []
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            size = os.path.getsize(file_path)
            if os.path.isdir(file_path):
                is_dir = True
            else:
                is_dir = False
            files_info.append(f"- {filename}: file_size={size} bytes, is_dir={is_dir}")

    except Exception as e:
        return f"Error: Cannot list {directory} as it is outside the permitted working directory\n"

    return "\n".join(files_info) + "\n"

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