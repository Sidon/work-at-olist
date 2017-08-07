import os
import json
from django.core.exceptions import ImproperlyConfigured
from Crypto.Cipher import AES


class Config(object):
    def __init__(self, _file):
        self._fconf = _file
        # Object for decrypt configurations
        self.__decryption = AES.new(os.environ['MASTERKEY'], AES.MODE_CBC,'This is an IV456')

        # Load encrypted configuration file
        with open(self._fconf,'rb') as f:
            crypt_conf = f.read()

        # Decrypt an converto to python dictionary
        decrypt_conf = self.__decryption.decrypt(crypt_conf).decode()
        lst_conf = decrypt_conf.split('\n')
        lst_conf = [s.strip() for s in lst_conf]
        self.__config = json.loads(' '.join(lst_conf))

    # Get the configuration from python dictionary (__config)
    def get_config(self,setting):
        try:
            return self.__config[setting]
        except KeyError:
            raise ImproperlyConfigured("Set the {0} environment variable".format(setting))
