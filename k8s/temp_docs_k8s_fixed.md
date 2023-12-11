# Cómo levantar un Clúster de Kubernetes con Vagrant

## Vagrant

Vagrant es una herramienta que podés usar para crear y gestionar entornos de desarrollo virtualizados de manera fácil y reproducible. Su uso típico es facilitar la creación de máquinas virtuales con configuraciones específicas para el desarrollo de proyectos.

Para comenzar un proyecto de Vagrant en el directorio /vagrant, el usuario puede seguir estos pasos:

### Instalación de Vagrant

Antes que nada, necesitás instalar Vagrant en tu máquina. Esto se puede hacer descargando el instalador desde el sitio oficial y siguiendo las [instrucciones](https://developer.hashicorp.com/vagrant/tutorials/getting-started/getting-started-install)

### Instalar el provider de VirtualBox

Descargar de la  [página oficial](https://www.virtualbox.org/wiki/Linux_Downloads).

**¡Importante!** Para poder configurar cierta red privada deberemos crear o modificar el archivo `/etc/vbox/networks.conf` añadiendo la red de la siguiente manera:

```ruby
sudo su
echo "* 0.0.0.0/0" > /etc/vbox/networks.conf
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

## Acceso a los nodos mediante SSH

Para acceder al nodo master:

```sh
ssh -i ~/.ssh/vagrant_key vagrant@192.168.100.171
```

Si queremos entrar como `root` simplemente cambiamos el usuario a root.

## Problemas

- Despliegue de MongoDB, ningun ejemplo da en el clavo con la versión, no la tienen fijada ni a la versión de Kubernetes ni a la versión de MongoDB y las que se logran desplegar no funciona el comando mongod ni mongo, por ende no puedo crear ni un replicaset y obtener el link para el acceso a la DB.
  - Probe tanto con minikube como nuestro cluster bare-metal en vagrant. Verisiones 1.17.0, 1.21.5 y 1.26.1 de Kubernetes. Versiones 4.2 , 4.2.6 y 4.4.2 de MongoDB.
- La carga de imágen del Docker no es tan simple como parece, se necesita usar el DockerHub.
  - Existen métodos que utilizan aplicaciones extra para buscar en las imágenes creadas en local pero son un bardo.
- A la hora de usar la API tiene que cargar valores de entorno los cuales los obtiene del .env, por ende la lógica del código para traer el .env no es la misma que para Kubernetes, donde usamos los Secrets o confimaps.
  - Cambiaría el archivo `config.py`, ya que no se obtendrían las variables de entorno de esa manera y el URL de la DB no sería ese.
  - Entiendo que los valores declarados en `config.py` son utilizado luego en los demás archivos haciendo una importación de módulos.
- ¿Por qué en el docler-compose se definen las variables de entorno como contraseñas si tenes el .env?

### Justificación de por qué correr la DB en una VM y mejor deployar la app solamente

[https://cloud.google.com/blog/products/databases/to-run-or-not-to-run-a-database-on-kubernetes-what-to-consider](https://cloud.google.com/blog/products/databases/to-run-or-not-to-run-a-database-on-kubernetes-what-to-consider)

- No tiene características "amigables" con kubernetes -> Tiene un operador (MongoDB K8s operator)-> La carga de trabajo NO es amigable con Kubernetes (uso en general) -> Es aceptable tener bastante sobrecarga ->  Correr en una VM.

- ¿Como hacemos esto? Instalamos docker en una de las VMs de Vagrant y hacemos el docker-compose del servicio.

# Minikube

Se detectaron problemas de DNS en el Cluster de Vagrant, estos son fácilmente verificables generando un pod de test [dns-utils](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/) y aplicando el siguiente comando:

```sh
kubectl exec -i -t dnsutils -- nslookup <nombre-servicio>.svc.default.cluster.local
```

Donde deberíamos obtener la IP del servicio o del pod al que estamos queriendo llegar con ese dominio. En el caso del Cluster de Vagrant no se obtenían las direcciones IP correspondientes, esto nos asegura que el `core-dns` no está funcionando como corresponde lo que indica una mala intalación de `kubelet`.

Resulta, que por experiencias previas sabíamos que esto podía ser así debido a que la configuración propuesta de Vagrant no permite los reinicios debido a que se corrompen las carpetas compartidas y al no poder reiniciar no se aplican como corresponde las configuraciones pertinentes al aprovisionamiento de Kubernetes.

Dicho esto, y entendiendo además que se complican las pruebas en local, se tomó la decisión de conservar la versión utilizada de Kubernetes (1.26.1) y hacer uso de Minikube, una herramienta opensource que mediante la creación de una máquina virtual nos permite disponer de un entorno sencillo de Kubernetes con la mayor parte de sus funcionalidades.

Para levantar el cluster necesario, ya teniendo Minikube instalado, aplicamos el siguiente comando:

```sh
minikube start --kubernetes-version='1.26.1' --memory='4096' --cpus='2' --disk-size='10GB' --vm=true --nodes=2 -p "test-1.26-2nodes"
minikube addons enable metrics-server
```

Podemos borrar nuestro perfil creado haciendo:

```sh
minikube delete -p test-1.26-2nodes
```

Podemos levantar el Dashboard para una mejor visualización de lo que ocurre con:

```sh
minikube dashboard -p test-1.26-2nodes
```

## Levantar base de datos MySQL

### ¿Por qué MySQL y no MongoDB u alguna otra?

Se hizo la búsqueda de información pertinente para poder hacer una selección adecuada para los requerimientos y en la misma se encontró que entre las bases de datos más utilizadas dentro de los entornos de Kubernetes son MySQL y PostgressSQL y que además, el uso de una base de datos en un entorno de Kuebernetes no es una decisión que debamos tomar a la ligera, debido a que resulta muy complicado el mantenimiento y la misma configuración.

Entendiendo lo anterior, se optó por MySQL como base de datos para el proyecto y la misma se desplegará sobre Kubernetes en una configuración denominada "Statefulset", que permite desplegar nombres de pods y volúmenes persistentes.

### ¿Qué arquitectura elegimos y por qué?

Se probaron 3 diferentes formas para levantar la base de datos en las cuales nos hemos topado con distitos inconvenientes por lo cuales hemos llegado a una decisión final.

Dentro de las pruebas se lograron diferenciar conceptos importantes:

**Headless Services vs. ClusterIP Services vs. NodePort Services**

Los Headless Services no asignan una dirección IP virtual estable, en lugar de eso, devuelven directamente las IP de los pods seleccionados, se usa cuando necesitas acceder a cada instancia individualmente, por ejemplo, en bases de datos distribuidas. Estos realizan "loadbalancing" a la hora de tener que distribuir el tráfico (no le pegan siempre al mmismo pod).

Los ClusterIP Services asignan una IP virtual estable que representa el servicio y dirige el tráfico a los pods seleccionados. Son ideales para servicios internos en el clúster que solo necesitan ser accedidos internamente. Estos realizan balanceo de carga entre los pods seleccionados.

Los NodePort Services exponen el servicio en un puerto en cada nodo del clúster, permitiendo el acceso externo. Son útiles cuando necesitas acceder al servicio desde fuera del clúster, pero no es ideal para producción debido a posibles problemas de seguridad. Este tipo de servicio proporciona balanceo de carga entre los nodos, pero no entre los pods directamente.

**Statefulset**

Es un controlador que mantiene un conjunto de pods con identidades únicas y persistentes. Se utiliza para aplicaciones que requieren identidades persistentes, como bases de datos, donde cada pod tiene un estado y un nombre único. Garantiza que los pods se creen y se escalen de manera ordenada, y proporciona almacenamiento persistente para cada pod.

A diferencia de Deployments, que son más adecuados para aplicaciones sin estado, un StatefulSet es ideal cuando se necesita mantener un estado específico y único para cada instancia, como en el caso de bases de datos.

Supongamos que tenemos un StatefulSet para una base de datos MySQL y decidimos llamar al  StatefulSet "mysql-db". La nomenclatura para los nombres de los pods y persistent volumes generados por el StatefulSet sería algo como:

- Pods generados por el StatefulSet:

  ```sh
  mysql-db-0
  mysql-db-1
  mysql-db-2
  ```

- Persistent Volumes generados por el StatefulSet:

  ```sh
  mysql-db-pv-0
  mysql-db-pv-1
  mysql-db-pv-2
  ```

Cada pod y cada volumen persistente tendría un nombre único basado en el nombre del StatefulSet y un índice que refleja su posición en la secuencia.

Ahora, si tuvieramos un Deployment común para una aplicación web llamado "web-app", los nombres de los pods generados serían más genéricos y probablemente se basarían en un identificador aleatorio o algún nombre de base, como:

- Pods generados por el Deployment:

  ```sh
  web-app-74d8b8b5f9-abcde
  web-app-74d8b8b5f9-12345
  web-app-74d8b8b5f9-xyzab
  ```

- Persistent Volumes generados por el Deployment: No habría persistent volumes específicos asociados directamente con los pods generados por el Deployment, a menos que configures almacenamiento persistente externamente.

En resumen, la diferencia radica en la predictibilidad y consistencia de los nombres. Los StatefulSets generan nombres que reflejan la posición y el propósito específico del pod en la secuencia, mientras que los Deployments comunes pueden generar nombres más aleatorios o genéricos.

**Replicar la base de datos**

Supongamos que gracias a los servicios configurados y nuestra API logramos escribir sobre la base de datos del Statefulset de MySQL, que para este ejemplo consta de 3 pods y por consiguiente 3 PV's.

Si hacemos intentos reiterados para escribir sobre la base de datos resultaría que, gracias al balanceo de cargas realizado por el servicio ClusterIP o Headless, escribiríamos algunos datos en una de las réplicas, otros en la siguiente y así sucesivamente, resultando que, cuando quisieramos leer, no obtendríamos todos los datos de una vez ya que cada réplica es una base de datos independientes y requerimos de una lógica extra para hacer la replicación de la información y así esta esté disponible en todas las replicas.

En el contexto de las DB, podemos configurar un conjunto de réplicas utilizando un controlador StatefulSet y configurar la replicación de cada tipo de DB dentro de los pods.

**Elección tomada**

Entendiendo lo anterior, creemos que un Headless service y una configuración Statefulset es la major elección para desplegar nuestra base de datos.

A la hora de la configuración sobre Minikube se encontró que la configuración de replicación de la DB que nos ofrece de ejemplo la documentación de Kubernetes no funciona como corresponde.

Debido a lo nombrado anteriormente es que se optó por una base de datos en una configuración Statefulset pero que contenga una única réplica así nos olvidamos del problema de la no-replicación.

![MySQL Structure](img/mysql-structure.png)

### Manifiestos de Kubernetes de la DB

Aquí se brinda el manifiesto utilizado:

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: mysql-headless
spec:
  clusterIP: None
  selector:
    app: db
  ports:
    - name: tcp
      protocol: TCP
      port: 3306
---
# $ echo -n "root" | base64
# cm9vdA==
apiVersion: v1
kind: Secret
metadata: 
    name: mysecret
type: Opaque
data:
   ROOT_PASSWORD: cm9vdA==
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: mysql-initdb-config
data:
  init.sql: |
    CREATE DATABASE IF NOT EXISTS api;
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  replicas: 1
  serviceName: mysql-headless
  selector:
    matchLabels:
      app: db
  template:
    metadata:
      labels:
        app: db
    spec:
      terminationGracePeriodSeconds: 10
      containers:
        - name: mysql
          image: mysql:5.7
          ports:
            - containerPort: 3306
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom: 
               secretKeyRef: 
                key: ROOT_PASSWORD
                name: mysecret
          volumeMounts:
            - name: mysql-initdb
              mountPath: /docker-entrypoint-initdb.d
            - name: data
              mountPath: /var/lib/mysql
      volumes:
      - name: mysql-initdb
        configMap:
          name: mysql-initdb-config
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: [ "ReadWriteOnce" ]
        resources:
          requests:
            storage: 1Gi
```

La DB quedará accesible entonces vía el siguiente dominio:

```txt
mysql+pymysql://root:root@mysql-0.mysql-headless.default.svc.cluster.local:3306/api
```

## Backend - Desplegar la API

La API debe ser accesible por fuera con el uso de un servicio tipo NodePort y a su vez debe poder acceder a la DB mediante el uso de DNS, pegandole al pod correspondiente (o al servicio, da igual porque tenemos un único pod) de la DB.

Para ello se creó el siguiente manifiesto:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api 
spec:
  type: NodePort
  ports:
    - port: 8000
      targetPort: 8000
      nodePort: 31000
  selector:
    app: api
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  labels:
    app: api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api-backend-fastapi
          image: aagustinconti/fast-api-products:latest #DockerHub repo
          ports:
            - containerPort: 8000
          imagePullPolicy: Always
          env:
          - name: MYSQL_HOST
            value: mysql-0.mysql-headless.default.svc.cluster.local
          - name: MYSQL_USER
            value: root
          - name: MYSQL_PASSWORD
            value: root
          - name: MYSQL_DATABASE
            value: api
          - name: DATABASE_URI
            value: 'mysql+pymysql://root:root@mysql-0.mysql-headless.default.svc.cluster.local:3306/todo'
```

Como dato a tener en cuenta, la API estará disponible en el puerto 31000 de la IP del nodo worker. Internamente el container tendrá expuesto el puerto 8000, el cual estará apuntado por el servicio tipo NodePort para poder exponerlo al 31000, justamente.

Otro dato importante es que se tuvo que dockerizar la API y subir la imagen al DockerHub para que Kubernetes la pueda descargar, como se ve, esta está disponible en `aagustinconti/fast-api-products:latest`.

La gráfica quedaría de la siguiente manera:

![Diagram API](img/diagram-api.png)

## Frontend - Desplegar la UI

La UI debe poder comunicarse con la API y y a su vez debe ser accesible desde el puerto 80 de la IP del nodo así los usuarios pueden acceder a la misma. Para lo anterior se creó otro servicio tipo NodePort y a su vez se le pasaron los datos importantes para que se pueda conectar a la API, como el host: `mysql-0.mysql-headless.default.svc.cluster.local`, la clave, el usuario y la DB.

El manifiesto utilizado fue el siguiente:

```yml
apiVersion: v1
kind: Service
metadata:
  name: ui 
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30001
  selector:
    app: ui
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ui
  labels:
    app: ui
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ui
  template:
    metadata:
      labels:
        app: ui
    spec:
      containers:
        - name: api-frontend-node
          image: aagustinconti/ui-node-products:latest # DockerHub repo
          ports:
            - containerPort: 80
          imagePullPolicy: Always
          env:
          # <service-name>.<namespace>.svc.cluster.local:<service-port>
          - name: API_URL
            value: 'http://api:8000'
          - name: PORT
            value: '80'
          - name: IMAGE_URL
            value: 'http://<worker-node-ip>:31000'

```

Nuevamente se utilizó Docker para crear la imágen y subirla al DockerHub para que sea accesible por Kubernetes a través de `aagustinconti/ui-node-products:latest`.

Por otro lado debemos observar algo clave, entre los valores de las variables de entorno que le suministramos, encontramos que encuentra perfectamente a la api mediante el servicio "api" en el puerto 8000 (utilizando la resolución de DNS), mientras que el otro parámetro es "IMAGE_URL" nos debería llamar la atención, ya que debemos configurar a mano la IP del nodo, lo que no es del todo conveniente porque al no usar resolución por DNS, si se cae el nodo puede aparecer con otra IP y no será más accesible.

Lo anterior se da debido a un inconveniente de programación de la UI, donde esta se divide en dos partes, Server y Client, el cliente está en la máquina del usuario que accede a la página web mientras que el Server es el pod que procesa todas las peticiones. En este caso, las imágenes deberían ser peticionadas al pod de UI desde ahí, el pod debería pedirle a la API las imágenes ya que el POD de la UI sí vé a la API internamente, pero sucede que no fue posible esa configuración, por lo que el cliente accedería a las imágenes de la API mediante el uso de la IP del servicio NodePort. Entendemos que no es conveniente, pero hasta la resolución de este inconveniente mantendremos en funcionamiento de esta manera.

El diagrama queda como sigue:

![Diagrama UI](img/diagrama-ui.png)

## Referencias

- [dns-utils](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/)

- [Google: Correr o no correr una DB en Kubernetes](https://cloud.google.com/blog/products/databases/to-run-or-not-to-run-a-database-on-kubernetes-what-to-consider)

- [StatefulSets & Headless Services Demo with MySQL DB | Sample Todo Application with MySQL DB](https://www.youtube.com/watch?v=nUm4Y5uEG7k&t=1502s)

- [Repositorio GitHub: kunchalavikram1427/StatefulSets_demo](https://github.com/kunchalavikram1427/StatefulSets_demo/tree/master/python_todo_app/kubernetes)

- [Kubernetes: Run a Replicated Stateful Application](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/)
