from flask import Flask
from flask import request
from library import create_token, validate_token, invalidate_token, hashing_data, validate_user
import json
import time
import os

service_port = os.environ['SERVICE_PORT']


app = Flask(__name__)

# redis = Redis(host='localhost', port=6379)
@app.route("/")
def hello_world():
    # redis.incr('hits')
    return "<p>Hello, World!</p>"

@app.route("/generate_token", methods=['POST'])
def get_token():
    if request.method == 'POST':
        datajson = request.get_json()
        print(datajson)
        # post = json.load(datajson)
        if datajson['username']:
            # print (datajson['username'] +"|"+ datajson['password'])
            cred = {}
            cred['user']=datajson['username']
            cred['pass']=hashing_data(datajson['password'])
            valid = validate_user(cred)
            if valid:
                # print (valid)
                payload = {}
                payload['id'] = valid[0]
                payload['username'] = valid[1]
                payload['login_time'] = str(time.time())
                try:
                    token = create_token(payload)
                    data = {}
                    data['token'] = token
                    data['token_type'] = 'Bearer'
                    data['expire_in'] = 86400
                    coderesponse = 200
                    datares = {
                            "status": 200,
                            "message": "success",
                            "data":data
                        }
                except Exception as e:
                    coderesponse = 400
                    datares = {
                            "status": 403,
                            "message": "problem with creating token"
                        }
            else:
                coderesponse = 400
                datares = {
                        "status": 402,
                        "message": "incorrect username or password"
                    }
        else:
            coderesponse = 400
            datares = {
                    "status": 401,
                    "message": "parameter is empty"
                }
        # return datajson
    
    return datares, coderesponse

@app.route('/send_data', methods=['POST'])
def get_data():
    if request.method == 'POST':
        token = request.headers['token'].split(' ')
        # print(token)
        valid = validate_token(token[1])
        print (valid)
        if valid:
            datajson = request.get_json()
            try:
                json_data = datajson['data']
                sdata = json.loads(json.dumps(datajson['data']))
                coderesponse = 200
                datares = {
                        "status": 200,
                        "message": "success",
                        "data":json_data,
                        "total data": len(json_data)
                    }
            except KeyError:
                coderesponse = 400
                datares = {
                        "status": 406,
                        "message": "parameter data not found"
                    }
        else:
            coderesponse = 400
            datares = {
                    "status": 405,
                    "message": "Invalid token"
                }
    return datares, coderesponse



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=service_port, debug=True)