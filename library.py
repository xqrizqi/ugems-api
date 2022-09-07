import redis
import jwt
import hashlib
import psycopg2


r = redis.StrictRedis(host='redis', port=6379, db=0)

def create_token(user):
    token = jwt.encode(user, 'secret-ugems', algorithm='HS256')
    pipe = r.pipeline()
    pipe.hmset('/t/'+token, user)
    pipe.expire('/t/'+token, 2592000)
    pipe.execute()
    return token

def validate_token(token):
    print ('/t/'+token)
    pipe = r.pipeline()
    res = pipe.hgetall('/t/'+token).execute()
    return res
    # if len(res[0]) != 0:
    #     return json.dumps(res[0])
    # return False

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

    conn = psycopg2.connect(database = "ugems_api", user = "postgres", password = "secret", host = "172.168.21.78", port = "5432")
    print ("Opened database successfully")
    print(conn)

    cur = conn.cursor()
    cur.execute("SELECT id, username,password  from api_user where username='"+user+"' and password='"+passwd+"'")

    rows = cur.fetchall()
    if (len(rows)>0):
        return rows[0]
    else:
        return None
