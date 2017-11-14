#!/usr/bin/env python
import os
import sys
#from django.conf import settings
#sys.path.append(os.path.join(settings.BASE_DIR, "apps"))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workatolist.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
