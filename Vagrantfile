# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

    config.vm.box = "4hm-vagrant-wheezy32"
    config.vm.box_url = "http://www.matteoparrucci.it/vagrant-wheezy32.box"
    config.ssh.private_key_path = "keys/id_rsa"
    config.ssh.port = 2202

    # Webserver
    config.vm.network :forwarded_port, guest: 22, host: 2202
    config.vm.network :forwarded_port, guest: 80, host: 8081
    config.vm.network :forwarded_port, guest: 8000, host: 8000
    config.vm.network :private_network, ip: "192.168.50.5"
    config.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--memory", "512"]
        v.name = "4hm"
    end

    # SALT STACK PROVISIONING
    ## For masterless, mount your salt file root
    config.vm.synced_folder "./salt/roots/", "/srv/"
    # config.vm.synced_folder "./development", "/var/www/"
    ## Use all the defaults:
    config.vm.provision :salt do |salt|
        salt.install_type = "stable"
        salt.verbose = true
        salt.run_highstate = true
        ## Optional Settings:
        salt.minion_config = "salt/minion.conf"
        # salt.temp_config_dir = "/existing/folder/on/basebox/"
        # salt.salt_install_type = "git"
        # salt.install_args = "develop"

        ## If you have a remote master setup, you can add
        ## your preseeded minion key
        # salt.minion_key = "salt/key/minion.pem"
        # salt.minion_pub = "salt/key/minion.pub"
    end
end
