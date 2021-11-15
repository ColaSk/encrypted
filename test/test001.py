import sys
sys.path.append('../')

from encrypted.encrypt import EncryptCore
from encrypted.conf.setting import Setting as setting
if __name__ == '__main__':
    pwd = '123456'
    work_secret_key_cipher_str = setting.work_secret_key_cipher_str
    ec = EncryptCore(work_secret_key_cipher_str)
    en_pwd = ec.encode(pwd)
    de_pwd = ec.decode(en_pwd)

    print(en_pwd)
    print(de_pwd)