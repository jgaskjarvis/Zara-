package com.jarvis.ai;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.AccessibilityServiceInfo;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Build;
import android.os.Bundle;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.widget.Toast;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import java.util.List;

public class JarvisAccessibilityService extends AccessibilityService {
    
    private static final String WHATSAPP_PACKAGE = "com.whatsapp";
    private static final String INSTAGRAM_PACKAGE = "com.instagram.android";
    private static final String TELEGRAM_PACKAGE = "org.telegram.messenger";
    
    private String currentApp = "";
    private String currentMessage = "";
    private String currentSender = "";
    
    @Override
    public void onCreate() {
        super.onCreate();
        
        // Register for auto-reply broadcasts
        LocalBroadcastManager.getInstance(this).registerReceiver(
            autoReplyReceiver,
            new IntentFilter("AUTO_REPLY_ACTION")
        );
    }
    
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() == AccessibilityEvent.TYPE_NOTIFICATION_STATE_CHANGED) {
            handleNotification(event);
        } else if (event.getEventType() == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED) {
            handleWindowChange(event);
        }
    }
    
    private void handleNotification(AccessibilityEvent event) {
        String packageName = event.getPackageName() != null ? event.getPackageName().toString() : "";
        
        if (packageName.equals(WHATSAPP_PACKAGE) || 
            packageName.equals(INSTAGRAM_PACKAGE) || 
            packageName.equals(TELEGRAM_PACKAGE)) {
            
            List<CharSequence> texts = event.getText();
            if (!texts.isEmpty()) {
                String message = texts.get(0).toString();
                String sender = extractSenderFromNotification(event);
                
                currentApp = packageName;
                currentMessage = message;
                currentSender = sender;
                
                // Trigger auto-reply handling
                Intent intent = new Intent("NEW_MESSAGE_DETECTED");
                intent.putExtra("platform", packageName);
                intent.putExtra("message", message);
                intent.putExtra("sender", sender);
                LocalBroadcastManager.getInstance(this).sendBroadcast(intent);
            }
        }
    }
    
    private String extractSenderFromNotification(AccessibilityEvent event) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR2) {
            Bundle extras = event.getParcelableData();
            if (extras != null) {
                String title = extras.getString("android.title");
                if (title != null) {
                    return title;
                }
            }
        }
        return "Unknown";
    }
    
    private void handleWindowChange(AccessibilityEvent event) {
        String packageName = event.getPackageName() != null ? event.getPackageName().toString() : "";
        
        if (packageName.equals(WHATSAPP_PACKAGE) || 
            packageName.equals(INSTAGRAM_PACKAGE)) {
            // We're in a messaging app, check for reply fields
            findAndAutoReply();
        }
    }
    
    private void findAndAutoReply() {
        AccessibilityNodeInfo rootNode = getRootInActiveWindow();
        if (rootNode != null) {
            // Find the reply text field
            List<AccessibilityNodeInfo> textFields = rootNode.findAccessibilityNodeInfosByViewId(
                currentApp.equals(WHATSAPP_PACKAGE) ? 
                    "com.whatsapp:id/entry" : "com.instagram.android:id/direct_text_input"
            );
            
            if (!textFields.isEmpty()) {
                // Store the reply field for later use
                // Implementation depends on specific UI structure
            }
            
            rootNode.recycle();
        }
    }
    
    public void sendReply(String platform, String sender, String reply) {
        AccessibilityNodeInfo rootNode = getRootInActiveWindow();
        if (rootNode == null) return;
        
        if (platform.equals(WHATSAPP_PACKAGE)) {
            sendWhatsAppReply(rootNode, reply);
        } else if (platform.equals(INSTAGRAM_PACKAGE)) {
            sendInstagramReply(rootNode, reply);
        }
        
        rootNode.recycle();
    }
    
    private void sendWhatsAppReply(AccessibilityNodeInfo rootNode, String reply) {
        // Find message input box
        List<AccessibilityNodeInfo> inputNodes = rootNode.findAccessibilityNodeInfosByViewId(
            "com.whatsapp:id/entry"
        );
        
        if (!inputNodes.isEmpty()) {
            AccessibilityNodeInfo inputNode = inputNodes.get(0);
            Bundle arguments = new Bundle();
            arguments.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, reply);
            inputNode.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, arguments);
            
            // Find and click send button
            List<AccessibilityNodeInfo> sendButtons = rootNode.findAccessibilityNodeInfosByViewId(
                "com.whatsapp:id/send"
            );
            
            if (!sendButtons.isEmpty()) {
                sendButtons.get(0).performAction(AccessibilityNodeInfo.ACTION_CLICK);
            }
            
            inputNode.recycle();
        }
    }
    
    private void sendInstagramReply(AccessibilityNodeInfo rootNode, String reply) {
        // Similar implementation for Instagram
        List<AccessibilityNodeInfo> inputNodes = rootNode.findAccessibilityNodeInfosByViewId(
            "com.instagram.android:id/direct_text_input"
        );
        
        if (!inputNodes.isEmpty()) {
            AccessibilityNodeInfo inputNode = inputNodes.get(0);
            Bundle arguments = new Bundle();
            arguments.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, reply);
            inputNode.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, arguments);
            
            // Find send button
            List<AccessibilityNodeInfo> sendButtons = rootNode.findAccessibilityNodeInfosByText("Send");
            if (!sendButtons.isEmpty()) {
                sendButtons.get(0).performAction(AccessibilityNodeInfo.ACTION_CLICK);
            }
            
            inputNode.recycle();
        }
    }
    
    private final BroadcastReceiver autoReplyReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String platform = intent.getStringExtra("platform");
            String sender = intent.getStringExtra("sender");
            String reply = intent.getStringExtra("reply");
            
            sendReply(platform, sender, reply);
        }
    };
    
    @Override
    public void onInterrupt() {
        // Handle interruption
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        LocalBroadcastManager.getInstance(this).unregisterReceiver(autoReplyReceiver);
    }
    
    @Override
    public void onServiceConnected() {
        super.onServiceConnected();
        
        // Configure the accessibility service
        AccessibilityServiceInfo info = new AccessibilityServiceInfo();
        info.eventTypes = AccessibilityEvent.TYPE_NOTIFICATION_STATE_CHANGED |
                         AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED |
                         AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED;
        
        info.feedbackType = AccessibilityServiceInfo.FEEDBACK_GENERIC;
        info.notificationTimeout = 100;
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR2) {
            info.flags = AccessibilityServiceInfo.FLAG_REPORT_VIEW_IDS |
                        AccessibilityServiceInfo.FLAG_RETRIEVE_INTERACTIVE_WINDOWS;
        }
        
        setServiceInfo(info);
        
        Toast.makeText(this, "Jarvis Accessibility Service Connected", Toast.LENGTH_SHORT).show();
    }
}
