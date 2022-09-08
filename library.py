import redis
import jwt
import hashlib
import psycopg2
import os
import json

redis_host = os.environ['REDIS_HOST']
redis_port = os.environ['REDIS_PORT']
postgres_host = os.environ['POSTGRES_HOST']
postgres_port = os.environ['POSTGRES_PORT']
postgres_user = os.environ['POSTGRES_USER']
postgres_pass = os.environ['POSTGRES_PASS']
postgres_db = os.environ['POSTGRES_DB']
hdfs_host = os.environ['HDFS_HOST']
hdfs_port = os.environ['HDFS_PORT']
hdfs_user = os.environ['HDFS_USER']


r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

def create_token(user):
    token = jwt.encode(user, 'secret-ugems', algorithm='HS256')
    pipe = r.pipeline()
    pipe.hmset('/t/'+token, user)
    pipe.expire('/t/'+token, 86400)
    pipe.execute()
    return token

def validate_token(token):
    print ('/t/'+token)
    pipe = r.pipeline()
    res = pipe.hgetall('/t/'+token).execute()
    #return res
    if len(res[0]) != 0:
        return res
    return False

def invalidate_token(token):
    pipe = r.pipeline()
    res = pipe.delete('/t/'+token).execute()
    return res

def hashing_data(raw):
    hash_object = hashlib.md5(raw.encode())
    return hash_object.hexdigest()

def validate_user(credential):
    user = credential['user']
    passwd = credential['pass']

    conn = psycopg2.connect(database = postgres_db, user = postgres_user, password = postgres_pass, host = postgres_host, port = postgres_port)
    print ("Opened database successfully")
    print(conn)

    cur = conn.cursor()
    cur.execute("SELECT id, username,password  from public.api_gps_user where username='"+user+"' and password='"+passwd+"'")

    rows = cur.fetchall()
    if (len(rows)>0):
        return rows[0]
    else:
        return None
