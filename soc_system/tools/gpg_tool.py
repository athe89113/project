# coding=utf-8
from __future__ import unicode_literals
import os
import tarfile
import commands


class GPGTool(object):

    def __init__(self, passphrase, send_id, recv_id, cls, clss):
        self.key = ""
        self.file = ''
        self.passphrase = passphrase
        self.send_id = send_id
        self.recv_id = recv_id
        self.cls = cls
        self.clss = clss
        if os.path.exists('/usr/local/bin/gpg'):
            self.bin_file = '/usr/local/bin/gpg'
        elif os.path.exists('/usr/bin/gpg'):
            self.bin_file = '/usr/bin/gpg'
        else:
            raise Exception("Please Install gunpg")

    def _run_cmd(self, cmd):

        cmd = '{0} --trust-model always --batch --quiet --yes --passphrase {1} {2}'\
            .format(self.bin_file,self.passphrase, cmd)
        status, result = commands.getstatusoutput(cmd)
        return status, result

    def import_keys(self, server=False):
        if server:
            keys = [
                '/data/keys/soc/pri-server.txt',
                '/data/keys/soc/pub-client.txt',
            ]
        else:
            import base64
            with open('/tmp/temp_cls', 'wb') as f:
                f.write(base64.b64decode(self.cls))
            with open('/tmp/temp_clss', 'wb') as f:
                f.write(base64.b64decode(self.clss))
            keys = [
                '/tmp/temp_cls',
                '/tmp/temp_clss',
            ]
        cmd = '--import {}'
        for key in keys:
            self._run_cmd(cmd.format(key))
        if os.path.isfile('/tmp/temp_cls'):
            os.remove('/tmp/temp_cls')
            os.remove('/tmp/temp_clss')

    @classmethod
    def remove_keys(cls):
        gpg_home = os.path.join(os.environ['HOME'], '.gnupg')
        os.system('rm -rf {}'.format(gpg_home))

    def list_keys(self):
        self._run_cmd('-k')

    def encrypt(self, path):
        """
        :param path: 原始包路径
        :return: 加密后的包路径
        """
        return path
        # self.run_cmd('gpg --recipient {} --output demo.en.txt --encrypt demo.txt'.format(self.key))

    def decrypt(self, input, output):
        """

        :param path: 原始包路径
        :return: 解密后的包路径
        --local-user {send}
        """
        self.import_keys()

        status, result = self._run_cmd('--local-user {send} --output {output}  --decrypt {input} '.
                                       format(send=self.send_id, output=output, input=input))
        if status != 0:
            if 'signature' in result:
                raise Exception("Sign Error")
            elif 'decryption' in result:
                raise Exception("Decryption Error")
            else:
                # 加密包错误
                raise Exception("Package Error")
        self.remove_keys()
        return status, result

    def sign(self, path):
        """
        :param path: 原始包路径
        :return: 签名后的包路径
        """
        return path
        # self.run_cmd('gpg --sign {}'.format(self.file))

    def verify(self, path, output):
        """
        :param path: 原始包路径
        :return: 验证签名结果
        """
        self._run_cmd('-r {} --verify {} {}'.format(self.recv_id, path, output))

    def encrypt_sign(self, input, output):
        """
        :param path: 原始包路径
        :return: 加密&签名后的包路径
        --local-user {send} --recipient {recv}
        """
        self.import_keys(server=True)
        return self._run_cmd(
            '--no-use-agent --trust-model always --local-user {send} --recipient {recv} --batch --quiet '
            '--yes --output {output} --armor -s --encrypt {input} '
            ''.format(send=self.send_id,
                      recv=self.recv_id,
                      input=input, output=output))

    @classmethod
    def info(cls, filename):
        """

        :param filename:
        :return: 压缩包的版本及类型
        """
        t = tarfile.open(filename)
        f_type = version = None
        for tarinfo in t:
            if '/__version' in tarinfo.name:
                version = tarinfo.name.split('__version_')[1]
            if '/__type' in tarinfo.name:
                f_type = tarinfo.name.split('__type_')[1]
        return f_type, version
