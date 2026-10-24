# WeatherPulse

Aplicación web modular con Flask que consulta las condiciones actuales de una
ciudad usando la API de OpenWeatherMap. Para afinar la búsqueda se indican
país, departamento o región y ciudad; primero se obtienen sus coordenadas y
después se consulta el clima.

## Configuración

1. Crea y activa un entorno virtual.
2. Instala las dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

3. En `.env`, configura tu clave sin subir ese archivo a Git:

   ```dotenv
   OPENWEATHER_API_KEY=tu_api_key
   DEBUG=false
   ```

   La aplicación también acepta `ApiKey` por compatibilidad con una configuración
   existente. `DEBUG` está desactivado por defecto.

## Ejecutar

```powershell
python run.py
```

Abre la dirección local que Flask muestra en la terminal. El formulario envía
país, departamento y ciudad por `POST` a `/weather`. También puedes consultar,
por ejemplo, `/weather?country=Colombia&department=Antioquia&city=Medellin`.
