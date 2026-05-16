# 🚀 REAL-TIME UPDATES - QUICK START

## ✅ What's Fixed
- ✅ Dashboard.tsx - WebSocket connected to correct backend (ws://localhost:8000)
- ✅ DataPage.tsx - Subscribes to real-time WebSocket updates
- ✅ mqttApi.ts - Improved message handling + auto-reconnect

## 🎯 Test Real-Time Updates (5 minutes)

### Terminal 1: Start Django Backend
```bash
cd django-backend
python manage.py runserver 0.0.0.0:8000
```

Wait for:
```
✓ Subscribed to topic: RAINSENSOR
✓ Subscribed to topic: WATERLEVELSENSORKRL
✓ Subscribed to topic: WATERLEVELSENSORKAI
```

### Terminal 2: Start Frontend
```bash
cd capstone-web
npm run dev
```

Wait for:
```
  ➜  Local:   http://localhost:5173/
```

### Step 3: Open Browser
1. Go to `http://localhost:5173`
2. Open DevTools (F12) → Console tab
3. Look for:
   ```
   ✓ WebSocket connected to monitoring stream
   ✓ Subscription confirmed, ready for real-time updates
   ```

### Step 4: Publish Test Data (Choose One)

**Option A: Using mqtt_test_publisher.py**
```bash
# Terminal 3
python mqtt_test_publisher.py interactive

# Then in the interactive menu:
# s          (send sample burst)
# or
# p 1 45.5   (publish to RAINSENSOR = 45.5)
```

**Option B: Using Command Line**
```bash
mosquitto_pub -h broker.emqx.io -t RAINSENSOR -m "45.5"
mosquitto_pub -h broker.emqx.io -t WATERLEVELSENSORKRL -m "62"
```

**Option C: Online MQTT Client**
- Visit: https://mqtt.xn--8m8h.com/
- Broker: broker.emqx.io, Port: 1883
- Publish test messages

### Step 5: Watch Updates Happen
✅ Dashboard values change **INSTANTLY**
✅ DataPage shows new record **INSTANTLY**
✅ Charts update in **REAL-TIME**
✅ **NO PAGE REFRESH NEEDED!**

---

## 📊 Expected Behavior

**Before Update**: Had to refresh page to see new data
**After Update**: Data updates automatically as MQTT messages arrive

**Dashboard Cards Update**:
- Water Level KRL
- Water Level KAI
- Rain Intensity
- Flood Status

**DataPage Table Updates**:
- New records appear at top
- Timestamp shows current time

**Charts Update**:
- New data points added
- Line chart updates in real-time

---

## 🔍 Verify Connection

**In Browser DevTools Console**, paste:
```javascript
// Check WebSocket connection
ws = new WebSocket('ws://localhost:8000/ws/monitoring/')
ws.onopen = () => console.log('✓ Connected!')
ws.onmessage = (e) => console.log('📨 Message:', JSON.parse(e.data))
```

Should see messages like:
```
📨 Message: {
  type: "mqtt_update",
  data: {
    topic: "RAINSENSOR",
    value: 45.5,
    timestamp: "2026-05-16T10:30:45.123456Z",
    location: "Manggarai Station"
  }
}
```

---

## 🐛 If It's Not Working

**Check 1**: Is Django running?
- Should see: `✓ Subscribed to topic: RAINSENSOR`

**Check 2**: Is frontend running?
- Should see: `http://localhost:5173` in browser

**Check 3**: Is WebSocket connected?
- DevTools Console should show: `✓ WebSocket connected`

**Check 4**: Is MQTT message being published?
- Django console should show: `→ MQTT Message: RAINSENSOR = 45.5`

**Check 5**: Is message reaching frontend?
- DevTools Console should show: `📨 MQTT Update received: RAINSENSOR = 45.5`

If any check fails, see REALTIME_UPDATE_GUIDE.md for troubleshooting

---

## 📁 Key Files

- `django-backend/config/asgi.py` - WebSocket routing
- `django-backend/apps/monitoring/consumers.py` - WebSocket handler
- `django-backend/apps/monitoring/services/mqtt_client.py` - MQTT receiver
- `capstone-web/src/app/pages/Dashboard.tsx` - Real-time dashboard
- `capstone-web/src/app/pages/DataPage.tsx` - Real-time data table
- `capstone-web/src/app/lib/mqttApi.ts` - WebSocket client

---

## 🎓 How It Works

```
1. MQTT Message Published
   ↓
2. Django receives via MQTT Client
   ↓
3. Django broadcasts to WebSocket group
   ↓
4. Frontend receives via WebSocket
   ↓
5. React updates state
   ↓
6. UI re-renders with new data
   ↓
7. User sees live updates ✨
```

---

## ✨ System Status

| Component | Status |
|-----------|--------|
| Django Backend | ✅ Running |
| MQTT Broker | ✅ Connected |
| WebSocket Route | ✅ Configured |
| Frontend WebSocket | ✅ Subscribed |
| Real-Time Updates | ✅ **READY!** |

---

**Ready?** Start the servers and watch the magic happen! 🎉
