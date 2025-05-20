# SQL Request Custom Component

This Home Assistant custom component allows you to perform SQL operations (INSERT, UPDATE, DELETE, INSERT OR REPLACE) on your SQLite database via Home Assistant services. It also provides a sensor to check for the existence of records.

## Installation

### Manual

1. Copy the `sql_request` folder to your `custom_components` directory.
2. Restart Home Assistant.

### With HACS

1. In HACS, go to **Integrations**.
2. Click the three dots menu (upper right) and select **Custom repositories**.
3. Add your repository URL and select **Integration** as the category.
4. Search for `sql_request` in HACS and install.
5. Restart Home Assistant.

## Configuration

Add the following to your `configuration.yaml`:

```yaml
sql_request:
  db: /config/home-assistant_v2.db  # Optional: path to your SQLite database
```

## Services

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
    db: "/config/home-assistant_v2.db"  # Optional
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
