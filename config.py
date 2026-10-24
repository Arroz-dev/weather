import os
from pathlib import Path

from dotenv import load_dotenv


# Carga el .env del proyecto sin reemplazar variables ya definidas en el sistema.
load_dotenv(Path(__file__).resolve().parent / ".env")


class Config:
    """Configuración de WeatherPulse."""

    # OPENWEATHER_API_KEY es el nombre recomendado; ApiKey mantiene compatibilidad.
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") or os.getenv("ApiKey")
    DEBUG = os.getenv("DEBUG", "false").strip().lower() in {"1", "true", "yes", "on"}