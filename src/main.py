import server as server, configparser
from translatescan import IPAdresa

if __name__ == '__main__':
    konfigurace = configparser.ConfigParser()
    konfigurace.read('config/konfigurace.ini', encoding='utf-8')
    server1 = server.Server(
        konfigurace['server']['ip'],
        int(konfigurace['server']['port']),
        konfigurace['server']['nazev'],
        IPAdresa(konfigurace['server']['ip_start']),
        IPAdresa(konfigurace['server']['ip_konec']),
        int(konfigurace['server']['port_start']),
        int(konfigurace['server']['port_konec'])
    )
    server1.start()