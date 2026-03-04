package com.jarvis.ai;

import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.SwitchCompat;

public class MainActivity extends AppCompatActivity {
    
    private JarvisAssistant jarvisAssistant;
    private WakeWordDetector wakeWordDetector;
    private SwitchCompat busyModeSwitch;
    private SwitchCompat dndModeSwitch;
    private TextView statusText;
    private Button accessibilitySetupBtn;
    private TextView networkStatusText;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        initializeViews();
        setupJarvis();
        checkPermissions();
        updateNetworkStatus();
    }
    
    private void initializeViews() {
        busyModeSwitch = findViewById(R.id.switch_busy_mode);
        dndModeSwitch = findViewById(R.id.switch_dnd_mode);
        statusText = findViewById(R.id.tv_status);
        accessibilitySetupBtn = findViewById(R.id.btn_accessibility_setup);
        networkStatusText = findViewById(R.id.tv_network_status);
        
        busyModeSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> {
            if (jarvisAssistant != null) {
                jarvisAssistant.setUserBusy(isChecked);
                updateStatus(isChecked ? "Busy Mode: ON" : "Busy Mode: OFF");
            }
        });
        
        dndModeSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> {
            if (jarvisAssistant != null) {
                jarvisAssistant.setDoNotDisturb(isChecked);
                updateStatus(isChecked ? "DND Mode: ON" : "DND Mode: OFF");
            }
        });
        
        accessibilitySetupBtn.setOnClickListener(v -> {
            openAccessibilitySettings();
        });
    }
    
    private void setupJarvis() {
        jarvisAssistant = new JarvisAssistant(this);
        wakeWordDetector = new WakeWordDetector(this, new WakeWordDetector.WakeWordListener() {
            @Override
            public void onWakeWordDetected() {
                runOnUiThread(() -> {
                    statusText.setText("Wake word detected! Listening...");
                    jarvisAssistant.onWakeWordDetected();
                });
            }
        });
        
        // Start listening for wake word
        wakeWordDetector.startListening();
    }
    
    private void updateStatus(String status) {
        statusText.setText(status);
    }
    
    private void checkPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!Settings.canDrawOverlays(this)) {
                Intent intent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                        Uri.parse("package:" + getPackageName()));
                startActivity(intent);
            }
        }
    }
    
    private void openAccessibilitySettings() {
        Intent intent = new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS);
        startActivity(intent);
        Toast.makeText(this, "Please enable Jarvis AI Accessibility Service", Toast.LENGTH_LONG).show();
    }
    
    private void updateNetworkStatus() {
        if (NetworkUtils.isNetworkAvailable(this)) {
            networkStatusText.setText("● Online");
            networkStatusText.setTextColor(getColor(android.R.color.holo_green_dark));
        } else {
            networkStatusText.setText("● Offline");
            networkStatusText.setTextColor(getColor(android.R.color.holo_red_dark));
        }
    }
    
    @Override
    protected void onResume() {
        super.onResume();
        updateNetworkStatus();
        checkAccessibilityServiceStatus();
    }
    
    private void checkAccessibilityServiceStatus() {
        boolean isAccessibilityEnabled = isAccessibilityServiceEnabled();
        if (!isAccessibilityEnabled) {
            accessibilitySetupBtn.setVisibility(View.VISIBLE);
        } else {
            accessibilitySetupBtn.setVisibility(View.GONE);
        }
    }
    
    private boolean isAccessibilityServiceEnabled() {
        String service = getPackageName() + "/" + JarvisAccessibilityService.class.getCanonicalName();
        try {
            String enabledServices = Settings.Secure.getString(
                    getContentResolver(),
                    Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES);
            return enabledServices != null && enabledServices.contains(service);
        } catch (Exception e) {
            return false;
        }
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (wakeWordDetector != null) {
            wakeWordDetector.stopListening();
        }
    }
                                             }
