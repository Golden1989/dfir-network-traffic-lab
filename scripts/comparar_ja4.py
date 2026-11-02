import argparse
import csv
import glob
import os
from collections import Counter

def detectar_codificacao(caminho):
    with open(caminho, "rb") as f:
        inicio = f.read(2)
    return "utf-16" if inicio in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"

parser = argparse.ArgumentParser(description="Compara as impressões JA4 de um nome (SNI) entre várias capturas")
parser.add_argument("--pasta", default=".", help="pasta com os CSVs hellos-captura??-*.csv (padrão: pasta atual)")
parser.add_argument("--nome", default="mobile.events.data.microsoft.com", help="parte do SNI a procurar")
args = parser.parse_args()

arquivos = sorted(glob.glob(os.path.join(args.pasta, "hellos-captura??-*.csv")))
for caminho in arquivos:
    contagem = Counter()
    with open(caminho, newline="", encoding=detectar_codificacao(caminho)) as f:
        for linha in csv.DictReader(f):
            if args.nome in linha["tls.handshake.extensions_server_name"]:
                contagem[linha["tls.handshake.ja4"]] += 1
    captura = os.path.basename(caminho).replace("hellos-", "").replace(".csv", "")
    if contagem:
        print(captura)
        for ja4, n in contagem.most_common():
            print(f"   {n}x {ja4}")
    else:
        print(f"{captura}: (nenhum)")
