// تسجيل Service Worker عند تحميل الصفحة
window.addEventListener('load', () => {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/service-worker.js')
      .then(registration => {
        console.log('Service Worker سجل بنجاح مع النطاق: ', registration.scope);
        
        // فرض تحديث Service Worker
        registration.update();
        
        // التعامل مع أحداث تحديث Service Worker
        registration.addEventListener('updatefound', function() {
            // احصل على Service Worker الجديد
            const newWorker = registration.installing;
            
            // تسجيل حالة التغيير
            newWorker.addEventListener('statechange', function() {
                console.log('Service Worker تغيرت حالته إلى: ', newWorker.state);
                
                // إذا تم التنصيب بنجاح
                if (newWorker.state === 'activated') {
                    console.log('تم تنشيط Service Worker الجديد');
                }
            });
        });
      })
      .catch(error => {
        console.log('فشل تسجيل Service Worker: ', error);
      });
  }
  
  // تحميل ملفات الصوت مسبقًا عند توفر اتصال بالإنترنت
  if (navigator.onLine && 'serviceWorker' in navigator) {
    // تحميل أول 5 ملفات صوتية بعد تحميل الصفحة بوقت قصير
    setTimeout(function() {
      for (let i = 1; i <= 5; i++) {
        fetch(`/api/audio/${i}`, { cache: 'force-cache' })
          .then(response => {
            if (response.ok) {
              console.log(`تم تحميل ملف الصوت للآية ${i} مسبقًا`);
            }
          })
          .catch(err => {
            console.error(`فشل تحميل ملف الصوت للآية ${i}:`, err);
          });
      }
    }, 3000);
  }
  
  // إضافة حدث "التثبيت" للأجهزة المحمولة
  let deferredPrompt;
  
  window.addEventListener('beforeinstallprompt', (e) => {
    // منع ظهور الحوار التلقائي
    e.preventDefault();
    // حفظ الحدث للاستخدام لاحقا
    deferredPrompt = e;
    // عرض زر التثبيت إذا كان موجودا
    const installButton = document.getElementById('installButton');
    if (installButton) {
      installButton.style.display = 'block';
      
      installButton.addEventListener('click', async () => {
        // إخفاء زر التثبيت
        installButton.style.display = 'none';
        // عرض حوار التثبيت
        deferredPrompt.prompt();
        // انتظار اختيار المستخدم
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`نتيجة اختيار المستخدم: ${outcome}`);
        // لم نعد بحاجة لهذا الحدث
        deferredPrompt = null;
      });
    }
  });
  
  // معالجة وضع عدم الاتصال بالإنترنت وإظهار إشعارات للمستخدم
  window.addEventListener('offline', function() {
    console.log('أنت غير متصل بالإنترنت، سيتم استخدام الملفات المخزنة مسبقًا');
    showNotification('أنت غير متصل بالإنترنت', 'سيتم استخدام الملفات المخزنة مسبقًا', 'warning');
  });
  
  window.addEventListener('online', function() {
    console.log('تم استعادة الاتصال بالإنترنت');
    showNotification('تم استعادة الاتصال', 'يمكنك الآن استخدام جميع الميزات', 'success');
  });
  
  // دالة مساعدة لعرض الإشعارات
  function showNotification(title, message, type = 'info') {
    // إنشاء عنصر الإشعار
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    notification.style.zIndex = '9999';
    notification.style.maxWidth = '90%';
    notification.innerHTML = `
      <strong>${title}</strong> - ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="إغلاق"></button>
    `;
    
    // إضافة الإشعار إلى المستند
    document.body.appendChild(notification);
    
    // إخفاء الإشعار تلقائيًا بعد فترة
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        notification.remove();
      }, 500);
    }, 5000);
  }
});