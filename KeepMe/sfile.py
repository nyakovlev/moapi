#!/usr/bin/python3.6

import subprocess
import sys
import os

def set(fname, settings, delim=None):
  fd = None
  rlines = []
  unset = [i for i in settings]
  with open(fname, "r") as f:
    fd = f.readlines()
  for i in range(0, len(fd)):
    ll = fd[i].split(delim)
    ll = [j.strip() for j in ll]
    if len(ll) > 0:
      sname = ll[0]
      if sname in settings:
        value = settings[sname]
        if value is not None:
          fd[i] = sname + (" " if delim is None else delim) + value + "\n"
        else:
          rlines.append(i)
        unset.remove(sname)
        if len(unset) == 0:
          break
  for ri in reversed(rlines):
    del fd[ri]
  for key in unset:
    if settings[key] is None:
      print("Nothing to remove for", key)
    else:
      fd.append(key + (" " if delim is None else delim) + settings[key] + "\n")
  with open(fname, "w") as f:
    f.writelines(fd)
def isSet(fname, settings, delim=None):
  res = True
  vals = get(fname, settings, delim=delim)
  for key in settings:
    if settings[key] != vals[key]:
      res = False
      break
  return res
def get(fname, settings, delim=None):
  res = {}
  fd = None
  unread = [i for i in settings]
  with open(fname, "r") as f:
    fd = f.readlines()
  for i in fd:
    ll = i.split(delim)
    ll = [j.strip() for j in ll]
    if len(ll) > 1:
      cset = ll[0]
      cval = ll[1]
      if cset in settings:
        res[cset] = cval
        unread.remove(cset)
        if len(unread) == 0:
          break
  if len(unread) > 0:
    for i in unread:
      res[i] = None
  return res
def installed(pkg_name):
  result = False
  dpkg_l = None
  try:
    dpkg_l = subprocess.check_output("dpkg -l " + pkg_name + " 2>&1", shell=True).decode("utf-8").split("\n")
  except:
    pass
  if (dpkg_l is not None) and (dpkg_l[5].startswith("ii")):
    result = True
  return result
def verifyInstall(pkg_name):
  if not installed(pkg_name):
    os.system("sudo apt-get install " + pkg_name + " -y")
def getStat(path):
  # returns (<str>octal, (<str>UID, <str>username), (<str>GID, <str>groupname))
  sdata = subprocess.check_output("stat " + path + " | grep ^Access", shell=True).decode("utf-8").split("\n")
  pl = sdata[0].split("(")
  octal = pl[1].split("/")[0]
  udata = pl[2].split(")")[0].split("/")
  uid = (udata[0].strip(), udata[1].strip())
  gdata = pl[3].split(")")[0].split("/")
  gid = (gdata[0].strip(), gdata[1].strip())
  return (octal, uid, gid)
