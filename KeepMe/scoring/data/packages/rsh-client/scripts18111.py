import os
import sfile

def fix():
  os.system("apt-get purge rsh-client rsh-redone-client -y")
def reset():
  os.system("apt-get install rsh-client rsh-redone-client -y")
def check():
  return not (sfile.installed("rsh-client") or sfile.installed("rsh-redone-client"))
