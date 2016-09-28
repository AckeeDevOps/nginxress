FROM ubuntu:16.04

RUN apt-get update && apt-get -y install nginx python3.5 python3-requests psmisc
COPY nginx.conf /etc/nginx/nginx.conf
COPY update.py /root/update.py
RUN chmod +x /root/update.py
COPY rc.local /etc/rc.local
RUN chmod +x /etc/rc.local

CMD ["/etc/rc.local"]

