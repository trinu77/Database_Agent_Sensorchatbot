import csv
import mysql.connector
from datetime import datetime

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="trina",
    database="sensor_db",
    auth_plugin='mysql_native_password',
    allow_local_infile=True
)
cursor = conn.cursor()

with open("C:/projects/db_sensor/sensor.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Clean timestamp
        ts = row["timestamp"].strip()

        # Try to fix formats
        try:
            if "-" in ts and ts.count("-") == 2 and ts.index("-") == 2:
                # Format: DD-MM-YYYY HH:MM
                ts = datetime.strptime(ts, "%d-%m-%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
            elif ts.endswith("-"):
                # Extra dash at the end
                ts = ts[:-1]
                ts = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            else:
                # Already in correct format
                ts = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"⚠️ Skipping bad timestamp: {ts}")
            continue

        try:
            cursor.execute("""
                INSERT INTO sensors (timestamp, temperature_one, temperature_two, vibration_x, vibration_y, vibration_z)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                ts,
                row["temperature_one"] or None,
                row["temperature_two"] or None,
                row["vibration_x"] or None,
                row["vibration_y"] or None,
                row["vibration_z"] or None
            ))
        except mysql.connector.Error as err:
            print(f"❌ MySQL error: {err}")

conn.commit()
cursor.close()
conn.close()
print("✅ CSV data imported successfully!")
