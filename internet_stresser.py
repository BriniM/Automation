import subprocess
import threading
import re

from time import sleep


class NetStresser:
    def __init__(self):
        self.DOWNLOAD_URL = 'https://download.fedoraproject.org/pub/fedora/linux/releases/31/Workstation/x86_64/iso' \
                            '/Fedora-Workstation-Live-x86_64-31-1.9.iso '
        self.PING_REGEXP = re.compile('Maximum = ([0-9]*)ms')
        self.is_running = False
        self.background_thread = threading.Thread()

    def stress(self):
        self.is_running = True
        self.background_thread = threading.Thread(name='Downloader', target=self.download)
        self.background_thread.start()

    def stop(self):
        self.is_running = False

    def download(self):
        proc = subprocess.Popen('curl -L {} --output -'.format(self.DOWNLOAD_URL), stdout=subprocess.DEVNULL)
        while self.is_running:
            sleep(1)
        proc.terminate()

    def get_max_ping(self):
        """
        Returns the maximum ping after 4 requests
        :return: int
        """
        execution = str(subprocess.check_output(['ping', 'google.com']))
        return int(self.PING_REGEXP.findall(execution)[0])


ns = NetStresser()

while True:
    if ns.get_max_ping() > 150:
        print('Ping exceeded 150ms, downloading file...')
        ns.stress()
        sleep(15)
        ns.stop()
    sleep(5)