import os
import subprocess

# def create_directory():
#     project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     directory_path = os.path.join(project_root, "notLofied")
#     if not os.path.exists(directory_path):
#         try:
#             os.makedirs(directory_path)
#         except OSError as e:
#             print(f"Error creating directory notLotified: {e}")
#             exit(1)
#         print(f"Directory notLofied created successfully.")
#     else:
#         print(f"directory notLofied already exists")


def setupenv():
    subprocess.run(
        """
        cd .. && \
        python3 -m venv venv && \
        source venv/bin/activate && \
        pip install --quiet spotdl
        """,
        shell=True,
        executable="/bin/bash",  # Make sure it's bash so `source` works
        check=True
    )
    print("venv created and SpotDL installed successfully.")

