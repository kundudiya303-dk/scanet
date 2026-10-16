"""
scanet — High-Speed Native Async Socket Port & Service Scanner
Provides a built-in, unprivileged fallback scanning engine when the native
Nmap binary is not installed in the host OS environment.
Outputs standard Nmap XML so all downstream adapters and parsers work seamlessly.
"""
import sys
import socket
import asyncio
import argparse
import time
from typing import List, Dict, Tuple

# Common top 100 TCP ports
TOP_100_PORTS = [
    20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 111, 119, 123, 135, 137, 138, 139,
    143, 161, 162, 179, 389, 443, 445, 465, 500, 514, 515, 520, 587, 631, 636, 873,
    990, 993, 995, 1025, 1080, 1194, 1433, 1434, 1521, 1723, 1812, 1813, 2049, 2082,
    2083, 2086, 2087, 2095, 2096, 2181, 2222, 2375, 2376, 3000, 3128, 3306, 3389, 3690,
    4000, 4040, 4444, 5000, 5432, 5601, 5672, 5900, 5984, 6379, 6667, 7000, 7001, 8000,
    8080, 8081, 8443, 8888, 9000, 9042, 9090, 9092, 9100, 9200, 9300, 9418, 9999, 10000,
    11211, 27017, 27018, 28017, 50000, 50070
]

WELL_KNOWN_SERVICES = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "domain", 80: "http",
    110: "pop3", 111: "rpcbind", 135: "msrpc", 139: "netbios-ssn", 143: "imap",
    443: "https", 445: "microsoft-ds", 587: "submission", 631: "ipp",
    993: "imaps", 995: "pop3s", 1433: "ms-sql-s", 1521: "oracle", 2049: "nfs",
    2222: "ssh-alt", 3000: "http-dev", 3306: "mysql", 3389: "ms-wbt-server",
    5000: "http-alt", 5432: "postgresql", 5900: "vnc", 6379: "redis",
    8000: "http-alt", 8080: "http-proxy", 8443: "https-alt", 8888: "http-alt",
    9000: "http-alt", 9200: "wap-wsp", 27017: "mongod"
}


async def probe_port(ip: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, str, str]:
    """Probes a single TCP port and attempts simple banner grabbing."""
    conn = asyncio.open_connection(ip, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=timeout)
    except Exception:
        return port, False, "", ""

    # Port is open
    service = WELL_KNOWN_SERVICES.get(port, "unknown")
    banner = ""

    try:
        # Quick HTTP probe if port is 80/443/8080/3000/5000/8000
        if port in (80, 8080, 3000, 5000, 8000, 8888):
            writer.write(b"HEAD / HTTP/1.0\r\nHost: " + ip.encode() + b"\r\n\r\n")
            await writer.drain()
            raw_banner = await asyncio.wait_for(reader.read(512), timeout=0.8)
            banner = raw_banner.decode("utf-8", errors="replace").splitlines()[0] if raw_banner else ""
            if "HTTP" in banner:
                service = "http"
        elif port == 21:
            raw_banner = await asyncio.wait_for(reader.read(256), timeout=0.8)
            banner = raw_banner.decode("utf-8", errors="replace").strip() if raw_banner else ""
        elif port in (22, 2222):
            raw_banner = await asyncio.wait_for(reader.read(256), timeout=0.8)
            banner = raw_banner.decode("utf-8", errors="replace").strip() if raw_banner else ""
    except Exception:
        pass
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

    return port, True, service, banner


async def scan_host(target: str, ports: List[int], concurrency: int = 64, timeout: float = 1.0):
    start_time = time.time()
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror as e:
        print(f"[scanet-scanner] Failed to resolve target '{target}': {e}", flush=True)
        return [], 0.0

    print(f"[scanet-scanner] Starting Scanet Native Recon Engine on {target} ({ip})", flush=True)
    print(f"[scanet-scanner] Scanning {len(ports)} target ports (concurrency={concurrency}, timeout={timeout}s)...", flush=True)

    sem = asyncio.Semaphore(concurrency)
    open_ports = []

    async def sem_probe(p):
        async with sem:
            res = await probe_port(ip, p, timeout=timeout)
            if res[1]:
                port, _, svc, banner = res
                banner_info = f" — [{banner[:40]}]" if banner else ""
                print(f"[scanet-scanner] Discovered open port {port}/tcp ({svc}){banner_info}", flush=True)
                open_ports.append(res)

    tasks = [sem_probe(p) for p in ports]
    await asyncio.gather(*tasks)

    duration = time.time() - start_time
    print(f"[scanet-scanner] Completed in {duration:.2f}s: {len(open_ports)} open ports found.", flush=True)
    return open_ports, ip, duration


def generate_nmap_xml(target: str, ip: str, open_ports: list, duration: float) -> str:
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE nmaprun>',
        f'<nmaprun scanner="scanet-native-scanner" args="scanet-native {target}" start="{int(time.time())}" version="7.94">',
        f'<host starttime="{int(time.time() - duration)}" endtime="{int(time.time())}">',
        '  <status state="up" reason="conn-refused"/>',
        f'  <address addr="{ip}" addrtype="ipv4"/>',
        '  <hostnames>',
        f'    <hostname name="{target}" type="user"/>',
        '  </hostnames>',
        '  <ports>'
    ]

    for port, is_open, svc, banner in sorted(open_ports, key=lambda x: x[0]):
        prod = banner.replace('"', '&quot;') if banner else ""
        xml_lines.append(f'    <port protocol="tcp" portid="{port}">')
        xml_lines.append('      <state state="open" reason="syn-ack"/>')
        xml_lines.append(f'      <service name="{svc}" product="{prod}" method="probed"/>')
        xml_lines.append('    </port>')

    xml_lines.append('  </ports>')
    xml_lines.append('</host>')
    xml_lines.append(f'<runstats><finished time="{int(time.time())}" elapsed="{duration:.2f}" summary="Scan completed"/></runstats>')
    xml_lines.append('</nmaprun>')
    return "\n".join(xml_lines)


def main():
    parser = argparse.ArgumentParser(description="Scanet Built-in Native Reconnaissance Scanner")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("--ports", default="top-100", help="Port profile: top-100, top-1000, top-65535, or custom comma-list")
    parser.add_argument("--speed", default="3", help="Timing speed 1-4")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout seconds")
    args = parser.parse_args()

    # Determine ports
    if args.ports == "top-100":
        port_list = TOP_100_PORTS
    elif args.ports == "top-1000":
        port_list = sorted(list(set(TOP_100_PORTS + list(range(1, 1024)))))
    elif args.ports == "top-65535":
        port_list = list(range(1, 65536))
    else:
        try:
            port_list = [int(p.strip()) for p in args.ports.split(",") if p.strip().isdigit()]
        except Exception:
            port_list = TOP_100_PORTS

    timeout = 0.6 if args.speed == "4" else (1.2 if args.speed == "2" else 0.9)
    concurrency = 128 if args.speed == "4" else 64

    open_ports, ip, duration = asyncio.run(scan_host(args.target, port_list, concurrency=concurrency, timeout=timeout))
    xml_output = generate_nmap_xml(args.target, ip, open_ports, duration)
    print("\n" + xml_output)


if __name__ == "__main__":
    main()
