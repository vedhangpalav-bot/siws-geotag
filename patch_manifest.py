p='android/app/src/main/AndroidManifest.xml'
s=open(p).read()
perms='''    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-feature android:name="android.hardware.camera" android:required="false" />
'''
s=s.replace('<application',perms+'    <application',1)
open(p,'w').write(s)
