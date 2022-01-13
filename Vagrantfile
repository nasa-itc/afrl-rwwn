# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "itc/itc-ubuntu-mate-20.04-amd64"
    config.vm.box_version = "= 1.0.0"
    config.vm.box_download_checksum_type = "sha256"
    config.vm.box_download_checksum = "dc566ba5bffdfc46988f938784b46596e63269222509c4d97802a78681ae0da7"
    config.vm.hostname = "afrl-vm"
    config.vm.provider "virtualbox" do |vb|
        vb.name = "AFRL-RWWN"
        vb.gui = true
        vb.cpus = 2
        vb.memory = "4096"
        vb.customize ["modifyvm", :id, "--graphicscontroller", "vmsvga"]
        vb.customize ["modifyvm", :id, "--vram", 64]
        vb.customize ["storageattach", :id,
                      "--storagectl", "IDE Controller",
                      "--port", "0",
                      "--device", "1",
                      "--type", "dvddrive",
                      "--medium", "emptydrive"] 
    end

    config.vm.provision "ansible_local" do |ansible|
        ansible.inventory_path = "ansible/hosts"
        ansible.limit = "localhost"
        ansible.playbook = "ansible/afrl.yml"
        ansible.extra_vars = {
            afrl_source: "/vagrant",
            afrl_user: "itc",
            vagrant_provisioning: true
        }
    end
end

