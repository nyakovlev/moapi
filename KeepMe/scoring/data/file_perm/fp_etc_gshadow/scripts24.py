import os
import sfile

def fix():
  os.system("chmod 640 /etc/gshadow")
  os.system("chown 0 /etc/gshadow")
  os.system("chgrp 42 /etc/gshadow")
def reset():
  os.system("chmod 644 /etc/gshadow")
  os.system("chown 42 /etc/gshadow")
  os.system("chgrp 1000 /etc/gshadow")
def check():
  fp = sfile.getStat("/etc/gshadow")
  return (fp[0] == "0640") and (fp[1][0] == "0") and (fp[2][0] == "42")
