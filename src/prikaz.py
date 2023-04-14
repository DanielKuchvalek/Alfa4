class Prikaz:
    def __init__(self, server):
        self.server = server
    
    '''
    :param klient: připojení s klientem
    :param ip:  ip a port klienta
    :param argument: argument příkazu
    '''
    def execute(self, klient, ip, argument):
        raise NotImplementedError