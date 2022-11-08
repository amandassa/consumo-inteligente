<h1 align="center">Consumo Inteligente</h1>
<p align="center">Gerenciamento de consumo em tempo real baseado em computação de borda</p>

<p align="center">
 <a href="#objetivo">Objetivo</a> •
 <a href="#diagrama">Diagrama</a> • 
 <a href="#tecnologias">Tecnologias</a> • 
 <a href="#restricoes">Restrições</a> •
 <a href="#solucao">Solução</a> •
 <a href="#modulos">Módulos</a> •
 <a href="#deploy">Deploy e Demonstração</a> •
 <a href="#final">Considerações finais</a>
</p>

<h2 href="#objetivo">Objetivo</h2>
<p>Este projeto é uma versão mehorada do Hidrômetro Inteligente, em que foi implementado o gerenciamento de consumo dos hidrômetros em tempo real, permitindo a concessionária estabelecer regras de consumo para períodos de racionamento, além de um controle maior do bloqueio em caso de não pagamento das faturas.</p>

<h2 href="#diagrama">Diagrama da infraestrutura</h2>

<img src="https://github.com/amandassa/consumo-inteligente/blob/main/images/diagrama.jpg"/>

<h2 href="#tecnologias">Tecnologias</h2>

- Hidrômetro:
    - [Java 11](https://www.oracle.com/br/java/technologies/javase/jdk11-archive-downloads.html)
- Servidores:
    - [Python 3.10](https://www.python.org/)
- Conectividade:
    - [MQTT](https://mqtt.org/)
- API Rest:
    - [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- Deploy e teste:
    - [Docker](https://www.docker.com/)

<h2 href="#restricoes">Restrições</h2>

- A interface do gerente deve permitir selecionar N hidrômetros de maior consumo.
- Entre os hidrômetros listados deve permitir selecionar um deles para visualizar os dados com o menor tempo de latência possível.
- O produto deve ser desenvolvido através de contêineres Docker.

<h2 href="solucao">Solução</h2>

<p>O Hidrômetro Inteligente é uma proposta para cidades inteligentes que querem cada vez mais oferecer automação e conectividade a seus residentes. Um dos problemas com a versão anterior era a latência causada pela centralização do processamento de dados na nuvem, o que prejudica o desempenho e limita a capacidade do sistema impedindo-o de atender à demanda de uma cidade muito populosa.</p>
<p>Como solução para este problema, este novo protótipo implementa a abordagem de Computação de borda (Edge Computing) de processamento descentralizado, seguindo as últimas tendências no mundo da Internet das Coisas (IoT).</p>
<p>Este modelo baseia-se na transferência de parte do processamento para os nós intermediários da névoa, que estão mais próximo de onde os dados são gerados. Isso permite uma latência menor nos endpoints acessados pela nuvem pois o volume de dados processados por cada operação na nuvem diminui drasticamente uma vez que a maior parte do trabalho já foi realizada antes mesmo dos dados chegarem lá.</p>
<p>Dessa forma, buscas e ordenações em grandes volumes de dados são evitados e as responsabilidades do servidor central são reduzidas, o que consequentemente permite obter o maior desempenho nas respostas da nuvem para a aplicação do usuário.</p>

<h2 href="modulos">Módulos do Sistema</h2>

<h3>Hidrômetro</h3>
<p>Como geradores de dados do sistema, cada hidrômetro é conectado ao nó da névoa correspondente à região da cidade onde foi instalado. Os hidrômetros enviam, além de seus campos identificadores, o consumo da residência em metros cúbicos e o horário de cada medição para a névoa mais próxima.</p>

<h3>Nós Intermediários</h3>
<p>Os nós da névoa estabelecem uma conexão entre um grupo de hidrômetros e a nuvem central, filtrando os dados de interesse da nuvem para enviá-los posteriormente. A névoa realiza o cálculo de sua média de consumo e a busca dos hidrômetros que mais consomem na região, além de transmitir aos seus hidrômetros as requisições mais críticas da nuvem, de bloqueio por exemplo.</p>

<h3>Nuvem</h3>
<p>A nuvem estabelece conexão com todos os nós da névoa, escutando e enviando requisições. Na nuvem, as solicitações de operações da API são enviadas e recebidas. Os identificadores das névoas são mantidos armazenados de forma a permitir o acesso rápido à região do hidrômetro solicitado pelo usuário, evitando que todas as névoas recebam a mesma requisição em que apenas uma deve responder.</p>

<h3>Conexão MQTT</h3>
<p>O padrão de comunicação MQTT foi utilizado nesta solução devido a sua extensa aplicação na Internet das Coisas (IoT) e sua capacidade de estabelecer uma comunicação facilitada numa rede segura.</p>
<p>A conectividade do sistema é baseada em 2 pontos de Brokers MQTT, um dedicado à comunicação Nuvem-Nós (apenas um broker) e outro responsável pela comunicação Nó-Hidrômetros (um broker por nó). Cada categoria de Broker presente no sistema e os tópicos utilizados são listados abaixo:</p>

<b>Broker Nuvem-Nós:   nuvem/</b>
<ul>
    <li>nuvem/media/[idNevoa] : <p>Tópico onde são publicadas as médias de consumo de cada névoa.</p>
    </li>
    <li>nuvem/temporeal/[idHidrometro] : <p>Quando há uma requisição do cliente para acompanhar o consumo de um hidrômetro em tempo real, os logs de consumo deste hidrômetro são transmitidos por este subtópico para a nuvem.</p>
    </li>
    <li>nuvem/consumo/[idNevoa] : <p>A nuvem solicita N hidrômetros e cada névoa envia sua lista com N hidrômetros que mais consomem por este subtópico. Caso seja um número inválido, a lista conterá 30% dos hidrômetros do nó solicitado.</p>
    </li>
</ul>

<b>Brokers Nós-Hidrômetros:   hidrometros/</b>
<ul>
    <li>hidrometros/status/[idHidro] : <p>Onde cada hidrômetro publica seu log de consumo.</p>
    </li>
    <li>hidrometros/bloqueio/[idHidro] : <p>Tópico em que a névoa transmite a mensagem de bloqueio para determinado hidrômetro, após verificar se o consumo se encontra dentro do permitido ou se a fatura foi paga.</p>
    </li>
</ul>


<h3>API Rest</h3>