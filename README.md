# dfir-network-traffic-lab

**English** | [Português (Brasil)](README.pt-BR.md)

A study lab on network traffic analysis for DFIR (digital forensics and incident response), carried out **only on my own network and my own devices**. This repository holds the **scripts** and a command guide. It does not contain packet captures (pcap), TLS key files, or any data derived from them.

## Scope and ethics

- I captured only my own computer's traffic and what the network announces to everyone (ARP, mDNS, SSDP).
- Port scans were run only against devices I own.
- Do not use these tools on other people's networks or devices without written authorization.

## What is here

| File | What it does |
| --- | --- |
| `scripts/contar_portas.py` | Version 1, didactic: counts distinct destination ports per source/destination pair over the whole capture, with no time window (edit the CSV path at the top of the file) |
| `scripts/contar_portas_v3.py` | Looks for port scans: counts distinct ports per source/destination pair in a sliding time window (`--limite` = threshold, `--janela` = window in seconds) |
| `scripts/portas_abertas.py` | Lists open ports (from SYN/ACK replies) and how many times each one answered |
| `scripts/contar_ja4.py` | Groups TLS Client Hellos by JA4 fingerprint and lists the server names (SNI) in each group |
| `scripts/comparar_ja4.py` | Compares the JA4 fingerprints of one server name (SNI) across several captures |
| `docs/comandos.md` | tshark commands and Wireshark display filters (in Portuguese) |

Script names, option names, and comments are in Portuguese, because this is a Brazilian study project.

## Reports

The full forensic report from this lab, in two languages:

- [`reports/forensic-report-en.pdf`](reports/forensic-report-en.pdf) (English)
- [`reports/relatorio-forense-pt.pdf`](reports/relatorio-forense-pt.pdf) (Portuguese)

## Requirements

- Python 3.8 or newer (standard library only)
- Wireshark (includes `tshark`) and Nmap

## How to use

1. Capture with Wireshark and save the `.pcapng` file in a folder **outside** this repository.
2. Export the fields you need to CSV with `tshark` (commands in `docs/comandos.md`).
3. Run a script on the CSV, for example:

```powershell
python .\scripts\contar_portas_v3.py syn-capture.csv --limite 100 --janela 5
```

The scripts detect on their own whether the CSV is UTF-16 (what `>` produces in Windows PowerShell 5) or UTF-8.

## Limitations

- The SYN and SYN/ACK scripts look at IPv4 only.
- Time-window detection misses slow scans: widen the window to catch them, at the cost of more false positives.
- A JA4 fingerprint shows the software family, not the exact application or website.
- A port scan is reconnaissance, not proof of intrusion.

## Not part of the repository

Captures, TLS key files, CSVs, and notes containing device addresses stay on my computer only and are listed in `.gitignore`.
