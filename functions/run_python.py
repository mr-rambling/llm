import os 
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory\n"
        if not os.path.exists(abs_file_path):
            return f"Error: File \"{file_path}\" not found.\n"
        if not abs_file_path[-3:] == '.py':
            return f"Error: \"{file_path}\" is not a Python file.\n"
        process_instance = subprocess.run(['python', abs_file_path], timeout=30, capture_output=True, cwd=abs_working_dir)

        if process_instance == None:
            return "No output produced"

        msg = f"STDOUT: {process_instance.stdout.decode()}\n STDERR: {process_instance.stderr.decode()}"
        if process_instance.returncode != 0:
            msg += f"Error: Process exited with code {process_instance.returncode}\n"
        return msg
    
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python script in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to execute, relative to the working directory.",
            ),
        },
    ),
)