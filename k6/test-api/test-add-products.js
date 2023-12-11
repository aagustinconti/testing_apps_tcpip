import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '2m', target: 100 },
    { duration: '1m', target: 1000 },
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
