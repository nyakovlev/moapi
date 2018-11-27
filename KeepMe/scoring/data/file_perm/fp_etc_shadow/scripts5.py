import os
import sfile

def fix():
  os.system("chmod 640 /etc/shadow")
  os.system("chown 0 /etc/shadow")
  os.system("chgrp 42 /etc/shadow")
def reset():
  os.system("chmod 644 /etc/shadow")
  os.system("chown 42 /etc/shadow")
  os.system("chgrp 1000 /etc/shadow")
def check():
  fp = sfile.getStat("/etc/shadow")
  return (fp[0] == "0640") and (fp[1][0] == "0") and (fp[2][0] == "42")
