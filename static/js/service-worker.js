// اسم تخزين الكاش
const CACHE_NAME = 'surah-mulk-cache-v3';
// تخزين منفصل للملفات الصوتية
const AUDIO_CACHE_NAME = 'surah-mulk-audio-v3';

// قائمة الملفات التي سيتم تخزينها للاستخدام دون اتصال بالإنترنت
const urlsToCache = [
  '/',
  '/static/css/styles.css',
  '/static/js/player.js',
  '/static/js/pwa-init.js',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/verses',
  '/export-apk',
  '/manifest.json',
  // قوالب HTML
  '/manage-audio',
  '/upload-audio',
  // ملفات البرنامج
  'https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.3/howler.min.js',
  // ملفات Bootstrap وأيقونات
  'https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.woff2'
];

// تثبيت Service Worker وتخزين الملفات في التخزين المؤقت
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// استجابة للطلبات: تحقق أولاً من التخزين المؤقت، ثم اطلب من الشبكة
self.addEventListener('fetch', event => {
  // تعامل خاص مع ملفات الصوت، لنسمح بتخزينها مؤقتا للاستخدام دون اتصال
  if (event.request.url.includes('/api/audio/')) {
    event.respondWith(
      caches.open(AUDIO_CACHE_NAME).then(cache => {
        return cache.match(event.request).then(response => {
          // إذا وجدنا الصوت في التخزين المؤقت، نستخدمه
          if (response) {
            console.log('استرجاع ملف الصوت من التخزين المؤقت:', event.request.url);
            return response;
          }
          
          // وإلا نجلبه من الخادم ونخزنه
          return fetch(event.request).then(networkResponse => {
            if (!networkResponse || networkResponse.status !== 200) {
              console.error('الاستجابة غير صالحة لملف الصوت:', networkResponse?.status);
              throw new Error('استجابة الشبكة غير صالحة');
            }
            
            console.log('تم تحميل ملف الصوت من الشبكة:', event.request.url);
            
            // نسخة للتخزين
            const responseToCache = networkResponse.clone();
            
            // تخزين الملف الصوتي
            console.log('تخزين ملف الصوت في التخزين المؤقت:', event.request.url);
            cache.put(event.request, responseToCache);
            
            return networkResponse;
          }).catch(error => {
            console.error('خطأ في تحميل ملف الصوت:', error, event.request.url);
            return new Response('خطأ في تحميل ملف الصوت', { 
              status: 502, 
              headers: { 'Content-Type': 'text/plain' } 
            });
          });
        });
      })
    );
    return;
  }
  
  // للطلبات الأخرى، نستخدم سلوك الكاش القياسي
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // إرجاع المحتوى من التخزين المؤقت إذا وجد
        if (response) {
          return response;
        }
        
        // وإلا، قم بجلب المحتوى من الشبكة
        return fetch(event.request)
          .then(response => {
            // تحقق من وجود استجابة صالحة
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // نسخ الاستجابة لأن الاستجابات هي streams ويمكن استهلاكها مرة واحدة فقط
            const responseToCache = response.clone();
            
            // إضافة الاستجابة إلى التخزين المؤقت
            caches.open(CACHE_NAME)
              .then(cache => {
                // تخزين المصادر الديناميكية فقط من موقعنا، وليس الملفات الخارجية
                if (event.request.url.startsWith(self.location.origin)) {
                  cache.put(event.request, responseToCache);
                }
              });
            
            return response;
          })
          .catch(error => {
            console.error('خطأ في جلب المورد:', error);
            // إرجاع صفحة خطأ دون اتصال
            if (event.request.mode === 'navigate') {
              return caches.match('/');
            }
          });
      })
  );
});

// تحديث Service Worker وحذف النسخ القديمة من التخزين المؤقت
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME, AUDIO_CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            console.log('حذف التخزين المؤقت القديم:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  
  // تفعيل على الفور دون انتظار تحميل الصفحات
  event.waitUntil(self.clients.claim());
});