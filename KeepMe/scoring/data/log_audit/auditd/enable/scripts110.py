import sfile
import subprocess
import os

def fix():
  sfile.verifyInstall("auditd")
  os.system("systemctl enable auditd")
def reset():
  if sfile.installed("auditd"):
    os.system("systemctl disable auditd")
def check():
  res = False
  try:
    out = subprocess.check_output("systemctl is-enabled auditd 2>&1", shell=True).decode("utf-8")
    res = (out == "enabled\n")
  except:
    pass
  return res
  
