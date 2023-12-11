import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },
    //{ duration: '2m', target: 100 },
    //{ duration: '1m', target: 1000 },
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
