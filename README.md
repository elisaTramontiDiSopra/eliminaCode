# eliminaCode

se la connessione sulla raspberry cade, provare a controllare il file /etc/network/interfaces
provare con la configurazione hotplug 

 auto eth0
 allow-hotplug eth0
 iface eth0 inet dhcp