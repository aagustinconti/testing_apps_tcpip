import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  http.get('https://aagustinconti.github.io/testing_apps_tcpip/');
  sleep(1);
}