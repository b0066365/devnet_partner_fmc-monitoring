# DevNet - FMC Insights
Content for DevNet FMC Insights Session

THIS IS A DEMO PROJECT - NOT INTENDED FOR PRODUCTION USE! 

***

# Installation
* Based on Centos 7.6.1810 (Minimal ISO) - http://mirror.cj2.nl/centos/7.6.1810/isos/x86_64/CentOS-7-x86_64-Minimal-1810.iso
* Update your System to the latests packages available
```
yum install -y epel-release
yum update -y
```

* Disable SELinux
```
sed -i 's/enforcing/disabled/g' /etc/selinux/config
```
* Configure your NTP and DNS correctly
* Reboot 

* Install Docker-CE
Following official Docker Documentation - https://docs.docker.com/install/linux/docker-ce/centos/

Add the Docker-CE Repo
```
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

Install the Docker Engine
```
yum install -y docker-ce docker-ce-cli containerd.io docker-compose
```

Start Docker Engine and Enable it Start at reboot
```
systemctl enable docker
systemctl start docker
systemctl status docker
```

Testing the Docker Engine
```
docker run hello-world
```


# Installing the Stack

Create a directory for the stack
```
mkdir /opt/devnet && cd /opt/devnet
```

```
mkdir -p conf/telegraf/telegraf.d/
```


```
mkdir -p conf/grafana
mkdir env
```



Create the docker-compose file (docker-compose.yml)

```yaml
version: '3'
services:
  influxdb: 
    image: influxdb
    volumes:
      - devnet-influxdb-data:/var/lib/influxdb:z
    ports:
      - 8080
      
volumes:
  devnet-influxdb-data:
    driver: local
```

Grafana Environement File (grafana.env)
```

```



***
# Configuration
***
# Collecting Metrics
## Basic Metrics
## Advanced Metrics
