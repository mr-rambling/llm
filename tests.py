# from subdirectory.filename import function_name
from functions.run_python import run_python_file

def main():
    directories = [
        "main.py",
        "tests.py",
        "../main.py",
        "nonexistent.py"
    ]

    inputs = [
        "wait, this isn't lorem ipsum",
        "lorem ipsum dolor sit amet",
        "this should not be allowed"
    ]

    for i in range(len(directories)):
        print(run_python_file("calculator", directories[i]))

if __name__ == "__main__":
    main()