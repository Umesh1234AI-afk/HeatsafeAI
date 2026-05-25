import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_tts/flutter_tts.dart';

void main() {
  runApp(const HeatSafeAI());
}

class HeatSafeAI extends StatelessWidget {
  const HeatSafeAI({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'HeatSafe AI',
      theme: ThemeData(
        primarySwatch: Colors.orange,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {

  final TextEditingController cityController = TextEditingController();

  final FlutterTts flutterTts = FlutterTts();

  String result = "";

  // =========================
  // API KEY
  // =========================

  String apiKey = "3484f45fe0f98c6411739651a84b37e7";

  // =========================
  // WEATHER FUNCTION
  // =========================

  Future<void> checkHeatRisk() async {

    String city = cityController.text;

    if (city.isEmpty) {

      setState(() {

        result = "❌ कृपया स्थान का नाम लिखें";

      });

      return;
    }

    String url =
        "https://api.openweathermap.org/data/2.5/weather?q=$city,IN&appid=$apiKey&units=metric";

    final response = await http.get(Uri.parse(url));

    final data = jsonDecode(response.body);

    // =========================
    // SUCCESS
    // =========================

    if (response.statusCode == 200) {

      double temp = data["main"]["temp"];

      int humidity = data["main"]["humidity"];

      String weather = data["weather"][0]["description"];

      String risk = "";

      String diseases = "";

      String precautions = "";

      String smartVoice = "";

      // =========================
      // AI ANALYSIS
      // =========================

      if (temp >= 45) {

        risk = "🚨 अत्यधिक खतरा";

        diseases =
            "🥵 हीटस्ट्रोक\n"
            "🤕 चक्कर आना\n"
            "💧 शरीर में पानी की कमी\n"
            "😵 बेहोशी\n"
            "🔥 त्वचा जलना";

        precautions =
            "💧 ORS पिएं\n"
            "🍋 नींबू पानी लें\n"
            "🧢 टोपी पहनें\n"
            "☀️ धूप में बाहर ना जाएं\n"
            "👶 बच्चों और बुजुर्गों का ध्यान रखें";

        smartVoice =
            "Warning. Bahut zyada garmi hai. "
            "Heat stroke ka khatra hai. "
            "Please paani piye aur dhoop se bachiye.";

      }

      else if (temp >= 38) {

        risk = "⚠️ मध्यम खतरा";

        diseases =
            "😓 डिहाइड्रेशन\n"
            "🤒 सिर दर्द\n"
            "🥵 थकान\n"
            "💦 कमजोरी";

        precautions =
            "💧 अधिक पानी पिएं\n"
            "🍉 जूस और फल लें\n"
            "🧢 टोपी पहनें\n"
            "☀️ दोपहर में बाहर कम जाएं";

        smartVoice =
            "Moderate heat risk detected. "
            "Paani peete rahiye aur body ko hydrate rakhiye.";

      }

      else {

        risk = "✅ मौसम सामान्य";

        diseases =
            "😊 गंभीर खतरा नहीं";

        precautions =
            "💧 नियमित पानी पिएं\n"
            "🏃 सामान्य गतिविधियां सुरक्षित हैं";

        smartVoice =
            "Weather normal hai. "
            "Health risk low hai.";

      }

      // =========================
      // FINAL RESULT
      // =========================

      result =
          "📍 स्थान: $city\n\n"
          "🌡️ तापमान: $temp °C\n"
          "💧 नमी: $humidity%\n"
          "☁️ मौसम: $weather\n\n"
          "$risk\n\n"
          "🩺 संभावित समस्याएं:\n$diseases\n\n"
          "🛡️ बचाव:\n$precautions";

      setState(() {});

      // =========================
      // AI VOICE
      // =========================

      await flutterTts.setLanguage("en-US");

      await flutterTts.setPitch(1.1);

      await flutterTts.setSpeechRate(0.45);

      await flutterTts.setVolume(1.0);

      await flutterTts.speak(smartVoice);

    }

    // =========================
    // ERROR
    // =========================

    else {

      setState(() {

        result = "❌ स्थान नहीं मिला";

      });

      await flutterTts.setLanguage("en-US");

      await flutterTts.setPitch(1.1);

      await flutterTts.setSpeechRate(0.45);

      await flutterTts.setVolume(1.0);

      await flutterTts.speak("Location not found");

    }

  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("🌡️ HeatSafe AI"),
        centerTitle: true,
      ),

      body: Padding(

        padding: const EdgeInsets.all(20),

        child: SingleChildScrollView(

          child: Column(

            children: [

              const SizedBox(height: 20),

              const Text(
                "🩺 हिंदी AI क्लाइमेट हेल्थ असिस्टेंट",
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 30),

              TextField(

                controller: cityController,

                decoration: InputDecoration(

                  labelText: "📍 स्थान का नाम लिखें",

                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(15),
                  ),

                ),
              ),

              const SizedBox(height: 20),

              ElevatedButton(

                onPressed: checkHeatRisk,

                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 30,
                    vertical: 15,
                  ),
                ),

                child: const Text(
                  "🔍 हीट रिस्क जांचें",
                  style: TextStyle(fontSize: 18),
                ),
              ),

              const SizedBox(height: 30),

              Text(
                result,
                style: const TextStyle(
                  fontSize: 20,
                ),
              ),

            ],
          ),
        ),
      ),
    );
  }
}