import os
try:
    string_type = basestring
    PYTHON_VERSION = 2
    import urllib
except NameError:
    string_type = str
    PYTHON_VERSION = 3
    import urllib.parse as urllib

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
log_host = ""

DATABASE = {
            'host': '',
            'port': 3306,
            'user': '',
            'passwd': '',
            'db': '',
            'charset': 'utf8'
            }
