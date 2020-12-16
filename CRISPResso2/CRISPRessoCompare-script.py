#!e:\anaconda3\envs\py2\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'CRISPResso2==2.0.44','console_scripts','CRISPRessoCompare'
__requires__ = 'CRISPResso2==2.0.44'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('CRISPResso2==2.0.44', 'console_scripts', 'CRISPRessoCompare')()
    )
