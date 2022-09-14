from datetime import datetime

from fastapi.openapi.utils import get_openapi


def convert_datetime(dt: datetime):
    """
    Приводит дату к формату ISO 8601
    """
    format_timedata = (dt.isoformat() + 'Z')
    return format_timedata


def change_doc_metadata(app):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="YaDisk API",
            version="1.0",
            description="Вступительное задание в осеннюю ШБР Яндекса 2022",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
