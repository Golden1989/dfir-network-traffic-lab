# Folha de custódia / Chain of custody sheet (EXEMPLO FICTÍCIO / FICTIONAL EXAMPLE)

> Todos os dados abaixo são inventados. Não existe esta captura, e o hash não pertence a nenhum arquivo real.
> All data below is made up. This capture does not exist, and the hash does not belong to any real file.

## 1. Identificação da evidência / Evidence identification

| Campo / Field | Valor / Value |
|---|---|
| Nº do caso / Case no. | CASE-0001 |
| Nº da evidência / Evidence no. | EV-001 |
| Descrição / Description | Captura de tráfego de rede (pcapng) da rede doméstica de teste / Network traffic capture (pcapng) of a home test network |
| Nome do arquivo / File name | example-capture-01.pcapng |
| Tamanho em bytes / Size in bytes | 123456 |
| SHA-256 | f5be3972e2cd6273cc7a66cf19cb9db017412d687724abe7574c7059a49acb7e |

## 2. Coleta / Collection

| Campo / Field | Valor / Value |
|---|---|
| Data e hora, com fuso / Date and time, with time zone | 2026-01-15 14:30 (UTC-03:00) |
| Coletado por / Collected by | Analyst A. Example |
| Local ou rede / Location or network | Wi-Fi da rede doméstica de teste / Home test network Wi-Fi |
| Ferramenta e versão / Tool and version | Wireshark 4.x, interface Wi-Fi |
| Autorização / Authorization | Rede e dispositivos próprios do analista / Analyst's own network and devices |
| Observações / Notes | Captura gerada durante um exercício de estudo / Capture produced during a study exercise |

## 3. Registro de movimentações / Transfer and access log

| Data e hora / Date-time | Quem / Who | Ação / Action | Origem → destino / From → to | Hash conferido? / Hash verified? |
|---|---|---|---|---|
| 2026-01-15 14:45 | Analyst A. Example | Salvou o arquivo / Saved the file | Wireshark → pasta de capturas / capture folder | Sim, manifesto gerado / Yes, manifest generated |
| 2026-01-16 09:10 | Analyst A. Example | Análise com scripts (somente leitura) / Analysis with scripts (read-only) | pasta de capturas / capture folder | Sim, `--verificar` ok / Yes, `--verificar` ok |
| 2026-01-20 18:00 | Analyst A. Example | Cópia para disco externo de backup / Copy to external backup drive | pasta de capturas → disco externo / capture folder → external drive | Sim, hashes iguais / Yes, hashes match |

## 4. Encerramento / Closing

| Campo / Field | Valor / Value |
|---|---|
| Situação final / Final status | Arquivado, sem alterações / Archived, unchanged |
| Hash final conferido / Final hash verified | Sim / Yes |
| Responsável / Responsible | Analyst A. Example |
| Data / Date | 2026-01-20 |
