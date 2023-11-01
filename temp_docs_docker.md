# Docker how to

Para ejecutar el docker correctamente se deben usar los siguientes commandos:

```bash
# Iniciar los contenedores
docker compose up -d --build

# Parar los contenedores
docker compose down
```

El `--build` forzara a buildear la imagen correspondiente a la Dockerfile.