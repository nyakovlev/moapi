import os
import sfile

def fix():
  os.system("apt-get purge wireshark wireshark-common wireshark-qt libwireshark8 libwireshark-data -y")
def reset():
  os.system("apt-get install wireshark -y")
def check():
  return not (sfile.installed("wireshark") or sfile.installed("wireshark-common") or sfile.installed("wireshark-qt") or sfile.installed("libwireshark8") or sfile.installed("libwireshark-data"))
