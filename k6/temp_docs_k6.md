# k6

## Hacer un test de cargar simple

### Descarga de dependencias

En Debian/Ubuntu, seguimos los pasos de la [página de K6](https://k6.io/docs/get-started/installation/).

Simplemente correremos en consola lo siguiente:

```sh
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### Creación de archivo del test de carga

Dentro de nuestro directorio de trabajo creamos un archivo `simple.js` (podría llamarse de cualquier forma) y dentro de él escribimos lo siguiente:

``` javascript
import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  http.get('https://aagustinconti.github.io/testing_apps_tcpip/');
  sleep(1);
```

Lo importante acá es entender que no correremos nuestro test sobre javascript, ya que es extremadamente ineficiente y no podría manejar miles y miles de peticiones. Quien puede manejar todo esto es `GO`.

Simplemente escribimos en este lenguaje porque es 'más fácil de entender', luego K6 será el encargado de convertir ese archivo `.js` a un archivo `GO`.

### Correr el test de carga

Para correr el test lo único que debemos hacer es poner en consola lo siguiente:

```sh
# on working dir
k6 run simple.js
```

### Observamos las métricas obtenidas

```sh
# En nuestro caso le apuntamos a la página de nuestra documentación 'https://aagustinconti.github.io/testing_apps_tcpip/'

> k6 run simple.js

          /\      |‾‾| /‾‾/   /‾‾/   
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: simple.js
     output: -

  scenarios: (100.00%) 1 scenario, 1 max VUs, 10m30s max duration (incl. graceful stop):
           * default: 1 iterations for each of 1 VUs (maxDuration: 10m0s, gracefulStop: 30s)


     data_received..................: 25 kB 13 kB/s
     data_sent......................: 707 B 349 B/s
     http_req_blocked...............: avg=372.61ms min=372.61ms med=372.61ms max=372.61ms p(90)=372.61ms p(95)=372.61ms
     http_req_connecting............: avg=100.67ms min=100.67ms med=100.67ms max=100.67ms p(90)=100.67ms p(95)=100.67ms
     http_req_duration..............: avg=650.6ms  min=650.6ms  med=650.6ms  max=650.6ms  p(90)=650.6ms  p(95)=650.6ms 
       { expected_response:true }...: avg=650.6ms  min=650.6ms  med=650.6ms  max=650.6ms  p(90)=650.6ms  p(95)=650.6ms 
     http_req_failed................: 0.00% ✓ 0        ✗ 1  
     http_req_receiving.............: avg=248.39µs min=248.39µs med=248.39µs max=248.39µs p(90)=248.39µs p(95)=248.39µs
     http_req_sending...............: avg=379.37µs min=379.37µs med=379.37µs max=379.37µs p(90)=379.37µs p(95)=379.37µs
     http_req_tls_handshaking.......: avg=67.17ms  min=67.17ms  med=67.17ms  max=67.17ms  p(90)=67.17ms  p(95)=67.17ms 
     http_req_waiting...............: avg=649.97ms min=649.97ms med=649.97ms max=649.97ms p(90)=649.97ms p(95)=649.97ms
     http_reqs......................: 1     0.493935/s
     iteration_duration.............: avg=2.02s    min=2.02s    med=2.02s    max=2.02s    p(90)=2.02s    p(95)=2.02s   
     iterations.....................: 1     0.493935/s
     vus............................: 1     min=1      max=1
     vus_max........................: 1     min=1      max=1


running (00m02.0s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m02.0s/10m0s  1/1 iters, 1 per VU
```

Lo que acabamos de hacer es simular que tenemos **un solo usuario virtual**.

Si observamos las métricas tentremos un panorama general del rendimiento, y estas son solo algunas, podremos agregar más.

Podremos utilizar las métricas que ya nos provee K6, pero también podremos crear métricas [nosotros mismos](https://k6.io/docs/using-k6/metrics/create-custom-metrics/).

## Simular más de un usuario virtual

Podemos indicar el número de usuarios que querramos probar de la siguiente manera:

```sh
k6 run --vus 10 --duration 30s simple.js
```

Como vemos agregamos dos parámetros más a la ejecución:

- `vus`: Indica el número de usuarios virtuales que queremos simular.
- `duration`: Indica la duracióon del test.

Veamos el output:

```sh
> k6 run --vus 10 --duration 30s simple.js

          /\      |‾‾| /‾‾/   /‾‾/   
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: simple.js
     output: -

  scenarios: (100.00%) 1 scenario, 10 max VUs, 1m0s max duration (incl. graceful stop):
           * default: 10 looping VUs for 30s (gracefulStop: 30s)


     data_received..................: 5.8 MB 190 kB/s
     data_sent......................: 32 kB  1.0 kB/s
     http_req_blocked...............: avg=8.15ms   min=285ns    med=1.14µs   max=231.92ms p(90)=1.78µs   p(95)=2.37µs  
     http_req_connecting............: avg=798.19µs min=0s       med=0s       max=22.95ms  p(90)=0s       p(95)=0s      
     http_req_duration..............: avg=75.69ms  min=28.22ms  med=35.04ms  max=1.01s    p(90)=70.44ms  p(95)=87.79ms 
       { expected_response:true }...: avg=75.69ms  min=28.22ms  med=35.04ms  max=1.01s    p(90)=70.44ms  p(95)=87.79ms 
     http_req_failed................: 0.00%  ✓ 0        ✗ 279 
     http_req_receiving.............: avg=29.47ms  min=234.26µs med=12.93ms  max=407.56ms p(90)=46.76ms  p(95)=65.02ms 
     http_req_sending...............: avg=137.36µs min=32.76µs  med=131.43µs max=649.49µs p(90)=171.43µs p(95)=200.64µs
     http_req_tls_handshaking.......: avg=3.19ms   min=0s       med=0s       max=93.61ms  p(90)=0s       p(95)=0s      
     http_req_waiting...............: avg=46.08ms  min=18.49ms  med=21.39ms  max=913.48ms p(90)=33.55ms  p(95)=64.56ms 
     http_reqs......................: 279    9.073319/s
     iteration_duration.............: avg=1.08s    min=1.02s    med=1.03s    max=2.24s    p(90)=1.07s    p(95)=1.08s   
     iterations.....................: 279    9.073319/s
     vus............................: 10     min=10     max=10
     vus_max........................: 10     min=10     max=10


running (0m30.7s), 00/10 VUs, 279 complete and 0 interrupted iterations
default ✓ [======================================] 10 VUs  30s
```


## Referencias

- [The Best Performance And Load Testing Tool? k6 By Grafana Labs](https://www.youtube.com/watch?v=5OgQuVAR14I)
- [K6 - Installation](https://k6.io/docs/get-started/installation/)
- [K6 - Create Custom Metrics](https://k6.io/docs/using-k6/metrics/create-custom-metrics/)
