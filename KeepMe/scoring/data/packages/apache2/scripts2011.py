import os
import sfile

def fix():
  os.system("apt-get purge apache2 apache2-bin apache2-data apache2-utils -y")
def reset():
  os.system("apt-get install apache2 -y")
def check():
  return not (sfile.installed("apache2") or sfile.installed("apache2-bin") or sfile.installed("apache2-data") or sfile.installed("apache2-utils"))
