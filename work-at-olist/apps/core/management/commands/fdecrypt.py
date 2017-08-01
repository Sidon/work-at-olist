import os
from django.core.management.base import BaseCommand, CommandError
from workatolist.settings import BASE_DIR, PROJECT_DIR, CONFIG_DIR
from Crypto.Cipher import AES
import json


class Command(BaseCommand):
    help = 'crypt a txt file'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('fileinput', type=str)
        parser.add_argument('fileoutput', type=str)

    def handle(self, *args, **options):

        file_input = os.path.join(CONFIG_DIR,options['fileinput'])
        file_output = os.path.join(CONFIG_DIR,options['fileoutput'])

        # make sure file path resolves
        if not os.path.isfile(file_input):
            raise CommandError("File path does not exist on project's root.")

        decryption_suite = AES.new(os.environ['MASTERKEY'], AES.MODE_CBC,'This is an IV456')
        fo = open(file_output,'wb')

        with open(file_input,'rb') as f:
            enc_str =  f.read()

        dec_str = decryption_suite.decrypt(enc_str)decode()
        lst_str = dec_str.split('\n')
        lst_str = [s.strip() for s in lst_str]
        dj = json.loads(' '.join(lst_str))


