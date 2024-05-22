import os
import pathlib
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from shutil import which
import re
import importlib.resources


def main():
    root = os.getcwd()

    if pathlib.Path(root).joinpath('go.mod').exists():
        with open(pathlib.Path(root).joinpath('go.mod')) as f:
            for line in f:
                m = re.search(r'^module\s+(\S+)', line)
                if m:
                    package_name = m.group(1)
                    print(f'package_name: {package_name}')
                    break
    else:
        print('目录下不存在go.mod')
        exit(-1)

    dirs = []

    extract_dir = pathlib.Path(root).joinpath('extract')

    if not extract_dir.exists():
        extract_dir.mkdir()
    else:
        print("目录extract已经存在")

    if which('yaegi') is None:
        print('未安装yaegi\ngo install github.com/traefik/yaegi/cmd/yaegi@latest')

    def list_directories(path):
        for entry in os.scandir(path):
            if entry.is_dir():
                if any(x.endswith('.go') for x in os.listdir(entry.path)):
                    dirs.append(entry.path)
                list_directories(entry.path)

    def extract_files(pack):
        os.chdir(extract_dir)
        time.sleep(1)
        res = subprocess.run(f'yaegi extract {package_name + pack[len(root):]}', shell=True, stdout=subprocess.PIPE, )
        print(pack[len(root):] + ' done')
        return res.stdout.decode().strip()

    list_directories(root)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(extract_files, pack) for pack in dirs]

        for f in futures:
            f.result()

    with open(extract_dir.joinpath('api.go'), 'w') as f:
        f.write(importlib.resources.open_text('go_console', 'api.go').read())
    print('生成完成')
    for file in os.listdir(extract_dir):
        res = subprocess.run(
            f'go vet {extract_dir.joinpath(file)}',
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).stderr.decode().strip()
        for line in res.splitlines():
            if line == '# command-line-arguments' or len(line.split()) <= 1:
                continue
            words = line.split()
            pos = words[1]
            info = ' '.join(words[2:])
            if info == 'undefined: Symbols':
                continue
            print(pos, info)
            tips = {
                'not exported': '可能存在未导出的类型',
                'redeclared': '可能存在重名包'
            }
            for k, v in tips.items():
                if k in info:
                    print(v)
                    break
            else:
                print('未知错误')
    print('!!!------------------------------------!!!')
    print(f'请在main包使用\nimport "{package_name}/extract"')
    print("console := extract.New()")
    print("""
console.Init(map[string]any{
    "key": value... // 需要引入的遍历
})""")


main()
