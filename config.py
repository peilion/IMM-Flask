import os

ENV = os.getenv("FLASK_ENV")
SECRET_KEY = b'qk\x03\r\xe4\x02~\x86,\x86\xa1\xaeh\xfdr\x06'
TESTING = True
SWAGGER = {
    'title': 'Api for IMM-FLASK',
    'uiversion': 3,
    'doc_dir': './docs/'
}