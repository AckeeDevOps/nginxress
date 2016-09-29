# nginxress
Nginx ingress - automatically exposes containers to public ip.

This is a simple container that contains the nginx webserver and a python script that generates proxy config that exposes selected services to a public IP (of this container).

It requires DNS records in following way: servicename-namespace.ack.ee
