import os
import logging
from flask import Flask, render_template, jsonify, request, send_from_directory

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Surah Al-Mulk data with all 30 verses
SURAH_MULK = [
    {
        "number": 1,
        "text": "تَبَٰرَكَ ٱلَّذِي بِيَدِهِ ٱلۡمُلۡكُ وَهُوَ عَلَىٰ كُلِّ شَيۡءٖ قَدِيرٌ"
    },
    {
        "number": 2,
        "text": "ٱلَّذِي خَلَقَ ٱلۡمَوۡتَ وَٱلۡحَيَوٰةَ لِيَبۡلُوَكُمۡ أَيُّكُمۡ أَحۡسَنُ عَمَلٗاۚ وَهُوَ ٱلۡعَزِيزُ ٱلۡغَفُورُ"
    },
    {
        "number": 3,
        "text": "ٱلَّذِي خَلَقَ سَبۡعَ سَمَٰوَٰتٖ طِبَاقٗاۖ مَّا تَرَىٰ فِي خَلۡقِ ٱلرَّحۡمَٰنِ مِن تَفَٰوُتٖۖ فَٱرۡجِعِ ٱلۡبَصَرَ هَلۡ تَرَىٰ مِن فُطُورٖ"
    },
    {
        "number": 4,
        "text": "ثُمَّ ٱرۡجِعِ ٱلۡبَصَرَ كَرَّتَيۡنِ يَنقَلِبۡ إِلَيۡكَ ٱلۡبَصَرُ خَاسِئٗا وَهُوَ حَسِيرٞ"
    },
    {
        "number": 5,
        "text": "وَلَقَدۡ زَيَّنَّا ٱلسَّمَآءَ ٱلدُّنۡيَا بِمَصَٰبِيحَ وَجَعَلۡنَٰهَا رُجُومٗا لِّلشَّيَٰطِينِۖ وَأَعۡتَدۡنَا لَهُمۡ عَذَابَ ٱلسَّعِيرِ"
    },
    {
        "number": 6,
        "text": "وَلِلَّذِينَ كَفَرُواْ بِرَبِّهِمۡ عَذَابُ جَهَنَّمَۖ وَبِئۡسَ ٱلۡمَصِيرُ"
    },
    {
        "number": 7,
        "text": "إِذَآ أُلۡقُواْ فِيهَا سَمِعُواْ لَهَا شَهِيقٗا وَهِيَ تَفُورُ"
    },
    {
        "number": 8,
        "text": "تَكَادُ تَمَيَّزُ مِنَ ٱلۡغَيۡظِۖ كُلَّمَآ أُلۡقِيَ فِيهَا فَوۡجٞ سَأَلَهُمۡ خَزَنَتُهَآ أَلَمۡ يَأۡتِكُمۡ نَذِيرٞ"
    },
    {
        "number": 9,
        "text": "قَالُواْ بَلَىٰ قَدۡ جَآءَنَا نَذِيرٞ فَكَذَّبۡنَا وَقُلۡنَا مَا نَزَّلَ ٱللَّهُ مِن شَيۡءٍ إِنۡ أَنتُمۡ إِلَّا فِي ضَلَٰلٖ كَبِيرٖ"
    },
    {
        "number": 10,
        "text": "وَقَالُواْ لَوۡ كُنَّا نَسۡمَعُ أَوۡ نَعۡقِلُ مَا كُنَّا فِيٓ أَصۡحَٰبِ ٱلسَّعِيرِ"
    },
    {
        "number": 11,
        "text": "فَٱعۡتَرَفُواْ بِذَنۢبِهِمۡ فَسُحۡقٗا لِّأَصۡحَٰبِ ٱلسَّعِيرِ"
    },
    {
        "number": 12,
        "text": "إِنَّ ٱلَّذِينَ يَخۡشَوۡنَ رَبَّهُم بِٱلۡغَيۡبِ لَهُم مَّغۡفِرَةٞ وَأَجۡرٞ كَبِيرٞ"
    },
    {
        "number": 13,
        "text": "وَأَسِرُّواْ قَوۡلَكُمۡ أَوِ ٱجۡهَرُواْ بِهِۦٓۖ إِنَّهُۥ عَلِيمُۢ بِذَاتِ ٱلصُّدُورِ"
    },
    {
        "number": 14,
        "text": "أَلَا يَعۡلَمُ مَنۡ خَلَقَ وَهُوَ ٱللَّطِيفُ ٱلۡخَبِيرُ"
    },
    {
        "number": 15,
        "text": "هُوَ ٱلَّذِي جَعَلَ لَكُمُ ٱلۡأَرۡضَ ذَلُولٗا فَٱمۡشُواْ فِي مَنَاكِبِهَا وَكُلُواْ مِن رِّزۡقِهِۦۖ وَإِلَيۡهِ ٱلنُّشُورُ"
    },
    {
        "number": 16,
        "text": "ءَأَمِنتُم مَّن فِي ٱلسَّمَآءِ أَن يَخۡسِفَ بِكُمُ ٱلۡأَرۡضَ فَإِذَا هِيَ تَمُورُ"
    },
    {
        "number": 17,
        "text": "أَمۡ أَمِنتُم مَّن فِي ٱلسَّمَآءِ أَن يُرۡسِلَ عَلَيۡكُمۡ حَاصِبٗاۖ فَسَتَعۡلَمُونَ كَيۡفَ نَذِيرِ"
    },
    {
        "number": 18,
        "text": "وَلَقَدۡ كَذَّبَ ٱلَّذِينَ مِن قَبۡلِهِمۡ فَكَيۡفَ كَانَ نَكِيرِ"
    },
    {
        "number": 19,
        "text": "أَوَلَمۡ يَرَوۡاْ إِلَى ٱلطَّيۡرِ فَوۡقَهُمۡ صَٰٓفَّٰتٖ وَيَقۡبِضۡنَۚ مَا يُمۡسِكُهُنَّ إِلَّا ٱلرَّحۡمَٰنُۚ إِنَّهُۥ بِكُلِّ شَيۡءِۢ بَصِيرٌ"
    },
    {
        "number": 20,
        "text": "أَمَّنۡ هَٰذَا ٱلَّذِي هُوَ جُندٞ لَّكُمۡ يَنصُرُكُم مِّن دُونِ ٱلرَّحۡمَٰنِۚ إِنِ ٱلۡكَٰفِرُونَ إِلَّا فِي غُرُورٍ"
    },
    {
        "number": 21,
        "text": "أَمَّنۡ هَٰذَا ٱلَّذِي يَرۡزُقُكُمۡ إِنۡ أَمۡسَكَ رِزۡقَهُۥۚ بَل لَّجُّواْ فِي عُتُوّٖ وَنُفُورٍ"
    },
    {
        "number": 22,
        "text": "أَفَمَن يَمۡشِي مُكِبًّا عَلَىٰ وَجۡهِهِۦٓ أَهۡدَىٰٓ أَمَّن يَمۡشِي سَوِيًّا عَلَىٰ صِرَٰطٖ مُّسۡتَقِيمٖ"
    },
    {
        "number": 23,
        "text": "قُلۡ هُوَ ٱلَّذِيٓ أَنشَأَكُمۡ وَجَعَلَ لَكُمُ ٱلسَّمۡعَ وَٱلۡأَبۡصَٰرَ وَٱلۡأَفۡـِٔدَةَۚ قَلِيلٗا مَّا تَشۡكُرُونَ"
    },
    {
        "number": 24,
        "text": "قُلۡ هُوَ ٱلَّذِي ذَرَأَكُمۡ فِي ٱلۡأَرۡضِ وَإِلَيۡهِ تُحۡشَرُونَ"
    },
    {
        "number": 25,
        "text": "وَيَقُولُونَ مَتَىٰ هَٰذَا ٱلۡوَعۡدُ إِن كُنتُمۡ صَٰدِقِينَ"
    },
    {
        "number": 26,
        "text": "قُلۡ إِنَّمَا ٱلۡعِلۡمُ عِندَ ٱللَّهِ وَإِنَّمَآ أَنَا۠ نَذِيرٞ مُّبِينٞ"
    },
    {
        "number": 27,
        "text": "فَلَمَّا رَأَوۡهُ زُلۡفَةٗ سِيٓـَٔتۡ وُجُوهُ ٱلَّذِينَ كَفَرُواْ وَقِيلَ هَٰذَا ٱلَّذِي كُنتُم بِهِۦ تَدَّعُونَ"
    },
    {
        "number": 28,
        "text": "قُلۡ أَرَءَيۡتُمۡ إِنۡ أَهۡلَكَنِيَ ٱللَّهُ وَمَن مَّعِيَ أَوۡ رَحِمَنَا فَمَن يُجِيرُ ٱلۡكَٰفِرِينَ مِنۡ عَذَابٍ أَلِيمٖ"
    },
    {
        "number": 29,
        "text": "قُلۡ هُوَ ٱلرَّحۡمَٰنُ ءَامَنَّا بِهِۦ وَعَلَيۡهِ تَوَكَّلۡنَاۖ فَسَتَعۡلَمُونَ مَنۡ هُوَ فِي ضَلَٰلٖ مُّبِينٖ"
    },
    {
        "number": 30,
        "text": "قُلۡ أَرَءَيۡتُمۡ إِنۡ أَصۡبَحَ مَآؤُكُمۡ غَوۡرٗا فَمَن يَأۡتِيكُم بِمَآءٖ مَّعِينِۢ"
    }
]

# Ensure audio directory exists
audio_dir = os.path.join(app.static_folder, 'audio')
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)
    logger.info(f"Created audio directory at {audio_dir}")

# Routes
@app.route('/')
def index():
    """Render the main page with Surah Al-Mulk"""
    return render_template('index.html', verses=SURAH_MULK)

@app.route('/verses')
def get_verses():
    """API to get all verses of Surah Al-Mulk"""
    return jsonify(SURAH_MULK)

@app.route('/verse/<int:verse_number>')
def get_verse(verse_number):
    """API to get a specific verse by number"""
    if 1 <= verse_number <= 30:
        return jsonify(SURAH_MULK[verse_number-1])
    return jsonify({"error": "Verse not found"}), 404

@app.route('/download-audio/<int:verse_number>')
def download_audio(verse_number):
    """Download audio file for a specific verse"""
    if 1 <= verse_number <= 30:
        audio_file = f"{verse_number}.mp4"
        try:
            return send_from_directory(directory=audio_dir, path=audio_file, as_attachment=True)
        except FileNotFoundError:
            logger.warning(f"Audio file {audio_file} not found in {audio_dir}")
            return jsonify({"error": "Audio file not found"}), 404
    return jsonify({"error": "Invalid verse number"}), 400

@app.route('/upload-audio', methods=['GET', 'POST'])
def upload_audio():
    """Upload audio files for verses"""
    if request.method == 'POST':
        # Check if this is a batch upload
        batch_upload = request.form.get('batch_upload') == 'true'
        
        if batch_upload:
            # Handle batch upload
            if 'audio_files' not in request.files:
                return jsonify({"error": "لم يتم اختيار ملفات"}), 400
                
            uploaded_files = request.files.getlist('audio_files')
            if not uploaded_files or uploaded_files[0].filename == '':
                return jsonify({"error": "لم يتم اختيار ملفات"}), 400
            
            success_count = 0
            error_count = 0
            errors = []
            
            for audio_file in uploaded_files:
                if audio_file and audio_file.filename != '':
                    # Try to extract verse number from filename
                    try:
                        # Extract verse number from filename (e.g., "1.mp4" -> 1)
                        filename_base = os.path.splitext(audio_file.filename)[0]
                        verse_number = int(filename_base)
                        
                        if not (1 <= verse_number <= 30):
                            error_count += 1
                            errors.append(f"رقم آية غير صحيح في الملف: {audio_file.filename}")
                            continue
                        
                        # Save the file with standardized name
                        filename = f"{verse_number}.mp4"
                        file_path = os.path.join(audio_dir, filename)
                        audio_file.save(file_path)
                        success_count += 1
                        logger.info(f"Batch upload: Saved audio file for verse {verse_number}: {file_path}")
                    except ValueError:
                        error_count += 1
                        errors.append(f"تعذر تحديد رقم الآية من اسم الملف: {audio_file.filename}")
                    except Exception as e:
                        error_count += 1
                        errors.append(f"خطأ في حفظ {audio_file.filename}: {str(e)}")
                else:
                    error_count += 1
                    errors.append(f"اسم ملف غير صالح: {audio_file.filename}")
            
            # Prepare response message
            if success_count > 0:
                message = f"تم رفع {success_count} ملف صوتي بنجاح"
                if error_count > 0:
                    message += f" مع {error_count} خطأ"
                return jsonify({
                    "success": True, 
                    "message": message,
                    "success_count": success_count,
                    "error_count": error_count,
                    "errors": errors[:5]  # Return first 5 errors only to keep response size manageable
                })
            else:
                return jsonify({
                    "error": "لم يتم رفع أي ملف بنجاح",
                    "errors": errors[:5]
                }), 400
        
        else:
            # Handle single file upload
            verse_number = request.form.get('verse_number', type=int)
            if not verse_number or not (1 <= verse_number <= 30):
                return jsonify({"error": "رقم الآية غير صحيح"}), 400
            
            if 'audio_file' not in request.files:
                return jsonify({"error": "لم يتم اختيار ملف"}), 400
                
            audio_file = request.files['audio_file']
            if audio_file.filename == '':
                return jsonify({"error": "لم يتم اختيار ملف"}), 400
                
            if audio_file:
                # Save as MP4 file with verse number as filename
                filename = f"{verse_number}.mp4"
                file_path = os.path.join(audio_dir, filename)
                
                try:
                    audio_file.save(file_path)
                    logger.info(f"Uploaded audio file for verse {verse_number}: {file_path}")
                    return jsonify({"success": True, "message": f"تم رفع الملف الصوتي للآية {verse_number} بنجاح"})
                except Exception as e:
                    logger.error(f"Error saving audio file: {str(e)}")
                    return jsonify({"error": str(e)}), 500
    
    # GET request - show upload form
    verse_number = request.args.get('verse', type=int)
    batch = request.args.get('batch') == 'true'
    return render_template('upload.html', verse_number=verse_number, batch=batch)

@app.route('/manage-audio')
def manage_audio():
    """Manage audio files"""
    # Check which audio files exist
    existing_files = []
    missing_files = []
    
    for i in range(1, 31):
        filename = f"{i}.mp4"
        file_path = os.path.join(audio_dir, filename)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / 1024  # KB
            existing_files.append({
                "verse_number": i,
                "filename": filename,
                "size_kb": round(file_size, 2)
            })
        else:
            missing_files.append(i)
    
    return render_template('manage_audio.html', 
                          existing_files=existing_files, 
                          missing_files=missing_files,
                          verses=SURAH_MULK)

@app.route('/delete-audio/<int:verse_number>', methods=['POST'])
def delete_audio(verse_number):
    """Delete audio file for a specific verse"""
    if not (1 <= verse_number <= 30):
        return jsonify({"error": "Invalid verse number"}), 400
        
    audio_file = f"{verse_number}.mp4"
    file_path = os.path.join(audio_dir, audio_file)
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted audio file for verse {verse_number}: {file_path}")
            return jsonify({"success": True, "message": f"تم حذف الملف الصوتي للآية {verse_number} بنجاح"})
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        logger.error(f"Error deleting audio file: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/export-apk')
def export_apk():
    """Show instructions for exporting to APK"""
    # Get the current app URL
    host_url = request.host_url.rstrip('/')
    app_url = host_url + '/'
    return render_template('export_apk.html', app_url=app_url)

@app.route('/api/audio/<int:verse_number>')
def get_audio(verse_number):
    """Get audio file for a specific verse with proper MIME type for mobile browsers"""
    if 1 <= verse_number <= 30:
        audio_file = f"{verse_number}.mp4"
        file_path = os.path.join(audio_dir, audio_file)
        
        try:
            # Check if the file exists
            if not os.path.exists(file_path):
                logger.warning(f"Audio file {audio_file} not found in {audio_dir}")
                return jsonify({"error": "Audio file not found"}), 404
                
            # Get the file size for Content-Length header
            file_size = os.path.getsize(file_path)
            
            # Create a custom response for better mobile compatibility
            response = send_from_directory(
                directory=audio_dir, 
                path=audio_file, 
                as_attachment=False,
                mimetype='audio/mp4'
            )
            
            # Add key headers for mobile browsers and service workers
            response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 1 day
            response.headers['Accept-Ranges'] = 'bytes'
            response.headers['Content-Length'] = str(file_size)
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['Access-Control-Allow-Origin'] = '*'  # CORS support
            
            # Allow direct mobile playback
            response.headers['Content-Disposition'] = 'inline'
            
            logger.info(f"Serving audio file {audio_file} ({file_size} bytes)")
            return response
        except Exception as e:
            logger.error(f"Error serving audio file: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Invalid verse number"}), 400
