import os
p='android/app/src/main/AndroidManifest.xml'
s=open(p).read()
perms='''    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28" />
    <uses-feature android:name="android.hardware.camera" android:required="false" />
'''
s=s.replace('<application',perms+'    <application',1)
open(p,'w').write(s)
d='android/app/src/main/java/in/edu/siwscollege/geotag'
os.makedirs(d,exist_ok=True)
open(d+'/MainActivity.java','w').write(r'''package in.edu.siwscollege.geotag;
import android.os.Bundle;
import com.getcapacitor.BridgeActivity;
public class MainActivity extends BridgeActivity {
  @Override
  public void onCreate(Bundle savedInstanceState) {
    registerPlugin(GallerySaverPlugin.class);
    super.onCreate(savedInstanceState);
  }
}
''')
open(d+'/GallerySaverPlugin.java','w').write(r'''package in.edu.siwscollege.geotag;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.net.Uri;
import android.os.Build;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import java.io.OutputStream;

@CapacitorPlugin(name = "GallerySaver")
public class GallerySaverPlugin extends Plugin {
  @PluginMethod
  public void save(PluginCall call) {
    try {
      byte[] bytes = Base64.decode(call.getString("data"), Base64.DEFAULT);
      String name = call.getString("name");
      ContentResolver r = getContext().getContentResolver();
      ContentValues v = new ContentValues();
      v.put(MediaStore.Images.Media.DISPLAY_NAME, name);
      v.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg");
      if (Build.VERSION.SDK_INT >= 29) {
        v.put(MediaStore.Images.Media.RELATIVE_PATH, Environment.DIRECTORY_PICTURES + "/SIWS-GeoTag");
        v.put(MediaStore.Images.Media.IS_PENDING, 1);
      }
      Uri u = r.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, v);
      if (u == null) { call.reject("Could not create file"); return; }
      OutputStream o = r.openOutputStream(u);
      o.write(bytes);
      o.close();
      if (Build.VERSION.SDK_INT >= 29) {
        ContentValues w = new ContentValues();
        w.put(MediaStore.Images.Media.IS_PENDING, 0);
        r.update(u, w, null, null);
      }
      call.resolve();
    } catch (Exception e) {
      call.reject(String.valueOf(e.getMessage()));
    }
  }
}
''')
