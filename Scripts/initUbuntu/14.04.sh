#!/bin/bash
echo "Start Initialization Ubuntu 14.04 LTS - NamHB"

# Copy sourelist, fpt mirror
cp /etc/apt/sources.list /etc/apt/sources.list.back
cp ./sources.list /etc/apt/sources.list
apt-get update && apt-get -y upgrade

# Apt install 
apt-get -y install build-essential gnome-session-fallback imagemagick vlc unrar p7zip dconf-tools filezilla tmux gdb
apt-get install build-essential
# Disable system report
apt-get -y remove update-notifier
cp ./apport /etc/default/apport
# Update network disable dnsmap
cp ./NetworkManager.conf /etc/NetworkManager/NetworkManager.conf
# Disable cup
cp ./cups-browsed.conf /etc/init/cups-browsed.conf
cp ./cups.conf /etc/init/cups.conf
# Install conky
apt-add-repository -y ppa:teejee2008/ppa
apt-get update
apt-get install -y conky-manager
# Install ubuntu-teak
add-apt-repository ppa:tualatrix/ppa
apt-get update
apt-get install -y ubuntu-tweak
wget https://github.com/anmoljagetia/Flatabulous/releases/download/14.04.1/Flatabulous-Theme.deb
dpkg -i Flatabulous-Theme.deb
# Install Flat Icons
add-apt-repository ppa:noobslab/icons
apt-get update
apt-get install -y ultra-flat-icons
# Config tmux
cp .tmux.conf /home/habachnam/.tmux.conf
# Create tools
mkdir -p /home/habachname/Tools
mkdir -p /home/habachname/git
mkdir -p /home/habachname/tmp
echo "Finish Initialization Ubuntu 14.04 LTS - NamHB"
# Reboot
reboot
