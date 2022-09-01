class Hidrometro:
    def __init__(self, matricula, funcionamento, statusConta, endereco, vazao):
        self.matricula = matricula
        self.funcionamento= funcionamento
        self.statusConta= statusConta
        self.endereco= endereco
        self.vazao= vazao
    
    def Ativar(self):
        self.funcionamento = "Ativado";
        print(self.funcionamento);

    def Desativar(self):
        self.funcionamento = "Desativado";
        print(self.funcionamento);

    def Status(self):
        print(self.funcionamento);

    def Conta(self):
        print(self.statusConta);

    def Endereco(self):
        print(self.endereco);

    def Vazao(self):
        print(self.vazao);

hidrometro1 = Hidrometro("1100","on","pago","Avenida Coronel Plinio da Silva Gomes","4 m³/s");

hidrometro1.Ativar();
hidrometro1.Desativar();
hidrometro1.Vazao();

#visando monitorar o abastecimento de água, medir o consumo de cada cliente, gerar a fatura a ser paga, bem como alertar sobre
#um possível vazamento de água em determinada zona da cidade. 