#!/usr/bin/env python3
"""
network_scanner.py
Now includes:
✓ Host Discovery
✓ Top 100 Port Scan
✓ OS Detection
✓ Vulnerability Scan using NSE (--script vuln)
✓ Custom Date Format (01-Dec-2025)
"""
import sys, subprocess, os, time
from pathlib import Path

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

TARGET = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1/32"

# ---------------------------
#   DATE FORMAT: 01-Dec-2025
# ---------------------------
TIMESTAMP = time.strftime("%d-%b-%Y")

HOST_DISCOVERY_TXT = REPORT_DIR / f"hosts_{TIMESTAMP}.txt"
PORT_SCAN_TXT = REPORT_DIR / f"ports_{TIMESTAMP}.txt"
OS_SCAN_TXT = REPORT_DIR / f"os_{TIMESTAMP}.txt"
VULN_SCAN_TXT = REPORT_DIR / f"vuln_{TIMESTAMP}.txt"
PORT_SCAN_XML = REPORT_DIR / f"ports_{TIMESTAMP}.xml"
HTML_REPORT = REPORT_DIR / f"network_report_{TIMESTAMP}.html"

def run(cmd):
    print("[+] Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    print("[*] Target:", TARGET)
    print("[*] Date Format:", TIMESTAMP)

    # 1) Host Discovery
    run(["nmap", "-sn", "-n", "-oN", str(HOST_DISCOVERY_TXT), TARGET])

    # 2) Top 100 Port Scan
    run([
        "nmap", "-sS", "-sV",
        "--top-ports", "100",
        "-oN", str(PORT_SCAN_TXT),
        "-oX", str(PORT_SCAN_XML),
        TARGET
    ])

    # 3) OS Detection
    run([
        "nmap", "-O",
        "-oN", str(OS_SCAN_TXT),
        TARGET
    ])

    # 4) Vulnerability Scan (Nmap NSE Scripts)
    print("[*] Running vulnerability scan... (this may take longer)")
    run([
        "nmap", "--script", "vuln",
        "-oN", str(VULN_SCAN_TXT),
        TARGET
    ])

    # 5) Build HTML Report
    html = []
    html.append("<html><head><meta charset='utf-8'><title>Network Scan Report</title></head><body>")
    html.append("<h1>Network Scan Report</h1>")
    html.append(f"<p>Target: {TARGET}</p>")
    html.append(f"<p>Date: {TIMESTAMP}</p>")

    html.append("<h2>Host Discovery</h2><pre>")
    html.append(HOST_DISCOVERY_TXT.read_text())
    html.append("</pre>")

    html.append("<h2>Top 100 Port Scan</h2><pre>")
    html.append(PORT_SCAN_TXT.read_text())
    html.append("</pre>")

    html.append("<h2>OS Detection</h2><pre>")
    html.append(OS_SCAN_TXT.read_text())
    html.append("</pre>")

    html.append("<h2>Vulnerability Scan (NSE)</h2><pre>")
    html.append(VULN_SCAN_TXT.read_text())
    html.append("</pre>")

    html.append("</body></html>")
    HTML_REPORT.write_text("\n".join(html))

    print("[+] HTML report:", HTML_REPORT.resolve())
    print("[+] VULN report:", VULN_SCAN_TXT.resolve())
    print("[+] OS report:", OS_SCAN_TXT.resolve())
    print("[+] Port XML report:", PORT_SCAN_XML.resolve())

if __name__ == '__main__':
    main()
