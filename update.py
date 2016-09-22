#!/usr/bin/python3

import json
import pprint
import requests
from subprocess import call
import os

domain="ack.ee"
apiurl=os.environ['K8S_URL']
apiuser=os.environ['K8S_USER']
apipass=os.environ['K8S_PASSWORD']

def make_config(name,namespace,ip,port):
    changed=True
    c = open("/etc/nginx/conf.d/"+name+"."+namespace+".conf","w")
    c.write("server {\n")
    c.write("    server_name "+name+"."+namespace+"."+domain+";\n")
    c.write("    location / {\n")
    if (namespace == "kube-system"):
        c.write("        allow 84.242.105.0/24;\n        allow 46.135.165.0/24;\n        allow 192.242.105.120/29;\n        deny all;\n")
    c.write("        proxy_pass http://"+ip+":"+str(port)+"/;\n")
    c.write("    }\n}\n")
    c.close()
    print("Created config for "+name+"."+namespace)
    call(["killall","-HUP","nginx"])

def delete_config(name,namespace):
    os.unlink("/etc/nginx/conf.d/"+name+"."+namespace+".conf")
    print("Deleted config for "+name+"."+namespace)
    call(["killall","-HUP","nginx"])

response = requests.get(apiurl,
                         auth=(apiuser,apipass), verify=False, stream=True)
for line in response.iter_lines():
    try:
        data = json.loads(line.decode('utf-8'))
        typ=ip=data["type"]
        ip=data["object"]["spec"]["clusterIP"]
        port=data["object"]["spec"]["ports"][0]["port"]
        name=data["object"]["metadata"]["name"]
        namespace=data["object"]["metadata"]["namespace"]
        if (port==80):
            if (typ=="ADDED"):
                make_config(name,namespace,ip,port)
            else:
                delete_config(name)
    except Exception as e:
        pprint.pprint(e)
        pass

print("Update exited")
