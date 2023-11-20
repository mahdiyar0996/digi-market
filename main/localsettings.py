import os

DB_NAME = 'digi_market'
DB_HOST = os.environ.get("MYSQL_HOST", 'localhost')
DB_PORT = os.environ.get('MYSQL_PORT', 3306)
DB_USER = os.environ.get('MYSQL_USER', 'root')
DB_PASS = os.environ.get('MYSQL_PASSWORD', 'Mysql@0996')

c_host = os.environ.get('REDIS_HOST', 'localhost')
c_port = os.environ.get('REDIS_PORT', '6379')
c_db = os.environ.get('REDIS_DB', '1')
CACHE_LOCATION = f"redis://{c_host}:{c_port}/{c_db}"

domain = 'localhost'
port = 8000
debug = True

# CACHE_LOCATION = "redis://127.0.0.1:6379/1"