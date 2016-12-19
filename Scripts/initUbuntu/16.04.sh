#!/bin/bash
echo "Start Initialization Ubuntu 14.04 LTS - NamHB"
# Apt config
cp souces1604.list /etc/apt/sources.list
apt-get update
# Install google chrome, download
# * Java JDK, extract, rename to java
# * Virtualbox: Download
# * Sublime, netbean
sudo apt-get install build-essential unity-tweak-tool git bleachbit compizconfig-settings-manager tmux vim vlc unrar p7zip filezilla python-pip gdb libssl-dev
sudo add-apt-repository -y ppa:noobslab/themes
sudo add-apt-repository -y ppa:noobslab/icons
sudo add-apt-repository -y ppa:numix/ppa
sudo apt-get update
sudo apt-get install -y flatabulous-theme arc-flatabulous-theme numix-gtk-theme ultra-flat-icons classicmenu-indicator
sudo apt-get purge -y cups-browsed cups-daemon libreoffice-math cheese unity-webapps-amazon* simple-scan

sudo cp ./NetworkManager.conf /etc/NetworkManager/NetworkManager.conf
cp ./.tmux.conf ~/

sudo apt-get install -y apt-transport-https ca-certificates
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install -y docker-engine
sudo usermod -aG docker habachnam
sudo docker login

# For java, push java folder herer
sudo cp -R java /opt
sudo update-alternatives --install /usr/bin/java java /opt/java/jre/bin/java 1
sudo update-alternatives --set java /opt/java/jre/bin/java
sudo update-alternatives --set javac /opt/java/bin/javac
sudo update-alternatives --set javac /opt/java/bin/javac
# For Android studio
sudo apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386
# Heroku
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
heroku login

# Create tools
mkdir -p /home/habachname/Tools
mkdir -p /home/habachname/git
mkdir -p /home/habachname/tmp
# Vim, bash
cp .bashrc ~/.bashrc
cp .vimrc ~/.vimrc
# Disable Guest
sudo sh -c 'printf "[SeatDefaults]\nallow-guest=false\n" > /etc/lightdm/lightdm.conf.d/50-no-guest.conf'
echo "Finish Initialization Ubuntu 16.04 LTS - NamHB"
