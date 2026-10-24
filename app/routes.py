from flask import Blueprint, render_template, request

from app.services import WeatherServiceError, get_weather


main = Blueprint("main", __name__)


@main.get("/")
def index():
    """Muestra el formulario de búsqueda."""
    return render_template(
        "index.html",
        country="",
        department="",
        city="",
        weather=None,
        error=None,
    )


@main.route("/weather", methods=["GET", "POST"])
def weather():
    """Busca el clima para una ubicación enviada por formulario o query string."""
    country = request.values.get("country", "").strip()
    department = request.values.get("department", "").strip()
    city = request.values.get("city", "").strip()
    if not country or not department or not city:
        return render_template(
            "index.html",
            country=country,
            department=department,
            city=city,
            weather=None,
            error="Completa el país, el departamento y la ciudad.",
        ), 400

    try:
        result = get_weather(country, department, city)
    except ValueError as exc:
        return render_template(
            "index.html",
            country=country,
            department=department,
            city=city,
            weather=None,
            error=str(exc),
        ), 400
    except WeatherServiceError as exc:
        return render_template(
            "index.html",
            country=country,
            department=department,
            city=city,
            weather=None,
            error=str(exc),
        ), exc.status_code

    return render_template(
        "index.html",
        country=country,
        department=department,
        city=city,
        weather=result,
        error=None,
    )