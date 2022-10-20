import json
class Node ():
    def __init__(self, id):
        self.db = {}

    def handleHidrometro (self, payload):
        msg = {}
        msg = json.loads(payload)
        self.db[msg.get('codigo')] = msg    # quando uma nova mensagem de consumo chega a antiga é sobrescrita?
        