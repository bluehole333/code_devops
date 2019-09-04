#!/usr/bin python
# coding=utf-8
import filecmp
import md5
import os
import sys
import time
import pdb
import commands

FILE_PATH = "/tmp/project/"
APP_NAME = "xxxx/"

PRD_FILE_PATH = "/home/liuxin/project/"


def file_cmp(file1, file2):
    return filecmp.cmp(file1, file2, shallow=False)


def compare_file(file1, file2):
    return md5.new(file1.read()).digest() == md5.new(file2.read()).digest()


def check_file(version):
    os.chdir(FILE_PATH)
    if not os.path.exists(APP_NAME):
        os.system("git clone ssh://git@xxxxxxxx/home/git/xxxxx.git")

    os.chdir(os.path.join(FILE_PATH, APP_NAME))
    commands.getstatusoutput("git pull")

    status, output = commands.getstatusoutput('git tag')
    if version not in output:
        return False

    os.system("git checkout -b %s %s" % (version, version))
    # commands.getstatusoutput("git checkout -b %s %s" % (version, version))

    return True


_add = []
_update = []
FILTERS = ['.git', '.pyc']


def main(version):
    print(u"本次更新版本:", version)
    if not check_file(version):
        print(u"%s版本不存在" % version)
        return

    # 以线上代码为参照 去比对最新代码库
    for root, dirs, files in os.walk(os.path.join(PRD_FILE_PATH, APP_NAME)):
        path = root.split(PRD_FILE_PATH)[1]
        for dir in dirs:
            if not os.path.exists(os.path.join(FILE_PATH, path, dir)):
                _add.append(os.path.join(FILE_PATH, path, dir))

        if dirs == '.git':
            continue

        for f in files:
            cmp_path = os.path.join(FILE_PATH, path, f)

            if os.path.exists(os.path.join(FILE_PATH, path, f)):
                # if f in "manage.py":
                #     pdb.set_trace()
                #     print "xxxxxxxxxxxxxx"
                if not compare_file(open(os.path.join(PRD_FILE_PATH, path, f), 'r'), open(cmp_path, 'r')):
                    _update.append(cmp_path)
            else:
                if not os.path.splitext(cmp_path)[1] in FILTERS:
                    _add.append(cmp_path)

    print(u"\n新添加文件:", len(_add))
    for item in _add:
        print(item)

    print(u"\n本次更新文件:")
    for item in _update:
        print(item)
    print("\n")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
