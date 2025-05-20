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

### `sql_request.insert`

Insert data into a table.

**Fields:**
- `table` (string): Name of the table.
- `values` (dict): Values to insert. Example: `{'power_target': 100, 'setpoint_temperature': 22}`

### `sql_request.update`

Update data in a table.

**Fields:**
- `table` (string): Name of the table.
- `values` (dict): Values to update. Example: `{'setpoint_temperature': 24}`
- `where` (string): WHERE condition. Example: `power_target = 100`

### `sql_request.delete`

Delete data from a table.

**Fields:**
- `table` (string): Name of the table.
- `where` (string): WHERE condition. Example: `power_target = 100`

### `sql_request.insert_or_replace`

Insert or replace data in a table.

**Fields:**
- `table` (string): Name of the table.
- `values` (dict): Values to insert or replace. Example: `{'power_target': 100, 'setpoint_temperature': 22}`

## Sensor Platform

You can create a sensor to check for the existence of a record:

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

## Service: `sql_request.update_sql_request_sensor`

Update the SQL request sensor with new query parameters.

**Fields:**
- `table` (string, optional)
- `columns` (string, optional)
- `where` (string, optional)

## Notes

- Use with caution: direct SQL access can modify your Home Assistant database.
- Always back up your database before using write operations.
