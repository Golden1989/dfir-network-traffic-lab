import argparse
import csv
from collections import defaultdict

def detectar_codificacao(caminho):
    with open(caminho, "rb") as f:
        inicio = f.read(2)
    return "utf-16" if inicio in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"

parser = argparse.ArgumentParser(description="Detecta taxa anormal de respostas ARP por origem (MAC)")
parser.add_argument("csv", help="CSV do tshark com frame.time_epoch e eth.src (respostas ARP)")
parser.add_argument("--limite", type=int, default=10, help="respostas na janela para disparar o alerta")
parser.add_argument("--janela", type=float, default=5.0, help="tamanho da janela, em segundos")
args = parser.parse_args()

respostas = defaultdict(list)
with open(args.csv, newline="", encoding=detectar_codificacao(args.csv)) as f:
    for linha in csv.DictReader(f):
        origem = linha["eth.src"]
        respostas[origem].append(float(linha["frame.time_epoch"]))

for origem, tempos in respostas.items():
    tempos.sort()
    melhor = 0
    inicio = 0
    for fim in range(len(tempos)):
        while tempos[fim] - tempos[inicio] > args.janela:
            inicio += 1
        melhor = max(melhor, fim - inicio + 1)
    estado = "ALERTA" if melhor > args.limite else "ok"
    print(f"{estado}: {origem}: máximo de {melhor} respostas em {args.janela} s (limite {args.limite})")
