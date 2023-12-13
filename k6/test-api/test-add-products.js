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
const token1 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIxQGV4YW1wbGUuY29tIiwiZXhwIjoxNzAzMDM4MDg1fQ.3me0mtW3kqdf8lHOd8iRk_XKQZ9yRFY-EP7klH6llM4';  // aagustinn@gmail.com
const token2 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzAzMDM4NTgxfQ.fCpxXllcC6E13j2nWZMXBbfxDNXQSHVgbLXXOrje2_I';  // aagustinn@gmail.com

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
