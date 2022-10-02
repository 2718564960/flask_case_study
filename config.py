HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'zlckqa'
USERNAME = 'root'
PASSWORD = 'xxxx'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = "sdfasdfsf"



# email
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "xxxx@qq.com"
MAIL_PASSWORD = "xxxx"
MAIL_DEFAULT_SENDER = "xxxx"