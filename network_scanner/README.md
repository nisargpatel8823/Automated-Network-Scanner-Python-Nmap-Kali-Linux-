# Automated Network Vulnerability Scanner

Simple starter project that runs nmap host discovery and a top-100 ports service/version scan,
then writes a basic HTML report.

Requirements:
- nmap installed on the host (Kali includes it).
- Python 3

Usage:
- cd into project folder and run:
  python3 network_scanner.py 192.168.1.0/24

Output:
- reports/network_report_<timestamp>.html
