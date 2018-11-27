import os
import subprocess
import sfile
fname = "/etc/ssh/sshd_config"
def fix():
  global fname
  if not os.path.isfile(fname):
    os.system("apt-get install openssh-server -y")
  sfile.set(fname, {"PermitRootLogin": "no"})
def reset():
  global fname
  if not os.path.isfile(fname):
    os.system("apt-get install openssh-server -y")
  sfile.set(fname, {"PermitRootLogin": "prohibit-password"})
def check():
  res = False
  global fname
  if os.path.isfile(fname) and sfile.isSet(fname, {"PermitRootLogin": "no"}):
    res = True
  return res
