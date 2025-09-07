from client.backend_client import ApiClientError, fetch_listings

from .session import set_error_message, set_last_items


def fetch_and_store_listings(params):
    items = []
    error_message = None
    try:
        items = fetch_listings(params)
        set_error_message(None)
    except ApiClientError as e:
        if hasattr(e, "status_code") and e.status_code == 404:
            error_message = "No listings found for the selected filters (404)."
        elif hasattr(e, "status_code") and e.status_code == 500:
            error_message = "Server error (500). Please try again later."
        else:
            error_message = e.user_message if hasattr(e, "user_message") else str(e)
        set_error_message(error_message)
    except Exception as ex:
        if "Connection refused" in str(ex) or "Failed to establish a new connection" in str(ex):
            error_message = "Unable to connect to backend service. Please ensure the backend server is running and reachable."
        else:
            error_message = f"Unexpected error: {ex}"
        set_error_message(error_message)
    set_last_items(items)
    from .session import set_filters_applied

    set_filters_applied(False)
    return items, error_message
