class Hidrometro():
    def __init__(self, matricula, endereco, contaPaga, funcionamento, vazao, consumo, vazamento, valorMax):
        #identificação
        self.matricula = matricula;
        self.endereco= endereco;
        #funcionamento
        self.contaPaga = contaPaga;
        self.funcionamento= funcionamento;
        self.consumo= consumo;
        #vazamento
        self.vazao= vazao;
        self.vazamento = vazamento;
        self.vazaoPadrao = 3;
        self.valorMax = valorMax;
    #--------------------------------------------------------------------
    ''' Bloco de Get '''
    def getMatricula(self):
        return self.matricula;

    def getEndereco(self):
        return self.endereco;

    def getContaPaga(self):
        return self.contaPaga;

    def getStatus(self):
        return self.funcionamento;
        
    def getConsumo(self):
        return self.consumo;

    def getVazao(self):
        return self.vazao;

    def getVazamento(self):
        return self.vazamento;

    def getVazaoPadrao(self):
        return self.vazaoPadrao;

    def getValorMax(self):
        return self.valorMax;

    #--------------------------------------------------------------------
    ''' Bloco de Set '''
    def setMatricula(self, matricula):
        self.matricula = matricula;

    def setEndereco(self,endereco):
        self.endereco = endereco;

    def setContaPaga(self, contaPaga):
        self.contaPaga = contaPaga;

    def setConsumo(self, consumo):
        self.consumo = consumo;

    def setVazao(self, vazao):
        self.vazao= vazao;

    def setVazamento(self, vazamento):
        self.vazamento = vazamento;
        
    def setVazaoPadrao(self, vazaoPadrao):
        self.vazaoPadrao = vazaoPadrao;
    
    def setValorMax(self, valorMax):
        self.valorMax = valorMax;
    #---------------------------------------------------------------------------------
    ''' ---------------------------------Funções--------------------------------- '''
    #Função que sinaliza que há vazamento
    def vazamentos(self):
        if (self.vazao > self.vazaoPadrao):
            self.vazamento = True;
            return True
        else:
            self.vazamento = False;
            return False    

    #Função que bloqueia caso a conta não esteja paga
    def conta(self):
        if self.contaPaga == False: self.funcionamento = False;

    #Função que bloqueia caso a vazão esteja maior que o valor máximo atribuído
    def bloqueioInsta(self):
        if (self.vazao > self.valorMax):
                self.novoStatus(self, False)
        else:
            if (self.contaPaga == True):
                self.novoStatus(self, True)

    #Função para ativar ou desativar o hidrometro
    def novoStatus(self, status):
        if status == True: self.funcionamento = True;
        else: self.funcionamento = False;
    
    #Função para atualização do consumo
    def atualizaConsumo(self): 
        if self.funcionamento == True:
                consumo = self.getConsumo() #Salva em uma variavel o valor
                vazao = self.getVazao() #Salva em uma variavel o valor
                novoValor = consumo + vazao; #Soma consumo + vazão
                self.setConsumo(novoValor); #Adiciona o novo valor no hidrometro


    ''' Futuras funções
    def mediaConsumo(ConsumoUsers, SomaUsers):
        mediaConsumo = ConsumoUsers/SomaUsers;
        return mediaConsumo; 
    
    def bloqueioMedia(self, mediaConsumo):
        if (self.consumo > mediaConsumo):
            if(self.funcionamento == True):
                self.novoStatus(self, False);
        else:
            if(funcionamento == False):
                if (self.contaPaga == True):
                    if (self.vazao < self.valorMax):
                        self.novoStatus(self, True);
        '''