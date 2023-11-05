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

Una sola instancia de k6 puede simular desde 30 a 40 mil usuarios simultáneos.

Con 30 mil usuarios concurrentes hacemos aproximadamente 300 mil request por segundo (RPS) o de 6 a 12 millones de request por minuto.

Si queremos simular más usuarios, deberemos hacer "distributed testing" o testing distribuido, es decir, podemos usar un Cluster de Kubernetes para levantar varios pods con varias instancias de K6 y así incrementar el número a un numero realmente grande.

Para tener una idea, la simulación de un virtual user requiere de 1 a 5 MB de RAM, por lo que para simular 1000 usuarios requerimos de 1 a 5 GB de RAM.

La CPU no es una gran limitación a considerar ya que está bastante optimizado.

## Opciones de K6

Crearemos otro archivo `.js` pero en este caso especificaremos ciertos parámetros u opciones dentro del mismo archivo. Entocnes, creamos el archivo `options.js`.

Dentro del mismo archivo observaremos que los parámetros que antes pasábamos por consola ahora los pasamos directamente como constantes dentro del mismo:

```js
export const options = {

  vus: 100,
  duration: '30s',

};
```

Ahora para ejectuar nuestro test directamente hacemos:

```sh
k6 run options.js
```

Y deberíamos obtener lo siguiente:

```sh

          /\      |‾‾| /‾‾/   /‾‾/   
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: options.js
     output: -

  scenarios: (100.00%) 1 scenario, 100 max VUs, 1m0s max duration (incl. graceful stop):
           * default: 100 looping VUs for 30s (gracefulStop: 30s)


     data_received..................: 60 MB  1.9 MB/s
     data_sent......................: 332 kB 11 kB/s
     http_req_blocked...............: avg=4.28ms   min=227ns   med=1.2µs    max=143.46ms p(90)=1.81µs   p(95)=2.29µs  
     http_req_connecting............: avg=1.1ms    min=0s      med=0s       max=42.57ms  p(90)=0s       p(95)=0s      
     http_req_duration..............: avg=66.49ms  min=22.5ms  med=35.39ms  max=1.31s    p(90)=101.7ms  p(95)=157.63ms
       { expected_response:true }...: avg=66.49ms  min=22.5ms  med=35.39ms  max=1.31s    p(90)=101.7ms  p(95)=157.63ms
     http_req_failed................: 0.00%  ✓ 0         ✗ 2846 
     http_req_receiving.............: avg=24.77ms  min=86.12µs med=12.1ms   max=936.75ms p(90)=62.42ms  p(95)=85.75ms 
     http_req_sending...............: avg=118.48µs min=21.21µs med=115.26µs max=1.31ms   p(90)=158.15µs p(95)=177.61µs
     http_req_tls_handshaking.......: avg=3.15ms   min=0s      med=0s       max=116.44ms p(90)=0s       p(95)=0s      
     http_req_waiting...............: avg=41.6ms   min=18.32ms med=21.54ms  max=949.15ms p(90)=42.2ms   p(95)=76.31ms 
     http_reqs......................: 2846   91.615347/s
     iteration_duration.............: avg=1.07s    min=1.02s   med=1.03s    max=2.44s    p(90)=1.1s     p(95)=1.16s   
     iterations.....................: 2846   91.615347/s
     vus............................: 3      min=3       max=100
     vus_max........................: 100    min=100     max=100


running (0m31.1s), 000/100 VUs, 2846 complete and 0 interrupted iterations
default ✓ [======================================] 100 VUs  30s
```

## Incluir fluctuaciones dentro de los test

Para ser un poco mas acordes a escenarios de la vida real deberemos considerar fluctuaciones en la cantidad de los usuarios y modificando el `.js` podremos icluirlas. Por eso creamos el archivo `stages.js` para contemplar esto:

```js
import http from "k6/http";
import { check, sleep } from 'k6';

export const options = {

  stages: [
    { duration: "30s", target: 25 },
    { duration: "1m", target: 50 },
    { duration: "20s", target: 0 },
  ],

};

export default function () {
  const pages = [
    "/",
    "/5-attachments",
    "/this-does-not-exist/",
  ]
  for (const page of pages) {
    const res = http.get("https://aagustinconti.github.io/testing_apps_tcpip" + page);
    check(res, {
      "status was 200": (r) => r.status == 200,
      "duration was <=": (r) => r.timings.duration <= 200
    });
    sleep(1)
  }
}
```

Notaremos que definimos diferentes stages o "etapas" de la prueba, donde, por ejemplo, en la primera tendremos una duración de 30 segundos y la cantidad de usuarios de la prueba será de 25.

Luego definimos páginas objetivo para cada prueba, entonces no solo hacemos el test de carga sobre la página home, por ejemplo, sino también sobre las diferentes subpáginas.

Se añadió un checkeo para ver si la respuesta es del tipo 200 y dura menos de 200ms para poder observar cuantas fueron OK y cuantas no de todas las request que se enviaron. Incluimos también una subpágina inexistente para ver cómo maneja los errores.

Nuevamente, para simular:

```sh
k6 run stages.js
```

Y lo que obtenemos de output es lo siguiente:

```sh

          /\      |‾‾| /‾‾/   /‾‾/   
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

  execution: local
     script: stages.js
     output: -

  scenarios: (100.00%) 1 scenario, 50 max VUs, 2m20s max duration (incl. graceful stop):
           * default: Up to 50 looping VUs for 1m50s over 3 stages (gracefulRampDown: 30s, gracefulStop: 30s)


     ✗ status was 200
      ↳  66% — ✓ 2028 / ✗ 1014
     ✗ duration was <=
      ↳  99% — ✓ 3029 / ✗ 13

     checks.........................: 83.11% ✓ 5057      ✗ 1027
     data_received..................: 61 MB  547 kB/s
     data_sent......................: 339 kB 3.0 kB/s
     http_req_blocked...............: avg=612.42µs min=180ns   med=1.1µs    max=174.74ms p(90)=1.82µs  p(95)=1.98µs  
     http_req_connecting............: avg=272.83µs min=0s      med=0s       max=68.29ms  p(90)=0s      p(95)=0s      
     http_req_duration..............: avg=33.68ms  min=18.67ms med=25.53ms  max=934.71ms p(90)=57.33ms p(95)=80.49ms 
       { expected_response:true }...: avg=32.19ms  min=18.67ms med=24.94ms  max=695.95ms p(90)=50.75ms p(95)=77.5ms  
     http_req_failed................: 25.00% ✓ 1014      ✗ 3042
     http_req_receiving.............: avg=9.38ms   min=32.15µs med=3.47ms   max=341.74ms p(90)=22.14ms p(95)=51.83ms 
     http_req_sending...............: avg=127.28µs min=25.12µs med=128.26µs max=965.15µs p(90)=181.2µs p(95)=205.91µs
     http_req_tls_handshaking.......: avg=334.8µs  min=0s      med=0s       max=106.08ms p(90)=0s      p(95)=0s      
     http_req_waiting...............: avg=24.17ms  min=18.5ms  med=21.37ms  max=926.46ms p(90)=26.99ms p(95)=30.78ms 
     http_reqs......................: 4056   36.330472/s
     iteration_duration.............: avg=3.14s    min=3.08s   med=3.1s     max=5.28s    p(90)=3.23s   p(95)=3.3s    
     iterations.....................: 1014   9.082618/s
     vus............................: 2      min=1       max=50
     vus_max........................: 50     min=50      max=50


running (1m51.6s), 00/50 VUs, 1014 complete and 0 interrupted iterations
default ✓ [======================================] 00/50 VUs  1m50s
```

Vemos que al incluir una página inexistente hubo 1014 request que no tuvieron respuesta del tipo 200 (OK). Además hubo 13 request que duraron más de 200ms.

Ahora, respecto a cómo manejó el error de una página existente, si observamos el exit code de la ejecución anterior:

```sh
> echo $?                                                                                                     
0
```

Nos dá `0`, lo que implica que NO HUBO ERRORES DE EJECUCIÓN, lo pudo manejar. Entonces, si estamos trabajando en algún pipeline, no hay necesidad de parar ya que NO existe error.

## Incluir K6 en CI/CD Pipelines

```js
import http from "k6/http";
import { check, sleep } from 'k6';


export const options = {
  stages: [
    { duration: "30s", target: 10 },
    { duration: "1m", target: 50 },
    { duration: "20s", target: 0 },
  ],

  thresholds: {
    http_req_duration: ["p(90)<200", "p(95)<300"],
    /*
    "http_req_duration{what:home}": [{
      thresholds: "p(95)<100",
      abortOnFail: true,
      delayAbortEval: "10s",
    }],
    */
  }
};

export default function () {
  const pages = [
    "/2-body",
    "/5-attachments",
    "/this-does-not-exist/",
  ]

  for (const page of pages) {
    const resHome = http.get(
      "https://aagustinconti.github.io/testing_apps_tcpip",
      {
        tags: { what: "home" }
      });

    check(resHome, {
      "status was 200": (r) => r.status == 200,
    });

    const resPage = http.get("https://aagustinconti.github.io/testing_apps_tcpip" + page);

    check(resPage, {
      "status was 200": (r) => r.status == 200,
    });

    sleep(1);
  }
}
```

Aquí incluimos, además de diferentes etapas, diferentes "requerimientos", donde definimos múltiples "umbrales" o "thresholds", para las diferentes páginas, siendo más o menos demandantes para cada una. Además le definimos que en el caso de que no se cumpla alguna de los requerimientos que pare el proceso.

Para ejecutar esto:

```sh
k6 run ci.js
```

## Referencias

- [The Best Performance And Load Testing Tool? k6 By Grafana Labs](https://www.youtube.com/watch?v=5OgQuVAR14I)
- [K6 - Installation](https://k6.io/docs/get-started/installation/)
- [K6 - Create Custom Metrics](https://k6.io/docs/using-k6/metrics/create-custom-metrics/)
