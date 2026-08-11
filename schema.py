DATABASE_SCHEMA = """
Database: smart_grid

Table: power_measurements

Columns:
- id: unique record ID
- timestamp: date and time of measurement
- transformer_id: transformer identifier
- feeder_id: feeder identifier
- voltage: measured voltage
- current: measured current
- power: measured power
- energy_consumption: energy consumption
"""

