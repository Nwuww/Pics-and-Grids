from cx_Freeze import setup, Executable
import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

build_options = {
    'packages': ['PIL'],
    'excludes': ['tkinter'],
    'include_msvcr': True,
    'replace_paths': [('*', '')]  # 禁用路径重定向
}

executables = [Executable('main.py', base=base)]

setup(
    name='grids%pics',
    version='0.1.2',
    description='Windows 7 Comp.',
    options={'build_exe': build_options},
    executables=executables
)