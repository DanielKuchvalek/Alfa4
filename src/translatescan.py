from prikaz import Prikaz
import re, socket

class TranslateScan(Prikaz):
    def __init__(self, server):
        super().__init__(server)
    '''
    Skenuje síť a hledá ostatní programy stejného typu v síti.
    Rozsah ip adres a portů je určen v konfiguračním souboru.

    :param klient: připojení ke klientovi
    :param ip: ip a port klienta
    :param argument: anglické slovo k přeložení
    '''
    def execute(self, klient, ip, argument):
        if argument in self.server.slovnik:
            klient.send(bytes('TRANSLATEDSUC"' + self.server.slovnik[argument] + '"', 'utf-8'))
        else:
            aktualni_ip: IPAdresa = self.server.ip_start
            ip_serveru = IPAdresa(self.server.ip)
            while True:
                aktualni_port = self.server.port_start
                while aktualni_port <= self.server.port_konec:
                    if not (aktualni_ip == ip_serveru and aktualni_port == self.server.port):
                        pripojeni = socket.socket()
                        pripojeni.settimeout(0.2)
                        try:
                            pripojeni.connect((str(aktualni_ip), aktualni_port))
                            pripojeni.send(bytes('TRANSLATELOCL"' + argument + '"', 'utf-8'))
                            odpoved = pripojeni.recv(100).decode()
                            if odpoved[:13] == 'TRANSLATEDSUC':
                                klient.send(bytes(odpoved, 'utf-8'))
                                pripojeni.close()
                                return
                        except:
                            pass
                        finally:
                            pripojeni.close()
                    aktualni_port += 1
                if aktualni_ip == self.server.ip_konec:
                    break
                aktualni_ip.pricti_jedna()
            klient.send(bytes('TRANSLATEDERR"Neznámé slovo"', 'utf-8'))

class IPAdresa:
    def __init__(self, ip) -> None:
        self.set_ip(ip)

    '''
    Převádí IP adresu na string
    '''
    def __str__(self):
        return str(self.ip[0]) + '.' + str(self.ip[1]) + '.' + str(self.ip[2]) + '.' + str(self.ip[3])
    
    '''
    Kontroluje, zda jsou dvě IP adresy stejné.
    '''
    def __eq__(self, __o: object) -> bool:
        return self.ip == __o.ip

    '''
    Převede IP adresu na pole čísel a uloží do proměnné.

    :param ip: ip adresa jako string
    '''
    def set_ip(self, ip):
        shoda = re.match(r'^([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3})$', ip)
        self.ip = [int(shoda.group(1)), int(shoda.group(2)), int(shoda.group(3)), int(shoda.group(4))]
    '''
    Přičte 1 k ip adrese. Pokud hodnota přesáhne rozsah ip adresy, ip zůstane 255.255.255.255.
    '''
    def pricti_jedna(self):
        self.ip[3] += 1
        if self.ip[3] > 255:
            self.ip[2] += 1
            self.ip[3] = 1
        if self.ip[2] > 255:
            self.ip[1] += 1
            self.ip[2] = 1
        if self.ip[1] > 255:
            self.ip[0] += 1
            self.ip[1] = 1
        if self.ip[0] > 255:
            self.ip = [255, 255, 255, 255]