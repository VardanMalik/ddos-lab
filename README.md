# DDoS Attack Simulation and Mitigation Lab

This project implements a small Docker-based testbed to study HTTP flood behaviour and two mitigation techniques: `iptables` rate limiting and TCP SYN cookies.

## 1. Project structure

text
ddos-lab/
  docker-compose.yml
  attacker/
    Dockerfile
    syn_flood.py
    http_flood.py
  defender/
    Dockerfile
    nginx.conf
    enable_iptables.sh
  victim/
    Dockerfile
    index.html
  captures/        (optional, can store .pcap files here)
  analysis/
    analyze.ipynb  (optional notebook for plotting / notes)
  README.md

## 2. Prerequisites 
	•	Docker Desktop (tested on macOS)
	•	Basic familiarity with a terminal
	
## 3. Starting the testbed
	
	From the ddos-lab directory:
		
		"docker compose up --build"
	
This starts:
	•	victim – Nginx web server (port 8080 exposed on host)
	•	defender – reverse proxy and firewall (port 8090 exposed on host)
	•	attacker1 and attacker2 – containers used to generate attack traffic

You can verify that the victim is running by visiting:
	•	http://localhost:8080 (direct)
	•	http://localhost:8090 (via defender)
	
## 4. Running the attacks
	
	In the new terminal:
	
	"cd /path/to/ddos-lab

    # SYN flood
	docker exec -it attacker1 python3 /syn_flood.py

	# HTTP flood
	docker exec -it attacker1 python3 /http_flood.py"
	
	These scripts target the defender’s HTTP service on port 80 inside the Docker network.
	
	
## 5. Capturing traffic (example: baseline)
	
	Create a capture directory and record traffic on the defender’s eth0 interface:
	
	"docker exec defender mkdir -p /captures

	# Capture 500 packets for the baseline case
	docker exec defender tcpdump -i eth0 -c 500 -w /captures/baseline.pcap"
	
	While tcpdump is running, launch the HTTP flood again from attacker1. When 500 packets are captured, tcpdump will exit automatically.

	Copy the pcap file back to the host:
	
	"docker cp defender:/captures/baseline.pcap ~/Desktop/baseline.pcap"
	
	Repeat this process for the iptables and syncookies cases.
	
## 6. Enabling defences

6.1 iptables rate limiting

	"# Restart defender to clear old rules
	docker restart defender

	# Apply iptables rules
	docker exec defender /enable_iptables.sh"
	
	Then repeat the capture + HTTP flood procedure, saving the result as iptables.pcap.

6.2 SYN cookies

	"# Restart defender to clear firewall rules
	docker restart defender

	# Enable SYN cookies
	docker exec defender sysctl -w net.ipv4.tcp_syncookies=1"
	
	Again, repeat the capture + HTTP flood procedure, saving the result as syncookies.pcap.

## 7. Analysis

The .pcap files can be opened in Wireshark. In the project report, the following filters were used:
	•	SYN packets to port 80:
	
		"tcp.flags.syn == 1 && tcp.flags.ack == 0 && tcp.dstport == 80"
	
	•	ACK responses from port 80:
		tcp.srcport == 80 && tcp.flags.ack == 1
		
Counting the displayed packets for these filters in each scenario provides a simple quantitative comparison of attack intensity and server responsiveness.

## 8. Stopping the testbed

	"docker compose down"
