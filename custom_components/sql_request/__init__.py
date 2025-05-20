
import sqlite3
import logging
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

DB_PATH = None 

def setup(hass, config):
    """Function call by Home Assistant to set up the component."""

    global DB_PATH 
    DB_PATH = config["sql_request"].get("db", hass.config.path("home-assistant_v2.db"))
   
    register_services(hass)
    return True


def execute_sql(query, params=()):
    """Executes an SQL query."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        _LOGGER.error(f"SQL Error: {e}")
        return str(e)

def register_services(hass: HomeAssistant):
    """Registers all intégration services."""

    _LOGGER.info("Registering SQL Request services...")

    def sql_insert(call: ServiceCall):
        """Executes a SQL INSERT statement."""

        table = call.data.get("table")
        values = call.data.get("values")
        if not table or not values:
            _LOGGER.error("Missing required parameters: 'table' or 'values'")
            return
        columns = ", ".join(values.keys())
        placeholders = ", ".join(["?" for _ in values])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        _LOGGER.info(f"Executing SQL INSERT: {query}")
        execute_sql(query, tuple(values.values()))
    
    def sql_insert_or_replace(call: ServiceCall):
        """Executes a SQL INSERT OR REPLACE statement."""

        table = call.data.get("table")
        values = call.data.get("values")
        if not table or not values:
            _LOGGER.error("Missing required parameters: 'table' or 'values'")
            return
        columns = ", ".join(values.keys())
        placeholders = ", ".join(["?" for _ in values])
        query = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        _LOGGER.info(f"Executing SQL INSERT OR REPLACE: {query}")
        execute_sql(query, tuple(values.values()))

    def sql_update(call: ServiceCall):
        """Executes a SQL UPDATE statement."""

        table = call.data.get("table")
        values = call.data.get("values")
        where_clause = call.data.get("where")
        if not table or not values or not where_clause:
            _LOGGER.error("Missing required parameters: 'table', 'values', or 'where'")
            return
        set_clause = ", ".join([f"{key} = ?" for key in values.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        _LOGGER.info(f"Executing SQL UPDATE: {query}")
        execute_sql(query, tuple(values.values()))

    def sql_delete(call: ServiceCall):
        """Executes a SQL DELETE statement."""

        table = call.data.get("table")
        where_clause = call.data.get("where")
        if not table or not where_clause:
            _LOGGER.error("Missing required parameters: 'table' or 'where'")
            return
        query = f"DELETE FROM {table} WHERE {where_clause}"
        _LOGGER.info(f"Executing SQL DELETE: {query}")
        execute_sql(query)


    hass.services.register("sql_request", "insert", sql_insert)
    hass.services.register("sql_request", "update", sql_update)
    hass.services.register("sql_request", "delete", sql_delete)
    hass.services.register("sql_request", "insert_or_replace", sql_insert_or_replace)
    _LOGGER.info("SQL Request services registered successfully!")
    _LOGGER.info(f"Using database path: {DB_PATH}")