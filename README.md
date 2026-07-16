# FAIROS

#@F_O_70
<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=40&duration=4000&color=39FF14&center=true&vCenter=true&width=600&height=70&lines=Z3R0_GH0ST;Python+%26+Cybersecurity;Remix+Master">
</div>




<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=40&duration=4000&color=39FF14&center=true&vCenter=true&width=600&height=70&lines=FAIROS123;Python+%26+Cybersecurity;Remix+Master">
</div>


<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=40&duration=4000&color=39FF14&center=true&vCenter=true&width=600&height=70&lines=FAIROS123;Python+%26+Cybersecurity;Remix+Master">
</div>


## 🎨 الألوان التلقائية
| العنصر | اللون | الكود |
|--------|-------|-------|
| خلفية الشاشة | أسود عميق | `#0A0A0A` |
| النصوص الرئيسية | نيون أخضر | `#39FF14` |
| الإضاءات والحدود | أزرق كهربائي | `#00D4FF` |
| التمييز والتحذيرات | برتقالي محترق | `#FF6B00` |

## 🎥 الملفات المرئية (GIF/فيديو)

### شاشة التشغيل (GIF)
![تشغيل المشروع](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGVhdmNocHMyZ3F6cTBnY3h0c3k3MnU0dXZwb2J0dzBkb3h5d3F4bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tn33aiTi1jkl6H6/giphy.gif)

### فيديو توضيحي (YouTube)
[![فيديو توضيحي](https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

---

## 📂 جميع ملفات المشروع
| الملف | الوصف | تاريخ التعديل |
|-------|-------|---------------|
| **app.py** | البوت الرئيسي لإدارة الأجهزة | 3 أيام |
| **A1** | إضافة سلاسل وكيل المستخدم | 4 شهور |
| **A2** | تغيير القيمة من 9999 إلى 0011 | الشهر الماضي |
| **A3** | إضافة معرفات GT متعددة | 4 شهور |
| **A4** | مولد وكيل مستخدم للأجهزة المحمولة | 4 شهور |
| **A5** | إعادة هيكلة الطلبات باستخدام asyncio و aiohttp | 4 شهور |
| **A6** | إضافة إدخالات اختبار إلى plist | 4 شهور |
| **A7** | تعليق استيراد requests | 4 شهور |
| **A8** | تحديث جملة الطباعة من Hello إلى Goodbye | 4 شهور |
| **A9** | تغيير السطر من 1 إلى 000 | الشهر الماضي |
| **README.md** | وصف المشروع والشعار | الآن |

---

## 🗺️ خريطة تفاعلية (JavaScript)
```html
<div id="map" style="height: 400px; width: 100%;"></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script>
// إعداد الخريطة
var map = L.map('map').setView([30.0444, 31.2357], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// بيانات تجريبية (سيتم جلبها تلقائياً من API)
var data = [
    {latitude: 30.0444, longitude: 31.2357, color: '#39FF14', species: 'نوع 1', description: 'وصف', sighted_at: '2026-07-16'},
    {latitude: 30.0524, longitude: 31.2439, color: '#00D4FF', species: 'نوع 2', description: 'وصف آخر', sighted_at: '2026-07-15'}
];

// إضافة العلامات تلقائياً
var group = L.featureGroup().addTo(map);
data.forEach(function(item) {
    var marker = L.circleMarker([item.latitude, item.longitude], {
        color: item.color,
        radius: 10,
        fillOpacity: 0.5
    }).addTo(group);
    marker.bindPopup(
        `<p><b>النوع:</b> ${item.species}</p>
         <p><b>الوصف:</b> ${item.description}</p>
         <p><b>الموقع:</b> ${item.latitude}, ${item.longitude}</p>
         <p><b>تاريخ المشاهدة:</b> ${item.sighted_at}</p>`
    );
});
map.fitBounds(group.getBounds());
</script>

