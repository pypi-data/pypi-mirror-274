import os
import subprocess

def main2():
    # Get the directory of the current module
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # script_path = os.path.join(current_dir, "main.py")
    # subprocess.call(["uvicorn", f"{script_path}:app", "--reload"])
    subprocess.call(["uvicorn", "glabel.main:app", "--reload"])

if __name__ == "__main__":
    main2()
