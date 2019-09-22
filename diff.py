#!/usr/bin python
# coding=utf-8
"""
代码发布脚本
获取当前tag列表:os.popen("cd /home/webapps/huisuproject/huisu/;git tag;").read().split('\n')
"""
import filecmp
import md5
import os
import sys
import time
import pdb
import commands

# FILE_PATH = "/Users/machiko/secret/"
# APP_NAME = "test2/"
#
# PRD_FILE_PATH = "/Users/machiko/Desktop/"

# FILE_PATH: 代码临时存放目录 用于比对文件
# PRD_FILE_PATH: 生产环境代码路径
GIT_URL = u"git@xxxxx:/data/git/xxxxx.git"
FILE_PATH = u"/tmp/xxxxx/"
PRD_FILE_PATH = u"/home/webapps/xxxxx/"
APP_NAME = u"xxxx/"

# 忽略检查文件夹 和 扩展名
FILTERS = ['.git', 'front_end', 'migrations', '.python-eggs', 'weixin_access_token.yaml', '.pki', 'analysis_charts']
FILTERS_EXTENSION = ['.git', '.pyc', '.sqlite3', '.yaml']


def file_cmp(file1, file2):
    return filecmp.cmp(file1, file2, shallow=False)


def compare_file(file1, file2):

    return md5.new(file1.read()).digest() == md5.new(file2.read()).digest()


def file_pass(path):
    status = False
    for item in FILTERS:
        if item in path:
            status = True
            break

    return status


def check_file(version):
    os.chdir(FILE_PATH)
    if not os.path.exists(APP_NAME):
        os.system("git clone %s" % GIT_URL)

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
_del = []


def main(version):
    print u"本次更新版本:", version
    if not check_file(version):
        print u"%s版本不存在" % version
        return

    # 以线上代码为参照 去比对最新代码库
    for root, dirs, files in os.walk(os.path.join(PRD_FILE_PATH, APP_NAME)):
        path = root.split(PRD_FILE_PATH)[1]

        if file_pass(path):
            continue

        for dir in dirs:
            if file_pass(dir):continue

            if not os.path.exists(os.path.join(FILE_PATH, path, dir)):
                _add.append(os.path.join(FILE_PATH, path, dir))

        for f in files:
            cmp_path = os.path.join(FILE_PATH, path, f)

            if os.path.exists(os.path.join(FILE_PATH, path, f)):
                if not compare_file(open(os.path.join(PRD_FILE_PATH, path, f), 'r'), open(cmp_path, 'r')):
                    _update.append(cmp_path)
            else:
                if not os.path.splitext(cmp_path)[1] in FILTERS_EXTENSION:
                    _del.append(cmp_path)

    print u"\n更新文件:", len(_update)
    for item in _update:
        print "\033[1;32;40m %s \033[0m" % item

    print u"\n新添加文件:", len(_add)
    for item in _add:
        print "\033[1;33;40m +%s \033[0m" % item

    print "\n"

    print u"\n删除文件:", len(_del)
    for item in _del:
        print "\033[1;31;40m -%s \033[0m" % item


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])


