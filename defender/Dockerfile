FROM ubuntu:20.04

RUN apt update && \
    apt install -y nginx iptables tcpdump

COPY nginx.conf /etc/nginx/nginx.conf
COPY enable_iptables.sh /enable_iptables.sh

RUN chmod +x /enable_iptables.sh

CMD ["nginx", "-g", "daemon off;"]
