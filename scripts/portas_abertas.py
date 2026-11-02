import argparse
import csv
from collections import defaultdict

def detectar_codificacao(caminho):
    with open(caminho, "rb") as f:
        inicio = f.read(2)
    return "utf-16" if inicio in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"

parser = argparse.ArgumentParser(description="Lista portas abertas a partir de SYN/ACK exportados pelo tshark")
parser.add_argument("csv", help="CSV com frame.time_epoch, ip.src e tcp.srcport")
parser.add_argument("--ip", help="mostrar só este IP (opcional)")
args = parser.parse_args()

respostas = defaultdict(list)
with open(args.csv, newline="", encoding=detectar_codificacao(args.csv)) as f:
    for linha in csv.DictReader(f):
        if not linha["ip.src"]:
            continue
        chave = (linha["ip.src"], int(linha["tcp.srcport"]))
        respostas[chave].append(float(linha["frame.time_epoch"]))

dispositivos = sorted({ip for ip, _ in respostas if not args.ip or ip == args.ip})
for ip in dispositivos:
    portas = sorted(porta for (origem, porta) in respostas if origem == ip)
    print(f"{ip}: {len(portas)} portas abertas")
    for porta in portas:
        tempos = respostas[(ip, porta)]
        print(f"  {porta}/tcp: {len(tempos)} SYN/ACK (1 resposta + {len(tempos) - 1} repetições)")
