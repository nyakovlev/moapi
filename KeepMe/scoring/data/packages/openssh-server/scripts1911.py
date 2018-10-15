import os
import sfile

def fix():
  os.system("apt-get purge openssh-server -y")
def reset():
  os.system("apt-get install openssh-server -y")
def check():
  return not sfile.installed("openssh-server")
