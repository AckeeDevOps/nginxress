FROM ubuntu:16.04

RUN apt-get update && apt-get -y install nginx python3.5 python3-requests psmisc
#COPY nginx.conf /etc/nginx/nginx.conf
COPY update.py /root/update.py
COPY rc.local /etc/rc.local

RUN sed -idefault 's/# server_names_hash_bucket_size 64/server_names_hash_bucket_size 128/gi' /etc/nginx/nginx.conf && \
    chmod +x /root/update.py && \
    chmod +x /etc/rc.local && \
    sed -i '11 a client_max_body_size 25M;' /etc/nginx/nginx.conf

WORKDIR /etc/nginx/conf.d/

#RUN echo "                       \
#    stream {                     \
#      server {                   \
#        listen 3306;             \
#        proxy_pass mysql:3306;   \
#      }                          \
#    }                            \
#   " >>/etc/nginx/nginx.conf

CMD ["/etc/rc.local"]
