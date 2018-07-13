"""Configuration Values"""

# DRIVER = 'mysql+pymysql://'
# URL_PARAMS = {
#     'username': 'root',
#     'password': 'root',
#     'host': 'localhost',
#     'port': '3306',
#     'database_name': 'hydro'
# }


# URL = DRIVER + '{username}:{password}@{host}:{port}/{database_name}'.format(
#     **URL_PARAMS)


class Config(object):
    # ENV = 'development'
    # DEBUG = True
    SECRET_KEY = ''.join(
        '4ed2e994cba06266df65170068c57ae7227482ddac10cfbd49d35f8e28b5fa0b'
    )
    SEND_FILE_MAX_AGE_DEFAULT = 0
    # SQLALCHEMY_DATABASE_URI = URL
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
