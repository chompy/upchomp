from cx_Freeze import setup, Executable

includes = ["pygame"]
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
packages = []
path = []           

GUI2Exe_Target_1 = Executable(
    # what to build
    script = "main.py",
    initScript = None,
    base = 'Win32GUI',
    targetDir = r"dist",
    targetName = "upchomp.exe",
    compress = True,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = "icon.ico"
    )            
            
setup(
        name = "UpChomp",
        version = "1.0",
        description = "Help Chompy get cookies!",   
        options = {"build_exe": {"includes": includes,
                                 "excludes": excludes,
                                 "packages": packages,
                                 "path": path
                                 }
                   },   
        executables = [GUI2Exe_Target_1]                        
        )
