import os
import sfile

def fix():
  os.system("apt-get install auditd -y")
def reset():
  os.system("apt-get purge auditd -y")
def check():
  return sfile.installed("auditd")
