import os
import subprocess
import sfile
# http://bookofzeus.com/harden-ubuntu/hardening/ssh/
fname = "/etc/ssh/sshd_config"
ideal_cfg = {
  "PermitRootLogin":"no",
  "PermitEmptyPasswords":"no",
  "PermitUserEnvironment":"no",
  "PrintLastLog":"no",
  "PasswordAuthentication":"no",
  "Protocol":"2",
  "Port":"2149",
  "UseDNS":"no",
  "ClientAliveInterval":"300",
  "ClientAliveCountMax":"0",
  "IgnoreRhosts":"yes",
  "RhostsAuthentication":"no",
  "RhostsRSAAuthentication":"no",
  "RSAAuthentication":"yes",
  "HostbasedAuthentication":"no",
  "LoginGraceTime":"30",
  "MaxStartups":"2",
  "AllowTcpForwarding":"no",
  "X11Forwarding":"no",
  "LogLevel":"VERBOSE",
  "StrictModes":"yes",
  "UsePAM":"no",
  "MaxAuthTries":"4",
  "MACs":"hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-512,hmac-sha2-256,umac-128@openssh.com,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256"
}
default_cfg = {
  "PermitRootLogin":"prohibit-password",
  "PermitEmptyPasswords":"no",
  "PermitUserEnvironment":None,
  "PrintLastLog":"yes",
  "PasswordAuthentication":None,
  "Protocol":"2",
  "Port":"22",
  "UseDNS":None,
  "ClientAliveInterval":None,
  "ClientAliveCountMax":None,
  "IgnoreRhosts":"yes",
  "RhostsAuthentication":None,
  "RhostsRSAAuthentication":"no",
  "RSAAuthentication":"yes",
  "HostbasedAuthentication":"no",
  "LoginGraceTime":"120",
  "MaxStartups":None,
  "AllowTcpForwarding":None,
  "X11Forwarding":"yes",
  "LogLevel":"INFO",
  "StrictModes":"yes",
  "UsePAM":"yes",
  "MaxAuthTries":None,
  "MACs":None
}
def fix():
  global fname
  global ideal_cfg
  if not os.path.isfile(fname):
    os.system("apt-get install openssh-server -y")
  sfile.set(fname, ideal_cfg)
  os.system("service ssh restart")
def reset():
  global fname
  global default_cfg
  if not os.path.isfile(fname):
    os.system("apt-get install openssh-server -y")
  sfile.set(fname, default_cfg)
  os.system("service ssh restart")
def check():
  res = False
  global fname
  if os.path.isfile(fname) and sfile.isSet(fname, ideal_cfg):
    res = True
  return res
