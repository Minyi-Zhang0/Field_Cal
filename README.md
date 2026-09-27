
A analysis tool for APT field calculation.

Dr. Minyi Zhang, Dr. Zhiyuan Ding

m.zhang@mpi-susmat.de

F(CSR) data: L Tegg, et al. Microscopy and Microanalysis 30.3 (2024): 466-475.

# Run the App by Double-Clicking

For Windows x86-64, a standalone .exe file built with PyInstaller is available on the GitHub Releases page. This is the simplest way to run the application, as no Python installation or environment setup is required.

For other platforms (Linux, macOS, etc.), or if you prefer to run the application in your own Python environment, please follow the instructions in the section below.

# Run the App from a Python Environment

1. Python

This application uses a Streamlit-based GUI and has been tested with Python 3.12.14. We recommend using Python's built-in `venv` module to create an isolated virtual environment.

2. Download the code

Download or clone the source code to a local directory. For example: `/code_path/`

3. Create an venv environment

Open a Terminal on Linux or Command Prompt/PowerShell on Windows. Navigate to the directory where you would like to store the virtual environment, and run `python -m venv my_env`. `my_env` is the name of the virtual environment and can be replaced with any name you prefer. This command creates an `my_env` directory containing the virtual environment.

4. Activate the venv environment

Run `source ./my_env/bin/activate` for Linux or `.\my_env\Scripts\activate.bat` for Windows

5. Install dependencies

With the virtual environment activated, install the required Python packages using `pip install -r /code_path/requirements.txt`. Replace `/code_path/` with the actual path to the downloaded source code.

6. Run GUI

Navigate to the source code directory, then start the app `streamlit run st_app.py`

Streamlit will display a local URL that you can open in your web browser to access the application.

You may also try `pyinstaller Field_Cal.spec` to build a standalone executable for your platform, allowing the application to run without requiring a separate Python environment.