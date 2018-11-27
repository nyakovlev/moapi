import os
import sfile

def fix():
  os.system("apt-get purge ldap-utils -y")
def reset():
  os.system("apt-get install ldap-utils -y")
def check():
  return not sfile.installed("ldap-utils")
