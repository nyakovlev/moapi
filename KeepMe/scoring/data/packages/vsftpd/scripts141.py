import os
import sfile

def fix():
  os.system("apt-get purge vsftpd -y")
def reset():
  os.system("apt-get install vsftpd -y")
def check():
  return not sfile.installed("vsftpd")
