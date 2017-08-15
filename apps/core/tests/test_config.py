import os
from django.test import TestCase
from workatolist.settings import CONFIG_DIR
from workatolist.config.conf import Config


class ConfigTestCase(TestCase):
    config = Config(os.path.join(CONFIG_DIR, 'config-tests.json'))
    secretkey = "w6**ci+meh34=n)o_299ee5qga7ubb&pb30=iyx^5$+v-_iv+u)!nw"
    hosts =  "localhost,127.0.0.1"
    apps = ["django_extensions"]
    db = {"default": { "ENGINE": "django.db.backends.postgresql_psycopg2", "NAME": "dbtest", "USER": "dbtest",
                       "PASSWORD": "password_99", "HOST": "localhost", "PORT": "5432" }}

    def test_vars(self):
        secret_key = self.config.get_config('secretk')
        self.assertEqual(self.secretkey, secret_key)

        hosts = self.config.get_config('ahosts')
        self.assertEqual(self.hosts,hosts)

        apps = self.config.get_config('add_apps')
        self.assertEqual(self.apps,apps)

        db = self.config.get_config('db')
        self.assertEqual(self.db,db)
