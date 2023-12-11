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
    { duration: '1m', target: 50 },
    { duration: '2m', target: 100 },
    { duration: '1m', target: 0 },
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
