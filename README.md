# Guía de Ejecución

El proyecto se divide en dos frentes:

- `plant`: página principal con el visor 3D y los formularios.
- `webPage`: proyecto Gulp/BrowserSync utilizado para compilar los recursos del tema y servir los archivos en desarrollo.

Toda la ejecución se resuelve con Docker, así que no necesitas instalar Node ni Gulp en tu máquina.

## Requisitos

- Docker Desktop 4.0+ (o Docker Engine reciente).
- Docker Compose v2 (incluido en Docker Desktop).

## Arranque rápido

1. Desde la raíz del repositorio ejecuta:

   ```bash
   docker compose up --build
   ```

   Este comando construye la imagen, instala dependencias y deja corriendo BrowserSync.

2. Cuando el contenedor muestre “Browsersync Access URLs” abre en tu navegador:

   - http://localhost:3000/ (listado de la carpeta plant)
   - http://localhost:3000/index.html (landing principal de plant)
   - http://localhost:3000/views/index_original.html (visor 3D y formularios)
   - http://localhost:3000/theme/index.html (salida generada del tema Themefisher)
   - http://localhost:3001 (panel de control de BrowserSync)

## Desarrollo diario

- Mantén `docker compose up` abierto mientras editas archivos. BrowserSync vigila `webPage/source` y `plant` para refrescar automáticamente.
- Para detener el entorno: `docker compose down`.
- Si necesitas reinstalar dependencias o limpiar caches usa:

   ```bash
   docker compose down --volumes
   docker compose up --build
   ```

## Uso del endpoint /predict

El archivo [plant/src/js/ia.js](plant/src/js/ia.js) envía peticiones POST a `http://localhost:5000/predict`.

- Levanta tu servicio de predicción en ese puerto o ajusta la URL en el código.
- Si el backend corre en otro contenedor, expón el puerto 5000 y usa la ruta `http://NOMBRE_SERVICIO:5000/predict`.
- Si el servicio no responde, el navegador mostrará errores de red y la simulación no devolverá resultados.

## Build de producción

Para generar los assets estáticos dentro del contenedor ejecuta:

```bash
docker compose run --rm web npm run build
```

El resultado queda en la carpeta `webPage/theme`.
