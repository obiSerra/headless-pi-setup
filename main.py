#!/usr/bin/python3

import argparse
import json
import os
import subprocess
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simpe provisioning tool PIes")

    parser.add_argument("-v", "--volume", metavar="volume", default=None, help="The Volume to update")

    args = parser.parse_args()

    VOLUME_PATH = args.volume

    print(f"[+] Provisioning volume: {VOLUME_PATH}")

    # Load the config file
    with open("config.json") as file_:
        config = json.load(file_)

    # Create the ssh file
    print("[+] Creating ssh file...")
    ssh_file = os.path.join(VOLUME_PATH, "ssh")
    Path(ssh_file).touch()

    # Create the userconf.txt file
    print("[+] Creating userconf.txt file...")
    user_name = config["user_name"]
    passwd = config["passwd"]
    cmd_1 = subprocess.run([f"echo '{passwd}' | openssl passwd -6 -stdin"], shell=True, stdout=subprocess.PIPE)
    user_conf_file = os.path.join(VOLUME_PATH, "userconf.txt")
    with open(user_conf_file, "w") as f:
        f.write(f"{user_name}:{cmd_1.stdout.decode('utf-8')}\n")

    # Create the wpa_supplicant.conf file
    print("[+] Creating wpa_supplicant.conf file...")

    wpa_template = f"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country={config['country']}

network={{
    ssid="{config['ssid']}"
    psk="{config['psk']}"
    key_mgmt=WPA-PSK
}}
"""

    wpa_file = os.path.join(VOLUME_PATH, "wpa_supplicant.conf")
    with open(wpa_file, "w") as file:
        file.write(wpa_template)

    print("\n\n----------------------- Check -----------------------\n")
    print("[?] ssh")
    subprocess.run([f"ls -la {VOLUME_PATH} | grep ssh"], shell=True)
    print("\n-----------------------------------------------------\n")
    print("[?] userconf\n")
    subprocess.run([f"ls -la {VOLUME_PATH} | grep userconf"], shell=True)
    print("\n  content:\n")
    subprocess.run([f"cat {user_conf_file}"], shell=True)
    print("\n-----------------------------------------------------\n")
    print("[?] wpa_supplicant.conf\n")
    subprocess.run([f"ls -la {VOLUME_PATH} | grep wpa_supplicant"], shell=True)
    print("\n  content:\n")
    subprocess.run([f"cat {wpa_file}"], shell=True)
    print("\n-----------------------------------------------------\n")
