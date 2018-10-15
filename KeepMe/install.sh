#!/bin/bash

#Check sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root. Type 'sudo ./install.sh'"
  exit
fi

printf "\n\nThank you for using Spontaneously Talos Education's new MoaPI system! We hope it doesn't crash or ruin your system.\n\n"

#Install required programs
apt-get install python2.7 -y
apt-get install python3.6 -y
python3.6 -m pip install websockets
python3.6 -m pip install pygame
dpkg -i google-chrome-stable_current_amd64.deb
apt-get install -f -y

#Get user directories
users=$(cat /etc/passwd | awk -F ':' '$3 >= 1000 && $1 != "nobody" {print "/home/"$1}')

#echo $users | xargs -Ipath sh -c 'cp ./Scoring\ Engine.desktop path/Desktop; chmod 755 path/Desktop/Scoring\ Engine.desktop; echo "Exec=gnome-terminal -e ${PATH}/start.sh" >> path/Desktop/Scoring\ Engine.desktop; printf "\nalias gen-vuln=${PATH}/meta_script/gen-vuln" >> path/.bashrc'
while read -r path; do
  #Create desktop shortcut for users
  cp ./Scoring\ Engine.desktop $path/Desktop
  echo "Exec=gnome-terminal -e ${PWD}/start.sh" >> $path/Desktop/Scoring\ Engine.desktop
  chmod 755 $path/Desktop/Scoring\ Engine.desktop
  #Create alias for Baker script and gen-vuln
  printf "\nalias gen-vuln=${PWD}/alias/gen-vuln" >> $path/.bashrc
  printf "\nalias gen-vuln=${PWD}/alias/baker" >> $path/.bashrc
done <<< $users

#Set permissions for base executables
find . -name "*.py" -print0 | while read -r -d $'\0' line; do
  chmod 755 line
done
chmod 755 start.sh
chmod -R 755 alias

printf "\n\nInstallation complete. To use the 'gen-vuln' and 'baker' commands, open a new terminal window.\n"
