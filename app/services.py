import requests
from flask import current_app


class WeatherServiceError(Exception):
    """Error controlado al consultar el servicio del clima."""

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


def get_weather(
    country: str, department: str, city: str
) -> dict[str, str | float | int]:
    """Geocodifica país, departamento y ciudad antes de consultar el clima."""
    country = country.strip()
    department = department.strip()
    city = city.strip()
    if not country or not department or not city:
        raise ValueError("Completa el país, el departamento y la ciudad.")

    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    if not api_key:
        raise WeatherServiceError(
            "Falta configurar OPENWEATHER_API_KEY en el archivo .env.",
            status_code=503,
        )

    try:
        location_response = requests.get(
            "https://api.openweathermap.org/geo/1.0/direct",
            params={
                "q": f"{city},{department},{country}",
                "limit": 1,
                "appid": api_key,
            },
            timeout=10,
        )
        location_response.raise_for_status()
    except requests.RequestException as exc:
        if getattr(exc.response, "status_code", None) == 401:
            raise WeatherServiceError(
                "La API Key no es válida o aún no está activa."
            ) from exc
        raise WeatherServiceError(
            "No se pudo conectar con el servicio de ubicación. Inténtalo de nuevo."
        ) from exc

    try:
        locations = location_response.json()
    except ValueError as exc:
        raise WeatherServiceError(
            "El servicio de ubicación devolvió una respuesta inesperada."
        ) from exc

    if not isinstance(locations, list):
        raise WeatherServiceError(
            "El servicio de ubicación devolvió una respuesta inesperada."
        )
    if not locations:
        raise WeatherServiceError(
            f"No se encontró {city}, {department}, {country}.", status_code=404
        )

    location = locations[0]
    try:
        latitude = location["lat"]
        longitude = location["lon"]
        if not isinstance(latitude, (int, float)) or not isinstance(
            longitude, (int, float)
        ):
            raise TypeError("Las coordenadas no son numéricas.")
    except (KeyError, TypeError) as exc:
        raise WeatherServiceError(
            "El servicio de ubicación devolvió una respuesta inesperada."
        ) from exc

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": latitude,
                "lon": longitude,
                "appid": api_key,
                "units": "metric",
                "lang": "es",
            },
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        status_code = getattr(exc.response, "status_code", None)
        if status_code == 401:
            raise WeatherServiceError(
                "La API Key no es válida o aún no está activa."
            ) from exc
        if status_code == 404:
            raise WeatherServiceError(
                f"No se encontró el clima para {city}.", status_code=404
            ) from exc
        raise WeatherServiceError(
            "No se pudo conectar con el servicio del clima. Inténtalo de nuevo."
        ) from exc

    try:
        data = response.json()
        current = data["main"]
        description = data["weather"][0]["description"]
        return {
            "city": data["name"],
            "department": location.get("state", department),
            "country": location.get("country", country),
            "temperature": current["temp"],
            "description": description,
            "humidity": current["humidity"],
        }
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise WeatherServiceError(
            "El servicio del clima devolvió una respuesta inesperada."
        ) from exc