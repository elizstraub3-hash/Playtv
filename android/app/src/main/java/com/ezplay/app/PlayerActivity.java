package com.ezplay.app;

import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.View;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import androidx.activity.OnBackPressedCallback;
import androidx.annotation.NonNull;
import androidx.annotation.OptIn;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import androidx.media3.common.C;
import androidx.media3.common.MediaItem;
import androidx.media3.common.MediaMetadata;
import androidx.media3.common.PlaybackException;
import androidx.media3.common.Player;
import androidx.media3.common.util.UnstableApi;
import androidx.media3.datasource.DefaultDataSource;
import androidx.media3.datasource.DefaultHttpDataSource;
import androidx.media3.exoplayer.DefaultRenderersFactory;
import androidx.media3.exoplayer.ExoPlayer;
import androidx.media3.exoplayer.source.DefaultMediaSourceFactory;
import androidx.media3.ui.PlayerView;
import java.util.ArrayList;

/** Player em tela cheia. Ao vivo: ▲/▼ ou CH+/CH− trocam de canal. Filmes/séries: retoma a posição. */
@OptIn(markerClass = UnstableApi.class)
public class PlayerActivity extends AppCompatActivity {

    private ExoPlayer player;
    private PlayerView view;
    private TextView titleView, subView, msgView, zapView;
    private LinearLayout topBar;
    private ArrayList<String> urls, titles, subs;
    private int index;
    private boolean live, autoNext, hadError;
    private long startMs;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private final Runnable hideZap = () -> zapView.setVisibility(View.GONE);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        WindowInsetsControllerCompat ic = WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
        ic.hide(WindowInsetsCompat.Type.systemBars());
        ic.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);

        Intent in = getIntent();
        urls = in.getStringArrayListExtra("urls");
        titles = in.getStringArrayListExtra("titles");
        subs = in.getStringArrayListExtra("subs");
        index = in.getIntExtra("index", 0);
        live = in.getBooleanExtra("live", false);
        autoNext = in.getBooleanExtra("autoNext", false);
        startMs = in.getLongExtra("startMs", 0);
        if (urls == null || urls.isEmpty()) { finish(); return; }

        buildLayout();

        DefaultHttpDataSource.Factory http = new DefaultHttpDataSource.Factory()
                .setUserAgent("EZPlay/2.0 (Linux; Android) ExoPlayer")
                .setAllowCrossProtocolRedirects(true)
                .setConnectTimeoutMs(15000)
                .setReadTimeoutMs(20000);
        DefaultDataSource.Factory data = new DefaultDataSource.Factory(this, http);
        DefaultRenderersFactory renderers = new DefaultRenderersFactory(this)
                .setEnableDecoderFallback(true)
                .setExtensionRendererMode(DefaultRenderersFactory.EXTENSION_RENDERER_MODE_PREFER);
        player = new ExoPlayer.Builder(this, renderers)
                .setMediaSourceFactory(new DefaultMediaSourceFactory(data))
                .build();
        view.setPlayer(player);
        player.addListener(new Player.Listener() {
            @Override public void onPlayerError(@NonNull PlaybackException error) {
                hadError = true;
                msgView.setText(live
                        ? "Não foi possível abrir este canal.\nUse ▲ ▼ para trocar de canal ou Voltar para sair."
                        : "Não foi possível reproduzir este conteúdo.\nO link pode estar fora do ar.");
                msgView.setVisibility(View.VISIBLE);
            }
            @Override public void onPlaybackStateChanged(int state) {
                if (state == Player.STATE_READY) { msgView.setVisibility(View.GONE); hadError = false; }
                if (state == Player.STATE_ENDED && !live) {
                    if (autoNext && index + 1 < urls.size()) { startMs = 0; load(index + 1); }
                    else finishWithResult();
                }
            }
        });
        view.setControllerVisibilityListener((PlayerView.ControllerVisibilityListener) v -> topBar.setVisibility(v));

        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override public void handleOnBackPressed() { finishWithResult(); }
        });
        load(index);
    }

    private void buildLayout() {
        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(Color.BLACK);
        view = new PlayerView(this);
        view.setKeepContentOnPlayerReset(true);
        view.setShowBuffering(PlayerView.SHOW_BUFFERING_ALWAYS);
        root.addView(view, new FrameLayout.LayoutParams(-1, -1));

        int pad = dp(20);
        topBar = new LinearLayout(this);
        topBar.setOrientation(LinearLayout.VERTICAL);
        topBar.setPadding(pad, pad, pad, dp(36));
        topBar.setBackground(new android.graphics.drawable.GradientDrawable(
                android.graphics.drawable.GradientDrawable.Orientation.TOP_BOTTOM,
                new int[]{0xCC000000, 0x00000000}));
        titleView = text(20, true, Color.WHITE);
        subView = text(14, false, 0xFFC8C2D6);
        topBar.addView(titleView);
        topBar.addView(subView);
        root.addView(topBar, new FrameLayout.LayoutParams(-1, -2, Gravity.TOP));

        msgView = text(16, false, Color.WHITE);
        msgView.setGravity(Gravity.CENTER);
        msgView.setPadding(pad, pad, pad, pad);
        msgView.setBackgroundColor(0xE61B1726);
        msgView.setVisibility(View.GONE);
        FrameLayout.LayoutParams mp = new FrameLayout.LayoutParams(-2, -2, Gravity.CENTER);
        mp.setMargins(pad, pad, pad, pad);
        root.addView(msgView, mp);

        zapView = text(22, true, Color.WHITE);
        zapView.setPadding(dp(18), dp(10), dp(18), dp(10));
        zapView.setBackgroundColor(0xE61B1726);
        zapView.setVisibility(View.GONE);
        FrameLayout.LayoutParams zp = new FrameLayout.LayoutParams(-2, -2, Gravity.TOP | Gravity.END);
        zp.setMargins(pad, pad, pad, pad);
        root.addView(zapView, zp);

        setContentView(root);
    }

    private TextView text(int sp, boolean bold, int color) {
        TextView t = new TextView(this);
        t.setTextSize(sp);
        t.setTextColor(color);
        t.setMaxLines(2);
        if (bold) t.setTypeface(Typeface.DEFAULT_BOLD);
        return t;
    }

    private int dp(int v) { return Math.round(v * getResources().getDisplayMetrics().density); }

    private void load(int i) {
        index = (i + urls.size()) % urls.size();
        String title = titles != null && index < titles.size() ? titles.get(index) : "";
        String sub = subs != null && index < subs.size() ? subs.get(index) : "";
        titleView.setText(title);
        subView.setText(sub);
        subView.setVisibility(sub.isEmpty() ? View.GONE : View.VISIBLE);
        msgView.setVisibility(View.GONE);
        MediaItem item = new MediaItem.Builder()
                .setUri(Uri.parse(urls.get(index)))
                .setMediaMetadata(new MediaMetadata.Builder().setTitle(title).build())
                .setLiveConfiguration(new MediaItem.LiveConfiguration.Builder().setTargetOffsetMs(live ? 8000 : C.TIME_UNSET).build())
                .build();
        if (startMs > 0 && !live) player.setMediaItem(item, startMs);
        else player.setMediaItem(item);
        player.prepare();
        player.play();
    }

    private void zap(int d) {
        if (urls.size() < 2) return;
        load(index + d);
        zapView.setText((index + 1) + "  " + titleView.getText());
        zapView.setVisibility(View.VISIBLE);
        handler.removeCallbacks(hideZap);
        handler.postDelayed(hideZap, 2500);
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        boolean controllerOpen = view.isControllerFullyVisible();
        if (live && !controllerOpen) {
            if (keyCode == KeyEvent.KEYCODE_DPAD_UP || keyCode == KeyEvent.KEYCODE_CHANNEL_UP) { zap(-1); return true; }
            if (keyCode == KeyEvent.KEYCODE_DPAD_DOWN || keyCode == KeyEvent.KEYCODE_CHANNEL_DOWN) { zap(1); return true; }
        } else if (live && (keyCode == KeyEvent.KEYCODE_CHANNEL_UP || keyCode == KeyEvent.KEYCODE_CHANNEL_DOWN)) {
            zap(keyCode == KeyEvent.KEYCODE_CHANNEL_UP ? -1 : 1); return true;
        }
        if (!live && !controllerOpen) {
            if (keyCode == KeyEvent.KEYCODE_DPAD_RIGHT) { player.seekTo(player.getCurrentPosition() + 10000); view.showController(); return true; }
            if (keyCode == KeyEvent.KEYCODE_DPAD_LEFT) { player.seekTo(Math.max(0, player.getCurrentPosition() - 10000)); view.showController(); return true; }
        }
        if (keyCode == KeyEvent.KEYCODE_DPAD_CENTER || keyCode == KeyEvent.KEYCODE_ENTER) {
            if (!controllerOpen) { view.showController(); return true; }
        }
        return super.onKeyDown(keyCode, event);
    }

    private void finishWithResult() {
        Intent data = new Intent();
        if (player != null) {
            long dur = player.getDuration();
            data.putExtra("position", player.getCurrentPosition());
            data.putExtra("duration", dur == C.TIME_UNSET ? 0 : dur);
        }
        data.putExtra("index", index);
        data.putExtra("error", hadError);
        setResult(RESULT_OK, data);
        finish();
    }

    @Override protected void onPause() { super.onPause(); if (player != null) player.pause(); }
    @Override protected void onResume() { super.onResume(); if (player != null && !hadError) player.play(); }
    @Override protected void onDestroy() {
        handler.removeCallbacksAndMessages(null);
        if (player != null) { player.release(); player = null; }
        super.onDestroy();
    }
}
