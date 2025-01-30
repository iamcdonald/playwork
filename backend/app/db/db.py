import psycopg
from app.conf import conf

conn = psycopg.connect(dbname="db", user="demo", password="password", host=conf.POSTGRES_HOST);
