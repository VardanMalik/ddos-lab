FROM python:3.9-slim

RUN apt update && apt install -y tcpdump iproute2 \
    && pip install scapy requests

COPY syn_flood.py /syn_flood.py
COPY http_flood.py /http_flood.py

CMD ["sleep", "infinity"]
