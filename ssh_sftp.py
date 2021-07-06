#!/usr/bin python
# coding:utf-8
# Created by yubiao.luo at 2021/7/5
import os
import stat
import logging
import paramiko
import threading


"""
一、使用paramiko通过ssh连接sftp,实现文件上传和下载
"""


class SSH4Sftp(object):

    def __init__(self, host_name, user_name, key_file, pass_phrase=None, pass_word=None, port=22, logger=None):
        self.host_name = host_name
        self.user_name = user_name
        self.key_file = key_file
        self.pass_phrase = pass_phrase
        self.pass_word = pass_word
        self.port = port
        self.sftp = None
        self.logger = logger or logging.getLogger(__file__)
        self.logger.debug("Start connect to host(%s), port(%s)", host_name, port)
        connect_count = 0   # 连接次数
        while connect_count < 3:
            try:
                sock = (self.host_name, self.port)
                self.trans = paramiko.Transport(sock=sock)
                if key_file is not None and pass_phrase is not None and pass_word is not None:
                    # 秘钥 + 密码
                    self.key_and_password_auth()
                elif key_file is not None and pass_phrase is not None:
                    # 秘钥
                    self.trans.start_client()
                    pkey = paramiko.RSAKey.from_private_key_file(key_file, password=pass_phrase)
                    self.trans.auth_publickey(user_name, pkey)
                else:
                    if pass_word is not None:
                        self.trans.connect(username=user_name, password=pass_word)
                    else:
                        raise Exception('Must supply either key_file or password')
                self.sftp = paramiko.SFTPClient.from_transport(self.trans)
                break
            except Exception as err:
                self.logger.error("Connect host error:%s", str(err))
                self.logger.debug("Trying to reconnect...")
                connect_count += 1

        if connect_count >= 3:
            self.logger.error("Connect to host failed.")
        else:
            self.logger.debug("Connect to host(%s), port(%s) successfully.", host_name, port)

    def key_and_password_auth(self):
        """
        https://github.com/paramiko/paramiko/issues/519
        适用于秘钥+密码授权连接
        Return an open paramiko SFTP client to a host that requires multifactor
        authentication.
        """
        pkey = paramiko.RSAKey.from_private_key_file(self.key_file, password=self.pass_phrase)
        self.trans.connect()
        # 秘钥授权
        self.trans.auth_publickey(self.user_name, pkey)
        event = threading.Event()
        auth_handler = paramiko.AuthHandler(self.trans)
        self.trans.auth_handler = auth_handler
        self.trans.lock.acquire()
        auth_handler.auth_event = event
        auth_handler.auth_method = 'password'
        auth_handler.username = self.user_name
        auth_handler.password = self.pass_word
        message = paramiko.Message()
        message.add_string('ssh-userauth')
        message.rewind()
        auth_handler._parse_service_accept(message)
        self.trans.lock.release()
        auth_handler.wait_for_response(event)

    def upload(self, local_file, remote_file, retry=3):
        """
        Copy localFile to remoteFile, overwriting or creating as needed.
        :param local_file:
        :param remote_file:
        :param retry:
        :return:
        """
        self.logger.info("###Upload file({}) start###".format(local_file))
        while retry > 0:
            self.sftp.put(local_file, remote_file)
            if os.path.split(remote_file)[1] in self.sftp.listdir(os.path.split(remote_file)[0]):
                self.logger.info("###Upload file({}) end###".format(local_file))
                return
            retry -= 1
        raise FileNotFoundError('###Upload file({}) failed...###'.format(local_file))

    def download(self, remote_file, local_file, retry=3):
        """
        Copy remote_file to local_file, overwriting or creating as needed.
        :param remote_file:
        :param local_file:
        :param retry:
        :return:
        """
        self.logger.info("###Download file({}) start###".format(remote_file))
        while retry > 0:
            self.sftp.get(remote_file, local_file)
            if os.path.exists(local_file):
                self.logger.info("###Download file({}) end###".format(remote_file))
                return
            retry -= 1
        raise FileNotFoundError("###Download file({}) failed...###".format(remote_file))

    def download_all(self, remote_path, local_path):
        """
        Copy all in remote_path file to local_path, overwriting or creating as needed.
        :param remote_path:
        :param local_path:
        :return:
        """
        try:
            self.sftp.chdir(os.path.split(remote_path)[0])

            if not os.path.exists(local_path):
                os.mkdir(local_path)

            files_attr = self.sftp.listdir_attr(remote_path)
            for file_attr in files_attr:
                if stat.S_ISDIR(file_attr.st_mode):
                    continue
                self.logger.info('remoteFileName: {}'.format(file_attr.filename))
                remote_file = os.path.join(os.path.sep, remote_path, file_attr.filename)
                local_file = os.path.join(local_path, file_attr.filename)
                self.download(remote_file=remote_file, local_file=local_file)
            self.logger.info('remote_path({}) not file'.format(remote_path))

        except FileNotFoundError as file_not_found_error:
            self.logger.error(file_not_found_error)
        except Exception as error:
            self.logger.error('get_all error: ' + str(error))
            raise error

