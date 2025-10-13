import pefile
import sys


def patch_exe(exe_path):
    pe = pefile.PE(exe_path)

    # 移除对 PssQuerySnapshot 的引用
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        if entry.dll.lower() == b'kernel32.dll':
            for imp in entry.imports:
                if imp.name and b'PssQuerySnapshot' in imp.name:
                    imp.name = b'GetProcessTimes'  # 替换为Win7支持的API

    pe.write(filename=exe_path + '.patched')
    pe.close()


if __name__ == '__main__':
    patch_exe(sys.argv[1])