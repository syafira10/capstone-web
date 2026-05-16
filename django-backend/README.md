# Flood Monitoring System - Django Backend

Professional Django REST Framework backend for real-time flood monitoring with MQTT IoT integration.

## Features

- **Real-time MQTT Integration**: Subscribe to IoT sensors (rain, water level) via MQTT broker
- **REST API**: Complete RESTful API for sensor data, alerts, and system settings
- **WebSocket Support**: Real-time data broadcasting to connected clients via Django Channels
- **Alert System**: Automatic threshold-based alert generation
- **SQLite/PostgreSQL**: Flexible database support
- **CORS Enabled**: Ready for frontend integration

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```
MQTT_BROKER_HOST=broker.emqx.io
MQTT_BROKER_PORT=1883
WATER_LEVEL_THRESHOLD_WARNING=60
WATER_LEVEL_THRESHOLD_CRITICAL=70
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (Optional, for admin access)

```bash
python manage.py createsuperuser
```

## Running the Server

### Using Development Server (SQLite)

```bash
python manage.py runserver
```

Server runs on `http://localhost:8000`

### Using Daphne (for WebSocket support)

```bash
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

## API Endpoints

### Sensor Data

- `GET /api/monitoring/realtime/` - Get latest value for each topic
- `GET /api/monitoring/historical/` - Get historical data with filters
- `GET /api/monitoring/latest/` - Get latest data for all topics
- `GET /api/monitoring/data/` - List all sensor records

### Alerts

- `GET /api/monitoring/alerts/` - List all alerts
- `GET /api/monitoring/alerts/active/` - Get active (unacknowledged) alerts
- `POST /api/monitoring/alerts/{id}/acknowledge/` - Acknowledge an alert

### System Settings

- `GET /api/monitoring/settings/thresholds/` - Get alert thresholds
- `PUT /api/monitoring/settings/{key}/` - Update setting

## WebSocket Connection

Connect to real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/monitoring/');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Update:', data);
};
```

## MQTT Configuration

The system subscribes to three MQTT topics:

- **RAINSENSOR** - Rain intensity (mm/h)
- **WATERLEVELSENSORKAI** - Water level at KAI station (cm)
- **WATERLEVELSENSORKRL** - Water level at KRL station (cm)

Broker: `broker.emqx.io:1883`

### Alert Thresholds

- Water Level Warning: 60 cm
- Water Level Critical: 70 cm
- Rain Intensity Warning: 50 mm/h

## Admin Interface

Access Django admin at `http://localhost:8000/admin/`

- Manage sensor data
- View and acknowledge alerts
- Configure system settings

## Database Models

### SensorData
- `topic` - MQTT topic name
- `value` - Sensor reading
- `location` - Sensor location
- `timestamp` - Message timestamp
- `created_at` - Record creation time

### Alert
- `title` - Alert title
- `message` - Alert message
- `severity` - 'info', 'warning', or 'critical'
- `location` - Alert location
- `timestamp` - Alert timestamp
- `acknowledged` - Boolean flag

### SystemSetting
- `key` - Setting key
- `value` - Setting value
- `description` - Setting description
- `updated_at` - Last update time

## Deployment

### PostgreSQL Setup

```bash
# Edit .env
DATABASE_URL=postgresql://user:password@localhost:5432/capstone

pip install psycopg2-binary
python manage.py migrate
```

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use Daphne or Gunicorn for ASGI
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure CORS for production domains
- [ ] Use Redis for Channels (instead of in-memory)

## Troubleshooting

### MQTT not connecting

Check MQTT broker availability:
```bash
pip install paho-mqtt
python -c "import paho.mqtt.client as mqtt; client = mqtt.Client(); client.connect('broker.emqx.io', 1883, 60); client.loop_start(); import time; time.sleep(2)"
```

### WebSocket connection issues

Ensure Daphne is running (not just `runserver`):
```bash
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

### Database locked error

Delete `db.sqlite3` if using SQLite:
```bash
rm db.sqlite3
python manage.py migrate
```

## Development

### Run Tests

```bash
python manage.py test
```

### Check Code Quality

```bash
pip install flake8
flake8 apps/ config/
```

## License

Proprietary - Flood Monitoring System
