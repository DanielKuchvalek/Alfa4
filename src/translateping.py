from prikaz import Prikaz

class TranslatePing(Prikaz):
    def __init__(self, server):
        super().__init__(server)

    '''
    Odešle klientovi odpověď TRANSLATEPONG s názvem programu.

    :param klient: připojení s klientem
    :param ip: ip a port klienta
    :param argument: název programu na straně klienta
    '''
    def execute(self, klient, ip, argument):
        klient.send(bytes('TRANSLATEPONG"' + self.server.nazev + '"', 'utf-8'))