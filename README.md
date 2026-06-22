Envwatch v36
Português

Sobre o projeto

O Envwatch é uma ferramenta modular de monitoramento e análise de segurança baseada em plugins.
Ele executa testes automatizados (ping, HTTP, scan de rede) e gera eventos e alertas em tempo real, com visualização em dashboard HTML.

O objetivo do projeto é simular um ambiente de Security Operations Center (SOC) local, auxiliando no aprendizado de análise de rede, monitoramento e detecção de anomalias.

Funcionalidades:

Sistema modular baseado em plugins

Execução de comandos (ping, curl, nmap)
Análise automática de respostas

Sistema de alertas (WARN / CRITICAL)

Dashboard HTML com atualização automática
Histórico de eventos em tempo real

Limite de memória para eventos e alertas

Como funciona:

O sistema carrega plugins da pasta "plugins/"

Cada plugin executa testes definidos

Os resultados são analisados automaticamente

Alertas são gerados quando regras são violadas

O dashboard HTML é atualizado continuamente

Estrutura do projeto:

envwatch/
├── envwatch.py
├── plugins/
│   ├── network.py
│   ├── osint.py
│   └── recon.py
├── rules.json
├── reports/
└── .gitignore

Execução
python envwatch.py

Aviso
Este projeto é apenas para fins educacionais e de pesquisa em segurança.



English

About the project
Envwatch is a modular security monitoring and analysis tool based on plugins.

It runs automated tests (ping, HTTP requests, network scans) and generates real-time events and alerts with an HTML dashboard.

The goal of the project is to simulate a lightweight Security Operations Center (SOC) environment to support learning in network monitoring and anomaly detection.

Features
Plugin-based modular system

Command execution (ping, curl, nmap)

Automatic response analysis

Alert system (WARN / CRITICAL)

Live HTML dashboard

Real-time event history

Memory-limited event storage


How it works:

The system loads plugins from the "plugins/" folder
Each plugin runs predefined tests
Outputs are automatically analyzed
Alerts are triggered when rules are violated
The HTML dashboard is continuously updated

Project structure

envwatch/
├── envwatch.py
├── plugins/
│   ├── network.py
│   ├── osint.py
│   └── recon.py
├── rules.json
├── reports/
└── .gitignore

Run
python envwatch.py

Disclaimer
This project is intended for educational and cybersecurity research purposes only.
