import os
import sfile

def fix():
  os.system("apt-get purge netcat netcat-traditional netcat-openbsd -y")
def reset():
  os.system("apt-get install netcat netcat-traditional netcat-openbsd -y")
def check():
  return not (sfile.installed("netcat") or sfile.installed("netcat-traditional") or sfile.installed("netcat-openbsd"))
