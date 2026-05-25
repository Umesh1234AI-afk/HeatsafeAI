from dotenv import load_dotenv
import os
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNPLASH_ACCESS_KEY")

import streamlit as st
import requests
import random
import asyncio
import edge_tts
import base64
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="HeatSafe AI",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# API KEYS
# =====================================================

OPENWEATHER_API_KEY = "7085b855fd6998722a4d9afbe03f80b5"
UNSPLASH_ACCESS_KEY = "bKBWtAow9gfnYe5Ugt3NdcqgR_ui1OUFQod2VSabrnQ"

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* BACKGROUND */

.stApp {

    background:
    linear-gradient(
        135deg,
        #020617 0%,
        #0f172a 45%,
        #111827 100%
    );

    color: white;
}

/* HIDE STREAMLIT */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* TITLE */

.main-title {

    font-size: 72px;
    font-weight: 800;
    text-align: center;
    color: white;
    margin-top: -20px;

    text-shadow:
        0 0 10px rgba(56,189,248,0.6),
        0 0 25px rgba(56,189,248,0.4),
        0 0 50px rgba(56,189,248,0.2);
}

/* SUBTITLE */

.sub-title {

    text-align: center;
    font-size: 24px;
    color: #cbd5e1;
    margin-bottom: 35px;
}

/* INPUT */

.stTextInput input {

    background: rgba(15,23,42,0.95) !important;
    color: white !important;
    border-radius: 20px !important;
    border: 2px solid #38bdf8 !important;
    padding: 18px !important;
    font-size: 18px !important;

    box-shadow:
        0 0 20px rgba(56,189,248,0.15);
}

/* BUTTON */

.stButton button {

    width: 100%;

    background:
    linear-gradient(
        90deg,
        #06b6d4,
        #2563eb
    );

    color: white;
    border: none;
    border-radius: 18px;
    padding: 16px;
    font-size: 18px;
    font-weight: bold;

    transition: 0.3s;
}

.stButton button:hover {

    transform: scale(1.02);

    box-shadow:
        0 0 20px rgba(56,189,248,0.35);
}

/* METRICS */

[data-testid="metric-container"] {

    background: #1e293b;
    border-radius: 20px;
    padding: 20px;

    border:
    1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 0 14px rgba(0,0,0,0.25);
}

[data-testid="metric-container"] * {

    color: white !important;
}

/* CHAT BOX */

.chat-box {

    background:
    linear-gradient(
        135deg,
        rgba(56,189,248,0.15),
        rgba(37,99,235,0.12)
    );

    border-left: 5px solid #67e8f9;

    border-radius: 20px;

    padding: 25px;

    margin-top: 20px;

    color: white;

    font-size: 18px;

    line-height: 1.9;
            
    backdrop-filter: blur(18px);

background:
linear-gradient(
135deg,
rgba(255,255,255,0.10),
rgba(255,255,255,0.04)
);

border:
1px solid rgba(255,255,255,0.16);

box-shadow:
0 0 25px rgba(0,0,0,0.30);
}

/* RISK CARD */

.risk-card {


    padding: 25px;

    border-radius: 22px;

    text-align: center;

    color: white;

    font-size: 32px;

    font-weight: bold;

    margin-top: 20px;

    margin-bottom: 20px;
            
    backdrop-filter: blur(16px);

  border:
  1px solid rgba(255,255,255,0.18);

  box-shadow:
  0 0 25px rgba(0,0,0,0.35);
}

/* SIDEBAR */

section[data-testid="stSidebar"] {

    background: #111827;
}

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* SUN EFFECT */
            
.sun-glow {

    position: fixed;

    top: -180px;

    right: -180px;

    width: 700px;

    height: 700px;

    border-radius: 50%;

    background:
    radial-gradient(
        circle,
        rgba(255,220,0,1) 0%,
        rgba(255,140,0,0.7) 25%,
        rgba(255,80,0,0.35) 45%,
        rgba(255,140,0,0) 72%
    );

    z-index: -1;

    filter: blur(22px);

    animation:
    sunPulse 4s infinite alternate,
    rotateGlow 18s linear infinite;
}

@keyframes rotateGlow {

    from {

        transform:
        rotate(0deg)
        scale(1);
    }

    to {

        transform:
        rotate(360deg)
        scale(1.12);
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SUN EFFECT
# =====================================================

st.markdown(
    '<div class="sun-glow"></div>',
    unsafe_allow_html=True
)

# =====================================================
# TITLE
# =====================================================

st.markdown("""

<h1 class='main-title'>
🌡️ HeatSafe AI
</h1>

<p class='sub-title'>
AI Powered Climate Health Assistant
</p>

""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🤖 HeatSafe AI")

    st.markdown("---")

    st.info("""

🌡️ Live Weather

🌧️ Rain Prediction

🩺 Health Risk Analysis

🔊 AI Voice Assistant

☀️ Heat Alerts

🌆 Dynamic City Visuals

""")
def load_lottieurl(url):

    r = requests.get(url)

    if r.status_code != 200:
        return None

    return r.json()
# =====================================================
# TEXT TO SPEECH
# =====================================================

async def text_to_speech(text):

    if os.path.exists("voice.mp3"):

        try:
            os.remove("voice.mp3")
        except:
            pass

    communicate = edge_tts.Communicate(
        text,
        voice="hi-IN-SwaraNeural"
    )

    await communicate.save("voice.mp3")

# =====================================================
# CITY INPUT
# =====================================================

city = st.text_input(
    "📍 Enter City Name"
)

# =====================================================
# MAIN BUTTON
# =====================================================


if st.button("🔍 Analyze Weather"):

    if city == "":

        st.error("Please enter city name")

    else:

        try:

            with st.spinner(
                "🧠 HeatSafe AI analyzing weather..."
            ):

                # =====================================================
                # GEO API
                # =====================================================

                geo_url = (
                    f"http://api.openweathermap.org/geo/1.0/direct?"
                    f"q={city}&limit=1"
                    f"&appid={OPENWEATHER_API_KEY}"
                )

                geo_data = requests.get(
                    geo_url
                ).json()

                if len(geo_data) == 0:

                    st.error("City not found")

                else:

                    lat = geo_data[0]["lat"]
                    lon = geo_data[0]["lon"]

                    # =====================================================
                    # WEATHER API
                    # =====================================================

                    weather_url = (
                        f"https://api.openweathermap.org/data/2.5/weather?"
                        f"lat={lat}&lon={lon}"
                        f"&appid={OPENWEATHER_API_KEY}"
                        f"&units=metric"
                    )

                    weather_data = requests.get(
                        weather_url
                    ).json()

                    forecast_url = (
                        f"https://api.openweathermap.org/data/2.5/forecast?"
                        f"lat={lat}&lon={lon}"
                        f"&appid={OPENWEATHER_API_KEY}"
                        f"&units=metric"
                    )

                    forecast_data = requests.get(
                        forecast_url
                    ).json()

                    # =====================================================
                    # WEATHER VALUES
                    # =====================================================

                    temp = weather_data["main"]["temp"]

                    feels_like = (
                        weather_data["main"]["feels_like"]
                    )

                    humidity = (
                        weather_data["main"]["humidity"]
                    )

                    wind_speed = (
                        weather_data["wind"]["speed"]
                    )

                    weather = (
                        weather_data["weather"][0]["description"]
                    )

                    weather_lower = weather.lower()

                    tomorrow_temp = (
                        forecast_data["list"][8]["main"]["temp"]
                    )

                    # =====================================================
                    # DYNAMIC CITY IMAGE
                    # =====================================================

                    unsplash_url = (
                        f"https://api.unsplash.com/search/photos?"
                        f"page=1"
                        f"&query={city}+landmark+cinematic"
                        f"&client_id={UNSPLASH_ACCESS_KEY}"
                    )

                    unsplash_data = requests.get(
                        unsplash_url
                    ).json()

                    if (
                        "results" in unsplash_data
                        and len(
                            unsplash_data["results"]
                        ) > 0
                    ):

                        random_image = random.choice(
                            unsplash_data["results"]
                        )

                        city_image = (
                            random_image["urls"]["regular"]
                        )

                        st.image(
                            city_image,
                            use_container_width=True
                        )
                    else:

                        st.warning(
                            "🌆 City image not available"
                        )

                    # =====================================================
                    # WEATHER VISUALS
                    # =====================================================
                    # =====================================================
                    # CINEMATIC WEATHER OVERLAY
                    # =====================================================

                    if temp >= 43:

                        st.markdown("""

                        <style>

                    .heat-overlay {

                        position: fixed;

                        top: 0;

                        left: 0;

                        width: 100%;

                        height: 100%;

                        pointer-events: none;

                        background:
                        radial-gradient(
                         circle at top right,
                         rgba(255,140,0,0.22),
                         transparent 45%
                        );

                        animation:
                        heatMove 6s infinite alternate;
                    }

                    @keyframes heatMove {

                      0% {

                         transform:
                         translateX(0px)
                         scale(1);
                        }

                       100% {

                          transform:
                          translateX(-40px)
                          scale(1.08);
                        }
                    }

                    </style>

                    <div class="heat-overlay"></div>

                    """, unsafe_allow_html=True)
                    if temp >= 38:

                        st.markdown("""
                        <div style="
                        text-align:center;
                        font-size:95px;
                        margin-top:-20px;
                        animation:sunPulse 3s infinite alternate;
                        ">
                        ☀️🔥
                        </div>
                        """, unsafe_allow_html=True)

                    elif (
                        "rain" in weather_lower
                        or "drizzle" in weather_lower
                        or humidity >= 85
                    ):

                        st.markdown("""
                        <div style="
                        text-align:center;
                        font-size:95px;
                        margin-top:-20px;
                        ">
                        🌧️☁️
                        </div>
                        """, unsafe_allow_html=True)

                    else:

                        st.markdown("""
                        <div style="
                        text-align:center;
                        font-size:95px;
                        margin-top:-20px;
                        ">
                        ⛅🌤️
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("""
                    <style>

                    .float-bot {

                     animation:
                    floatBot 4s infinite ease-in-out;
                    }

                    @keyframes floatBot {

                    0% {

                       transform:
                       translateY(0px);
                    }

                    50% {

                         transform:
                         translateY(-12px);
                    }

                    100% {

                         transform:
                         translateY(0px);
                        }

                    }

                    </style>
                    """, unsafe_allow_html=True)

                    
                    # =====================================================
                    # AI SPEAKING ANIMATION
                    # =====================================================

                    st.markdown("""

                    <div style="
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:center;
                    margin-top:30px;
                    margin-bottom:20px;
                    ">

                    <div style="
                    width:90px;
                    height:90px;
                    border-radius:50%;
                    background:radial-gradient(circle,#67e8f9 0%,#2563eb 45%);
                    box-shadow:0 0 20px #38bdf8,0 0 50px #2563eb;
                    animation:pulse 1.5s infinite;
                    ">
                    </div>

                    <div style="
                    display:flex;
                    gap:6px;
                    margin-top:20px;
                    align-items:flex-end;
                    ">

                    <div class="wave"></div>
                    <div class="wave"></div>
                    <div class="wave"></div>
                    <div class="wave"></div>
                    <div class="wave"></div>

                    </div>

                    <h3 style="
                    margin-top:15px;
                    color:white;
                    ">
                    🤖 HeatSafe AI बोल रही है...
                    </h3>

                    </div>

                    <style>

                    @keyframes pulse {
                    0% {transform:scale(1);}
                    50% {transform:scale(1.15);}
                    100% {transform:scale(1);}
                    }

                    .wave {
                    width:8px;
                    height:35px;
                    background:#67e8f9;
                    border-radius:10px;
                    animation:wave 1s infinite ease-in-out;
                    }

                    .wave:nth-child(2){animation-delay:0.2s;}
                    .wave:nth-child(3){animation-delay:0.4s;}
                    .wave:nth-child(4){animation-delay:0.6s;}
                    .wave:nth-child(5){animation-delay:0.8s;}

                    @keyframes wave {
                    0% {height:20px;}
                    50% {height:60px;}
                    100% {height:20px;}
                    }

                    </style>

                    """, unsafe_allow_html=True)

                    # =====================================================
                    # RISK CARD
                    # =====================================================

                    if temp >= 45:

                        risk = "🚨 Extreme Heat Risk"

                        gradient = (
                            "linear-gradient(135deg,#ef4444,#991b1b)"
                        )

                    elif temp >= 38:

                        risk = "⚠️ Heat Increasing"

                        gradient = (
                            "linear-gradient(135deg,#f59e0b,#ea580c)"
                        )

                    else:

                        risk = "✅ Weather Normal"

                        gradient = (
                            "linear-gradient(135deg,#10b981,#047857)"
                        )

                    st.markdown(
                        f"""
                        <div class="risk-card"
                        style="background:{gradient};">

                        {risk}

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # =====================================================
                    # WEATHER CARD
                    # =====================================================

                    st.markdown(
                        f"""
                        <div class="chat-box">

                        <h2>
                        🤖 HeatSafe AI Assistant
                        </h2>

                        📍 <b>Location:</b> {city}<br><br>

                        🌡️ <b>Temperature:</b> {temp}°C<br><br>

                        🥵 <b>Feels Like:</b> {feels_like}°C<br><br>

                        💧 <b>Humidity:</b> {humidity}%<br><br>

                        🌬️ <b>Wind Speed:</b> {wind_speed} m/s<br><br>

                        ☁️ <b>Weather:</b> {weather}<br><br>

                        📅 <b>Tomorrow Temperature:</b> {tomorrow_temp}°C

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # =====================================================
                    # METRICS
                    # =====================================================

                    st.markdown(
                        "## 📊 Live Climate Analysis"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "🌡️ Temperature",
                            f"{temp} °C",
                            f"Feels {feels_like} °C"
                        )

                        st.metric(
                            "💧 Humidity",
                            f"{humidity}%",
                            "Moisture Level"
                        )

                    with col2:

                        st.metric(
                            "🌬️ Wind Speed",
                            f"{wind_speed} m/s",
                            "Air Flow"
                        )

                        st.metric(
                            "📅 Tomorrow Temp",
                            f"{tomorrow_temp} °C",
                            "Forecast"
                        )

                    # =====================================================
                    # AI VOICE
                    # =====================================================

                    alert_voice = f"""

                    Namaste.

                    Mai HeatSafe AI Assistant bol rahi hu.

                    Aaj {city} ka live climate analysis ready hai.

                    Current temperature {temp} degree Celsius record kiya gaya hai.

                    Feels like temperature {feels_like} degree hai.

                    Humidity level {humidity} percent hai.

                    Wind speed {wind_speed} meter per second hai.

                    Kal ka expected temperature {tomorrow_temp} degree tak pahunch sakta hai.

                    """

                    if temp >= 43:

                        alert_voice += """

                        Warning.

                        Extreme heat conditions detect hui hain.

                        Heat stroke,
                        severe dehydration,
                        body weakness,
                        dizziness,
                        high fatigue,
                        aur headache ho sakta hai.

                        Din bhar zyada paani peejiyega.

                        ORS,
                        coconut water,
                        aur fresh fruits beneficial rahenge.

                        Direct sunlight avoid kijiye.

                        Afternoon me unnecessary travel avoid kijiye.

                        Light cotton clothes pehniye.

                        Cap aur sunglasses use kijiye.
"""

                    elif temp >= 38:

                        alert_voice += """

                        Heat level gradually increase ho raha hai.

                        Hydrated rahiye.
                        """

                    else:

                        alert_voice += """

                        Weather currently stable hai.
                        """

                    if (
                        "rain" in weather_lower
                        or "drizzle" in weather_lower
                        or humidity >= 85
                    ):

                        alert_voice += """

                        Rain possibility detect hui hai.

                        Umbrella carry kijiye.
                        """

                    alert_voice += """

                    Stay safe.

                    Thank you.
                    """

                    # =====================================================
                    # GENERATE VOICE
                    # =====================================================

                    asyncio.run(
                        text_to_speech(alert_voice)
                    )

                    with open(
                        "voice.mp3",
                        "rb"
                    ) as audio_file:

                        audio_bytes = audio_file.read()

                    # =====================================================
                    # AUDIO
                    # =====================================================

                    st.audio(
                        audio_bytes,
                        format="audio/mp3",
                        autoplay=True
                    )

        except Exception as e:

            st.error("Technical Error")

            st.write(e)

