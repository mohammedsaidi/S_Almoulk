import flet as ft
from flet_audio import Audio
import os
import shutil
import tempfile
from pathlib import Path

# قائمة سورة الملك
SURAH_MULK = [
    {"verse_number": 1, "arabic_text": "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ تَبَارَكَ الَّذِي بِيَدِهِ الْمُلْكُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ"},
    {"verse_number": 2, "arabic_text": "الَّذِي خَلَقَ الْمَوْتَ وَالْحَيَاةَ لِيَبْلُوَكُمْ أَيُّكُمْ أَحْسَنُ عَمَلًا وَهُوَ الْعَزِيزُ الْغَفُورُ"},
    {"verse_number": 3, "arabic_text": "الَّذِي خَلَقَ سَبْعَ سَمَاوَاتٍ طِبَاقًا مَا تَرَى فِي خَلْقِ الرَّحْمَنِ مِنْ تَفَاوُتٍ فَارْجِعِ الْبَصَرَ هَلْ تَرَى مِنْ فُطُورٍ"},
    {"verse_number": 4, "arabic_text": "ثُمَّ ارْجِعِ الْبَصَرَ كَرَّتَيْنِ يَنْقَلِبْ إِلَيْكَ الْبَصَرُ خَاسِئًا وَهُوَ حَسِيرٌ"},
    {"verse_number": 5, "arabic_text": "وَلَقَدْ زَيَّنَّا السَّمَاءَ الدُّنْيَا بِمَصَابِيحَ وَجَعَلْنَاهَا رُجُومًا لِلشَّيَاطِينِ وَأَعْتَدْنَا لَهُمْ عَذَابَ السَّعِيرِ"},
    {"verse_number": 6, "arabic_text": "وَلِلَّذِينَ كَفَرُوا بِرَبِّهِمْ عَذَابُ جَهَنَّمَ وَبِئْسَ الْمَصِيرُ"},
    {"verse_number": 7, "arabic_text": "إِذَا أُلْقُوا فِيهَا سَمِعُوا لَهَا شَهِيقًا وَهِيَ تَفُورُ"},
    {"verse_number": 8, "arabic_text": "تَكَادُ تَمَيَّزُ مِنَ الْغَيْظِ كُلَّمَا أُلْقِيَ فِيهَا فَوْجٌ سَأَلَهُمْ خَزَنَتُهَا أَلَمْ يَأْتِكُمْ نَذِيرٌ"},
    {"verse_number": 9, "arabic_text": "قَالُوا بَلَى قَدْ جَاءَنَا نَذِيرٌ فَكَذَّبْنَا وَقُلْنَا مَا نَزَّلَ اللَّهُ مِنْ شَيْءٍ إِنْ أَنْتُمْ إِلَّا فِي ضَلَالٍ كَبِيرٍ"},
    {"verse_number": 10, "arabic_text": "وَقَالُوا لَوْ كُنَّا نَسْمَعُ أَوْ نَعْقِلُ مَا كُنَّا فِي أَصْحَابِ السَّعِيرِ"},
    {"verse_number": 11, "arabic_text": "فَاعْتَرَفُوا بِذَنْبِهِمْ فَسُحْقًا لِأَصْحَابِ السَّعِيرِ"},
    {"verse_number": 12, "arabic_text": "إِنَّ الَّذِينَ يَخْشَوْنَ رَبَّهُمْ بِالْغَيْبِ لَهُمْ مَغْفِرَةٌ وَأَجْرٌ كَبِيرٌ"},
    {"verse_number": 13, "arabic_text": "وَأَسِرُّوا قَوْلَكُمْ أَوِ اجْهَرُوا بِهِ إِنَّهُ عَلِيمٌ بِذَاتِ الصُّدُورِ"},
    {"verse_number": 14, "arabic_text": "أَلَا يَعْلَمُ مَنْ خَلَقَ وَهُوَ اللَّطِيفُ الْخَبِيرُ"},
    {"verse_number": 15, "arabic_text": "هُوَ الَّذِي جَعَلَ لَكُمُ الْأَرْضَ ذَلُولًا فَامْشُوا فِي مَنَاكِبِهَا وَكُلُوا مِنْ رِزْقِهِ وَإِلَيْهِ النُّشُورُ"},
    {"verse_number": 16, "arabic_text": "أَأَمِنْتُمْ مَنْ فِي السَّمَاءِ أَنْ يَخْسِفَ بِكُمُ الْأَرْضَ فَإِذَا هِيَ تَمُورُ"},
    {"verse_number": 17, "arabic_text": "أَمْ أَمِنْتُمْ مَنْ فِي السَّمَاءِ أَنْ يُرْسِلَ عَلَيْكُمْ حَاصِبًا فَسَتَعْلَمُونَ كَيْفَ نَذِيرِ"},
    {"verse_number": 18, "arabic_text": "وَلَقَدْ كَذَّبَ الَّذِينَ مِنْ قَبْلِهِمْ فَكَيْفَ كَانَ نَكِيرِ"},
    {"verse_number": 19, "arabic_text": "أَوَلَمْ يَرَوْا إِلَى الطَّيْرِ فَوْقَهُمْ صَافَّاتٍ وَيَقْبِضْنَ مَا يُمْسِكُهُنَّ إِلَّا الرَّحْمَنُ إِنَّهُ بِكُلِّ شَيْءٍ بَصِيرٌ"},
    {"verse_number": 20, "arabic_text": "أَمَّنْ هَذَا الَّذِي هُوَ جُنْدٌ لَكُمْ يَنْصُرُكُمْ مِنْ دُونِ الرَّحْمَنِ إِنِ الْكَافِرُونَ إِلَّا فِي غُرُورٍ"},
    {"verse_number": 21, "arabic_text": "أَمَّنْ هَذَا الَّذِي يَرْزُقُكُمْ إِنْ أَمْسَكَ رِزْقَهُ بَلْ لَجُّوا فِي عُتُوٍّ وَنُفُورٍ"},
    {"verse_number": 22, "arabic_text": "أَفَمَنْ يَمْشِي مُكِبًّا عَلَى وَجْهِهِ أَهْدَى أَمَّنْ يَمْشِي سَوِيًّا عَلَى صِرَاطٍ مُسْتَقِيمٍ"},
    {"verse_number": 23, "arabic_text": "قُلْ هُوَ الَّذِي أَنْشَأَكُمْ وَجَعَلَ لَكُمُ السَّمْعَ وَالْأَبْصَارَ وَالْأَفْئِدَةَ قَلِيلًا مَا تَشْكُرُونَ"},
    {"verse_number": 24, "arabic_text": "قُلْ هُوَ الَّذِي ذَرَأَكُمْ فِي الْأَرْضِ وَإِلَيْهِ تُحْشَرُونَ"},
    {"verse_number": 25, "arabic_text": "وَيَقُولُونَ مَتَى هَذَا الْوَعْدُ إِنْ كُنْتُمْ صَادِقِينَ"},
    {"verse_number": 26, "arabic_text": "قُلْ إِنَّمَا الْعِلْمُ عِنْدَ اللَّهِ وَإِنَّمَا أَنَا نَذِيرٌ مُبِينٌ"},
    {"verse_number": 27, "arabic_text": "فَلَمَّا رَأَوْهُ زُلْفَةً سِيئَتْ وُجُوهُ الَّذِينَ كَفَرُوا وَقِيلَ هَذَا الَّذِي كُنْتُمْ بِهِ تَدَّعُونَ"},
    {"verse_number": 28, "arabic_text": "قُلْ أَرَأَيْتُمْ إِنْ أَهْلَكَنِيَ اللَّهُ وَمَنْ مَعِيَ أَوْ رَحِمَنَا فَمَنْ يُجِيرُ الْكَافِرِينَ مِنْ عَذَابٍ أَلِيمٍ"},
    {"verse_number": 29, "arabic_text": "قُلْ هُوَ الرَّحْمَنُ آمَنَّا بِهِ وَعَلَيْهِ تَوَكَّلْنَا فَسَتَعْلَمُونَ مَنْ هُوَ فِي ضَلَالٍ مُبِينٍ"},
    {"verse_number": 30, "arabic_text": "قُلْ أَرَأَيْتُمْ إِنْ أَصْبَحَ مَاؤُكُمْ غَوْرًا فَمَنْ يَأْتِيكُمْ بِمَاءٍ مَعِينٍ"}
]

class SurahMulkApp:
    def __init__(self):
        # إنشاء مجلد للصوتيات
        self.audio_dir = os.path.join(os.getcwd(), "audio_files")
        os.makedirs(self.audio_dir, exist_ok=True)
        
        # حالة التطبيق
        self.current_verse = 1
        self.is_playing = False
        self.is_repeating = False
        self.repeat_count = 1
        self.current_repeat_counter = 0
        self.start_verse = 1
        self.end_verse = 30
        self.audio_player = None
        self.audio_instance = None
        self.active_verse_ref = None
        self.upload_verse = 1
        self.upload_verse_dropdown = None
        
        # حالة الاتصال
        self.is_online = True
        
        # تفعيل وضع عدم الاتصال
        self.can_work_offline = True

    def main(self, page: ft.Page):
        # حفظ مرجع للصفحة لاستخدامه في الدوال الأخرى
        self.page = page
        
        # إعداد الصفحة
        page.title = "تطبيق حفظ سورة الملك"
        page.theme_mode = ft.ThemeMode.DARK
        page.rtl = True  # للغة العربية
        page.padding = 10
        page.scroll = ft.ScrollMode.AUTO
        
        # عناصر التحكم بالصوت
        self.audio_player = Audio(
            src_base64=None,
            autoplay=False,
            volume=1.0,
            balance=0.0,
            release_mode="release",
            on_loaded=self.on_audio_loaded,
            on_position_changed=self.on_position_changed,
            on_state_changed=self.on_state_changed,
            on_duration_changed=self.on_duration_changed,
        )
        page.overlay.append(self.audio_player)
        
        # شريط التقدم
        self.progress_bar = ft.ProgressBar(width=page.width * 0.9, value=0, color=ft.colors.GREEN)
        
        # أزرار التحكم
        play_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            icon_color=ft.colors.GREEN,
            icon_size=40,
            tooltip="تشغيل",
            on_click=self.play_audio
        )
        
        pause_button = ft.IconButton(
            icon=ft.icons.PAUSE,
            icon_color=ft.colors.ORANGE,
            icon_size=40,
            tooltip="إيقاف مؤقت",
            on_click=self.pause_audio
        )
        
        self.repeat_button = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.icons.REPEAT, color=ft.colors.WHITE),
                ft.Text("تكرار")
            ]),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
            ),
            on_click=self.toggle_repeat
        )
        
        # قوائم اختيار الآيات
        start_verse_dropdown = ft.Dropdown(
            label="الآية البداية",
            width=120,
            options=[ft.dropdown.Option(key=str(i), text=f"الآية {i}") for i in range(1, 31)],
            value="1",
            on_change=self.on_start_verse_change
        )
        
        end_verse_dropdown = ft.Dropdown(
            label="الآية النهاية",
            width=120,
            options=[ft.dropdown.Option(key=str(i), text=f"الآية {i}") for i in range(1, 31)],
            value="30",
            on_change=self.on_end_verse_change
        )
        
        # مدخل عدد التكرارات
        repeat_count_field = ft.TextField(
            label="عدد التكرارات",
            value="1",
            width=100,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.on_repeat_count_change
        )
        
        # قسم التحكم
        controls_section = ft.Container(
            content=ft.Column([
                ft.Text("تطبيق حفظ سورة الملك", size=25, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                self.progress_bar,
                ft.Row([play_button, pause_button, self.repeat_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    start_verse_dropdown, 
                    end_verse_dropdown, 
                    repeat_count_field
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]),
            padding=10,
            margin=5,
            border_radius=10,
            bgcolor=ft.colors.SURFACE_VARIANT
        )
        
        # إنشاء قسم التبويب الرئيسي
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="آيات السورة",
                    icon=ft.icons.MENU_BOOK,
                    content=self.build_verses_view(page),
                ),
                ft.Tab(
                    text="إدارة الملفات الصوتية",
                    icon=ft.icons.AUDIO_FILE,
                    content=self.build_audio_management_view(page),
                ),
            ],
        )
        
        # إضافة العناصر إلى الصفحة
        page.add(
            controls_section,
            tabs,
            ft.Container(height=20),  # مسافة في الأسفل
            ft.Text("تطبيق حفظ سورة الملك - جميع الحقوق محفوظة © 2025", 
                  size=12, 
                  color=ft.colors.GREY_400,
                  text_align=ft.TextAlign.CENTER)
        )
        
        # تحديث الصفحة
        page.update()
    
    def build_verses_view(self, page):
        """بناء قائمة الآيات"""
        verses_list = ft.ListView(expand=True, spacing=2, padding=20, auto_scroll=False)
        
        for verse in SURAH_MULK:
            verse_number = verse["verse_number"]
            
            verse_item = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"{verse_number}", size=16, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon=ft.icons.PLAY_CIRCLE_FILL,
                            icon_color=ft.colors.GREEN,
                            tooltip=f"تشغيل الآية {verse_number}",
                            on_click=lambda e, n=verse_number: self.play_specific_verse(n)
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(
                        content=ft.Text(
                            verse["arabic_text"],
                            size=18,
                            text_align=ft.TextAlign.RIGHT,
                            selectable=True
                        ),
                        margin=ft.margin.only(top=5, bottom=5),
                    ),
                ]),
                bgcolor=ft.colors.SURFACE_VARIANT if verse_number % 2 == 0 else None,
                border_radius=8,
                padding=10,
                data={"verse_number": verse_number},
                key=f"verse-{verse_number}"
            )
            
            # حفظ مرجع للآية الأولى للاستخدام لاحقًا لتحديد الآية النشطة
            if verse_number == 1:
                self.active_verse_ref = verse_item

            verses_list.controls.append(verse_item)
            
        return verses_list
    
    def build_audio_management_view(self, page):
        """بناء واجهة إدارة الملفات الصوتية"""
        self.audio_files_list = ft.ListView(expand=1, spacing=2, padding=20)
        
        # قسم رفع الملفات
        # إنشاء قائمة اختيار رقم الآية
        self.upload_verse_dropdown = ft.Dropdown(
            label="اختر رقم الآية",
            width=150,
            options=[ft.dropdown.Option(key=str(i), text=f"الآية {i}") for i in range(1, 31)],
            value="1",
            on_change=self.on_upload_verse_change
        )
        
        upload_section = ft.Container(
            content=ft.Column([
                ft.Text("رفع ملفات صوتية", size=18, weight=ft.FontWeight.BOLD),
                
                # رفع ملف واحد
                ft.Text("رفع ملف صوتي واحد:"),
                ft.Row([
                    self.upload_verse_dropdown,
                    ft.FilePicker(
                        on_result=self.on_file_picker_result,
                    ),
                    ft.ElevatedButton(
                        "اختر ملف صوتي",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: self.pick_files(False),
                    ),
                ]),
                
                # رفع ملفات متعددة
                ft.Text("رفع ملفات متعددة:"),
                ft.Row([
                    ft.Text("ملاحظة: يجب أن تكون أسماء الملفات هي أرقام الآيات (مثل 1.mp3، 2.mp3، إلخ)"),
                    ft.FilePicker(
                        on_result=self.on_multiple_files_result,
                    ),
                    ft.ElevatedButton(
                        "اختر ملفات متعددة",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: self.pick_files(True),
                    ),
                ]),
            ]),
            padding=10,
            margin=ft.margin.only(bottom=10),
            border_radius=10,
            bgcolor=ft.colors.SURFACE_VARIANT
        )
        
        # إضافة FilePicker إلى الصفحة
        page.overlay.extend([
            upload_section.content.controls[2].controls[1],  # Single file picker
            upload_section.content.controls[4].controls[1],  # Multiple files picker
        ])
        
        # زر تحديث قائمة الملفات
        refresh_button = ft.ElevatedButton(
            "تحديث قائمة الملفات",
            icon=ft.icons.REFRESH,
            on_click=self.refresh_audio_files
        )
        
        # بناء واجهة الإدارة
        return ft.Column([
            upload_section,
            refresh_button,
            ft.Text("الملفات الصوتية المتوفرة:", size=16, weight=ft.FontWeight.BOLD),
            self.audio_files_list,
        ])
    
    def pick_files(self, multiple=False):
        """اختيار ملفات للرفع"""
        if multiple:
            # رفع ملفات متعددة
            file_picker = self.page.overlay[2]
            file_picker.pick_files(
                allow_multiple=True,
                allowed_extensions=["mp3", "mp4", "wav"],
                dialog_title="اختيار ملفات صوتية"
            )
        else:
            # رفع ملف واحد
            file_picker = self.page.overlay[1]
            file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["mp3", "mp4", "wav"],
                dialog_title="اختيار ملف صوتي"
            )
    
    def on_file_picker_result(self, e: ft.FilePickerResultEvent):
        """معالجة نتيجة اختيار ملف واحد"""
        if e.files:
            file_path = e.files[0].path
            file_name = e.files[0].name
            
            # نسخ الملف إلى مجلد الصوتيات مع تسمية ملائمة
            verse_number = int(self.upload_verse_dropdown.value)
            file_ext = os.path.splitext(file_name)[1]
            new_file_name = f"{verse_number}{file_ext}"
            new_file_path = os.path.join(self.audio_dir, new_file_name)
            
            try:
                shutil.copy(file_path, new_file_path)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"تم رفع الملف الصوتي للآية {verse_number} بنجاح"),
                    bgcolor=ft.colors.GREEN
                )
                self.page.snack_bar.open = True
                self.refresh_audio_files()
            except Exception as e:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"خطأ في رفع الملف: {str(e)}"),
                    bgcolor=ft.colors.RED
                )
                self.page.snack_bar.open = True
            
            self.page.update()
    
    def on_multiple_files_result(self, e: ft.FilePickerResultEvent):
        """معالجة نتيجة اختيار ملفات متعددة"""
        if e.files:
            success_count = 0
            error_count = 0
            
            for file_info in e.files:
                file_path = file_info.path
                file_name = file_info.name
                
                try:
                    # استخراج رقم الآية من اسم الملف
                    base_name = os.path.splitext(file_name)[0]
                    verse_number = int(base_name)
                    
                    if 1 <= verse_number <= 30:
                        # نسخ الملف إلى مجلد الصوتيات مع تسمية ملائمة
                        file_ext = os.path.splitext(file_name)[1]
                        new_file_name = f"{verse_number}{file_ext}"
                        new_file_path = os.path.join(self.audio_dir, new_file_name)
                        
                        shutil.copy(file_path, new_file_path)
                        success_count += 1
                    else:
                        error_count += 1
                except (ValueError, Exception) as e:
                    error_count += 1
            
            # عرض رسالة النتيجة
            if success_count > 0:
                message = f"تم رفع {success_count} ملف صوتي بنجاح"
                if error_count > 0:
                    message += f" مع {error_count} خطأ"
                
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(message),
                    bgcolor=ft.colors.GREEN if error_count == 0 else ft.colors.ORANGE
                )
            else:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("لم يتم رفع أي ملف بنجاح"),
                    bgcolor=ft.colors.RED
                )
            
            self.page.snack_bar.open = True
            self.refresh_audio_files()
            self.page.update()
    
    def refresh_audio_files(self, e=None):
        """تحديث قائمة الملفات الصوتية"""
        self.audio_files_list.controls.clear()
        
        # الحصول على قائمة الملفات الموجودة
        existing_files = []
        missing_files = []
        
        for i in range(1, 31):
            found = False
            for ext in ['.mp3', '.mp4', '.wav']:
                file_path = os.path.join(self.audio_dir, f"{i}{ext}")
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path) / 1024  # بالكيلوبايت
                    existing_files.append({
                        "verse_number": i,
                        "file_path": file_path,
                        "filename": os.path.basename(file_path),
                        "size_kb": round(file_size, 2)
                    })
                    found = True
                    break
            
            if not found:
                missing_files.append(i)
        
        # إضافة الملفات الموجودة إلى القائمة
        for file_info in existing_files:
            verse_number = file_info["verse_number"]
            
            file_item = ft.Container(
                content=ft.Row([
                    ft.Text(f"الآية {verse_number}", weight=ft.FontWeight.BOLD),
                    ft.Text(file_info["filename"]),
                    ft.Text(f"{file_info['size_kb']} KB"),
                    ft.IconButton(
                        icon=ft.icons.PLAY_CIRCLE,
                        icon_color=ft.colors.GREEN,
                        tooltip="تشغيل",
                        on_click=lambda e, n=verse_number: self.play_specific_verse(n)
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color=ft.colors.RED,
                        tooltip="حذف",
                        on_click=lambda e, n=verse_number, p=file_info["file_path"]: self.delete_audio_file(n, p)
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=ft.colors.SURFACE_VARIANT if verse_number % 2 == 0 else None,
                border_radius=8,
                padding=10
            )
            
            self.audio_files_list.controls.append(file_item)
        
        # إضافة الآيات التي لا تملك ملفات صوتية
        if missing_files:
            missing_section = ft.Container(
                content=ft.Column([
                    ft.Text("الآيات التي لا تملك ملفات صوتية:", weight=ft.FontWeight.BOLD),
                    ft.Text(", ".join(map(str, missing_files)))
                ]),
                padding=10,
                margin=5,
                border_radius=10,
                bgcolor=ft.colors.ERROR_CONTAINER
            )
            
            self.audio_files_list.controls.append(missing_section)
        
        self.page.update()
    
    def delete_audio_file(self, verse_number, file_path):
        """حذف ملف صوتي"""
        try:
            os.remove(file_path)
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"تم حذف الملف الصوتي للآية {verse_number} بنجاح"),
                bgcolor=ft.colors.GREEN
            )
            self.page.snack_bar.open = True
            self.refresh_audio_files()
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"خطأ في حذف الملف: {str(e)}"),
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
        
        self.page.update()
    
    def play_specific_verse(self, verse_number):
        """تشغيل آية محددة"""
        # تحديث الآية الحالية
        self.current_verse = verse_number
        self.current_repeat_counter = 0
        
        # تحقق من وجود ملف صوتي للآية
        audio_file = self.find_audio_file(verse_number)
        
        if audio_file:
            # إيقاف التشغيل الحالي إذا كان موجوداً
            if self.audio_player:
                self.audio_player.pause()
                self.audio_player.release()
            
            # تشغيل الملف الصوتي
            with open(audio_file, "rb") as f:
                audio_data = f.read()
            
            # تحديث حالة التشغيل
            self.is_playing = True
            
            # استخدام كائن Audio لتشغيل الملف
            self.audio_player.src_base64 = audio_data
            self.audio_player.play()
            
            # تحديث القائمة لإظهار الآية النشطة
            self.highlight_active_verse(verse_number)
        else:
            # عرض رسالة خطأ إذا لم يكن هناك ملف صوتي
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"لا يوجد ملف صوتي للآية {verse_number}"),
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def find_audio_file(self, verse_number):
        """البحث عن ملف صوتي للآية المحددة"""
        for ext in ['.mp3', '.mp4', '.wav']:
            file_path = os.path.join(self.audio_dir, f"{verse_number}{ext}")
            if os.path.exists(file_path):
                return file_path
        return None
    
    def highlight_active_verse(self, verse_number):
        """تمييز الآية النشطة في القائمة"""
        # إعادة تعيين كل الآيات للحالة الافتراضية
        verses_tab = self.page.controls[1].tabs[0].content
        
        # تحديث لون خلفية كل آية
        for i, verse_container in enumerate(verses_tab.controls):
            verse_data = verse_container.data
            if verse_data and verse_data["verse_number"] == verse_number:
                # تمييز الآية النشطة
                verse_container.bgcolor = ft.colors.GREEN_700
                self.active_verse_ref = verse_container
            else:
                # إعادة تعيين لون الخلفية للآيات الأخرى
                verse_container.bgcolor = ft.colors.SURFACE_VARIANT if verse_data["verse_number"] % 2 == 0 else None
        
        # التمرير إلى الآية النشطة
        verse_key = f"verse-{verse_number}"
        for control in verses_tab.controls:
            if control.key == verse_key:
                control.scroll_to()
                break
        
        self.page.update()
    
    def play_next_verse(self):
        """تشغيل الآية التالية"""
        # تحقق من إذا كان التكرار مفعل وعداد التكرار أقل من العدد المطلوب
        if self.is_repeating and self.current_repeat_counter < self.repeat_count - 1:
            self.current_repeat_counter += 1
            self.play_specific_verse(self.current_verse)
            return
        
        # إعادة تعيين عداد التكرار
        self.current_repeat_counter = 0
        
        # تشغيل الآية التالية أو العودة إلى آية البداية
        if self.current_verse < self.end_verse:
            next_verse = self.current_verse + 1
        else:
            next_verse = self.start_verse
        
        self.play_specific_verse(next_verse)
    
    def play_audio(self, e):
        """تشغيل الصوت"""
        if self.audio_player and self.is_playing:
            self.audio_player.pause()
            self.is_playing = False
        elif self.audio_player and not self.is_playing:
            self.audio_player.play()
            self.is_playing = True
        else:
            # تشغيل آية البداية
            self.play_specific_verse(self.start_verse)
    
    def pause_audio(self, e):
        """إيقاف الصوت مؤقتاً"""
        if self.audio_player and self.is_playing:
            self.audio_player.pause()
            self.is_playing = False
    
    def toggle_repeat(self, e):
        """تفعيل/تعطيل التكرار"""
        self.is_repeating = not self.is_repeating
        
        if self.is_repeating:
            self.repeat_button.style.bgcolor = ft.colors.GREEN
        else:
            self.repeat_button.style.bgcolor = ft.colors.BLUE
        
        self.page.update()
    
    # دوال معالجة أحداث تغيير القيم
    def on_start_verse_change(self, e):
        """معالجة تغيير آية البداية"""
        self.start_verse = int(e.control.value)
        
        # تأكد من أن آية البداية لا تتجاوز آية النهاية
        if self.start_verse > self.end_verse:
            self.page.controls[1].tabs[0].controls[2].controls[0].value = str(self.end_verse)
            self.start_verse = self.end_verse
        
        self.page.update()
    
    def on_end_verse_change(self, e):
        """معالجة تغيير آية النهاية"""
        self.end_verse = int(e.control.value)
        
        # تأكد من أن آية النهاية لا تقل عن آية البداية
        if self.end_verse < self.start_verse:
            self.page.controls[1].tabs[0].controls[2].controls[1].value = str(self.start_verse)
            self.end_verse = self.start_verse
        
        self.page.update()
    
    def on_repeat_count_change(self, e):
        """معالجة تغيير عدد التكرارات"""
        try:
            value = int(e.control.value)
            if value < 1:
                value = 1
                e.control.value = "1"
            self.repeat_count = value
        except ValueError:
            e.control.value = "1"
            self.repeat_count = 1
        
        self.page.update()
    
    def on_upload_verse_change(self, e):
        """معالجة تغيير رقم الآية المراد رفع ملف لها"""
        try:
            self.upload_verse = int(e.control.value)
        except ValueError:
            self.upload_verse = 1
        
        self.page.update()
    
    # دوال معالجة أحداث الصوت
    def on_audio_loaded(self, e):
        """معالجة حدث تحميل الصوت"""
        # تم تحميل الملف الصوتي بنجاح
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"تم تحميل الملف الصوتي للآية {self.current_verse}"),
            bgcolor=ft.colors.GREEN,
            duration=1000
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def on_position_changed(self, e):
        """معالجة تغيير موضع التشغيل"""
        if e and e.position is not None and e.duration is not None and e.duration > 0:
            # تحديث شريط التقدم
            progress = e.position / e.duration
            self.progress_bar.value = progress
            self.page.update()
    
    def on_state_changed(self, e):
        """معالجة تغيير حالة التشغيل"""
        if e.state == 'completed':
            # تم الانتهاء من تشغيل الملف الصوتي
            self.play_next_verse()
    
    def on_duration_changed(self, e):
        """معالجة تغيير مدة الملف الصوتي"""
        pass  # يمكن استخدامها لعرض المدة الإجمالية للملف الصوتي


# تشغيل التطبيق
app = SurahMulkApp()
ft.app(target=app.main, assets_dir="assets")