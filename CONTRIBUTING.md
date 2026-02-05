# Katkıda Bulunma

Projeye katkıda bulunmak istiyorsanız aşağıdaki adımları takip edebilirsiniz.

## Hata Bildirimi

- GitHub Issues üzerinden hata bildirebilirsiniz
- Hatayı tekrar oluşturma adımlarını yazın
- Python sürümü ve işletim sistemi bilgisini ekleyin

## Kod Katkısı

### 1. Fork ve Clone

```bash
git clone https://github.com/KULLANICI_ADINIZ/Security-sistem-for-pc.git
cd Security-sistem-for-pc
```

### 2. Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Branch Oluştur

```bash
git checkout -b feature/yeni-ozellik
# veya
git checkout -b fix/hata-duzeltme
```

### 4. Test Et

```bash
python test_system.py
```

### 5. Commit ve Push

```bash
git add .
git commit -m "feat: yeni özellik eklendi"
git push origin feature/yeni-ozellik
```

### 6. Pull Request

GitHub üzerinden Pull Request oluşturun.

## Commit Mesajları

- `feat:` Yeni özellik
- `fix:` Hata düzeltme
- `docs:` Dokümantasyon
- `refactor:` Kod düzenleme

## Kod Standartları

- PEP 8 kurallarına uyun
- Fonksiyonlara docstring ekleyin
- Anlaşılır değişken isimleri kullanın

## Lisans

Katkılarınız MIT lisansı altında yayınlanacaktır.
