import os
import subprocess
def fix():
  os.system("passwd -l root");
def reset():
  os.system("passwd -u root");
def check():
  return (subprocess.check_output("sudo cat /etc/shadow | cut -d: -f2", shell=True).decode("utf-8")[0] == "!")
