# hook-PIL.py（保存在 PyInstaller 的 hooks 目录或与 main.py 同目录）
from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('PIL')
