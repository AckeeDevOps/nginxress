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

response = requests.get(apiurl+'api/v1/watch/services',
                         auth=(apiuser,apipass), verify=False, stream=True)
for line in response.iter_lines():
    try:
        data = json.loads(line.decode('utf-8'))
        typ=ip=data["type"]
        ip=data["object"]["spec"]["clusterIP"]
        port=data["object"]["spec"]["ports"][0]["port"]
        name=data["object"]["metadata"]["name"]
        link=data["object"]["metadata"]["selfLink"]
        namespace=data["object"]["metadata"]["namespace"]
        labels=requests.get(apiurl+link,auth=(apiuser,apipass), verify=False, stream=False)
        generate=False
        for i in labels.iter_lines():
            l=json.loads(i.decode('utf-8'))['metadata']['labels']
            if ('visibility' in l):
                if (l['visibility'] == 'publichttp'):
                    generate=True
        if (generate==True):
            if (typ=="ADDED"):
                make_config(name,namespace,ip,port)
            else:
                delete_config(name)
    except Exception as e:
        pprint.pprint(e)
#        pprint.pprint(data)
        pass

print("Update exited")
