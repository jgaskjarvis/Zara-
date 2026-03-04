package com.jarvis.ai;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.speech.RecognizerIntent;
import android.telephony.PhoneCall;
import android.widget.Toast;
import androidx.core.app.ActivityCompat;
import com.jarvis.ai.models.UserContext;
import com.jarvis.ai.utils.NetworkUtils;
import com.jarvis.ai.utils.TextToSpeechHelper;
import java.util.List;

public class JarvisAssistant {
    
    private Context context;
    private GeminiAIModel geminiBrain;
    private TextToSpeechHelper ttsHelper;
    private boolean isUserBusy = false;
    private boolean isDoNotDisturb = false;
    
    // App package constants
    public static final String WHATSAPP_PACKAGE = "com.whatsapp";
    public static final String INSTAGRAM_PACKAGE = "com.instagram.android";
    public static final String TELEGRAM_PACKAGE = "org.telegram.messenger";
    public static final String YOUTUBE_PACKAGE = "com.google.android.youtube";
    
    public JarvisAssistant(Context context) {
        this.context = context;
        this.ttsHelper = new TextToSpeechHelper(context);
        this.geminiBrain = new GeminiAIModel(context);
    }
    
    public void onWakeWordDetected() {
        ttsHelper.speak("Yes, I'm listening");
        
        if (NetworkUtils.isNetworkAvailable(context)) {
            activateGeminiOnlineMode();
        } else {
            activateOfflineMode();
        }
    }
    
    private void activateGeminiOnlineMode() {
        ttsHelper.speak("Online mode activated. How can I help you?");
        // Start voice recognition
        startVoiceRecognition();
    }
    
    private void activateOfflineMode() {
        ttsHelper.speak("Offline mode activated. Available commands: Call, YouTube, Tracker");
        startVoiceRecognition();
    }
    
    private void startVoiceRecognition() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak command...");
        
        if (context instanceof MainActivity) {
            ((MainActivity) context).startActivityForResult(intent, 100);
        }
    }
    
    public void processVoiceCommand(String command) {
        if (NetworkUtils.isNetworkAvailable(context)) {
            // Use Gemini for processing
            String response = geminiBrain.processQuery(command, getUserContext());
            ttsHelper.speak(response);
            
            // Execute any action if needed
            if (command.contains("call")) {
                handlePhoneControl(command);
            } else if (command.contains("open")) {
                handlePhoneControl(command);
            }
        } else {
            // Offline command processing
            executeOfflineCommand(command);
        }
    }
    
    public void handleAutoReply(String incomingMessage, String sender, String platform) {
        if (isUserBusy && !isDoNotDisturb) {
            String reply = generateSmartReply(incomingMessage, platform);
            sendDirectReply(platform, sender, reply);
        } else if (isDoNotDisturb) {
            // Queue message for later
            queueMessageForLater(incomingMessage, sender, platform);
        }
    }
    
    private String generateSmartReply(String incomingMessage, String platform) {
        if (NetworkUtils.isNetworkAvailable(context)) {
            return geminiBrain.generateReply(incomingMessage, platform);
        } else {
            return getOfflineAutoReply(incomingMessage);
        }
    }
    
    private String getOfflineAutoReply(String message) {
        // Simple offline replies
        if (message.toLowerCase().contains("hello") || message.toLowerCase().contains("hi")) {
            return "Hi! I'm Jarvis. My boss is busy right now. I'll let them know you messaged.";
        } else if (message.toLowerCase().contains("urgent")) {
            return "This seems urgent. I'll notify my boss immediately.";
        } else {
            return "Thanks for your message. My boss is currently busy and will get back to you soon.";
        }
    }
    
    private void sendDirectReply(String platform, String sender, String reply) {
        // This will be handled by AccessibilityService
        Intent intent = new Intent("AUTO_REPLY_ACTION");
        intent.putExtra("platform", platform);
        intent.putExtra("sender", sender);
        intent.putExtra("reply", reply);
        context.sendBroadcast(intent);
    }
    
    private void queueMessageForLater(String message, String sender, String platform) {
        // Store in SharedPreferences for later
        // Implementation here
    }
    
    public void handlePhoneControl(String command) {
        if (command.contains("call")) {
            makePhoneCall(command);
        } else if (command.contains("open youtube")) {
            openApp(YOUTUBE_PACKAGE);
        } else if (command.contains("open whatsapp")) {
            openApp(WHATSAPP_PACKAGE);
        } else if (command.contains("open instagram")) {
            openApp(INSTAGRAM_PACKAGE);
        }
    }
    
    private void makePhoneCall(String command) {
        // Extract phone number or contact name from command
        String number = extractPhoneNumber(command);
        
        if (number != null) {
            Intent callIntent = new Intent(Intent.ACTION_CALL);
            callIntent.setData(Uri.parse("tel:" + number));
            callIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            
            if (ActivityCompat.checkSelfPermission(context, android.Manifest.permission.CALL_PHONE) 
                    == PackageManager.PERMISSION_GRANTED) {
                context.startActivity(callIntent);
            } else {
                ttsHelper.speak("I don't have permission to make calls");
            }
        } else {
            ttsHelper.speak("Please specify who to call");
        }
    }
    
    private String extractPhoneNumber(String command) {
        // Simple extraction - in production, use regex or NLP
        String[] words = command.split(" ");
        for (String word : words) {
            if (word.matches("\\d+")) {
                return word;
            }
        }
        return null;
    }
    
    private void openApp(String packageName) {
        Intent launchIntent = context.getPackageManager()
                .getLaunchIntentForPackage(packageName);
        
        if (launchIntent != null) {
            launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(launchIntent);
            ttsHelper.speak("Opening app");
        } else {
            ttsHelper.speak("App not installed");
        }
    }
    
    private UserContext getUserContext() {
        UserContext context = new UserContext();
        context.setTimestamp(System.currentTimeMillis());
        return context;
    }
    
    public void setUserBusy(boolean busy) {
        this.isUserBusy = busy;
        if (busy) {
            ttsHelper.speak("Auto-reply activated");
        } else {
            ttsHelper.speak("Auto-reply deactivated");
        }
    }
    
    public void setDoNotDisturb(boolean dnd) {
        this.isDoNotDisturb = dnd;
        if (dnd) {
            ttsHelper.speak("Do not disturb mode activated");
        } else {
            ttsHelper.speak("Do not disturb mode deactivated");
        }
    }
  }
