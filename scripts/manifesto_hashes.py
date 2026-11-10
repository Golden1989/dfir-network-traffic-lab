"""Manifesto de hashes SHA-256 das capturas (cadeia de custódia).

Sem opção: calcula o SHA-256 de cada captura (.pcap e .pcapng) da PASTA e grava o
manifesto em SAIDA, uma linha por arquivo no formato "hash  nome" (o mesmo do
sha256sum). Se o manifesto já existir, o script recusa sobrescrever, para não
apagar o registro que prova uma alteração.

Com --verificar: recalcula os hashes e compara com o manifesto. Resultados:
  ok          o hash é o mesmo do manifesto
  ALTERADO    o arquivo existe, mas o hash mudou
  AUSENTE     o manifesto cita o arquivo, mas ele não está na pasta
  NOVO        há um arquivo na pasta que o manifesto nunca registrou

ANTES DE USAR: troque PASTA e SAIDA pelos seus caminhos. A pasta de SAIDA precisa
existir. Guarde o manifesto fora do repositório, junto com as capturas.
"""
import hashlib
from pathlib import Path
import argparse


PASTA = Path(r"C:\caminho\da\pasta-de-trabalho\pcaps")  # <- EDITE AQUI
SAIDA = Path(r"C:\caminho\da\pasta-de-trabalho\notas\manifesto-sha256.txt")  # <- EDITE AQUI

def hash_arquivo(arquivo):
    """Calcula o hash SHA256 de um arquivo."""
    h = hashlib.sha256()
    with open(arquivo, "rb") as f:
        while True:
            pedaco = f.read(1024 * 1024)  # Lê em blocos de 1 MB
            if not pedaco:
                break
            h.update(pedaco)
    return h.hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument("--verificar", action="store_true")
args = parser.parse_args()
if args.verificar:
    esperado = {}
    for linha in SAIDA.read_text(encoding="utf-8").splitlines():
        h, nome = linha.split("  ", 1)
        esperado[nome] = h

    for nome, h_esperado in esperado.items():
        arquivo = PASTA / nome
        if not arquivo.exists():
            print(f"AUSENTE: {nome}")
        elif hash_arquivo(arquivo) == h_esperado:
            print(f"ok: {nome}")
        else:
            print(f"ALTERADO: {nome}")

    for arquivo in sorted(PASTA.glob("*.pcap*")):
        if arquivo.name not in esperado:
            print(f"NOVO (fora do manifesto): {arquivo.name}")

else:
    if SAIDA.exists():
        print("O manifesto já existe. Não vou sobrescrever.")
        raise SystemExit(1)
    linhas = []
    for arquivo in sorted(PASTA.glob("*.pcap*")):
        h = hash_arquivo(arquivo)
        linhas.append(f"{h}  {arquivo.name}")

    SAIDA.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"{len(linhas)} arquivos no manifesto")
