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