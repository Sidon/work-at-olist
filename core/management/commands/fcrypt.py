import os
from math import ceil
from django.core.management.base import BaseCommand, CommandError
from workatolist.settings import CONFIG_DIR
from Crypto.Cipher import AES


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
            raise CommandError("File path does not exist on project'templates root.")

        # Create a encryptation suite
        encryption_suite = AES.new(os.environ['MASTERKEY'], AES.MODE_CBC,'This is an IV456')

        fo = open(file_output,'wb')
        with open(file_input,'r') as f:
            for line in f:
                line.rstrip()
                spaces = ' ' * ( (16 * ceil( len(line)/16) ) - len(line))
                line += spaces
                cipher_text = encryption_suite.encrypt(line)
                fo.write(cipher_text)
