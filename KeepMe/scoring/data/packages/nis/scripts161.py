import os
import sfile

def fix():
  os.system("apt-get purge nis -y")
def reset():
  os.system("apt-get install nis -y")
def check():
  return not sfile.installed("nis")
