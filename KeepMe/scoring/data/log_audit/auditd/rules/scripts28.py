import os
import copy

fname = "/etc/audit/audit.rules"
default_file = '''# This file contains the auditctl rules that are loaded
# whenever the audit daemon is started via the initscripts.
# The rules are simply the parameters that would be passed
# to auditctl.

# First rule - delete all
-D

# Increase the buffers to survive stress events.
# Make this bigger for busy systems
-b 320

# Feel free to add below this line. See auditctl man page
'''
ideal_file = '''# This file contains the auditctl rules that are loaded
# whenever the audit daemon is started via the initscripts.
# The rules are simply the parameters that would be passed
# to auditctl.

# First rule - delete all
-D

# Increase the buffers to survive stress events.
# Make this bigger for busy systems
-b 1024

# Feel free to add below this line. See auditctl man page

-a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change
-a always,exit -F arch=b32 -S adjtimex -S settimeofday -S stime -k time-change
-a always,exit -F arch=b64 -S clock_settime -k time-change 
-a always,exit -F arch=b32 -S clock_settime -k time-change
-w /etc/localtime -p wa -k time-change
-w /etc/group -p wa -k identity
-w /etc/passwd -p wa -k identity
-w /etc/gshadow -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/security/opasswd -p wa -k identity
-a always,exit -F arch=b64 -S sethostname -S setdomainname -k system-locale
-a always,exit -F arch=b32 -S sethostname -S setdomainname -k system-locale
-w /etc/issue -p wa -k system-locale
-w /etc/issue.net -p wa -k system-locale
-w /etc/hosts -p wa -k system-locale
-w /etc/sysconfig/network -p wa -k system-locale
#SELINUX ONLY
-w /etc/selinux/ -p wa -k MAC-policy
-w /usr/share/selinux/ -p wa -k MAC-policy
#=====
#APPARMOR ONLY
-w /etc/apparmor/ -p wa -k MAC-policy
-w /etc/apparmor.d/ -p wa -k MAC-policy
#=====
-w /var/log/faillog -p wa -k logins
-w /var/log/lastlog -p wa -k logins
-w /var/log/tallylog -p wa -k logins
-w /var/run/utmp -p wa -k session
-w /var/log/wtmp -p wa -k logins
-w /var/log/btmp -p wa -k logins
-a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b32 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b64 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b32 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b64 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b32 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access
-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access
-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access
-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access
-a always,exit -F arch=b64 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts
-a always,exit -F arch=b32 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts
-a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete
-a always,exit -F arch=b32 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete
-w /etc/sudoers -p wa -k scope
-w /etc/sudoers.d/ -p wa -k scope
-w /var/log/sudo.log -p wa -k actions
-w /sbin/insmod -p x -k modules
-w /sbin/rmmod -p x -k modules
-w /sbin/modprobe -p x -k modules
-a always,exit -F arch=b64 -S init_module -S delete_module -k modules

-e 2
'''

rule_list = {
  "basic_conf" : [
    '-D',
    '-b 1024',
    '-e 2'
  ],
  "date_time" : [
    '-a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change',
    '-a always,exit -F arch=b32 -S adjtimex -S settimeofday -S stime -k time-change',
    '-a always,exit -F arch=b64 -S clock_settime -k time-change',
    '-a always,exit -F arch=b32 -S clock_settime -k time-change',
    '-w /etc/localtime -p wa -k time-change'],
  "user_group" : ['-w /etc/group -p wa -k identity',
    '-w /etc/passwd -p wa -k identity',
    '-w /etc/gshadow -p wa -k identity',
    '-w /etc/shadow -p wa -k identity',
    '-w /etc/security/opasswd -p wa -k identity'],
  "sys_net" : ['-a always,exit -F arch=b64 -S sethostname -S setdomainname -k system-locale',
    '-a always,exit -F arch=b32 -S sethostname -S setdomainname -k system-locale',
    '-w /etc/issue -p wa -k system-locale',
    '-w /etc/issue.net -p wa -k system-locale',
    '-w /etc/hosts -p wa -k system-locale',
    '-w /etc/sysconfig/network -p wa -k system-locale'],
  "selinux" : ['-w /etc/selinux/ -p wa -k MAC-policy',
    '-w /usr/share/selinux/ -p wa -k MAC-policy'],
  "apparmor" : ['-w /etc/apparmor/ -p wa -k MAC-policy',
    '-w /etc/apparmor.d/ -p wa -k MAC-policy'],
  "login_logout" : ['-w /var/log/faillog -p wa -k logins',
    '-w /var/log/lastlog -p wa -k logins',
    '-w /var/log/tallylog -p wa -k logins'],
  "session_init" : ['-w /var/run/utmp -p wa -k session',
    '-w /var/log/wtmp -p wa -k logins',
    '-w /var/log/btmp -p wa -k logins'],
  "dac_mod" : ['-a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod',
    '-a always,exit -F arch=b32 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod',
    '-a always,exit -F arch=b64 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod',
    '-a always,exit -F arch=b32 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod',
    '-a always,exit -F arch=b64 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod',
    '-a always,exit -F arch=b32 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod'],
  "file_acc" : ['-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access',
    '-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access',
    '-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access',
    '-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access'],
  "sys_mnt" : ['-a always,exit -F arch=b64 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts',
    '-a always,exit -F arch=b32 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts'],
  "file_del" : ['-a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete',
    '-a always,exit -F arch=b32 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete'],
  "sudoers" : ['-w /etc/sudoers -p wa -k scope',
    '-w /etc/sudoers.d/ -p wa -k scope'],
  "sudolog" : ['-w /var/log/sudo.log -p wa -k actions'],
  "kern_mod" : ['-w /sbin/insmod -p x -k modules',
    '-w /sbin/rmmod -p x -k modules',
    '-w /sbin/modprobe -p x -k modules',
    '-a always,exit -F arch=b64 -S init_module -S delete_module -k modules']
}
active_rule_list = {}
def line_remove(line):
  for key in active_rule_list:
    if line in active_rule_list[key]:
      active_rule_list[key].remove(line)
      break
def fix():
  with open(fname, "w") as f:
    f.write(ideal_file)
def reset():
  with open(fname, "w") as f:
    f.write(default_file)
def check():
  active_rule_list = copy.deepcopy(rule_list)
  flines = []
  with open(fname, "r") as f:
    flines = f.readlines()
  for i in flines:
    line_remove(i.strip())
  remaining = []
  for key in active_rule_list:
    if len(active_rule_list[key]) > 0:
      remaining.append(key)
  if ("selinux" not in remaining) and ("apparmor" in remaining):
    remaining.remove("apparmor")
  if ("selinux" in remaining) and ("apparmor" not in remaining):
    remaining.remove("selinux")
  print(remaining)
  return (len(remaining) == 0)
