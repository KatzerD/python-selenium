# Twitter Scraper

Este script utiliza Selenium para extraer tweets recientes de una cuenta de Twitter.

## Instalación
1. Clonar el repositorio.
2. Crear un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En macOS/Linux
    .\venv\Scripts\activate  # En Windows
    ```
3. Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Crear un archivo `.env` con tus credenciales de Twitter:
    ```bash
    TWITTER_USERNAME=tu_usuario
    TWITTER_PASSWORD=tu_contraseña
    PHONE_NUMBER=tu_telefono
    ```

5. Ejecutar el script:
    ```bash
    python scraper.py
    ```

## Notas:
Si encuentras un captcha, será necesario resolverlo manualmente en esta versión del script.
