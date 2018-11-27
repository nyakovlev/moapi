import os
import subprocess
def setDefs(max_days, min_days, warn_age):
  fd = None
  with open("/etc/login.defs", "r") as f:
    fd = f.readlines()
  with open("/etc/login.defs", "w") as f:
    for i in range(0, len(fd)):
      l = fd[i]
      ct = 0
      if l.startswith("PASS_MAX_DAYS"):
        fd[i] = "PASS_MAX_DAYS\t" + str(max_days) + "\n"
        ct += 1
        if ct == 3:
          break
      elif l.startswith("PASS_MIN_DAYS"):
        fd[i] = "PASS_MIN_DAYS\t" + str(min_days) + "\n"
        ct += 1
        if ct == 3:
          break
      elif l.startswith("PASS_WARN_AGE"):
        fd[i] = "PASS_WARN_AGE\t" + str(warn_age) + "\n"
        ct += 1
        if ct == 3:
          break
    f.writelines(fd)

def fix():
  setDefs(30, 2, 7)
def reset():
  setDefs(99999, 0, 7)
def check():
  res = True
  pd = subprocess.check_output('cat /etc/login.defs | grep ^PASS', shell=True).decode("utf-8").split()
  for i in range(0, 6, 2):
    lbl = pd[i]
    v = int(pd[i + 1])
    if ((lbl == u'PASS_MAX_DAYS') and (v > 30)) or ((lbl == u'PASS_MIN_DAYS') and (v == 0 or v > 3)) or ((lbl == u'PASS_WARN_AGE') and (v < 7)):
      res = False
  return res
