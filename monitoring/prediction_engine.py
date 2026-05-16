from collections import deque


# ======================================
# WATER HISTORY
# ======================================

water_history = deque(maxlen=5)


# ======================================
# SENSOR VALIDATION
# ======================================

def validate_sensor(current, previous):

    difference = abs(current - previous)

    if difference > 8:

        return "FALSE DETECTION"

    return "VALID"


# ======================================
# TREND ANALYSIS
# ======================================

def analyze_trend(history):

    if len(history) < 3:

        return "STABLE"

    if history[-1] > history[-2] > history[-3]:

        return "RISING"

    elif history[-1] < history[-2]:

        return "FALLING"

    return "STABLE"


# ======================================
# RAIN ANALYSIS
# ======================================

def rain_intensity(rain):

    if rain > 70:

        return "HEAVY"

    elif rain > 30:

        return "MEDIUM"

    return "LOW"


# ======================================
# FLOOD PREDICTION
# ======================================

def predict_status(water, rain, trend):

    rain_status = rain_intensity(rain)

    if water >= 5:

        return "KRL STOP"

    elif trend == "RISING" and rain_status == "HEAVY":

        return "HIGH RISK"

    elif trend == "RISING":

        return "WARNING"

    return "SAFE"