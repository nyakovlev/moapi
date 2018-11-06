#!/bin/bash

#Check sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root. Type 'sudo ./install.sh'"
  exit
fi

printf "\n\nThank you for using Spontaneously Talos Education's new MoaPI system! We hope it doesn't crash or ruin your system.\n\n"

#Install required programs
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
apt-get install python2.7 -y
sudo apt-get install python3.6 -y
apt-get install python3-pip -y
python3.6 -m pip install websockets
python3.6 -m pip install pygame
#dpkg -i google-chrome-stable_current_amd64.deb
apt-get install -f -y

#Get usernames
users=$(cat /etc/passwd | awk -F ':' '$3 >= 1000 && $1 != "nobody" {print $1}')

for user in `echo $users`; do
  #Create desktop shortcut for users
  cp "./Scoring Engine.desktop" "/home/$user/Desktop"
  echo "Exec=gnome-terminal -e ${PWD}/start.sh" >> "/home/${user}/Desktop/Scoring Engine.desktop"
  chmod 755 "/home/${user}/Desktop/Scoring Engine.desktop"
  chown $user "/home/${user}/Desktop/Scoring Engine.desktop"
  chgrp $user "/home/${user}/Desktop/Scoring Engine.desktop"
  #Create alias for Baker script and gen-vuln
  printf "\nalias gen-vuln=${PWD}/alias/gen-vuln" >> $path/.bashrc
  printf "\nalias gen-vuln=${PWD}/alias/baker" >> $path/.bashrc
done

#Set permissions for base executables
find . -name "*.py" -print0 | while read -r -d $'\0' line; do
  chmod 755 $line
done
chmod 755 start.sh
chmod -R 755 alias

printf "\n\nInstallation complete. To use the 'gen-vuln' and 'baker' commands, open a new terminal window.\n"
