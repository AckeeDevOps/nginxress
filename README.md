# nginxress
Nginx ingress - expose some containers to public ip.

This is a simple container that containx the nginx webserver and a python script that generates proxy config that exposes selected services to a public IP (of this container).

Container expects those variables:
    K8S_URL - k8s api endpoint 
    K8S_USER - username
    K8S_PASSWORD - password


