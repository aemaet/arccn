sudo /etc/init.d/openvswitch-switch stop
sudo rm -rf /var/log/openvswitch/*
sudo rm -rf /etc/openvswitch/conf.db
sudo /etc/init.d/openvswitch-switch start
sudo ovs-vsctl show
