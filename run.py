from surah_mulk_app import SurahMulkApp
import flet as ft
import os
import platform

def main():
    # تشغيل التطبيق مع توفير الخاصية لتشغيله على الويب
    # Use port 8080 to avoid conflict with Flask running on 5000
    port = int(os.environ.get("PORT", 8080))
    
    # إعدادات إضافية للـ Android APK
    app_name = "سورة الملك"
    package_name = "com.quran.surah_mulk"
    
    # عند تشغيله على الجوال استخدم وضع التطبيق المحمول بدل المتصفح
    if platform.system() == "Android":
        view = ft.AppView.NATIVE
    else:
        view = ft.AppView.WEB_BROWSER
    
    ft.app(
        name=app_name,
        target=SurahMulkApp().main, 
        assets_dir="assets", 
        port=port, 
        view=view, 
        web_renderer=ft.WebRenderer.HTML,
        # إعدادات الهاتف المحمول
        use_color_emoji=True,
        mobile_web_renderer=ft.WebRenderer.HTML
    )

if __name__ == "__main__":
    main()