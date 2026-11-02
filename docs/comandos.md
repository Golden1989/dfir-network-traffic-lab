# Comandos e filtros (guia rápido)

Tudo roda no PowerShell do Windows. As capturas e os CSVs ficam numa pasta de trabalho **fora** do repositório; o repositório só tem os scripts e este guia.

## 0. Preparo (a cada nova sessão do PowerShell)

```powershell
$lab = "C:\caminho\da\pasta-de-trabalho"   # fora do repositório
$cap = "captura01-nome"   # nome da captura, sem .pcapng (o arquivo fica em $lab\pcaps)
$tshark = "C:\Program Files\Wireshark\tshark.exe"
Get-FileHash "$lab\pcaps\$cap.pcapng" -Algorithm SHA256
```

O hash (SHA-256) é a "impressão digital" do arquivo: anote para provar depois que a captura não mudou.

## 1. Achar varredura de portas (SYN puro)

```powershell
& $tshark -r "$lab\pcaps\$cap.pcapng" -Y "tcp.flags.syn==1 and tcp.flags.ack==0" -T fields -e frame.time_epoch -e ip.src -e ip.dst -e tcp.dstport -E "separator=," -E header=y | Out-File -Encoding utf8 "$lab\dados\syn-$cap.csv"
python .\scripts\contar_portas_v3.py "$lab\dados\syn-$cap.csv" --limite 100 --janela 5
```

`--limite` é quantas portas distintas disparam o alerta, e `--janela` é o tamanho da janela, em segundos. Teste combinações. Para pegar scans lentos, aumente a janela.

## 2. Listar portas abertas (SYN/ACK)

```powershell
& $tshark -r "$lab\pcaps\$cap.pcapng" -Y "tcp.flags.syn==1 and tcp.flags.ack==1" -T fields -e frame.time_epoch -e ip.src -e tcp.srcport -E "separator=," -E header=y | Out-File -Encoding utf8 "$lab\dados\synack-$cap.csv"
python .\scripts\portas_abertas.py "$lab\dados\synack-$cap.csv" --ip 192.168.1.40
```

`--ip` é opcional (mostra só um aparelho). Várias respostas por porta são as repetições do SYN/ACK de conexões meio abertas.

## 3. Client Hello e impressão JA4

```powershell
& $tshark -r "$lab\pcaps\$cap.pcapng" -Y "tls.handshake.type==1" -T fields -e frame.time_epoch -e ip.src -e ipv6.src -e tls.handshake.extensions_server_name -e tls.handshake.ja4 -E "separator=," -E header=y | Out-File -Encoding utf8 "$lab\dados\hellos-$cap.csv"
python .\scripts\contar_ja4.py "$lab\dados\hellos-$cap.csv"
```

Agrupa os Client Hello por JA4 e lista os nomes (SNI) de cada grupo.

## 4. Comparar um nome entre todas as capturas

Primeiro exporte os Client Hello de todas as capturas:

```powershell
Get-ChildItem $lab\pcaps\captura*.pcapng | ForEach-Object {
  $saida = "$lab\dados\hellos-" + $_.BaseName + ".csv"
  & $tshark -r $_.FullName -Y "tls.handshake.type==1" -T fields -e frame.time_epoch -e ip.src -e ipv6.src -e tls.handshake.extensions_server_name -e tls.handshake.ja4 -E "separator=," -E header=y | Out-File -Encoding utf8 $saida
}
python .\scripts\comparar_ja4.py --pasta "$lab\dados" --nome mobile.events.data.microsoft.com
```

Troque `--nome` por qualquer parte do SNI (por exemplo `spotify`).

## 4b. Taxa de respostas ARP (enxurrada de respostas sem pergunta)

```powershell
& $tshark -r "$lab\pcaps\$cap.pcapng" -Y "arp.opcode == 2" -T fields -e frame.time_epoch -e eth.src -e arp.src.hw_mac -e arp.src.proto_ipv4 -e arp.dst.proto_ipv4 -E header=y -E "separator=," | Out-File -Encoding utf8 "$lab\dados\arp-$cap.csv"
python .\scripts\taxa_arp.py "$lab\dados\arp-$cap.csv" --limite 10 --janela 5
```

`arp.opcode == 2` deixa só as respostas (1 é requisição). O script conta respostas por MAC de origem numa janela deslizante. Para checar spoofing, compare `eth.src` com `arp.src.hw_mac` e veja se um MAC diz ter vários IPs (ou um IP, vários MACs).

## Cuidados
- No PowerShell, argumentos com vírgula precisam de aspas: `-E "separator=,"`.
- Use `| Out-File -Encoding utf8` para gravar os CSVs. Os scripts também leem UTF-16, mas UTF-8 é o padrão daqui para frente.
- Os scripts olham só IPv4 (os de SYN e SYN/ACK). Pacotes IPv6 não entram, e isso é uma limitação.
- Apague os CSVs de capturas que você não quer guardar .

# Filtros de exibição do Wireshark (guia rápido)

Digite na barra de filtro: verde = sintaxe válida, vermelho = erro. O contador "Exibidos" na barra de baixo mostra quantos pacotes passaram.

## Combinar
```
and   or   not   ==   !=   contains
tcp.port in {80 443}          (valores separados por espaço, sem vírgula)
(dns or tls) and ip.addr == 192.168.1.10
```

## Endereços
```
ip.addr == 192.168.1.20       (IPv4, origem ou destino)
ipv6.addr == 2001:4860:4860::8844   (IPv6: não use ip.addr)
ip.src == ...   ip.dst == ...
eth.addr == aa:bb:cc:dd:ee:ff       (MAC)
ip.ttl < 64                   (TTL do IP, o dos saltos)
```

## ARP e descoberta
```
arp
arp.opcode == 1               (perguntas: who-has)
arp.opcode == 2               (respostas: is-at)
arp.src.proto_ipv4 == 192.168.1.30
mdns      ssdp      dhcp
vlan
```

## DNS
```
dns
dns.flags.response == 0       (perguntas)
dns.flags.response == 1       (respostas)
dns.qry.name contains "globo"
dns.qry.name == "www.globo.com" and dns.flags.response == 1
dns.qry.type == 65            (HTTPS)
dns.flags.rcode == 3          (NXDOMAIN)
```
Colunas úteis (botão direito, Aplicar como coluna): `dns.time` (tempo da resposta), `dns.resp.ttl`.

## TCP (portas e varredura)
```
tcp.flags.syn == 1 and tcp.flags.ack == 0   (SYN puro: "posso conversar?")
tcp.flags.syn == 1 and tcp.flags.ack == 1   (SYN/ACK: porta aberta)
tcp.flags.reset == 1                        (RST: porta fechada ou recusa)
tcp.port == 443        tcp.dstport == 80
tcp.analysis.retransmission                 (repetições)
udp.port == 15600
```

## TLS, QUIC e HTTP
```
tls.handshake.type == 1       (Client Hello)
tls.handshake.type == 2       (Server Hello)
tls.handshake.type == 11      (Certificate: some no TLS 1.3)
tls.handshake.extensions_server_name contains "spotify"   (SNI)
quic
http or http2 or http3        (só aparecem com o arquivo de chaves)
```
Colunas úteis: `tls.handshake.extensions_server_name`, `tls.handshake.ja3`, `tls.handshake.ja4`.

## Outros atalhos
- Estatísticas, Conversas e Pontos finais: contagem por IP ou por par, sem filtrar um a um.
- Estatísticas, Hierarquia de protocolos: quanto de cada protocolo.
- Botão direito em um pacote, Seguir, Fluxo TCP: lê a conversa inteira.
- Exibir, Formato de data e hora, Hora do dia: alinha pacotes com o relógio.
- Clicar no cabeçalho "No." restaura a ordem de tempo depois de ordenar por outra coluna.
