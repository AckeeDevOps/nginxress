#!/bin/bash
createCNAMERecord() {
 EMAIL="$CLOUDFLARE_API_AUTH_EMAIL"
 KEY="$CLOUDFLARE_API_AUTH_KEY"
 ZONE="$CLOUDFLARE_ZONE_ID"
 name="$1"
 domain="$2"
 curl -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
    -H "Content-Type:application/json" \
    -H "X-Auth-Key:$KEY" \
    -H "X-Auth-Email:$EMAIL" \
    --data '{"type":"CNAME","name":"'${name}'","content":"'${domain}'","ttl":1,"proxied":true}'
}

vhosts=$(cat /etc/nginx/conf.d/* | grep -o '[^ ]*.'$DOMAIN | cut -d. -f-1)

for vhost in $vhosts
do
  createCNAMERecord "$vhost" "$HOST"
done
