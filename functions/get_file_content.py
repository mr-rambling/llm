import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        file = os.path.abspath(os.path.join(working_directory, file_path))
        if not file.startswith(abs_working_dir):
            return f"Error: Cannot access {file_path} as it is outside the permitted working directory\n"
        if not os.path.isfile(file):
            return f"Error: File not found or is not a regular file: {file_path}"

        with open(file, 'r') as f:
                content = f.read(MAX_CHARS) 

        if len(content) > MAX_CHARS:
            return content[0:MAX_CHARS-1] + f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]\n"
        return content + "\n"

    except Exception as e:
        return f"Error: {e}\n"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
    ),
)