import psycopg
import app.conf

conn = psycopg.connect(
    dbname=app.conf.POSTGRES_DB,
    user=app.conf.POSTGRES_USER,
    password=app.conf.POSTGRES_PASSWORD,
    host=app.conf.POSTGRES_HOST);
