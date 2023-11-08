#!/bin/bash

sudo apt install python3-pip -y
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:ansible/ansible-2.9 -y
sudo apt-get update -y
sudo apt install ansible -y
ansible --version 
if [ $? -eq 0 ] ; then
echo 'Ansible is installed' > /home/vagrant/ansible_check
else
echo 'Ansible is NOT installed -- installing' > /home/vagrant/ansible_check
sudo apt install ansible -y
fi

echo 'export ANSIBLE_HOST_KEY_CHECKING=False' >> /home/vagrant/.bashrc
