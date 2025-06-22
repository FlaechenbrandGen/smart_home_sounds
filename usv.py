import subprocess
import requests
import time
import logging
# Logging-Konfiguration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Funktion zum Auslesen des USV-Status
def get_battery_status(ups_name='servers'):
    try:
        output = subprocess.check_output(['/usr/bin/upsc', f'{ups_name}@localhost'], universal_newlines=True)
        for line in output.strip().split('\n'):
            if line.startswith('battery.charge:'):
                return int(line.split(':')[1].strip())
    except subprocess.CalledProcessError as e:
        print("Fehler beim Auslesen der USV:", e)
        return None



def get_load_status(ups_name='servers'):
    try:
        output = subprocess.check_output(['/usr/bin/upsc', f'{ups_name}@localhost'], universal_newlines=True)
        for line in output.strip().split('\n'):
            if line.startswith('ups.status:'):
                return line.split(':')[1].strip()
    except subprocess.CalledProcessError as e:
        print("Fehler beim Auslesen der USV:", e)
        return None


def get_ups_status(ups_name='servers'):
    try:
        output = subprocess.check_output(['/usr/bin/upsc', f'{ups_name}@localhost'], universal_newlines=True)
        status = {}
        for line in output.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                status[key.strip()] = value.strip()
        return status
    except subprocess.CalledProcessError as e:
        print("Fehler beim Auslesen der USV:", e)
        return None

def send_alarm():
    url = "http://pi3:8000/alarm"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Alarm gesendet: {response.status_code}")
    except requests.RequestException as e:
        print(f"Fehler beim Senden des Alarms: {e}")

def monitor_usv():
    while True:
        battery_status = get_battery_status()
        load_status = get_load_status()
        if battery_status < 95 and load_status != 'OL CHRG':
            logger.warning(f"Akkustand unter 95%: {battery_status}%")
            send_alarm()
        time.sleep(300)  # 5 Minuten warten

if __name__ == "__main__":
    monitor_usv()
