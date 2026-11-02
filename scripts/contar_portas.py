"""Versão 1 (didática): conta portas de destino distintas por par origem -> destino.

Sem janela de tempo e sem limite: só mostra o total da captura inteira.
Para detectar varredura de verdade, use contar_portas_v3.py.

ANTES DE USAR: troque ARQUIVO pelo caminho do seu CSV.
O CSV deve ter as colunas ip.src, ip.dst e tcp.dstport (exportado com tshark).
O exemplo abaixo está em UTF-16 (o que o '>' do Windows PowerShell 5 gera);
se exportou com Out-File -Encoding utf8, troque CODIFICACAO por "utf-8-sig".
"""
import csv
from collections import defaultdict

ARQUIVO = r"C:\caminho\da\pasta-de-trabalho\dados\syn-exemplo.csv"  # <- EDITE AQUI
CODIFICACAO = "utf-16"

portas_por_par = defaultdict(set)

with open(ARQUIVO, newline="", encoding=CODIFICACAO) as f:
    for linha in csv.DictReader(f):
        origem = linha["ip.src"] or "(sem IPv4)"
        destino = linha["ip.dst"] or "(sem IPv4)"
        portas_por_par[(origem, destino)].add(linha["tcp.dstport"])

for (origem, destino), portas in sorted(portas_por_par.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"{origem} -> {destino}: {len(portas)} portas distintas")
