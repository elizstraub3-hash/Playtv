package com.ezplay.app;

import android.content.Intent;
import androidx.activity.result.ActivityResult;
import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.ActivityCallback;
import com.getcapacitor.annotation.CapacitorPlugin;
import java.util.ArrayList;
import org.json.JSONObject;

/** Abre o player nativo (Media3/ExoPlayer) e devolve posição e item atual ao fechar. */
@CapacitorPlugin(name = "NativePlayer")
public class NativePlayerPlugin extends Plugin {

    @PluginMethod
    public void play(PluginCall call) {
        JSArray items = call.getArray("items");
        if (items == null || items.length() == 0) {
            call.reject("Nenhum item para reproduzir");
            return;
        }
        ArrayList<String> urls = new ArrayList<>();
        ArrayList<String> titles = new ArrayList<>();
        ArrayList<String> subs = new ArrayList<>();
        try {
            for (int i = 0; i < items.length(); i++) {
                JSONObject o = items.getJSONObject(i);
                urls.add(o.optString("url", ""));
                titles.add(o.optString("title", ""));
                subs.add(o.optString("sub", ""));
            }
        } catch (Exception e) {
            call.reject("Lista inválida");
            return;
        }
        Intent intent = new Intent(getContext(), PlayerActivity.class);
        intent.putStringArrayListExtra("urls", urls);
        intent.putStringArrayListExtra("titles", titles);
        intent.putStringArrayListExtra("subs", subs);
        intent.putExtra("index", call.getInt("index", 0));
        intent.putExtra("live", Boolean.TRUE.equals(call.getBoolean("live", false)));
        intent.putExtra("autoNext", Boolean.TRUE.equals(call.getBoolean("autoNext", false)));
        Double start = call.getDouble("startPosition", 0.0);
        intent.putExtra("startMs", (long) ((start == null ? 0 : start) * 1000));
        startActivityForResult(call, intent, "onPlayerClosed");
    }

    @ActivityCallback
    private void onPlayerClosed(PluginCall call, ActivityResult result) {
        if (call == null) return;
        JSObject ret = new JSObject();
        Intent data = result.getData();
        ret.put("position", data != null ? data.getLongExtra("position", 0) / 1000.0 : 0);
        ret.put("duration", data != null ? data.getLongExtra("duration", 0) / 1000.0 : 0);
        ret.put("index", data != null ? data.getIntExtra("index", 0) : 0);
        ret.put("error", data != null && data.getBooleanExtra("error", false));
        call.resolve(ret);
    }
}
