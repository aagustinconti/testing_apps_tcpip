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
    "0bce1d8a-fd10-42ee-be89-22da799116f2",
    "ca26241a-fda5-46fe-a117-3f66072b3fb8",
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
