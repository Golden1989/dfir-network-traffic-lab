import argparse
import csv
from collections import defaultdict

def detectar_codificacao(caminho):
    with open(caminho, "rb") as f:
        inicio = f.read(2)
    return "utf-16" if inicio in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"

parser = argparse.ArgumentParser(description="Detecta varredura de portas em um CSV de SYN")
parser.add_argument("csv", help="caminho do CSV exportado pelo tshark")
parser.add_argument("--limite", type=int, default=100, help="portas distintas para disparar o alerta")
parser.add_argument("--janela", type=float, default=5.0, help="tamanho da janela, em segundos")
args = parser.parse_args()

pacotes = defaultdict(list)
with open(args.csv, newline="", encoding=detectar_codificacao(args.csv)) as f:
    for linha in csv.DictReader(f):
        if not linha["ip.src"]:
            continue
        par = (linha["ip.src"], linha["ip.dst"])
        pacotes[par].append((float(linha["frame.time_epoch"]), linha["tcp.dstport"]))

for par, lista in pacotes.items():
    lista.sort()
    melhor = 0
    inicio = 0
    for fim in range(len(lista)):
        while lista[fim][0] - lista[inicio][0] > args.janela:
            inicio += 1
        portas = {porta for _, porta in lista[inicio:fim + 1]}
        melhor = max(melhor, len(portas))
    estado = "ALERTA" if melhor > args.limite else "ok"
    print(f"{estado}: {par[0]} -> {par[1]}: máximo de {melhor} portas distintas em {args.janela} s (limite {args.limite})")
