package app.tvhome.hogwarts;

import android.app.Activity;
import android.app.SearchManager;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.media.tv.TvContract;
import android.media.tv.TvInputInfo;
import android.media.tv.TvInputManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.webkit.ConsoleMessage;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/**
 * The castle home: the page in assets/www (copied from hogwarts/ by build.sh) in a full-screen WebView.
 * The remote's arrows and OK reach the page as ordinary key presses; Back goes up a section (or closes at the top);
 * the page asks the TV for its apps and inputs, and opens things, through the bridge below.
 */
public class MainActivity extends Activity {

    /** The short names older pages used for the dock apps. */
    private static final Map<String, String> NAMES = new HashMap<>();
    static {
        NAMES.put("netflix", "com.netflix.ninja");
        NAMES.put("prime", "com.amazon.amazonvideo.livingroom");
        NAMES.put("jiohotstar", "in.startv.hotstar");
        NAMES.put("youtube", "com.google.android.youtube.tv");
        NAMES.put("appletv", "com.apple.atve.androidtv.appletv");
        NAMES.put("ps5", "input:playstation");
    }

    private WebView web;
    private boolean isHome;                                // started as the home screen
    private final Map<String, String> icons = new HashMap<>();

    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        isHome = getIntent().hasCategory(Intent.CATEGORY_HOME);
        if ((getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0) WebView.setWebContentsDebuggingEnabled(true);

        web = new WebView(this);
        web.setBackgroundColor(Color.BLACK);
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);
        web.setVerticalScrollBarEnabled(false);
        web.setHorizontalScrollBarEnabled(false);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setAllowFileAccess(true);                       // the page and its pictures live in file:///android_asset
        s.setDomStorageEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        web.addJavascriptInterface(new Bridge(), "TV");
        web.setWebChromeClient(new WebChromeClient() {   // the page's console (its frame-time reports) goes to logcat
            @Override public boolean onConsoleMessage(ConsoleMessage m) {
                Log.i("Castle", m.message());
                return true;
            }
        });
        web.setWebViewClient(new WebViewClient() {        // nothing ever navigates away from the page
            @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) { return true; }
        });
        setContentView(web);
        web.loadUrl("file:///android_asset/www/index.html");
        web.requestFocus();
    }

    @Override public boolean dispatchKeyEvent(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.KEYCODE_BACK) {
            if (e.getAction() == KeyEvent.ACTION_UP)
                // up a section (or out of the Customise panel); at the top, close, unless this is the home screen
                web.evaluateJavascript("window.tvBack ? tvBack() : false", handled -> { if (!"true".equals(handled) && !isHome) finish(); });
            return true;
        }
        return super.dispatchKeyEvent(e);
    }

    /** Home pressed while we're the home screen: back to the castle. */
    @Override protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        if (intent.hasCategory(Intent.CATEGORY_HOME)) { isHome = true; web.evaluateJavascript("window.tvHome && tvHome()", null); }
    }

    @Override protected void onResume() { super.onResume(); web.onResume(); web.requestFocus(); }
    @Override protected void onPause() { web.onPause(); super.onPause(); }
    @Override protected void onDestroy() { web.destroy(); super.onDestroy(); }

    /** What the page can ask the TV to do. */
    private final class Bridge {
        /** Open a dock entry: an app's package, or "input:<name>" for an HDMI port. */
        @JavascriptInterface public void launch(String target) { runOnUiThread(() -> open(target)); }

        /** A film: its link in that app if there is one, else that app's search, else the TV's search. */
        @JavascriptInterface public void openFilm(String url, String pkg, String title) {
            runOnUiThread(() -> {
                boolean isLink = url != null && (url.startsWith("https://") || url.startsWith("http://"));
                if (pkg == null || pkg.isEmpty() || "search".equals(pkg) || !installed(pkg)) { search(title, null); return; }
                if (isLink && start(new Intent(Intent.ACTION_VIEW, Uri.parse(url)).setPackage(pkg))) return;
                search(title, pkg);
            });
        }

        /** Search the TV for a title (or search inside one app, when pkg is given). */
        @JavascriptInterface public void search(String query, String pkg) { runOnUiThread(() -> MainActivity.this.search(query, pkg)); }

        /** The TV's apps, as [{pkg, label, media}], sorted by name (this app left out). media: an app you'd watch or
         *  play something in (one you installed or that updates from the store, or one that says it's video, audio or a
         *  game), rather than one of the TV's own tools. */
        @JavascriptInterface public String apps() {
            PackageManager pm = getPackageManager();
            Map<String, ApplicationInfo> found = new LinkedHashMap<>();
            for (String cat : new String[] { Intent.CATEGORY_LEANBACK_LAUNCHER, Intent.CATEGORY_LAUNCHER }) {
                for (ResolveInfo r : pm.queryIntentActivities(new Intent(Intent.ACTION_MAIN).addCategory(cat), 0)) {
                    String p = r.activityInfo.packageName;
                    if (p.equals(getPackageName()) || found.containsKey(p)) continue;
                    found.put(p, r.activityInfo.applicationInfo);
                }
            }
            List<JSONObject> list = new ArrayList<>();
            for (Map.Entry<String, ApplicationInfo> e : found.entrySet()) {
                ApplicationInfo ai = e.getValue();
                boolean tool = (ai.flags & ApplicationInfo.FLAG_SYSTEM) != 0 && (ai.flags & ApplicationInfo.FLAG_UPDATED_SYSTEM_APP) == 0;
                if (Build.VERSION.SDK_INT >= 26 && (ai.category == ApplicationInfo.CATEGORY_VIDEO || ai.category == ApplicationInfo.CATEGORY_AUDIO
                        || ai.category == ApplicationInfo.CATEGORY_GAME)) tool = false;
                JSONObject o = obj("pkg", e.getKey(), "label", String.valueOf(ai.loadLabel(pm)));
                try { o.put("media", !tool); } catch (JSONException ignored) { }
                list.add(o);
            }
            list.sort((a, b) -> a.optString("label").compareToIgnoreCase(b.optString("label")));
            JSONArray out = new JSONArray();
            for (JSONObject o : list) out.put(o);
            return out.toString();
        }

        /** The TV's HDMI ports, as [{id, label}]: a port with an HDMI-CEC device is named after the device. */
        @JavascriptInterface public String inputs() {
            JSONArray out = new JSONArray();
            TvInputManager tim = (TvInputManager) getSystemService(Context.TV_INPUT_SERVICE);
            if (tim == null) return out.toString();
            Map<String, String> ports = new LinkedHashMap<>();
            for (TvInputInfo i : tim.getTvInputList())
                if (i.getType() == TvInputInfo.TYPE_HDMI && i.getParentId() == null) ports.put(i.getId(), label(i));
            for (TvInputInfo i : tim.getTvInputList())     // CEC devices hang off their port
                if (i.getParentId() != null && ports.containsKey(i.getParentId()))
                    ports.put(i.getParentId(), label(i) + " · " + ports.get(i.getParentId()));
            for (Map.Entry<String, String> e : ports.entrySet()) out.put(obj("id", e.getKey(), "label", e.getValue()));
            return out.toString();
        }

        /** An app's TV banner (or else its icon) as a PNG data URL, for the Customise panel. */
        @JavascriptInterface public String icon(String pkg) {
            if (icons.containsKey(pkg)) return icons.get(pkg);
            String url = "";
            try {
                PackageManager pm = getPackageManager();
                ApplicationInfo ai = pm.getApplicationInfo(pkg, 0);
                Drawable d = ai.loadBanner(pm);
                boolean banner = d != null;
                if (!banner) d = ai.loadIcon(pm);
                int w = banner ? 240 : 120, h = banner ? 135 : 120;
                Bitmap b = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
                d.setBounds(0, 0, w, h);
                d.draw(new Canvas(b));
                ByteArrayOutputStream png = new ByteArrayOutputStream();
                b.compress(Bitmap.CompressFormat.PNG, 100, png);
                url = (banner ? "banner:" : "icon:") + "data:image/png;base64," + Base64.encodeToString(png.toByteArray(), Base64.NO_WRAP);
            } catch (PackageManager.NameNotFoundException | RuntimeException e) {
                url = "";
            }
            icons.put(pkg, url);
            return url;
        }

        /** Whether a dock entry exists on this TV (an installed app, or an HDMI port that resolves). */
        @JavascriptInterface public boolean has(String target) {
            target = alias(target);
            return target.startsWith("input:") ? resolveInput(target.substring(6)) != null : installed(target);
        }

        /** The Customise panel's choices, kept with the app (the page's own storage is a fallback). */
        @JavascriptInterface public String loadConfig() { return prefs().getString("config", ""); }
        @JavascriptInterface public void saveConfig(String json) { prefs().edit().putString("config", json).apply(); }
    }

    private SharedPreferences prefs() { return getSharedPreferences("castle", MODE_PRIVATE); }

    private static String alias(String target) { String t = NAMES.get(target); return t != null ? t : target; }

    private String label(TvInputInfo i) {
        CharSequence l = i.loadLabel(this);
        return l == null ? i.getId() : l.toString();
    }

    private static JSONObject obj(String k1, String v1, String k2, String v2) {
        JSONObject o = new JSONObject();
        try { o.put(k1, v1); o.put(k2, v2); } catch (JSONException ignored) { }
        return o;
    }

    private boolean installed(String pkg) {
        try { getPackageManager().getApplicationInfo(pkg, 0); return true; }
        catch (PackageManager.NameNotFoundException e) { return false; }
    }

    /** An HDMI port: the exact TV input id, or the port whose (CEC device) name contains the given name. */
    private String resolveInput(String name) {
        TvInputManager tim = (TvInputManager) getSystemService(Context.TV_INPUT_SERVICE);
        if (tim == null) return null;
        if (tim.getTvInputInfo(name) != null) return name;
        String want = name.toLowerCase(Locale.ROOT);
        boolean playstation = want.contains("playstation") || want.matches(".*\\bps[345]\\b.*");
        for (TvInputInfo i : tim.getTvInputList()) {
            if (i.getType() != TvInputInfo.TYPE_HDMI && i.getParentId() == null) continue;
            String l = label(i).toLowerCase(Locale.ROOT);
            if (l.contains(want) || (playstation && (l.contains("playstation") || l.matches(".*\\bps[345]\\b.*"))))
                return i.getParentId() != null ? i.getParentId() : i.getId();
        }
        if (playstation) {                                // the port named in strings.xml, if this TV has it
            String id = getString(R.string.ps5_input);
            if (tim.getTvInputInfo(id) != null) return id;
        }
        return null;
    }

    private void open(String target) {
        target = alias(target);
        if (target.startsWith("input:")) {                // an HDMI port, not an app
            String id = resolveInput(target.substring(6));
            if (id == null || !start(new Intent(Intent.ACTION_VIEW, TvContract.buildChannelUriForPassthroughInput(id))))
                Toast.makeText(this, "Couldn't switch to that input", Toast.LENGTH_SHORT).show();
            return;
        }
        PackageManager pm = getPackageManager();
        Intent i = pm.getLeanbackLaunchIntentForPackage(target);
        if (i == null) i = pm.getLaunchIntentForPackage(target);
        if (i == null || !start(i)) Toast.makeText(this, "That app isn't on this TV", Toast.LENGTH_SHORT).show();
    }

    /** Inside one app if it takes a search, else that app opened; with no app, the TV's own search. */
    private void search(String query, String pkg) {
        if (pkg != null && !pkg.isEmpty()) {
            if (start(new Intent(Intent.ACTION_SEARCH).setPackage(pkg).putExtra(SearchManager.QUERY, query))) return;
            PackageManager pm = getPackageManager();
            Intent i = pm.getLeanbackLaunchIntentForPackage(pkg);
            if (i == null) i = pm.getLaunchIntentForPackage(pkg);
            if (i != null && start(i)) {
                Toast.makeText(this, "Search for " + query, Toast.LENGTH_LONG).show();
                return;
            }
        }
        if (start(new Intent("android.search.action.GLOBAL_SEARCH").putExtra(SearchManager.QUERY, query))) return;
        if (start(new Intent(Intent.ACTION_WEB_SEARCH).putExtra(SearchManager.QUERY, query))) return;
        Toast.makeText(this, "This TV has no search to open", Toast.LENGTH_SHORT).show();
    }

    private boolean start(Intent i) {
        try {
            i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(i);
            return true;
        } catch (ActivityNotFoundException | SecurityException e) {
            return false;
        }
    }
}
