import os
import sfile

def fix():
  os.system("chmod 644 /etc/passwd")
  os.system("chown 0 /etc/passwd")
  os.system("chgrp 0 /etc/passwd")
def reset():
  os.system("chmod 664 /etc/passwd")
  os.system("chown 1000 /etc/passwd")
  os.system("chgrp 1000 /etc/passwd")
def check():
  fp = sfile.getStat("/etc/passwd")
  return (fp[0] == "0644") and (fp[1][0] == "0") and (fp[2][0] == "0")
