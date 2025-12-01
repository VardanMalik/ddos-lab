#!/bin/bash

echo "Applying iptables rate limits..."
iptables -A INPUT -p tcp --syn -m limit --limit 5/s --limit-burst 10 -j ACCEPT
iptables -A INPUT -p tcp --syn -j DROP

echo "iptables rules applied."
