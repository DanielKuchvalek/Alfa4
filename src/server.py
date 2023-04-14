import socket, time, threading
import translatelocl, translateping, translatescan, prikaz

class Server:
    def __init__(self, ip, port, nazev, ip_start, ip_konec, port_start, port_konec):
        self.ip = ip
        self.port = port
        self.nazev = nazev
        self.ip_start = ip_start
        self.ip_konec = ip_konec
        self.port_start = port_start
        self.port_konec = port_konec
        self.slovnik = {
            'smart': 'chytrý',
            'desktop': 'plocha',
            'thread': 'vlákno',
            'execution': 'poprava',
            'graveyard': 'hřbitov'
        }
        self.prikazy: list[prikaz.Prikaz] = {
            'TRANSLATELOCL': translatelocl.TranslateLocl(self),
            'TRANSLATEPING': translateping.TranslatePing(self),
            'TRANSLATESCAN': translatescan.TranslateScan(self)
        }

    '''
    Spustí server a přijímá klienty, kterým vytvoří samostatné vlákno.
    '''
    def start(self):
        s = socket.socket()
        s.bind((self.ip, self.port))
        s.listen()
        with open('logs/log.txt', 'a', encoding='utf-8') as soubor:
            soubor.write('Server spuštěn na ' + str(self.ip) + ':' + str(self.port) + '\n')
        while True:
            klient, klient_ip = s.accept()
            vlakno = threading.Thread(target=self.klient, args=(klient, klient_ip))
            vlakno.start()

    '''
    Funkce, která se spouští ve vlákně. Přijímá příkaz od klienta.
    Ten se zpracuje a spojení se ukončí.

    :param klient: připojení s klientem
    '''
    def klient(self, klient, ip):
        zprava = klient.recv(80).decode().strip()
        prikaz = zprava[:13]
        argument = zprava[14:-1]
        if prikaz in self.prikazy:
            self.prikazy[prikaz].execute(klient, ip, argument)
        else:
            klient.send(bytes('TRANSLATEDERR"Neznam teno prikaz"', 'utf-8'))
        time.sleep(0.02)
        klient.close()
        with open('logs/log.txt', 'a', encoding='utf-8') as soubor:
            soubor.write('Klient ' + str(ip[0]) + ':' + str(ip[1]) + ' provedl příkaz ' + zprava + '\n')