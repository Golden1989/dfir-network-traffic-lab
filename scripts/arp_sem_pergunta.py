"""Conta, por MAC de origem, as respostas ARP que NÃO tiveram pergunta antes.

Uma resposta "tem pergunta" se, nos últimos --espera segundos, quem a recebeu
pediu justamente o IP de quem respondeu. Use junto com taxa_arp.py: a taxa mede
a densidade; este script mede a origem.

O CSV vem do tshark com o filtro "arp" (perguntas e respostas), campos:
frame.time_epoch, arp.opcode, eth.src, arp.src.proto_ipv4, arp.dst.proto_ipv4.
"""
import argparse
import csv
from collections import defaultdict

def detectar_codificacao(caminho):
    with open(caminho, "rb") as f:
        inicio = f.read(2)
    return "utf-16" if inicio in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"

parser = argparse.ArgumentParser(description="Conta respostas ARP que não tiveram pergunta antes")
parser.add_argument("csv", help="CSV do tshark com perguntas e respostas ARP (arp.opcode)")
parser.add_argument("--espera", type=float, default=20.0, help="segundos entre a pergunta e a resposta para ainda contar")
args = parser.parse_args()

perguntas = {}                  # (quem_perguntou, ip_perguntado) -> instante da última pergunta
total = defaultdict(int)
sem_pergunta = defaultdict(int)

with open(args.csv, newline="", encoding=detectar_codificacao(args.csv)) as f:
    for linha in csv.DictReader(f):
        t = float(linha["frame.time_epoch"])
        if linha["arp.opcode"] == "1":
            perguntas[(linha["arp.src.proto_ipv4"], linha["arp.dst.proto_ipv4"])] = t
        else:
            mac = linha["eth.src"]
            total[mac] += 1
            chave = (linha["arp.dst.proto_ipv4"], linha["arp.src.proto_ipv4"])
            if chave not in perguntas or t - perguntas[chave] > args.espera:
                sem_pergunta[mac] += 1

for mac, n in total.items():
    print(f"{mac}: {n} respostas, {sem_pergunta[mac]} sem pergunta (espera de {args.espera} s)")