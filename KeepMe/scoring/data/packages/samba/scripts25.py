import os
import sfile

def fix():
  os.system("apt-get purge samba samba-common samba-common-bin python-samba samba-dsdb-modules samba-libs samba-vfs-modules -y")
def reset():
  os.system("apt-get install samba -y")
def check():
  return not (sfile.installed("samba") or sfile.installed("samba-common") or sfile.installed("samba-common-bin") or sfile.installed("python-samba") or sfile.installed("samba-dsdb-modules") or sfile.installed("samba-libs") or sfile.installed("samba-vfs-modules"))
