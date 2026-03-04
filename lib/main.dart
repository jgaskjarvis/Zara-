import 'package:flutter/material.dart';
import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:url_launcher/url_launcher.dart';

void main() => runApp(MaterialApp(home: ZaraApp(), theme: ThemeData.dark()));

class ZaraApp extends StatefulWidget {
  @override
  _ZaraAppState createState() => _ZaraAppState();
}

class _ZaraAppState extends State<ZaraApp> {
  final SpeechToText _speech = SpeechToText();
  final FlutterTts _tts = FlutterTts();
  String _text = "ZARA Online. Press Mic to Speak.";
  
  // Aapki Gemini API Key
  final model = GenerativeModel(model: 'gemini-pro', apiKey: 'AIzaSyCRqE6NrySBhTPbYAKM3TPJ9qlaDSJNH3E');

  void _listen() async {
    bool available = await _speech.initialize();
    if (available) {
      _speech.listen(onResult: (val) {
        if (val.finalResult) _askGemini(val.recognizedWords);
      });
    }
  }

  void _askGemini(String query) async {
    setState(() => _text = "ZARA is thinking...");
    
    // Commands: Instagram aur Zubeen Garg
    if (query.contains("zubeen")) {
      await launchUrl(Uri.parse("https://www.youtube.com/results?search_query=zubeen+garg+songs"));
    } else {
      final content = [Content.text(query)];
      final response = await model.generateContent(content);
      setState(() => _text = response.text!);
      await _tts.speak(response.text!);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text("ZARA MASTER", style: TextStyle(color: Colors.cyan, fontSize: 30, fontWeight: FontWeight.bold)),
            SizedBox(height: 30),
            Padding(
              padding: EdgeInsets.all(20),
              child: Text(_text, textAlign: TextAlign.center, style: TextStyle(fontSize: 18)),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _listen,
        backgroundColor: Colors.cyan,
        child: Icon(Icons.mic),
      ),
    );
  }
}
