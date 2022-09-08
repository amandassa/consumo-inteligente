class Hidrometro:
    def __init__(self, matricula, funcionamento, endereco, vazao):
        self.matricula = matricula
        self.funcionamento= funcionamento
        self.endereco= endereco
        self.vazao= vazao
    
    def Ativar(self):
        self.funcionamento = True;

    def Desativar(self):
        self.funcionamento = False;

    def getMatricula(self):
        return self.matricula;

    def getStatus(self):
        return self.funcionamento;

    def getEndereco(self):
        return self.endereco;

    def getVazao(self):
        return self.vazao;

hidrometro1 = Hidrometro("1100",True,"Avenida Coronel Plinio da Silva Gomes","4 m³/s");

hidrometro1.Ativar();
print(hidrometro1.getStatus());
hidrometro1.Desativar();
print(hidrometro1.getStatus());
hidrometro1.getVazao();