import argparse
import os
import shutil
import subprocess
import sys
import tempfile

# تحديد المجلدات الهامة التي نحتاج لتضمينها في تطبيق الأندرويد
def create_app_bundle():
    print("بدء إنشاء حزمة تطبيق الأندرويد...")
    
    # مجلد تطبيق الفلت
    flet_app_dir = "."
    
    # إنشاء مجلد مؤقت للعمل
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"إنشاء مجلد مؤقت: {temp_dir}")
        
        # نسخ ملفات التطبيق إلى المجلد المؤقت
        app_dir = os.path.join(temp_dir, "app")
        os.makedirs(app_dir, exist_ok=True)
        
        # نسخ ملفات بايثون الأساسية
        for file in ["surah_mulk_app.py", "run.py"]:
            shutil.copy2(os.path.join(flet_app_dir, file), app_dir)
            
        # نسخ مجلد الأصول
        assets_dir = os.path.join(flet_app_dir, "assets")
        if os.path.exists(assets_dir):
            shutil.copytree(assets_dir, os.path.join(app_dir, "assets"))
            
        # نسخ مجلد ملفات الصوت
        audio_dir = os.path.join(flet_app_dir, "audio_files")
        if os.path.exists(audio_dir):
            shutil.copytree(audio_dir, os.path.join(app_dir, "audio_files"))
        else:
            os.makedirs(os.path.join(app_dir, "audio_files"), exist_ok=True)
            
        # نسخ مجلد الأندرويد
        android_dir = os.path.join(flet_app_dir, "android")
        if os.path.exists(android_dir):
            shutil.copytree(android_dir, os.path.join(app_dir, "android"))
            
        # إنشاء ملف وصف التطبيق
        with open(os.path.join(app_dir, "app.json"), "w", encoding="utf-8") as f:
            f.write("""{
                "name": "سورة الملك",
                "package": "com.quran.surah_mulk",
                "version": "1.0.0",
                "orientation": "portrait",
                "offline": true,
                "permissions": [
                    "INTERNET",
                    "READ_EXTERNAL_STORAGE",
                    "WRITE_EXTERNAL_STORAGE"
                ]
            }""")

        # استنساخ ملف flet_export.py من مجلد flet الخاص بالمستخدم
        flet_export_script = """
import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="إنشاء تطبيق أندرويد APK")
    parser.add_argument("--app", type=str, required=True, help="مسار مجلد التطبيق")
    args = parser.parse_args()
    
    # التحقق من وجود مجلد التطبيق
    if not os.path.isdir(args.app):
        print(f"خطأ: مجلد التطبيق غير موجود: {args.app}")
        sys.exit(1)
    
    # التأكد من وجود ملف run.py في مجلد التطبيق
    run_py = os.path.join(args.app, "run.py")
    if not os.path.isfile(run_py):
        print(f"خطأ: ملف run.py غير موجود في: {run_py}")
        sys.exit(1)
    
    # تشغيل الأمر لإنشاء ملف APK
    cmd = [
        sys.executable, "-m", "flet", "build", "apk",
        "--project-name", "سورة الملك",
        "--package-name", "com.quran.surah_mulk",
        run_py
    ]
    
    print("جاري تنفيذ الأمر:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("تم إنشاء ملف APK بنجاح!")

if __name__ == "__main__":
    main()
"""
        
        # حفظ السكريبت في المجلد المؤقت
        with open(os.path.join(temp_dir, "flet_export.py"), "w", encoding="utf-8") as f:
            f.write(flet_export_script)
        
        # تنفيذ السكريبت لإنشاء ملف APK
        cmd = [sys.executable, os.path.join(temp_dir, "flet_export.py"), "--app", app_dir]
        print("تنفيذ الأمر:", " ".join(cmd))
        subprocess.run(cmd, check=True)
        
        # نسخ ملف APK إلى مجلد المشروع
        apk_file = os.path.join(temp_dir, "build", "app", "outputs", "flutter-apk", "app-release.apk")
        if os.path.exists(apk_file):
            target_path = os.path.join(flet_app_dir, "surah_mulk.apk")
            shutil.copy2(apk_file, target_path)
            print(f"تم نسخ ملف APK بنجاح إلى: {target_path}")
        else:
            print(f"خطأ: لم يتم العثور على ملف APK في: {apk_file}")
            
        print("اكتمل إنشاء حزمة تطبيق الأندرويد!")

if __name__ == "__main__":
    create_app_bundle()