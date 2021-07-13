#!/usr/bin python
# coding:utf-8
# Created by yubiao.luo at 2021/7/5
import os
import zipfile
import shutil


# zipfile读取出来的文件会有编码问题，需要做一次转码
def encode(name):
    if os.name == 'nt':
        try:
            return name.encode('cp437').decode("gbk")
        except UnicodeDecodeError:
            pass
        except UnicodeEncodeError:
            try:
                return name.encode('utf-8').decode("gbk")
            except UnicodeDecodeError or UnicodeEncodeError:
                pass
    return name


def clean_dir(dir_name):
    shutil.rmtree(dir_name)
    os.makedirs(dir_name)


def unzip(zip_name, unzip_dir):
    if not zip_name:
        return

    if not os.path.exists(unzip_dir):
        os.makedirs(unzip_dir, exist_ok=True)

    zf = zipfile.ZipFile(zip_name, 'r')
    for file_name in zf.namelist():
        file_name = file_name.replace('\\', '/')
        if file_name.endswith('/'):
            file_dir = os.path.join(unzip_dir, encode(file_name)).replace('\\', '/')
            if os.path.isdir(file_dir):
                pass
            else:
                os.mkdir(file_dir)
        else:

            ext_filename = os.path.join(unzip_dir, encode(file_name))
            ext_filedir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_filedir):
                os.mkdir(encode(ext_filedir))
            data = zf.read(file_name)
            with open(ext_filename, 'wb+') as f:
                f.write(data)
    zf.close()


def zip(zip_name, file_list, dict_files=None):
    zf = zipfile.ZipFile(zip_name, mode='w')
    try:
        for file_name in file_list:
            with open(file_name, 'rb+') as f:
                zf.writestr(os.path.basename(file_name), data=f.read())
        if dict_files:
            for key, f_list in dict_files.items():
                for item in f_list:
                    file_name = item.get('file_name')
                    old, ext = os.path.splitext(os.path.basename(file_name))
                    new_name = '{}{}'.format(item.get('display_name'), ext)
                    try:
                        with open(file_name, 'rb+') as f:
                            zf.writestr(os.path.join(key, new_name), data=f.read())
                    except FileNotFoundError:
                        pass
    finally:
        zf.close()
    return zf
