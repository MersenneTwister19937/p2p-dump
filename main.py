import pyshark

capture = pyshark.LiveCapture(interface='wlp2s0', display_filter="stun.type == 0x0101")

for packet in capture:
    print(packet)
