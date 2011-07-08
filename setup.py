from cx_Freeze import setup, Executable

setup(
        name = "UpChomp",
        version = "0.1",
        description = "Help Chompy get cookies!",
        executables = [Executable("main.py")]
        )
