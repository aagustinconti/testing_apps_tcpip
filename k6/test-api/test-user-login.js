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
  const username = 'user1@example.com';
  const password = 'soyuser1';

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
