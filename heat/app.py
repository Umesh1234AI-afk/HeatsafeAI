import streamlit as st
import requests
from gtts import gTTS
import base64

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="HeatSafe AI",
    page_icon="🌡️",
    layout="centered"
)

# =====================================================
# TITLE
# =====================================================

st.title("🌡️ HeatSafe AI")
st.subheader("🩺 हिंदी AI क्लाइमेट हेल्थ असिस्टेंट")

# =====================================================
# API KEY
# =====================================================

API_KEY = "7085b855fd6998722a4d9afbe03f80b5"

# =====================================================
# USER INPUT
# =====================================================

city = st.text_input("📍 शहर का नाम लिखें")

# =====================================================
# BUTTON
# =====================================================

if st.button("🔍 मौसम और हीट रिस्क जांचें"):

    if city == "":

        st.error("❌ कृपया शहर का नाम लिखें")

    else:

        try:

            # =====================================================
            # GET LATITUDE & LONGITUDE
            # =====================================================

            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"

            geo_response = requests.get(geo_url)

            geo_data = geo_response.json()

            # =====================================================
            # CHECK CITY FOUND
            # =====================================================

            if len(geo_data) == 0:

                st.error("❌ शहर नहीं मिला")

            else:

                # =====================================================
                # COORDINATES
                # =====================================================

                lat = geo_data[0]["lat"]
                lon = geo_data[0]["lon"]

                # =====================================================
                # CURRENT WEATHER
                # =====================================================

                weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

                weather_response = requests.get(weather_url)

                weather_data = weather_response.json()

                # =====================================================
                # FORECAST WEATHER
                # =====================================================

                forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

                forecast_response = requests.get(forecast_url)

                forecast_data = forecast_response.json()

                # =====================================================
                # WEATHER VALUES
                # =====================================================

                temp = weather_data["main"]["temp"]

                feels_like = weather_data["main"]["feels_like"]

                humidity = weather_data["main"]["humidity"]

                pressure = weather_data["main"]["pressure"]

                weather = weather_data["weather"][0]["description"]

                wind_speed = weather_data["wind"]["speed"]

                tomorrow_temp = forecast_data["list"][8]["main"]["temp"]

                # =====================================================
                # HEAT ANALYSIS
                # =====================================================

                risk = ""
                diseases = ""
                solutions = ""
                alert_voice = ""
                box_color = ""

                # =====================================================
                # EXTREME HEAT
                # =====================================================

                if temp >= 45 or feels_like >= 48:

                    risk = "🚨 अत्यधिक गर्मी का खतरा"

                    diseases = """
🥵 हीट स्ट्रोक  
💧 डिहाइड्रेशन  
😵 बेहोशी  
🤕 चक्कर आना  
🔥 त्वचा जलना  
❤️ BP बढ़ना  
🤒 तेज सिर दर्द
"""

                    solutions = """
💧 ORS और पानी पिएं  
🍋 नींबू पानी लें  
☀️ धूप से बचें  
🧢 टोपी पहनें  
🚿 ठंडे पानी से नहाएं  
🥒 खीरा और फल खाएं  
👶 बच्चों और बुजुर्गों का ध्यान रखें
"""

                    alert_voice = f"""
चेतावनी।

{city} में अत्यधिक गर्मी है।

वर्तमान तापमान {temp} डिग्री सेल्सियस है।
महसूस तापमान {feels_like} डिग्री है।
नमी {humidity} प्रतिशत है।

कल अनुमानित तापमान {tomorrow_temp} डिग्री रह सकता है।

इस मौसम में
हीट स्ट्रोक,
डिहाइड्रेशन,
बेहोशी,
चक्कर,
और त्वचा जलने जैसी समस्याएं हो सकती हैं।

कृपया ORS और पानी पिएं।
धूप में बाहर ना जाएं।
टोपी पहनें।
और बच्चों तथा बुजुर्गों का विशेष ध्यान रखें।

सुरक्षित रहें।
"""

                    box_color = "red"

                # =====================================================
                # HIGH HEAT
                # =====================================================

                elif temp >= 38:

                    risk = "⚠️ गर्मी बढ़ रही है"

                    diseases = """
🤒 सिर दर्द  
😓 थकान  
💦 कमजोरी  
🥵 शरीर गर्म होना  
😴 आलस  
💧 पानी की कमी
"""

                    solutions = """
💧 ज्यादा पानी पिएं  
🍉 फल खाएं  
☀️ दोपहर में बाहर कम जाएं  
🧃 जूस पिएं  
😴 आराम करें  
🧢 सिर ढककर बाहर जाएं
"""

                    alert_voice = f"""
सावधान।

{city} में तापमान {temp} डिग्री सेल्सियस है।
महसूस तापमान {feels_like} डिग्री है।
नमी {humidity} प्रतिशत है।

कल अनुमानित तापमान {tomorrow_temp} डिग्री रह सकता है।

गर्मी बढ़ रही है।

इस मौसम में
डिहाइड्रेशन,
सिर दर्द,
कमजोरी,
थकान,
और शरीर गर्म होने जैसी समस्याएं हो सकती हैं।

कृपया ज्यादा पानी पिएं।
जूस और फल लें।
दोपहर में धूप से बचें।
और सिर ढककर बाहर जाएं।

अपना और अपने परिवार का ध्यान रखें।
"""

                    box_color = "orange"

                # =====================================================
                # NORMAL WEATHER
                # =====================================================

                else:

                    risk = "✅ मौसम सामान्य"

                    diseases = """
😊 कोई बड़ा स्वास्थ्य खतरा नहीं
"""

                    solutions = """
💧 नियमित पानी पिएं  
🥗 हेल्दी भोजन करें  
🏃 सामान्य गतिविधियां सुरक्षित हैं
"""

                    alert_voice = f"""
अच्छी खबर।

{city} का मौसम सामान्य है।

वर्तमान तापमान {temp} डिग्री सेल्सियस है।
महसूस तापमान {feels_like} डिग्री है।
नमी {humidity} प्रतिशत है।

कल अनुमानित तापमान {tomorrow_temp} डिग्री रह सकता है।

फिलहाल कोई बड़ा स्वास्थ्य खतरा नहीं है।

फिर भी नियमित पानी पीते रहें।
स्वस्थ भोजन करें।
और अपना ध्यान रखें।
"""

                    box_color = "green"

                # =====================================================
                # RISK BOX
                # =====================================================

                st.markdown(
                    f"""
                    <div style="
                        background-color:{box_color};
                        padding:18px;
                        border-radius:15px;
                        text-align:center;
                        color:white;
                        font-size:28px;
                        font-weight:bold;
                    ">
                    {risk}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")

                # =====================================================
                # WEATHER DETAILS
                # =====================================================

                col1, col2 = st.columns(2)

                with col1:

                    st.metric("🌡️ तापमान", f"{temp} °C")

                    st.metric("💧 नमी", f"{humidity}%")

                    st.metric("📅 कल तापमान", f"{tomorrow_temp} °C")

                with col2:

                    st.metric("🥵 महसूस तापमान", f"{feels_like} °C")

                    st.metric("🌬️ हवा की गति", f"{wind_speed} m/s")

                    st.metric("📍 Latitude", lat)

                st.info(f"☁️ मौसम: {weather}")

                # =====================================================
                # DISEASES
                # =====================================================

                st.subheader("🩺 संभावित स्वास्थ्य समस्याएं")

                st.warning(diseases)

                # =====================================================
                # SOLUTIONS
                # =====================================================

                st.subheader("🛡️ बचाव के उपाय")

                st.success(solutions)

                # =====================================================
                # EXTRA AI TIPS
                # =====================================================

                st.subheader("🌿 AI हेल्थ टिप्स")

                if humidity > 70:
                    st.info("💦 नमी अधिक है, पसीना जल्दी नहीं सूखेगा")

                if temp > 40:
                    st.error("☀️ दोपहर 12 बजे से 4 बजे तक बाहर ना जाएं")

                if tomorrow_temp > temp:
                    st.warning("📈 कल तापमान और बढ़ सकता है")

                if feels_like > temp:
                    st.warning("🥵 महसूस तापमान वास्तविक तापमान से अधिक है")

                if wind_speed < 1:
                    st.warning("🌬️ हवा कम चल रही है, गर्मी ज्यादा महसूस हो सकती है")

                # =====================================================
                # AI HINDI FEMALE-LIKE VOICE
                # =====================================================

                tts = gTTS(
                    text=alert_voice,
                    lang='hi',
                    slow=False
                )

                tts.save("alert.mp3")

                # =====================================================
                # AUTOPLAY AUDIO
                # =====================================================

                audio_file = open("alert.mp3", "rb")

                audio_bytes = audio_file.read()

                b64 = base64.b64encode(audio_bytes).decode()

                audio_html = f"""
                <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """

                st.markdown(audio_html, unsafe_allow_html=True)

        # =====================================================
        # ERROR HANDLING
        # =====================================================

        except Exception as e:

            st.error("⚠️ कुछ तकनीकी समस्या हुई")

            st.write(e)