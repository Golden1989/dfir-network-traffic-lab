# dfir-network-traffic-lab

[English](README.md) | **Português (Brasil)**

Laboratório de análise de tráfego de rede para DFIR (forense digital e resposta a incidentes), feito **só na minha própria rede e nos meus próprios aparelhos**, com fins de estudo. Este repositório guarda os **scripts** e o guia de comandos. Não contém capturas (pcap), chaves TLS nem dados derivados delas.

## Escopo e ética

- Capturei apenas o tráfego do meu computador e o que a rede anuncia a todos (ARP, mDNS, SSDP).
- Varreduras de portas foram feitas só em aparelhos meus.
- Não use estas ferramentas em redes ou aparelhos de terceiros sem autorização por escrito.

## Principais achados

Evidências, limites e casos em aberto estão no [relatório](reports/relatorio-forense-pt.pdf).

| Achado | Certeza |
| --- | --- |
| O tráfego QUIC para `dns.google` só aparece com o navegador Opera GX rodando (7 capturas comparadas, mudando uma condição por vez) | Alta |
| Com o arquivo de chaves TLS (`SSLKEYLOGFILE`), o Wireshark lê em claro o tráfego HTTP do meu próprio navegador; sem as chaves, só ficam visíveis o SNI, os IPs, as portas, os tempos e os tamanhos | Alta |
| Uma varredura de 1.000 portas se reconhece por contagem: 1.000 portas distintas em 1,17 s da mesma origem, detectadas por um script de janela deslizante (a navegação normal não o disparou) | Alta |

## O que há aqui

| Arquivo | O que faz |
| --- | --- |
| `scripts/contar_portas.py` | Versão 1, didática: conta portas distintas por par origem/destino na captura inteira, sem janela de tempo (edite o caminho do CSV no topo do arquivo) |
| `scripts/contar_portas_v3.py` | Procura varredura de portas: conta portas distintas por par origem/destino em uma janela deslizante (`--limite`, `--janela`) |
| `scripts/taxa_arp.py` | Procura taxa anormal de respostas ARP: conta respostas ARP por MAC de origem em uma janela deslizante, para achar enxurradas de respostas não solicitadas (`--limite`, `--janela`) |
| `scripts/arp_sem_pergunta.py` | Conta as respostas ARP que não tiveram pergunta correspondente nos `--espera` segundos anteriores, por MAC de origem (checagem de resposta não solicitada; use junto com `taxa_arp.py`) |
| `scripts/portas_abertas.py` | Lista as portas abertas (SYN/ACK) e quantas vezes cada uma respondeu |
| `scripts/contar_ja4.py` | Agrupa os Client Hello pela impressão JA4 e lista os nomes (SNI) de cada grupo |
| `scripts/comparar_ja4.py` | Compara as impressões JA4 de um nome (SNI) entre várias capturas |
| `docs/comandos.md` | Comandos do tshark e filtros de exibição do Wireshark |

## Relatórios

O relatório forense completo deste laboratório, em dois idiomas:

- [`reports/relatorio-forense-pt.pdf`](reports/relatorio-forense-pt.pdf) (português)
- [`reports/forensic-report-en.pdf`](reports/forensic-report-en.pdf) (inglês)

## Requisitos

- Python 3.8 ou mais novo (só biblioteca padrão)
- Wireshark (inclui o `tshark`) e Nmap

## Como usar

1. Capture com o Wireshark e salve o arquivo `.pcapng` numa pasta **fora** deste repositório.
2. Exporte os campos que interessam para CSV com o `tshark` (comandos em `docs/comandos.md`).
3. Rode o script sobre o CSV, por exemplo:

```powershell
python .\scripts\contar_portas_v3.py syn-captura.csv --limite 100 --janela 5
```

Os scripts detectam sozinhos se o CSV está em UTF-16 (o `>` do Windows PowerShell 5) ou UTF-8.

## Teste sem ter nenhuma captura

A pasta `examples/` tem CSVs pequenos e **sintéticos** (faixas de IP de documentação e nomes `.example`, sem dados reais) e a saída esperada de cada script. A partir da raiz do repositório:

```powershell
python .\scripts\contar_portas_v3.py .\examples\syn-example.csv --limite 100 --janela 5
python .\scripts\portas_abertas.py .\examples\synack-example.csv
python .\scripts\taxa_arp.py .\examples\arp-example.csv --limite 10 --janela 5
python .\scripts\arp_sem_pergunta.py .\examples\arp-todos-example.csv --espera 20
python .\scripts\contar_ja4.py .\examples\hellos-captura01-example.csv
python .\scripts\comparar_ja4.py --pasta .\examples --nome telemetry.example.net
```

Compare a sua saída com [`examples/expected-output.txt`](examples/expected-output.txt).

## Limitações

- Os scripts de SYN e SYN/ACK olham só IPv4.
- A detecção por janela de tempo perde varreduras lentas: aumente a janela para pegá-las, ao custo de mais falsos positivos.
- A impressão JA4 mostra a família do software, não o aplicativo exato nem o site.

## Não faz parte do repositório

Capturas, arquivos de chaves TLS, CSVs e notas com endereços de aparelhos ficam só no meu computador e estão no `.gitignore`.
