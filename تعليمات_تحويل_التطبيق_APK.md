# تعليمات تحويل تطبيق سورة الملك إلى APK واستخدامه بدون إنترنت

## تحويل التطبيق إلى APK

لتحويل التطبيق إلى ملف APK وتثبيته على جهاز أندرويد، اتبع الخطوات التالية:

### 1. متطلبات أساسية
- تثبيت فلتر (Flutter) على جهاز الكمبيوتر
- تثبيت أداة Flet على جهاز الكمبيوتر
- توفر Java JDK
- توفر Android SDK

### 2. تنفيذ الأمر التالي في الطرفية (Terminal):

```bash
python -m pip install flet flet-core flet-runtime
```

### 3. تنفيذ أمر Flet لإنشاء ملف APK:

```bash
python -m flet build apk --project-name "سورة الملك" --package-name "com.quran.surah_mulk" run.py
```

أو يمكن استخدام السكريبت الذي قمنا بإنشائه:

```bash
python surah_mulk_app_bundle.py
```

### 4. تجهيز الملفات الصوتية للاستخدام بدون إنترنت

قبل تثبيت التطبيق على الجوال، يجب توفير الملفات الصوتية للآيات في مجلد `audio_files` داخل التطبيق. يمكنك نسخ الملفات الصوتية التي تستخدمها بحيث تكون جاهزة للاستخدام بدون إنترنت.

## استخدام التطبيق بدون إنترنت

1. تأكد من تنزيل الملف APK الناتج (surah_mulk.apk) إلى هاتفك الأندرويد.
2. افتح الملف وقم بتثبيت التطبيق (قد تحتاج إلى السماح بتثبيت تطبيقات من مصادر غير معروفة).
3. بعد التثبيت، افتح التطبيق وسيعمل بشكل طبيعي حتى بدون اتصال بالإنترنت.
4. يمكنك الاستماع إلى الآيات المخزنة مسبقًا.

## ملاحظات هامة

- جميع الملفات الصوتية التي قمت بتحميلها في التطبيق ستكون متاحة للاستخدام حتى عند عدم وجود اتصال بالإنترنت.
- تأكد من تنزيل الملفات الصوتية لجميع الآيات التي تريد الاستماع إليها قبل استخدام التطبيق بدون إنترنت.
- أثناء تحويل التطبيق إلى APK، سيتم تضمين جميع الملفات الموجودة في المجلد `audio_files` داخل الـ APK.
- في حالة تحديث الملفات الصوتية، تحتاج لإعادة بناء APK جديد.

## حل المشكلات الشائعة

1. **مشكلة عدم تشغيل الملفات الصوتية**:
   - تأكد من وجود الملفات الصوتية في المجلد الصحيح
   - تأكد من تسمية الملفات بشكل صحيح (مثال: 1.mp3، 2.mp3)

2. **مشكلة في تثبيت APK**:
   - تأكد من تفعيل خيار "تثبيت من مصادر غير معروفة" في إعدادات الأمان بهاتفك
   - تأكد من وجود مساحة كافية في هاتفك

3. **عدم ظهور بعض الآيات**:
   - قد تكون بعض الملفات الصوتية مفقودة، تأكد من رفع جميع الملفات الصوتية للآيات من 1 إلى 30