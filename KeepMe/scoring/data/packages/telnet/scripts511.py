import os
import sfile

def fix():
  os.system("apt-get purge telnet -y")
def reset():
  os.system("apt-get install telnet -y")
def check():
  return not sfile.installed("telnet")
