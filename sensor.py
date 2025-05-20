import sqlite3
import logging
import json
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DB_PATH = "/config/home-assistant_v2.db"

def check_sql_exist(table, columns="*", where=None):
    """Check if a record exists in the database and return it as JSON if exist or unknown otherwise."""
    
    query = f"SELECT {columns} FROM {table}"
    if where:
        query += f" WHERE {where}"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            # Récupère les noms de colonnes
            col_names = [desc[0] for desc in cursor.description]
            row_dict = dict(zip(col_names, result))
            conn.close()
            return json.dumps(row_dict)
        else:
            conn.close()
            return "unknown"
    except sqlite3.Error as e:
        _LOGGER.error(f"SQL Error: {e}")
        return "unknown"

def setup_platform(hass, config, add_entities, discovery_info=None):
    table = config.get("table")
    columns = config.get("columns", "*")
    where = config.get("where")
    name = config.get("name", f"SQL Exist {table}")

    sensor = SqlExistSensor(name, table, columns, where)
    add_entities([sensor])

    # Register the service to update the sensor
    def handle_update_sensor(call):
        table = call.data.get("table", sensor._table)
        columns = call.data.get("columns", sensor._columns)
        where = call.data.get("where", sensor._where)
        sensor.set_query(table, columns, where)
        sensor.schedule_update_ha_state(True)

    hass.services.register(
        "sql_request",
        "update_sql_exist_sensor",
        handle_update_sensor
    )

class SqlExistSensor(Entity):
    def __init__(self, name, table, columns, where):
        self._name = name
        self._table = table
        self._columns = columns
        self._where = where
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def set_query(self, table, columns, where):
        self._table = table
        self._columns = columns
        self._where = where

    def update(self):
        self._state = check_sql_exist(self._table, self._columns, self._where)
