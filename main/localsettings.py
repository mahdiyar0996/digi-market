import os

DB_NAME = 'digi_market'
DB_HOST = 'db'
DB_PORT = 3306
DB_USER = "root"
DB_PASS = "Mysql@0996"
# DB_HOST = os.environ.get("MYSQL_HOST", 'localhost')
# DB_PORT = os.environ.get('MYSQL_PORT', 3306)
# DB_USER = os.environ.get('MYSQL_USER', 'root')
# DB_PASS = os.environ.get('MYSQL_PASSWORD', 'Mysql@0996')

c_host = os.environ.get('REDIS_HOST', 'localhost')
c_slave_host = os.environ.get('REDIS_SLAVE_HOST', 'localhost')
c_port = os.environ.get('REDIS_PORT', '6379')
c_db = os.environ.get('REDIS_DB', '0')
c_password = 'b446c4229de28d4055ef3261266fa34a8b51bc571436673dea5a70f38c42eb09'
CACHE_LOCATION = f"redis://{c_host}:{c_port}/{c_db}"
CACHE_SLAVE_LOCATION = f'redis://{c_slave_host}:{c_port}/{c_db}'

domain = 'localhost'
port = 8000
debug = True
