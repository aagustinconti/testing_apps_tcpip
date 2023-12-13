# k6

## ¿Qué es k6?

k6 es una herramienta de código abierto destinada a realizar pruebas de carga y rendimiento en aplicaciones y servicios web. Utilizando JavaScript/ES6 para escribir scripts de prueba, k6 destaca por su sencilla sintaxis y soporte para protocolos como HTTP/1.1, HTTP/2 y WebSockets. Diseñado para ejecutarse en la nube y ser fácilmente integrado en flujos de trabajo de CI/CD, k6 proporciona informes detallados y métricas para evaluar el rendimiento de las aplicaciones bajo diversas condiciones de carga. Su flexibilidad y extensibilidad lo convierten en una herramienta valiosa para evaluar y mejorar la escalabilidad de sistemas web.

Entonces, k6 simplifica la realización de pruebas de rendimiento al ofrecer una solución basada en JavaScript con características como integración en la nube, generación de informes detallados y soporte para varios protocolos, proporcionando a los equipos de desarrollo la capacidad de evaluar y optimizar el rendimiento de sus aplicaciones de manera efectiva.

Gracias a ella pudimos plantear pruebas de stress locales hacia diferentes host y endpoints de nuestra api para poder verificar el cumplimiento de los requerimientos acordados con el cliente.

## K6 junto con Prometheus y Grafana

La visualización de datos a través de Grafana en conjunto con Prometheus ofrece una visión integral y en tiempo real del rendimiento del cluster que hospeda la aplicación. Al integrar estadísticas proporcionadas por k6 con los datos de consumo de recursos obtenidos mediante Prometheus, los equipos de desarrollo y operaciones pueden identificar patrones y correlaciones significativas. Esto permite una comprensión profunda de cómo las pruebas de carga impactan los recursos del cluster y cómo estos afectan directamente al rendimiento de la aplicación en producción. Grafana, con sus capacidades de visualización altamente personalizables, proporciona paneles intuitivos y gráficos dinámicos que facilitan la identificación de tendencias, cuellos de botella y áreas de mejora, permitiendo una toma de decisiones informada para optimizar la escalabilidad y la eficiencia del sistema.

La combinación de k6, Prometheus y Grafana proporciona una sinergia poderosa al permitir que los equipos monitoreen y analicen simultáneamente el rendimiento de las pruebas de carga y el comportamiento del cluster en producción. Esta integración facilita la identificación proactiva de posibles problemas y la optimización continua del rendimiento, respaldando la toma de decisiones basada en datos con una representación visual clara y detallada de la salud y eficiencia del sistema en tiempo real.

## Instalación de k6

En Debian/Ubuntu, seguimos los pasos de la [página de K6](https://k6.io/docs/get-started/installation/).

Simplemente correremos en consola lo siguiente:

```sh
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### Correr el test de carga

Para correr cualquier test lo único que debemos hacer es poner en consola lo siguiente:

```sh
# on k6 dir
k6 run test-api/<nombre-del-test>.js
```

## Pruebas realizadas

Las pruebas se centraron en cumplir con los requisitos de resistencia del cliente, priorizando la capacidad de la interfaz de usuario para soportar más de 5000 usuarios simultáneos en su página principal. Además, se llevaron a cabo pruebas adicionales, como la creación masiva de usuarios y productos para evaluar la robustez de la API y la base de datos. Otra prueba se centró en medir el consumo de red al recuperar datos en formato base64 de imágenes completas desde la base de datos. Por último, se evaluó el rendimiento del procesamiento de la API, incluyendo pruebas de carga en el proceso de inicio de sesión que involucra tokens y contraseñas encriptadas con BCrypt. En todos los escenarios, se monitorearon detenidamente la CPU, la RAM, la lectura/escritura del disco y el consumo de red para obtener una visión completa del rendimiento del sistema.

### Test 1: UI

Archivo de configuración de K6 utilizado:

```js
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '15s', target: 1000 },
    { duration: '30s', target: 2500 },
    { duration: '1m', target: 5000 },
  ],
};

export default function () {
  http.get('http://192.168.39.203:30001/');
  sleep(1);
}
```

Resultado de consola de k6:

```sh
     data_received..................: 141 MB 1.1 MB/s
     data_sent......................: 1.3 MB 10 kB/s
     http_req_blocked...............: avg=74.96ms  min=951ns  med=5.29µs  max=7.3s   p(90)=529.72µs p(95)=5.64ms  
     http_req_connecting............: avg=42.82ms  min=0s     med=0s      max=7.3s   p(90)=357.86µs p(95)=447.3µs 
     http_req_duration..............: avg=25.35s   min=8.63ms med=23.68s  max=1m0s   p(90)=46.43s   p(95)=49.46s  
       { expected_response:true }...: avg=24.8s    min=8.63ms med=23.67s  max=59.98s p(90)=44.26s   p(95)=47.46s  
     http_req_failed................: 1.57%  ✓ 227        ✗ 14208 
     http_req_receiving.............: avg=84.93µs  min=0s     med=80.47µs max=4.41ms p(90)=113.12µs p(95)=127.36µs
     http_req_sending...............: avg=430.38ms min=5.32µs med=21.77µs max=9.55s  p(90)=83.96µs  p(95)=4.17s   
     http_req_tls_handshaking.......: avg=0s       min=0s     med=0s      max=0s     p(90)=0s       p(95)=0s      
     http_req_waiting...............: avg=24.92s   min=8.44ms med=23.68s  max=1m0s   p(90)=41.57s   p(95)=49.46s  
     http_reqs......................: 14435  110.617989/s
     iteration_duration.............: avg=26.4s    min=1s     med=24.69s  max=1m1s   p(90)=47.43s   p(95)=50.46s  
     iterations.....................: 14435  110.617989/s
     vus............................: 744    min=42       max=4984
     vus_max........................: 5000   min=5000     max=5000


running (2m10.5s), 0000/5000 VUs, 14435 complete and 0 interrupted iterations
default ✓ [======================================] 0000/5000 VUs  1m45s
```

Resultado de Grafana:

![CPU usage](img/test1-cpu.png)
![Network traffic](img/test1-network.png)
![Memory usage](img/test1-memory.png)
![Disk usage](img/test1-disk-usage.png)

### Test 2: User login

Archivo de configuración de K6 utilizado:

```js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '15s', target: 1000 },
    { duration: '30s', target: 2500 },
    { duration: '1m', target: 5000 },
  ],
};

export default function () {
  // Datos del usuario para el login
  const username = 'aagustin@gmail.com';
  const password = '12345678';

  // Realizar la solicitud POST para el login del usuario
  const res = http.post('http://192.168.39.203:31000/auth/login', {
    grant_type: '',
    username,
    password,
    scope: '',
    client_id: '',
    client_secret: '',
  }, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json',
    },
  });

  // Verificar si la respuesta es exitosa (código 2xx)
  check(res, {
    'status was 2xx': (r) => r.status >= 200 && r.status < 300,
  });

  // Introducir una pausa de 1 segundo entre las solicitudes
  sleep(1);
}
```

Resultado de consola de k6:

```sh
     ✗ status was 2xx
      ↳  3% — ✓ 407 / ✗ 12074

     checks.........................: 3.26%  ✓ 407       ✗ 12074 
     data_received..................: 126 kB 993 B/s
     data_sent......................: 3.5 MB 28 kB/s
     http_req_blocked...............: avg=513.73ms min=2.45µs   med=1.11ms   max=3.13s    p(90)=3.02s    p(95)=3.03s 
     http_req_connecting............: avg=513.25ms min=0s       med=949.58µs max=3.05s    p(90)=3.02s    p(95)=3.03s 
     http_req_duration..............: avg=29.51s   min=452.04ms med=31.15s   max=50.44s   p(90)=37.05s   p(95)=41.74s
       { expected_response:true }...: avg=9.24s    min=452.04ms med=7.96s    max=32.5s    p(90)=19.42s   p(95)=27.41s
     http_req_failed................: 96.73% ✓ 12074     ✗ 407   
     http_req_receiving.............: avg=4.57µs   min=0s       med=0s       max=8.86ms   p(90)=0s       p(95)=0s    
     http_req_sending...............: avg=718.89µs min=11.89µs  med=66.83µs  max=101.88ms p(90)=510.25µs p(95)=1.15ms
     http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s    
     http_req_waiting...............: avg=29.51s   min=451.86ms med=31.15s   max=50.44s   p(90)=37.05s   p(95)=41.74s
     http_reqs......................: 12481  98.263787/s
     iteration_duration.............: avg=31.22s   min=1.46s    med=33.61s   max=51.91s   p(90)=38.37s   p(95)=43.05s
     iterations.....................: 12481  98.263787/s
     vus............................: 982    min=41      max=4995
     vus_max........................: 5000   min=5000    max=5000


running (2m07.0s), 0000/5000 VUs, 12481 complete and 0 interrupted iterations
default ✓ [======================================] 0000/5000 VUs  1m45s
```

Resultado de Grafana:

![CPU usage](img/test2-cpu.png)
![Network traffic](img/test2-network.png)
![Memory usage](img/test2-memory.png)
![Disk usage](img/test2-disk-usage.png)

### Test 3: Register new users

Archivo de configuración de K6 utilizado:

```js
import http from 'k6/http';
import { check, sleep } from 'k6';

// Función para generar una cadena aleatoria de longitud dada
function generateRandomString(length) {
  const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * charset.length);
    result += charset.charAt(randomIndex);
  }
  return result;
}

export const options = {
  stages: [
    { duration: '15s', target: 1000 },
    { duration: '30s', target: 2500 },
    { duration: '1m', target: 5000 },
  ],
};

export default function () {
  // Generar datos aleatorios para cada usuario
  const email = `user${Math.floor(Math.random() * 100000)}@example.com`;
  const password = generateRandomString(8);

  // Crear el objeto de usuario
  const user = {
    email,
    password,
  };

  // Realizar la solicitud POST para registrar un nuevo usuario
  const res = http.post('http://192.168.39.203:31000/auth/register', JSON.stringify({ user }), {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  });

  // Verificar si la respuesta es exitosa (código 2xx)
  check(res, {
    'status was 2xx': (r) => r.status >= 200 && r.status < 300,
  });

  // Introducir una pausa de 1 segundo entre las solicitudes
  sleep(1);
}

```

Resultado de consola de k6:

```sh
 ✗ status was 2xx
      ↳  2% — ✓ 345 / ✗ 11276

     checks.........................: 2.96%  ✓ 345       ✗ 11276 
     data_received..................: 122 kB 952 B/s
     data_sent......................: 2.8 MB 22 kB/s
     http_req_blocked...............: avg=241.39ms min=2.51µs   med=610.72µs max=7.14s    p(90)=1.03s    p(95)=1.05s 
     http_req_connecting............: avg=241.29ms min=0s       med=532.82µs max=7.14s    p(90)=1.03s    p(95)=1.05s 
     http_req_duration..............: avg=31.44s   min=372.26ms med=31.69s   max=58.3s    p(90)=41.86s   p(95)=46.66s
       { expected_response:true }...: avg=8.98s    min=372.26ms med=6.89s    max=37.73s   p(90)=20.51s   p(95)=25.54s
     http_req_failed................: 97.03% ✓ 11276     ✗ 345   
     http_req_receiving.............: avg=2.46µs   min=0s       med=0s       max=532.61µs p(90)=0s       p(95)=0s    
     http_req_sending...............: avg=229.78µs min=10.67µs  med=59.28µs  max=11.64ms  p(90)=408.53µs p(95)=1.26ms
     http_req_tls_handshaking.......: avg=0s       min=0s       med=0s       max=0s       p(90)=0s       p(95)=0s    
     http_req_waiting...............: avg=31.44s   min=372.09ms med=31.69s   max=58.3s    p(90)=41.86s   p(95)=46.66s
     http_reqs......................: 11621  91.116311/s
     iteration_duration.............: avg=32.78s   min=1.37s    med=32.84s   max=59.53s   p(90)=43.03s   p(95)=47.82s
     iterations.....................: 11621  91.116311/s
     vus............................: 766    min=41      max=4994
     vus_max........................: 5000   min=5000    max=5000


running (2m07.5s), 0000/5000 VUs, 11621 complete and 0 interrupted iterations
default ✓ [======================================] 0000/5000 VUs  1m45s
```

Resultado de Grafana:

![CPU usage](img/test3-cpu.png)
![Network traffic](img/test3-network.png)
![Memory usage](img/test3-memory.png)
![Disk usage](img/test3-disk-usage.png)

### Test 4: Register new products

Archivo de configuración de K6 utilizado:

```js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '15s', target: 1000 },
    { duration: '30s', target: 2500 },
    { duration: '1m', target: 5000 },
  ],
};

// Tokens para dos usuarios distintos
const token1 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFhZ3VzdGlubkBnbWFpbC5jb20iLCJleHAiOjE3MDI5MjgzOTd9.VveUVEFxY8E1fT20h-yUxEj46rAzZugdpTW1XpuksYU';  // aagustinn@gmail.com
const token2 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFhZ3VzdGlubkBnbWFpbC5jb20iLCJleHAiOjE3MDI5MjgzOTd9.VveUVEFxY8E1fT20h-yUxEj46rAzZugdpTW1XpuksYU';  // aagustinn@gmail.com

export default function () {
  // Alternancia entre usuarios
  const userToken = __VU % 2 === 0 ? token1 : token2;

  // Datos aleatorios para la creación de productos
  const productCodeLength = Math.floor(Math.random() * 6) + 8; // Entre 8 y 13 caracteres
  const productCode = Math.random().toString(36).substring(2, productCodeLength + 2);
  const productName = `product_${productCode}`;
  const price = Math.floor(Math.random() * 1000);
  const amount = Math.floor(Math.random() * 100);

  // Realizar la solicitud POST para la creación de productos
  const res = http.post('http://192.168.39.203:31000/product/add', `{
    "new_product": {
      "product_code": "${productCode}",
      "name": "${productName}",
      "price": ${price},
      "amount": ${amount}
    }
  }`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${userToken}`,
    },
  });

  // Verificar si la respuesta es exitosa (código 2xx)
  check(res, {
    'status was 2xx': (r) => r.status >= 200 && r.status < 300,
  });

  // Introducir una pausa de 1 segundo entre las solicitudes
  sleep(1);
}

```

Resultado de consola de k6:

```sh
     ✗ status was 2xx
      ↳  10% — ✓ 1316 / ✗ 10795

     checks.........................: 10.86% ✓ 1316      ✗ 10795 
     data_received..................: 323 kB 2.4 kB/s
     data_sent......................: 5.6 MB 42 kB/s
     http_req_blocked...............: avg=203.4ms  min=2.42µs med=755.2µs  max=1.03s  p(90)=1.02s    p(95)=1.02s  
     http_req_connecting............: avg=203.31ms min=0s     med=638.59µs max=1.03s  p(90)=1.02s    p(95)=1.02s  
     http_req_duration..............: avg=30.57s   min=8.11ms med=30.84s   max=55.6s  p(90)=47.06s   p(95)=50.89s 
       { expected_response:true }...: avg=1.54s    min=8.11ms med=287.59ms max=27.99s p(90)=1.17s    p(95)=3.11s  
     http_req_failed................: 89.13% ✓ 10795     ✗ 1316  
     http_req_receiving.............: avg=11.27µs  min=0s     med=0s       max=5.32ms p(90)=49.44µs  p(95)=74.14µs
     http_req_sending...............: avg=105.04µs min=10.8µs med=57.93µs  max=4.71ms p(90)=206.62µs p(95)=298.7µs
     http_req_tls_handshaking.......: avg=0s       min=0s     med=0s       max=0s     p(90)=0s       p(95)=0s     
     http_req_waiting...............: avg=30.57s   min=8.02ms med=30.84s   max=55.6s  p(90)=47.06s   p(95)=50.89s 
     http_reqs......................: 12111  89.698041/s
     iteration_duration.............: avg=31.93s   min=1s     med=32.03s   max=57.1s  p(90)=48.34s   p(95)=52.15s 
     iterations.....................: 12111  89.698041/s
     vus............................: 94     min=34      max=4999
     vus_max........................: 5000   min=5000    max=5000


running (2m15.0s), 0000/5000 VUs, 12111 complete and 94 interrupted iterations
default ✓ [======================================] 0060/5000 VUs  1m45s
```

Resultado de Grafana:

![CPU usage](img/test4-cpu.png)
![Network traffic](img/test4-network.png)
![Memory usage](img/test4-memory.png)
![Disk usage](img/test4-disk-usage.png)

### Test 5: Get images

Archivo de configuración de K6 utilizado:

```js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '15s', target: 1000 },
    { duration: '30s', target: 2500 },
    { duration: '1m', target: 5000 },
  ],
};

export default function () {
  // Proporcionar una lista de IDs de las imágenes
  const imageIds = [
    '57d2adf1-8062-4908-a73f-02f4c9320d35',
    '23598a4e-2d32-4b3a-b55e-00773c8cbe46',
  ];

  // Realizar solicitudes GET para obtener imágenes
  imageIds.forEach((imageId) => {
    const res = http.get(`http://192.168.39.203:31000/image/get/?id=${imageId}`, {
      headers: {
        'Accept': 'application/json',
      },
    });

    // Verificar si la respuesta es exitosa (código 2xx)
    check(res, {
      'status was 2xx': (r) => r.status >= 200 && r.status < 300,
    });

    // Introducir una pausa de 1 segundo entre las solicitudes
    sleep(1);
  });
}

```

Resultado de consola de k6:

```sh
     ✗ status was 2xx
      ↳  0% — ✓ 46 / ✗ 12242

     checks.........................: 0.37%  ✓ 46        ✗ 12242 
     data_received..................: 2.2 MB 16 kB/s
     data_sent......................: 2.2 MB 17 kB/s
     http_req_blocked...............: avg=781.12ms min=4.71µs  med=1.15ms   max=7.24s    p(90)=3.03s    p(95)=3.06s   
     http_req_connecting............: avg=780.93ms min=0s      med=991.98µs max=7.24s    p(90)=3.03s    p(95)=3.06s   
     http_req_duration..............: avg=30.27s   min=73.76ms med=30.33s   max=1m0s     p(90)=48.87s   p(95)=54.06s  
       { expected_response:true }...: avg=419.68ms min=73.76ms med=414.18ms max=800.17ms p(90)=684.03ms p(95)=763.76ms
     http_req_failed................: 99.62% ✓ 12242     ✗ 46    
     http_req_receiving.............: avg=254.2ms  min=0s      med=0s       max=30.77s   p(90)=0s       p(95)=0s      
     http_req_sending...............: avg=74.72ms  min=11.36µs med=97.25µs  max=26.8s    p(90)=704.63µs p(95)=1.56ms  
     http_req_tls_handshaking.......: avg=0s       min=0s      med=0s       max=0s       p(90)=0s       p(95)=0s      
     http_req_waiting...............: avg=29.95s   min=6.22ms  med=30.33s   max=1m0s     p(90)=48.55s   p(95)=53.75s  
     http_reqs......................: 12288  90.987543/s
     iteration_duration.............: avg=1m4s     min=26.73s  med=1m7s     max=1m35s    p(90)=1m28s    p(95)=1m30s   
     iterations.....................: 5423   40.155065/s
     vus............................: 1442   min=42      max=4999
     vus_max........................: 5000   min=5000    max=5000


running (2m15.1s), 0000/5000 VUs, 5423 complete and 1442 interrupted iterations
default ✓ [======================================] 1432/5000 VUs  1m45s
```

Resultado de Grafana:

![CPU usage](img/test5-cpu.png)
![Network traffic](img/test5-network.png)
![Memory usage](img/test5-memory.png)
![Disk usage](img/test5-disk-usage.png)

## Conclusiones de las pruebas realizadas

En términos generales, hemos logrado cumplir con los requisitos establecidos por la empresa, confirmando que la plataforma es capaz de soportar hasta 5000 usuarios en su página de inicio, aunque esta evaluación consideró un número limitado de productos al inicio de la prueba. No obstante, las pruebas adicionales revelaron limitaciones notables, principalmente relacionadas con la capacidad del disco tanto en términos de la cantidad de productos y usuarios que podemos agregar como en su rendimiento de lectura/escritura, siendo este un factor determinante en las operaciones que involucran la base de datos.

En todas las instancias en las que la base de datos estuvo involucrada, como la creación de nuevos productos y usuarios, el rendimiento del disco se destacó como el factor crítico. Observamos que las pruebas centradas en usuarios afectaron más al CPU, especialmente cuando la API tuvo que encriptar o desencriptar contraseñas. A lo largo de todas las pruebas, la memoria mostró una estabilidad notable, mientras que la red experimentó una mayor actividad durante las transmisiones y recepciones de información en las solicitudes a la API.

Como conclusión, consideramos que el sistema es fiable para el uso actual de la empresa. Sin embargo, en caso de requerir una mayor creación de usuarios o un mayor número de solicitudes, se sugiere la implementación de un Ingress Controller y un balanceador de carga, junto con el escalado de los Deployments de la UI, la API y la DB. En particular, para la base de datos, se recomienda configurarla como un ReplicaSet para optimizar su rendimiento.

## Referencias

- [The Best Performance And Load Testing Tool? k6 By Grafana Labs](https://www.youtube.com/watch?v=5OgQuVAR14I)
- [K6 - Installation](https://k6.io/docs/get-started/installation/)
- [K6 - Create Custom Metrics](https://k6.io/docs/using-k6/metrics/create-custom-metrics/)
