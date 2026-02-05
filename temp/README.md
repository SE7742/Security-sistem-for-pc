# Temp / Geçici Dosyalar

Bu klasör tespit edilen bilinmeyen kişilerin geçici fotoğraflarını içerir.

## İçerik

- Bilinmeyen kişi tespit fotoğrafları
- Telegram'a gönderilen görüntüler
- Geçici işlem dosyaları

## Önemli

⚠️ **Gizlilik Uyarısı**: Bu klasördeki dosyalar `.gitignore` tarafından Git'e yüklenmez.
Tespit fotoğraflarınız GitHub'a gönderilmez.

## Otomatik Temizlik

- Geçici dosyalar `AUTO_CLEANUP_DAYS` ayarına göre otomatik olarak silinir (varsayılan: 7 gün)
- `MAX_TEMP_FILES` değerine ulaşıldığında en eski dosyalar silinir (varsayılan: 100 dosya)
