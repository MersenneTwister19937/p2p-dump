import time
import threading
import subprocess
import sys

# this is the worst part of making open source programs
# you always gotta do stuff automatically because skids dont know anything

def installpkg(pkg):
    for p in pkg:
        subprocess.check_call([sys.executable, "-m", "pip", "install", p, "--break-system-packages"])

try:
    import pyshark
    from pyshark.tshark.tshark import get_tshark_interfaces, get_all_tshark_interfaces_names

    from termcolor import cprint
    import pyfiglet
except ImportError:
    installpkg(["pyshark", "termcolor", "pyfiglet"])

    import pyshark
    from pyshark.tshark.tshark import get_tshark_interfaces, get_all_tshark_interfaces_names

    from termcolor import cprint
    import pyfiglet


ip_file = "captured.txt"

inters = get_all_tshark_interfaces_names()

cprint(pyfiglet.figlet_format("P2P DUMPER"), "red")

print("popular platforms this will work with: ")

print("\n")

cprint("- Snapchat", "yellow")
cprint("- WhatsApp", "green")
cprint("- Facebook messanger", "blue")
cprint("- Any other chat platform that use p2p for calling", "red")

print("\n")

time.sleep(1.5)

cprint("select the interface you wanna use.", "green")
time.sleep(0.5)
for number, name in enumerate(get_tshark_interfaces(), 1):
    print(f"{number}. {name}")

while True:
    try:
        global selected_inter
        selected_inter = int(input())
        break
    except ValueError:
        cprint("input a number.", "red")

cprint("starting packet capture...", "green")
capture = pyshark.LiveCapture(interface=inters[selected_inter], display_filter="stun.type == 0x0101")

def checkifgotpackets(): # yeah im crap at naming stuff what u gonna do about it
    if (len(ips) == 0):
        cprint("No stun packets picked up!", "red")
        cprint("Make sure you are in an environment that would pick them up, like a call", "red")
        cprint("Or check if you're using the right interface.", "red")
        quit()

thread = threading.Timer(5, checkifgotpackets)
thread.start()

ips = []

for packet in capture:
    if (hasattr(packet.stun, "att_ipv4")):
        ip = packet.stun.att_ipv4

        if (ip not in ips):
            print(f"ip found! {ip}")
            ips.append(ip)
            with open(ip_file, 'r') as file:
                if (ip not in file.read()):
                    with open(ip_file, 'a') as file:
                        file.write(ip + "\n")



