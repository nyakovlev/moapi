import os
import subprocess
def fix():
  os.system("ufw enable");
def reset():
  os.system("ufw disable");
def check():
  return (b'Status: active\n' in subprocess.check_output(["ufw", "status"]))
