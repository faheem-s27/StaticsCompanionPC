import os
import time
import requests
from flask import Flask, jsonify

data = []
name = ""
PID = ""
port = ""
password = ""
protocol = ""
accessToken = ""
entitelmentToken = ""


# start the flask server
app = Flask(__name__)

@app.route("/")
def send_message():
    return jsonify({"accessToken": accessToken, "entitelmentToken": entitelmentToken})


def getLockFile():
    return os.path.join(os.getenv('LOCALAPPDATA'), R'Riot Games\Riot Client\Config\lockfile')


# try to read the lockfile
while True:
    try:
        with open(getLockFile()) as lockfile:
            data = lockfile.read().split(':')
            break
    except:
        # tell user that valorant is not running then wait for keypress
        print("Valorant is not running! Please open Valorant and press any key to continue...")
        input()

name = data[0]
PID = data[1]
port = data[2]
password = data[3]
protocol = data[4]

# print("Name: " + name)
# print("PID: " + PID)
# print("Port: " + port)
# print("Password: " + password)
# print("Protocol: " + protocol)

# print out the device IP
import socket

# Get the IPV4 address of the local host
ip_address = socket.gethostbyname(socket.gethostname())

# Print out the IPV4 address
#print("IPV4 address:", ip_address)

r = requests.get(f"https://127.0.0.1:{port}/entitlements/v1/token", auth=('riot', password),
                        verify=False)
accessToken = r.json()["accessToken"]
entitelmentToken = r.json()["token"]

# print("Access Token: " + accessToken)
# print("Entitelment Token: " + entitelmentToken)

# # copy it to clipboard
# import pyperclip
# msg = "Access Token: " + accessToken + "\n\nEntitelment Token: " + entitelmentToken
# pyperclip.copy(msg)

# # tell user that the tokens have been copied to clipboard
# print("Access Token and Entitelment Token have been copied to clipboard!")

# if the tokens are not empty, start the server
if (accessToken != "", entitelmentToken != ""):
    print("Server started! Enter the IP into Statics: " + ip_address)
    app.run(host='0.0.0.0', port=5000, debug=True)
    
