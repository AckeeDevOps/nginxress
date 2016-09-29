# nginxress
Nginx ingress - automatically exposes containers to public ip.

This is a simple container that contains the nginx webserver and a python script that generates proxy config that automatically exposes kubernetes services to a public IP (of this container).

It requires DNS records in following way: servicename-namespace.domain

Domain is set as DOMAIN system env and is the only required parameter.
