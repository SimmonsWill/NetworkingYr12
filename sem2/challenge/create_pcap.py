
from scapy.all import IP, TCP, UDP, DNS, DNSQR, Raw, wrpcap
import random

random.seed(42)

packets = []
destination_ip = "192.0.2.10"
source_ip = "192.0.2.20"

# Fictional credentials for the CTF challenge
username = "trainee"
password = "chain_reaction_7f3a"

def add_packet(packet):
    packets.append(packet)

# 1. Generate background DNS traffic
for i in range(100):
    src = f"192.0.2.{random.randint(30, 80)}"
    dns_id = random.randint(1, 65535)
    domain = random.choice([
        "training.example",
        "updates.example",
        "docs.example",
        "status.example",
        "files.example",
        "mail.example",
        "portal.example",
        "cdn.example",
    ])

    add_packet(
        IP(src=src, dst="192.0.2.53") /
        UDP(sport=random.randint(20000, 60000), dport=53) /
        DNS(
            id=dns_id,
            rd=1,
            qd=DNSQR(qname=domain)
        )
    )

# 2. Generate background TCP traffic
for i in range(100):
    src = f"192.0.2.{random.randint(30, 80)}"
    dst = f"192.0.2.{random.randint(90, 110)}"
    sport = random.randint(20000, 60000)
    dport = random.choice([80, 443, 22, 8080])

    add_packet(
        IP(src=src, dst=dst) /
        TCP(
            sport=sport,
            dport=dport,
            flags="S",
            seq=random.randint(1000, 900000)
        )
    )

# 3. Create a synthetic TCP conversation for the login
client_port = 51514
client_seq = 1000
server_seq = 5000

# TCP handshake
add_packet(
    IP(src=source_ip, dst=destination_ip) /
    TCP(sport=client_port, dport=80, flags="S", seq=client_seq)
)

add_packet(
    IP(src=destination_ip, dst=source_ip) /
    TCP(sport=80, dport=client_port, flags="SA",
        seq=server_seq, ack=client_seq + 1)
)

add_packet(
    IP(src=source_ip, dst=destination_ip) /
    TCP(sport=client_port, dport=80, flags="A",
        seq=client_seq + 1, ack=server_seq + 1)
)

# HTTP login request
body = f"username={username}&password={password}".encode()

http_request = (
    b"POST /login HTTP/1.1\r\n"
    b"Host: training.example\r\n"
    b"Content-Type: application/x-www-form-urlencoded\r\n"
    + f"Content-Length: {len(body)}\r\n".encode()
    + b"\r\n"
    + body
)

add_packet(
    IP(src=source_ip, dst=destination_ip) /
    TCP(
        sport=client_port,
        dport=80,
        flags="PA",
        seq=client_seq + 1,
        ack=server_seq + 1
    ) /
    Raw(load=http_request)
)

# Simulated HTTP response
response = (
    b"HTTP/1.1 401 Unauthorized\r\n"
    b"Content-Length: 18\r\n"
    b"Connection: keep-alive\r\n"
    b"\r\n"
    b"Invalid password."
)

add_packet(
    IP(src=destination_ip, dst=source_ip) /
    TCP(
        sport=80,
        dport=client_port,
        flags="PA",
        seq=server_seq + 1,
        ack=client_seq + 1 + len(http_request)
    ) /
    Raw(load=response)
)

# 4. Add more unrelated UDP traffic
for i in range(100):
    src = f"192.0.2.{random.randint(30, 80)}"
    dst = f"192.0.2.{random.randint(90, 110)}"

    add_packet(
        IP(src=src, dst=dst) /
        UDP(
            sport=random.randint(1024, 65535),
            dport=random.choice([53, 123, 5000, 9000])
        ) /
        Raw(load=random.randbytes(random.randint(10, 80)))
    )

# Shuffle packets so the player must investigate the capture
random.shuffle(packets)

# Write the capture file
wrpcap("secret.pcap", packets)

print("Successfully created secret.pcap")
print(f"Total packets: {len(packets)}")
print("Open secret.pcap in Wireshark to investigate.")

