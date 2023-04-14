from prikaz import Prikaz

class TranslateLocl(Prikaz):
    def __init__(self, server):
        super().__init__(server)

    '''
    Přeloží slovo a odešle odpověď ve tvaru TRANLATEDSUC"překlad"

    :param klient: připojení s klientem
    :param ip: ip a port klienta
    :param argument: anglické slovo k přeložení
    '''
    def execute(self, klient, ip, argument):
        if argument in self.server.slovnik:
            klient.send(bytes('TRANSLATEDSUC"' + self.server.slovnik[argument] + '"', 'utf-8'))
        else:
            klient.send(bytes('TRANSLATEDERR"Neznam toto slovo"', 'utf-8'))