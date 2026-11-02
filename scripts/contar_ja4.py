import argparse
import csv
from collections import defaultdict

def detectar_codificacao(caminho):
    with open(caminho, "rb") as f:
        inicio = f.read(2)
    return "utf-16" if inicio in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"

parser = argparse.ArgumentParser(description="Agrupa Client Hello por impressão JA4")
parser.add_argument("csv", help="CSV com tls.handshake.ja4 e tls.handshake.extensions_server_name")
args = parser.parse_args()

nomes_por_ja4 = defaultdict(list)
with open(args.csv, newline="", encoding=detectar_codificacao(args.csv)) as f:
    for linha in csv.DictReader(f):
        ja4 = linha["tls.handshake.ja4"]
        nomes_por_ja4[ja4].append(linha["tls.handshake.extensions_server_name"])

total = sum(len(nomes) for nomes in nomes_por_ja4.values())
print(f"{total} Client Hello, {len(nomes_por_ja4)} impressões JA4 distintas\n")

for ja4, nomes in sorted(nomes_por_ja4.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"{len(nomes)}x {ja4}")
    for nome in sorted(set(nomes)):
        print(f"     {nome}")
