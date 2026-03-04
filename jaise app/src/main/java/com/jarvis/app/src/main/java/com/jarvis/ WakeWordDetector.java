package com.jarvis.ai;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;
import edu.cmu.pocketsphinx.*;
import java.io.File;
import java.io.IOException;

public class WakeWordDetector implements RecognitionListener {
    
    private static final String WAKE_WORD = "jarvis";
    private static final String KEYPHRASE = "wakeup";
    
    private Context context;
    private SpeechRecognizer recognizer;
    private WakeWordListener listener;
    private boolean isListening = false;
    
    public interface WakeWordListener {
        void onWakeWordDetected();
    }
    
    public WakeWordDetector(Context context, WakeWordListener listener) {
        this.context = context;
        this.listener = listener;
        initRecognizer();
    }
    
    private void initRecognizer() {
        try {
            // Create assets directory and copy models
            File assetsDir = new File(context.getFilesDir(), "sync");
            if (!assetsDir.exists()) {
                assetsDir.mkdir();
            }
            
            // Copy default acoustic model from assets
            Assets assets = new Assets(context);
            File modelDir = assets.syncAssets();
            
            // Setup recognizer
            recognizer = SpeechRecognizerSetup.defaultSetup()
                    .setAcousticModel(new File(modelDir, "en-us-ptm"))
                    .setDictionary(new File(modelDir, "cmudict-en-us.dict"))
                    .setKeywordThreshold(1e-45f)
                    .getRecognizer();
            
            recognizer.addListener(this);
            
            // Create keyword search
            recognizer.addKeyphraseSearch(KEYPHRASE, WAKE_WORD);
            
        } catch (IOException e) {
            Log.e("WakeWordDetector", "Error initializing recognizer", e);
        }
    }
    
    public void startListening() {
        if (recognizer != null && !isListening) {
            recognizer.startListening(KEYPHRASE);
            isListening = true;
        }
    }
    
    public void stopListening() {
        if (recognizer != null && isListening) {
            recognizer.stop();
            isListening = false;
        }
    }
    
    @Override
    public void onBeginningOfSpeech() {
        // Speech started
    }
    
    @Override
    public void onEndOfSpeech() {
        // Speech ended, restart listening
        if (isListening) {
            recognizer.startListening(KEYPHRASE);
        }
    }
    
    @Override
    public void onPartialResult(Hypothesis hypothesis) {
        if (hypothesis == null) return;
        
        String text = hypothesis.getHypstr();
        if (text.equalsIgnoreCase(WAKE_WORD)) {
            if (listener != null) {
                listener.onWakeWordDetected();
            }
        }
    }
    
    @Override
    public void onResult(Hypothesis hypothesis) {
        // Final result
    }
    
    @Override
    public void onError(Exception e) {
        Log.e("WakeWordDetector", "Recognition error", e);
    }
    
    @Override
    public void onTimeout() {
        // Restart listening on timeout
        if (isListening) {
            recognizer.startListening(KEYPHRASE);
        }
    }
}
