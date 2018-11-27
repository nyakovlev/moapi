import subprocess
import os
from random import shuffle

last_ct = 0
pulse_ct = 4
last_state = False
#os.system("apt-get update")

def fix():
  os.system("apt-get upgrade -y")
def reset():
  print("This feature is not yet available.")
def check():
  global last_ct
  global pulse_ct
  global last_state
  res = last_state
  if pulse_ct > 3:
    upgrade_ct = int(subprocess.check_output('sudo apt-get upgrade --dry-run | grep "^[[:digit:]]* upgraded"', shell=True).decode("utf-8").split()[0])
    if upgrade_ct != last_ct:
      print(str(upgrade_ct) + " packages need updating.")
      last_ct = upgrade_ct
    res = (upgrade_ct == 0)
    last_state = res
    pulse_ct = 0
  else:
    pulse_ct += 1
  return res
