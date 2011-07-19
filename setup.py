from cx_Freeze import setup, Executable

setup(
        name = "UpChomp",
        version = "1.0",
        description = "Help Chompy get cookies!",
        executables = [Executable("main.py")]
        )
