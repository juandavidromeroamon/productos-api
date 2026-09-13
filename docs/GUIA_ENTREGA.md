# Guía de entrega paso a paso

## 1. Subir a GitHub

```bash
cd productos-api

git init
git add .
git commit -m "Backend de productos en Python con FastAPI y arquitectura por capas"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/productos-api.git
git push -u origin main
```

Antes del `push` hay que crear el repositorio vacío en github.com (sin README, sin .gitignore,
porque el proyecto ya los trae).

## 2. Desplegar en Render

1. Entra a render.com y conecta tu cuenta de GitHub.
2. **New → Web Service** y selecciona el repositorio `productos-api`.
3. Configuración:
   - Runtime: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: **Free**
4. **Create Web Service** y espera a que el log muestre `Application startup complete`.
5. Copia la URL que aparece arriba, del estilo `https://productos-api-xxxx.onrender.com`.

Verificación inmediata: abre `https://TU-URL.onrender.com/docs` en el navegador. Si carga
Swagger UI con los endpoints, el despliegue quedó bien.

### Alternativa: Railway

1. railway.app → **New Project → Deploy from GitHub repo**.
2. Railway detecta el `Procfile` solo.
3. **Settings → Networking → Generate Domain** para obtener la URL pública.

## 3. Capturar la evidencia

Para la entrega conviene reunir:

- [ ] URL del repositorio de GitHub
- [ ] URL pública de la API desplegada
- [ ] Captura de `/docs` (Swagger) con todos los endpoints visibles
- [ ] Captura de Postman con la colección importada y al menos las 6 operaciones respondiendo
- [ ] Captura del dashboard de Render/Railway con el servicio activo
- [ ] APK de la app móvil consumiendo la URL pública (evidencia adicional)

Para las capturas de Postman: importa `docs/postman_collection.json`, edita la variable
`base_url` de la colección y reemplaza `http://127.0.0.1:8000` por la URL de producción. Así una
sola ejecución sirve de evidencia para todos los casos.

## 4. Texto sugerido para la entrega

> **Repositorio backend:** https://github.com/TU_USUARIO/productos-api
> **API desplegada:** https://TU-SERVICIO.onrender.com
> **Documentación interactiva:** https://TU-SERVICIO.onrender.com/docs
>
> El backend está construido en Python con FastAPI, aplicando programación orientada a objetos
> y una arquitectura por capas basada en Clean Architecture (dominio, aplicación,
> infraestructura y presentación). Las seis operaciones solicitadas se implementaron como casos
> de uso independientes, expuestos mediante endpoints REST. Se adjunta la colección de Postman
> con las pruebas funcionales y el APK de la aplicación móvil que consume el servicio.

## 5. Repositorio de la app móvil

Cuando construyas la app, súbela como un segundo repositorio (`productos-app-movil`) y entrega
las dos URLs. En su README menciona la URL de la API que consume, para que quede clara la
relación entre ambos proyectos.
