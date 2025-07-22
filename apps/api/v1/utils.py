import logging


def log_api_info(request, view_name, action=None):
    # Optional: can be continued by writing a custom middleware.
    # todo: add request body
    logger = logging.getLogger("api_info")
    logger.info(
        f"API called: {view_name}{'.' + action if action else ''}",
        extra={
            "user_id": getattr(request.user, "id", None),
            "method": request.method,
            "path": request.path,
            "ip": request.META.get("REMOTE_ADDR"),
        },
    )
