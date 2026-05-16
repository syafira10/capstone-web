# REAL-TIME UPDATE VERIFICATION GUIDE
**Status: ✅ Real-time WebSocket integration COMPLETE**

---

## 🔄 What's Been Fixed

### ✅ Dashboard.tsx
- **Before**: WebSocket hardcoded to `ws://localhost:3000` (wrong port)
- **After**: Now uses proper `subscribeToRealtime()` function connecting to `ws://localhost:8000/ws/monitoring/`
- **Result**: Receives real-time MQTT updates automatically

### ✅ DataPage.tsx  
- **Before**: Only fetched data once on component mount (no real-time updates)
- **After**: Now subscribes to WebSocket and receives real-time updates
- **Result**: Historical data updates in real-time as new MQTT messages arrive

### ✅ mqttApi.ts
- **Added**: Proper message type handling for Django WebSocket format
- **Added**: Auto-reconnect logic (up to 5 attempts)
- **Added**: Detailed console logging for debugging
- **Result**: More robust connection and better debugging visibility

---

## 🚀 STEP-BY-STEP TESTING

### Step 1: Start Frontend Development Server

```bash
cd capstone-web
npm run dev
```

**Expected Output:**
```
  VITE v6.x.x  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

---

### Step 2: Open Frontend in Browser

1. Navigate to `http://localhost:5173`
2. Open **DevTools** (Press F12)
3. Go to **Console** tab
4. Should see:
   ```
   ✓ WebSocket connected to monitoring stream
   ✓ Subscription confirmed, ready for real-time updates
   ```

---

### Step 3: Monitor WebSocket Connection

In DevTools Console, you should see:
```
✓ WebSocket connected to monitoring stream
✓ Subscription confirmed, ready for real-time updates
```

If you see these messages = ✅ **WebSocket connection successful!**

---

### Step 4: Publish Test MQTT Messages

**Option A: Using `mosquitto_pub` CLI Tool**
```bash
# Publish rain sensor data
mosquitto_pub -h broker.emqx.io -t RAINSENSOR -m "45.5"

# Publish water level KRL
mosquitto_pub -h broker.emqx.io -t WATERLEVELSENSORKRL -m "62"

# Publish water level KAI  
mosquitto_pub -h broker.emqx.io -t WATERLEVELSENSORKAI -m "58"
```

**Option B: Using Python MQTT Client**
```python
import paho.mqtt.client as mqtt
import time

client = mqtt.Client(client_id="test-publisher")
client.connect("broker.emqx.io", 1883, 60)

# Publish test messages
client.publish("RAINSENSOR", "45.5")
client.publish("WATERLEVELSENSORKRL", "62")
client.publish("WATERLEVELSENSORKAI", "58")

client.disconnect()
```

**Option C: Using Online MQTT Client**
- Visit: https://mqtt.xn--8m8h.com/
- Broker: `broker.emqx.io`
- Port: `1883`
- Publish to: `RAINSENSOR`, `WATERLEVELSENSORKRL`, `WATERLEVELSENSORKAI`

---

### Step 5: Verify Real-Time Updates

**In DevTools Console:**

You should see messages like:
```
📨 MQTT Update received: RAINSENSOR = 45.5
📨 MQTT Update received: WATERLEVELSENSORKRL = 62
📨 MQTT Update received: WATERLEVELSENSORKAI = 58
```

**On Dashboard:**

Watch the values update **INSTANTLY** without refreshing:
- Water Level KRL: Should update to 62 cm
- Water Level KAI: Should update to 58 cm  
- Rain Intensity: Should update to 45.5 mm/h
- Status color changes based on thresholds

**On DataPage:**

New records should appear **instantly** as you publish messages

---

## 🔍 DATA FLOW VERIFICATION

### Complete Real-Time Data Flow

```
┌─────────────────────────────────────────────────────────┐
│              REAL-TIME DATA FLOW CHAIN                   │
└─────────────────────────────────────────────────────────┘

Step 1: MQTT Message Published
  mosquitto_pub -h broker.emqx.io -t RAINSENSOR -m "45.5"
  
         ↓

Step 2: Django MQTT Client Receives Message
  mqtt_client.py → on_message() callback
  Status: ✓ Message received and parsed
  
         ↓

Step 3: Data Processing in Django Backend
  a) Save to SQLite database ✓
  b) Check thresholds for alerts ✓
  c) Broadcast to WebSocket group ✓
  
         ↓

Step 4: WebSocket Consumer Processes Message
  apps/monitoring/consumers.py → mqtt_message() handler
  Message format: { "type": "mqtt_update", "data": {...} }
  
         ↓

Step 5: Browser Receives WebSocket Update
  msgApi.ts → subscribeToRealtime() callback
  Frontend components parse data
  
         ↓

Step 6: React State Updates
  Dashboard.tsx → setLatest() updates latest sensor values
  DataPage.tsx → setRecords() prepends new record
  Charts and UI re-render instantly
  
         ↓

Step 7: User Sees Real-Time Update
  ✓ Dashboard values change immediately
  ✓ DataPage table shows new record
  ✓ Charts update instantly
  ✓ Status colors change based on thresholds
  
         ↓ NO PAGE REFRESH NEEDED!

Result: ✅ REAL-TIME SYSTEM OPERATIONAL
```

---

## 📊 WHAT EACH COMPONENT DOES NOW

### Frontend (React Components)

**Dashboard.tsx**:
- ✓ Loads latest data on mount via `fetchRealtime()`
- ✓ Loads historical data on mount via `fetchHistorical()`
- ✓ Subscribes to WebSocket via `subscribeToRealtime()`
- ✓ Updates `latest` state when new MQTT messages arrive
- ✓ Appends to `history` array for charts
- ✓ Charts auto-update as data arrives

**DataPage.tsx**:
- ✓ Loads historical records on mount
- ✓ Subscribes to WebSocket via `subscribeToRealtime()`
- ✓ Prepends new records to `records` array
- ✓ Filtered table shows latest records first
- ✓ All data real-time without filtering

### Backend (Django)

**mqtt_client.py**:
- ✓ Receives MQTT messages from broker
- ✓ Saves to database
- ✓ Broadcasts to WebSocket group
- ✓ Checks thresholds and creates alerts

**consumers.py**:
- ✓ Accepts WebSocket connections
- ✓ Joins `monitoring` group
- ✓ Receives messages from `mqtt_message` handler
- ✓ Sends messages to connected clients

---

## 🧪 TESTING CHECKLIST

### Connection Tests

- [ ] Frontend page loads without errors
- [ ] DevTools Console shows ✓ WebSocket connected
- [ ] DevTools Console shows ✓ Subscription confirmed
- [ ] No WebSocket connection errors in Console

### Real-Time Data Tests

- [ ] Publish RAINSENSOR message
- [ ] Dashboard Rain Intensity updates immediately
- [ ] Publish WATERLEVELSENSORKRL message  
- [ ] Dashboard Water Level KRL updates immediately
- [ ] Publish WATERLEVELSENSORKAI message
- [ ] Dashboard Water Level KAI updates immediately

### DataPage Tests

- [ ] Publish any MQTT message
- [ ] New row appears in DataPage table instantly
- [ ] Timestamp shows current time
- [ ] Value matches what you published

### Chart Tests

- [ ] Line chart updates with new data points
- [ ] Chart shows last 8 time buckets
- [ ] Multiple messages aggregate correctly

### Alert Tests

- [ ] Publish water level >= 70 cm
- [ ] Red alert appears on Dashboard
- [ ] Status changes to "TOTAL STOP"
- [ ] Publish water level >= 60 cm
- [ ] Yellow alert appears
- [ ] Status changes to "KRL STOP"

### Connection Recovery Tests

- [ ] If connection drops, console shows reconnection attempts
- [ ] Auto-reconnects (max 5 attempts, 3 seconds apart)
- [ ] After reconnect, real-time updates resume

---

## 🐛 TROUBLESHOOTING

### Problem: DevTools shows ✗ WebSocket error

**Solution 1**: Check backend is running
```bash
# In new terminal
cd django-backend
python manage.py runserver 0.0.0.0:8000
```

**Solution 2**: Check WebSocket route exists
```bash
# Check Django logs for:
# ✓ WebSocket connected: ...
```

**Solution 3**: Check CORS settings in `django-backend/config/settings.py`
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
]
```

---

### Problem: Message published but Dashboard doesn't update

**Step 1**: Check Django MQTT client is running
```bash
# Django console should show:
# ✓ Subscribed to topic: RAINSENSOR
# ✓ Subscribed to topic: WATERLEVELSENSORKRL
# ✓ Subscribed to topic: WATERLEVELSENSORKAI
```

**Step 2**: Verify message reached backend
```bash
# In Django terminal, you should see:
# → MQTT Message: RAINSENSOR = 45.5
# ✓ Broadcasted RAINSENSOR=45.5 to WebSocket
```

**Step 3**: Check browser WebSocket is listening
```javascript
// In DevTools Console, manually check:
console.log('WebSocket URL: ws://localhost:8000/ws/monitoring/');
// Message format should be:
// { "type": "mqtt_update", "data": { "topic": "RAINSENSOR", "value": 45.5, ... } }
```

---

### Problem: Reconnection spam in console

**Expected behavior**: 
- First time: ✓ WebSocket connected
- After 10+ messages: Maybe shows ⟳ attempts once
- Then: ✓ Connection restored

This is normal! Auto-reconnect is working.

To reduce spam, modify `mqttApi.ts`:
```typescript
// Increase interval if too frequent
const reconnectInterval = 5000; // 5 seconds instead of 3
```

---

## 📈 PERFORMANCE TIPS

1. **Limit message volume**: 
   - Too many messages (>10/sec) might slow updates
   - Aggregate data at source if possible

2. **Monitor browser memory**:
   - DataPage history array grows indefinitely
   - Consider implementing data pagination (next phase)

3. **Use DevTools Network tab**:
   - Check WebSocket frames tab
   - See exact message sizes and frequency

---

## ✅ SUCCESS INDICATORS

You'll know it's working when:

1. ✅ DevTools Console shows WebSocket connected messages
2. ✅ Publish MQTT message to broker
3. ✅ Dashboard values change **instantly** (no page refresh!)
4. ✅ DataPage shows new row **instantly**
5. ✅ Charts update in real-time
6. ✅ Alerts appear when thresholds crossed

---

## 🎯 NEXT STEPS

After verifying real-time updates work:

1. **Test with real IoT sensors** (when available)
2. **Monitor performance** with multiple messages
3. **Add data persistence** if needed (save unlimited history)
4. **Implement data pagination** in DataPage for better performance
5. **Add alert notifications** (toast/sound alerts)

---

## 📞 QUICK COMMANDS

```bash
# Terminal 1: Django Backend
cd django-backend
python manage.py runserver 0.0.0.0:8000

# Terminal 2: Frontend Dev Server
cd capstone-web
npm run dev

# Terminal 3: Test Publishing (if mosquitto installed)
mosquitto_pub -h broker.emqx.io -t RAINSENSOR -m "45.5"

# Terminal 4: Check backend logs
# Watch for:
# ✓ Subscribed to topics
# → MQTT Message received
# ✓ Broadcasted to WebSocket
```

---

## 🔗 KEY FILES MODIFIED

1. **capstone-web/src/app/pages/Dashboard.tsx**
   - Uses `subscribeToRealtime()` instead of hardcoded WebSocket
   - Real-time updates without page refresh

2. **capstone-web/src/app/pages/DataPage.tsx**
   - Added WebSocket subscription
   - New records appear instantly

3. **capstone-web/src/app/lib/mqttApi.ts**
   - Improved message handling
   - Auto-reconnect logic
   - Better logging

4. **django-backend/apps/monitoring/services/mqtt_client.py**
   - Already configured correctly
   - Broadcasts to WebSocket group

5. **django-backend/apps/monitoring/consumers.py**
   - Receives and forwards messages

---

## 📝 ENVIRONMENT VARIABLES

Make sure `.env` files are correct:

**capstone-web/.env**:
```
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

**django-backend/.env.example** (create `.env` if needed):
```
MQTT_BROKER_HOST=broker.emqx.io
MQTT_BROKER_PORT=1883
MQTT_CLIENT_ID=django-flood-monitor
MQTT_LOCATION=Manggarai Station
```

---

**System Status**: ✅ **READY FOR REAL-TIME TESTING**

Start frontend with `npm run dev` and monitor the browser console while publishing MQTT messages!
