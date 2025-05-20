
def setup(hass, config):
    from .sql_request import register_services
    register_services(hass)
    return True