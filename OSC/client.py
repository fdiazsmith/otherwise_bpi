from pythonosc import udp_client

class Client:
    def __init__(self, ip ="192.168.1.133", port=10000):
        self.cli =   udp_client.SimpleUDPClient(ip, port)
        pass

    def send_message(self, addr, msg):
        self.cli.send_message(addr, msg)