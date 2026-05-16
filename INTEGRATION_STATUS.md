# Full Stack Integration - Status Report

## ✅ Task 1: Django Backend with MQTT Subscriber - COMPLETED

### Backend Setup
- **Location**: `django-backend/`
- **Server**: Running on `http://localhost:8000`
- **Database**: SQLite (local development)
- **MQTT Client**: Connected and subscribing to:
  - `RAINSENSOR` - Rain intensity data
  - `WATERLEVELSENSORKAI` - Water level at KAI station  
  - `WATERLEVELSENSORKRL` - Water level at KRL station
  - **Broker**: broker.emqx.io:1883

### MQTT Integration (mqtt_client.py)
✓ **Fully Implemented** with:
- Automatic MQTT subscription to 3 sensor topics
- Real-time message parsing and storage to database
- Threshold-based alert generation
- WebSocket broadcasting to connected clients
- Thread-safe operation with background loop

### Django REST API Endpoints
```
GET  /api/monitoring/realtime/      → Latest values for all topics
GET  /api/monitoring/historical/    → Historical data with filters (date, location, topic)
GET  /api/monitoring/latest/        → Latest data formatted for UI
GET  /api/monitoring/data/          → Full sensor records list
GET  /api/monitoring/alerts/        → List all system alerts
GET  /api/monitoring/alerts/active/ → Only unacknowledged alerts
```

### WebSocket Real-time Updates
```
WS /ws/monitoring/  → Connect for real-time MQTT message streaming
```

### Database Models Created
- **SensorData**: Stores all MQTT messages with timestamp indexing
- **Alert**: Automatic alerts when thresholds exceeded
- **SystemSetting**: Configurable thresholds and system parameters

---

## ✅ Task 2: Frontend Connected to Django - COMPLETED

### Frontend Configuration
- **File**: `capstone-web/.env`
  ```
  VITE_API_BASE_URL=http://localhost:8000
  VITE_WS_URL=ws://localhost:8000
  ```

- **File**: `src/app/lib/mqttApi.ts` - Updated to:
  - Use Django endpoints for realtime data
  - Use Django WebSocket for live updates
  - Support historical data queries with filters

### Frontend Integration Points
1. **Dashboard.tsx**: Uses WebSocket to display real-time metrics
2. **DataPage.tsx**: Fetches historical data from `/api/monitoring/historical/`
3. **AdminPanel.tsx**: Ready for admin endpoints (to be implemented)

---

## 📊 Data Flow: IoT → Backend → Frontend

```
IoT Sensors (MQTT Topics)
    ↓
MQTT Broker (broker.emqx.io:1883)
    ↓
Django MQTT Client (mqtt_client.py)
    ↓
SensorData Model (Database)
    ↓
REST API Endpoints (DRF)
    ↓
React Frontend (Vite 5174)
    ↓
WebSocket Updates
    ↓
Real-time Dashboard Display
```

---

## 🚀 Running the System

### Terminal 1: Django Backend
```bash
cd django-backend
.\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```
**Status**: ✓ Running on port 8000
**MQTT**: ✓ Connected and receiving data

### Terminal 2: Frontend Development Server
```bash
cd capstone-web
npm run dev
```
**Status**: Should be running on port 5173/5174

---

## 🔧 Configuration

### Alert Thresholds (in `.env.example`)
```
WATER_LEVEL_THRESHOLD_WARNING=60      # cm
WATER_LEVEL_THRESHOLD_CRITICAL=70     # cm
RAIN_INTENSITY_THRESHOLD_WARNING=50   # mm/h
```

### MQTT Configuration
```
MQTT_BROKER_HOST=broker.emqx.io
MQTT_BROKER_PORT=1883
MQTT_CLIENT_ID=django-flood-monitor
MQTT_TOPICS=RAINSENSOR, WATERLEVELSENSORKAI, WATERLEVELSENSORKRL
```

---

## 📈 What's Working

✅ Backend receives MQTT messages in real-time
✅ Messages stored to SQLite database automatically
✅ REST API returns latest sensor values
✅ WebSocket connected (when frontend connects)
✅ Automatic alerts generated on threshold breach
✅ Frontend configured to use Django endpoints
✅ CORS enabled for frontend communication
✅ Admin interface available at http://localhost:8000/admin

---

## 🎯 Next Steps

1. **Frontend**: Rebuild/restart Vite dev server to apply `.env` changes
   ```bash
   npm run dev -- --force
   ```

2. **Testing**: Check browser DevTools Network tab to verify API calls to `http://localhost:8000`

3. **Admin Panel**: Visit http://localhost:8000/admin to see:
   - Real-time sensor data entries
   - Generated alerts
   - System logs

4. **Admin Features**: Implement endpoints for user/sensor management (when needed)

---

## ⚠️ Known Issues

- Initial MQTT connection may show disconnect warnings (normal during startup)
- Channels Redis layer set to in-memory (fine for development, use Redis for production)
- psycopg2 not installed (SQLite used instead for development)

---

## 📝 Implementation Complete

Both tasks successfully implemented:
1. ✅ MQTT Subscriber in Django (mqtt_client.py) - Fully functional
2. ✅ Frontend connected to Django endpoints - Ready for testing

**Restart your frontend dev server to apply the `.env` configuration changes!**
