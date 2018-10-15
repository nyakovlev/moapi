import sfile
import os

fname = "/etc/audit/auditd.conf"

ideal_cfg = {
  "max_log_file" : "10",
  "space_left_action":"email",
  "action_mail_acct":"root",
  "admin_space_left_action":"halt",
  "max_log_file_action":"keep_logs"
}
poor_cfg = {
  "max_log_file" : "3",
  "space_left_action":"SYSLOG",
  "action_mail_acct":"root",
  "admin_space_left_action":"SUSPEND",
  "max_log_file_action":"ROTATE"
}

def fix():
  sfile.verifyInstall("auditd")
  sfile.set(fname, ideal_cfg, delim=" = ")
def reset():
  if os.path.isfile(fname):
    sfile.set(fname, poor_cfg, delim=" = ")
def check():
  res = True
  if not os.path.isfile(fname):
    res = False
  else:
    ccfg = sfile.get(fname, ideal_cfg, delim=" = ")
    for key in ccfg:
      if key == "max_log_file":
        if int(ccfg["max_log_file"]) < 6:
          res = False
          break
      elif ccfg[key].lower() != ideal_cfg[key].lower():
        res = False
        break
  return res
