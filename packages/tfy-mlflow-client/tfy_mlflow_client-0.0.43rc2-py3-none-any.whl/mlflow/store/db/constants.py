import os

DB_POSTGRES_SCHEMA = os.getenv("DB_POSTGRES_SCHEMA") or ""
DB_SSL_CERT_PATH = os.getenv("DB_SSL_CERT_PATH")
DB_SSL_KEY_PATH = os.getenv("DB_SSL_KEY_PATH")
DB_SSL_CA_PATH = os.getenv("DB_SSL_CA_PATH")
DB_SSL_MODE = os.getenv("DB_SSL_MODE")
