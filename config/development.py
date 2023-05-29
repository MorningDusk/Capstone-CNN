from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'capstone.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"

'''from config.default import *
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv(os.path.join(BASE_DIR, '.env'))

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dbmasteruser:g<#wHS>79|E!pGF9JJ7!$a[?&nLA?aP%@ls-491dfa0f47b6c73fb81aa4b4794c82f223f8cc98.cxfmrdeq6htd.ap-northeast-2.rds.amazonaws.com:5432/flask_capstone'.format(
    user=os.getenv('dbmasteruser'),
    pw=os.getenv('g<#wHS>79|E!pGF9JJ7!$a[?&nLA?aP%'),
    url=os.getenv('ls-491dfa0f47b6c73fb81aa4b4794c82f223f8cc98.cxfmrdeq6htd.ap-northeast-2.rds.amazonaws.com'),
    db=os.getenv('flask_capstone'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x1d"3\xd0&\x08\xcb3\x98\xdb\x91\xc5)\xa2?l'
'''