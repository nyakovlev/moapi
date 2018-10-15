import os
import sfile

def fix():
  os.system("apt-get purge talk -y")
def reset():
  os.system("apt-get install talk -y")
def check():
  return not sfile.installed("talk")
