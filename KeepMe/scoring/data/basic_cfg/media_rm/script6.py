import os
from shutil import copyfile
import random
name_list = ["system", "cat", "doggo", "lore", "hosts", "sysctl", "ugotme", "saga", "ls", "logo", "wabuffet"]
mfloc = os.path.join("media", "mfloc")
def fix():
  global mfloc
  fd = None
  with open(mfloc, "r") as f:
    fd = f.readlines()
  for i in fd:
    os.remove(i[:-1])
  open(mfloc, "w").close()
def reset():
  global mfloc
  global name_list
  flist = []
  for i in range(0, random.randint(1, 4)):
    nrd = getRdir("/home")
    nfp = os.path.join(nrd, ("." if random.random() > 0.5 else "") + str(random.choice(name_list) + ".jpg"))
    copyfile(os.path.join("media", str(random.randint(1, 8)) + ".jpg"), nfp)
    flist.append(nfp + "\n")
  with open(mfloc, "w") as f:
    f.writelines(flist)
def check():
  global mfloc
  res = True
  fd = None
  with open(mfloc, "r") as f:
    fd = f.readlines()
  for i in fd:
    if os.path.isfile(i[:-1]):
      res = False
      break
  return res

def getRdir(root):
  res = root
  cdl = next(os.walk(root))
  cdl = cdl[1]
  if len(cdl) == 0:
    res = root
  else:
    cdir = random.choice(cdl)
    if cdir == "KeepMe":
      res = root
    else:
      rstp = os.path.join(root, cdir)
      if random.random() < .1:
        res = rstp
      else:
        res = getRdir(rstp)
  return res
