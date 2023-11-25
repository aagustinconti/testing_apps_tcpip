# Cómo levantar un Clúster de Kubernetes con Vagrant

## Vagrant

Vagrant es una herramienta que podés usar para crear y gestionar entornos de desarrollo virtualizados de manera fácil y reproducible. Su uso típico es facilitar la creación de máquinas virtuales con configuraciones específicas para el desarrollo de proyectos.

Para comenzar un proyecto de Vagrant en el directorio /vagrant, el usuario puede seguir estos pasos:

### Instalación de Vagrant

Antes que nada, necesitás instalar Vagrant en tu máquina. Esto se puede hacer descargando el instalador desde el sitio oficial y siguiendo las [instrucciones](https://developer.hashicorp.com/vagrant/tutorials/getting-started/getting-started-install)

**¡Importante!** Para poder configurar cierta red privada deberemos crear o modificar el archivo `/etc/vbox/networks.conf` añadiendo la red de la siguiente manera:

```ruby
sudo su
echo "* 0.0.0.0/0" > networks.conf
```

### Crear las claves públicas y privadas para las conexiones SSH

Creamos nuestra propia clave pública y privada con `ssh-keygen`, procuramos no poner passphrase para que no se la solicite a las VMs a la hora de iniciarlas.

```bash
# ~/.ssh/
> ssh-keygen -t rsa -b 4096
Generating public/private rsa key pair.
Enter file in which to save the key (/home/aagustin/.ssh/id_rsa): vagrant_key
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in vagrant_key
Your public key has been saved in vagrant_key.pub
The key fingerprint is:
SHA256:K4v2o7EKOLfjCMLk7zVD4v234234c06peueU aagustin@hp-agustin
The key's randomart image is:
+---[RSA 4096]----+
|                 |
|                 |
|                 |
|                 |
| . . . .S     .  |
|= . 3 o ..   o.. |
|*o.+.*.... +.++. |
|o=o.B4==  . *++  |
|..=*+*=++ .+o. E |
+----[SHA256]-----+
```

## Instalación de Ansible

Ejecutamos los siguientes comandos en nuestra máquina host:

```
sudo apt update
sudo apt install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt update
sudo apt install ansible
```

## Personalizar nuestros archivos de configuración y aprovisionar

### Configuraciones de perfil

Ingresamos al archivo `ansible/group_vars/all.yml` y elegimos la cantidad de nodos que deseemos, también la versión de Kubernetes. Además seleccionamos los recursos.

En nuestro caso se dejó de la siguiente manera:

```yaml
---
settings:
  env: 'test_api'
  users:
    test_api:
      prod_test: false
      
      environment: ""
      
      user_dir_path: /home/aagustin
      node_home_dir: /home/vagrant

      shared_folders:
        - host_path: ./shared_folder
          vm_path: /home/vagrant 

      cluster_name: Kubernetes Cluster
      
      ssh:
        user: "vagrant"
        password: "vagrant"
        private_key_path: /home/aagustin/.ssh/vagrant_key # Crearse una para que funcione
        public_key_path: /home/aagustin/.ssh/vagrant_key.pub # Crearse una para que funcione

      nodes:
        control:
          cpu: 2
          memory: 4096 
        workers:
          count: 2 
          cpu: 2 
          memory: 4096 
      
      network:
        control_ip: 192.168.100.171
        dns_servers:
          - 8.8.8.8
          - 1.1.1.1
        pod_cidr: 172.16.1.0/16
        service_cidr: 172.17.1.0/18
      

      software:
        box: bento/ubuntu-22.04
        calico: 3.25.0
        kubernetes: 1.26.1-00
        os: xUbuntu_22.04
 
        flannel: 0.23.0
        contained: v1.5


```

### Levantar máquinas virtuales de Vagrant

Levantarlas:

```sh
# en <project-dir>/k8s/
vagrant up
```

Si deseamos eliminarlas:

```sh
# en <project-dir>/k8s/
vagrant destroy
```

### Aprovisionamos con Ansible

Desde la máquina host, posicionados en `<project-dir>/k8s/`, ejecutaremos los siguientes comandos:

```sh
ansible -i ansible/inventory_local.yml -m ping all
```

Y nos aseguraremos de tener respuesta de todos los nodos creados.

Y luego aprovisionamos con:

```sh
ansible-playbook -vvv ansible/site.yml -i ansible/inventory_local.yml
```
