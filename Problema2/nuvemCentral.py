# banco de dados com os dados das nevoas
nevoaDB = {}
# conexáo mqtt com todas as nevoas
nevoas = {
    'broker': 'localhost',      # mudar para maquina central do larsid
    'port': 1883,
    'topicPub': "nuvem/",     
    'topicSub': "nuvem/#"
}

def maiorConsumo(param):
    print()
    # A nuvem irá enviar uma mensagem para o topico central/consumo
    # contendo o valor n=param referente a quantidade max de hidrometros 
    # na lista de maiores consumidores que ela quer ver.
    # como resposta a nevoa retorna a lista em json dos maiores hidrometros.
    # da nuvem central a lista deve ir para uma pagina web 

def tempoReal(param):
    print()
    # Enviar uma mensagem para o topico central/temporeal/:param
    # onde Param será o id do hidrometro que ele selecionou para ver.
    # a nevoa irá publicar em tempo real no topico desse hidrometro
    # a nuvem deve se inscrever e mandar os dados para a pagina web via websocket.