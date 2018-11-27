import os
import sfile

def fix():
  os.system("chmod 644 /etc/group")
  os.system("chown 0 /etc/group")
  os.system("chgrp 0 /etc/group")
def reset():
  os.system("chmod 664 /etc/group")
  os.system("chown 1000 /etc/group")
  os.system("chgrp 1000 /etc/group")
def check():
  fp = sfile.getStat("/etc/group")
  return (fp[0] == "0644") and (fp[1][0] == "0") and (fp[2][0] == "0")
