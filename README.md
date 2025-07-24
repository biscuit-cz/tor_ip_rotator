# tor_ip_rotator.py
I created this script while solving CTF challenges. It can be used as a sample for brute-forcing a user's password.  

## Config  
```
sudo nano /etc/tor/torrc
```  
```
# Add this to torrc
....
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
....
```

## Fix Permission denied: '/run/tor/control.authcookie 
- Stage1: allow all users to read the file  
```
chmod o+r ~/path/to/tor_ip_rotator_sample.py
```  
```
chmod o+x /path/to/parent /path/to/parent/subdir
```  

- Stage2: add user to the debian-tor group and apply the new group without logout  
```
sudo usermod -a -G debian-tor $USER
```  
```
newgrp debian-tor
```  

- Stage3:  
```
python3 tor_ip_rotator_sample.py
```  
