package com.jarvis.ai;

import android.content.Context;
import android.util.Log;
import com.jarvis.ai.models.GeminiResponse;
import com.jarvis.ai.models.UserContext;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class GeminiAIModel {
    
    private static final String API_KEY = "AIzaSyCRqE6NrySBhTPbYAKM3TPJ9qlaDSJNH3E";
    private static final String API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent";
    
    private Context context;
    private ExecutorService executorService;
    
    public GeminiAIModel(Context context) {
        this.context = context;
        this.executorService = Executors.newSingleThreadExecutor();
    }
    
    public String processQuery(String query, UserContext userContext) {
        try {
            String fullUrl = API_URL + "?key=" + API_KEY;
            URL url = new URL(fullUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);
            
            // Create request body
            JSONObject requestBody = new JSONObject();
            JSONArray contents = new JSONArray();
            JSONObject content = new JSONObject();
            JSONArray parts = new JSONArray();
            JSONObject part = new JSONObject();
            
            // Add context to the query
            String contextualQuery = buildContextualQuery(query, userContext);
            part.put("text", contextualQuery);
            parts.put(part);
            content.put("parts", parts);
            contents.put(content);
            requestBody.put("contents", contents);
            
            // Send request
            OutputStream os = connection.getOutputStream();
            os.write(requestBody.toString().getBytes());
            os.flush();
            os.close();
            
            // Read response
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                StringBuilder response = new StringBuilder();
                
                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();
                
                // Parse response
                return parseGeminiResponse(response.toString());
            } else {
                return "Sorry, I couldn't process that request. Error: " + responseCode;
            }
            
        } catch (Exception e) {
            Log.e("GeminiAI", "Error processing query", e);
            return "I encountered an error. Please try again.";
        }
    }
    
    public String generateReply(String message, String platform) {
        String prompt = "Generate a short, professional auto-reply for " + platform + 
                       " message: '" + message + "'. The user is busy and can't reply right now. " +
                       "Keep it polite and under 100 characters.";
        
        return processQuery(prompt, new UserContext());
    }
    
    private String buildContextualQuery(String query, UserContext userContext) {
        StringBuilder contextualQuery = new StringBuilder();
        contextualQuery.append("Context: Current time is ").append(userContext.getTimestamp());
        contextualQuery.append(". Query: ").append(query);
        return contextualQuery.toString();
    }
    
    private String parseGeminiResponse(String jsonResponse) {
        try {
            JSONObject response = new JSONObject(jsonResponse);
            JSONArray candidates = response.getJSONArray("candidates");
            
            if (candidates.length() > 0) {
                JSONObject firstCandidate = candidates.getJSONObject(0);
                JSONObject content = firstCandidate.getJSONObject("content");
                JSONArray parts = content.getJSONArray("parts");
                
                if (parts.length() > 0) {
                    JSONObject firstPart = parts.getJSONObject(0);
                    return firstPart.getString("text");
                }
            }
            
            return "I understand, but I couldn't generate a proper response.";
            
        } catch (Exception e) {
            Log.e("GeminiAI", "Error parsing response", e);
            return "I received a response but couldn't understand it.";
        }
    }
    
    public void processQueryAsync(String query, UserContext userContext, GeminiCallback callback) {
        executorService.execute(() -> {
            String response = processQuery(query, userContext);
            callback.onResponse(response);
        });
    }
    
    public interface GeminiCallback {
        void onResponse(String response);
    }
}
