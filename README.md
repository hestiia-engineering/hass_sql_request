# SQL Request Custom Component

This Home Assistant custom component allows you to perform SQL operations (INSERT, UPDATE, DELETE, INSERT OR REPLACE) on your SQLite database via Home Assistant services. It also provides a sensor to check for the existence of records.

## Installation

### Manual Installation

1. Download the latest release file: `sql_request.zip` from the [releases page](https://github.com/hestiia-engineering/sql_request/releases).
2. Unzip the contents into your `custom_components` directory in your Home Assistant configuration folder.
   - The resulting path should be: `custom_components/sql_request/`
3. Restart Home Assistant.

### HACS Installation

1. In HACS, go to "Integrations" and click the three dots in the top right, then "Custom repositories".
2. Add this repository URL: `https://github.com/hestiia-engineering/sql_request` and select "Integration" as the category.
3. Install the integration from the HACS UI.
4. Restart Home Assistant.

> **Note:**  
> If you do not add this repository as a custom repository in HACS, the integration will not be available for installation via HACS.

## Configuration

Add the following to your `configuration.yaml`:

```yaml
sql_request:
  db_url: /config/home-assistant_v2.db  # Optional: path to your SQLite database
```

## Services

### `set_db_path`

Dynamically update the database path used by the integration **for services only** (insert, update, delete, insert_or_replace) without restarting Home Assistant.

> **Note:**  
> This service does **not** affect the database used by the sensor platform.  
> To change the database for a sensor, you must update the `db_url` in your sensor configuration and restart Home Assistant.

**YAML Example:**
```yaml
service: sql_request.set_db_path
data:
  db_path: /config/another_database.db
```

**Fields:**
- `db_path` (string): The new path to your SQLite database.

### `insert`

Insert data into a table.

**YAML Example:**
```yaml
service: sql_request.insert
data:
  table: operating_power
  values:
    power_target: 100
    setpoint_temperature: 22
```

**Fields:**
- `table` (string): Name of the table.
- `values` (dict): Values to insert. Example: `{'power_target': 100, 'setpoint_temperature': 22}`

### `update`

Update data in a table.

**YAML Example:**
```yaml
service: sql_request.update
data:
  table: operating_power
  values:
    setpoint_temperature: 24
  where: power_target = 100
```

**Fields:**
- `table` (string): Name of the table.
- `values` (dict): Values to update. Example: `{'setpoint_temperature': 24}`
- `where` (string): WHERE condition. Example: `power_target = 100`

### `delete`

Delete data from a table.

**YAML Example:**
```yaml
service: sql_request.delete
data:
  table: operating_power
  where: power_target = 100
```

**Fields:**
- `table` (string): Name of the table.
- `where` (string): WHERE condition. Example: `power_target = 100`

### `insert_or_replace`

Insert or replace data in a table.

**YAML Example:**
```yaml
service: sql_request.insert_or_replace
data:
  table: operating_power
  values:
    power_target: 100
    setpoint_temperature: 22
```

**Fields:**
- `table` (string): Name of the table.
- `values` (dict): Values to insert or replace. Example: `{'power_target': 100, 'setpoint_temperature': 22}`

## Sensor Platform

You can create a sensor to check for the existence of a record by adding the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: sql_request
    name: "Check Power Target"
    table: "operating_power"
    columns: "power_target, setpoint_temperature"
    where: "power_target = 100"
    db_url: "/config/home-assistant_v2.db"  # Optional
    scan_interval: 60  # Optional, in seconds
```

The sensor state will be a JSON string of the first matching row, or `"unknown"` if no match.

### Service: `update_sql_request_sensor`

Update the sensor with new query parameters.

**YAML Example:**
```yaml
service: sql_request.update_sql_request_sensor
data:
  table: operating_power
  columns: power_target, setpoint_temperature
  where: power_target = 100
```

**Fields:**
- `table` (string, optional)
- `columns` (string, optional)
- `where` (string, optional)

## Notes

- Use with caution: direct SQL access can modify your Home Assistant database.
- Always back up your database before using write operations.
- **It is recommended to alter only a different database than the main Home Assistant database, or at least to create and use a new table for your custom data. Modifying existing Home Assistant tables may cause data corruption or unexpected behavior.**

---

**Disclaimer:**  
This custom component is provided as-is. If you encounter any problems or data loss, the author is not responsible. Use at your own risk.
