import cv2
import numpy as np

# PC Güvenlik Sistemi - Lite Mod (OpenCV tabanlı)
print("🚀 PC Güvenlik Sistemi - Lite Mod aktif (OpenCV + LBPH)")
import logging
import time
from datetime import datetime
import os
from config import *
from face_database import FaceDatabase
from telegram_notifier import TelegramNotifier

# Font ve renk sabitleri
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.6
FONT_THICKNESS = 2
WHITE_COLOR = (255, 255, 255)

class FaceDetector:
    def __init__(self):
        self.face_db = FaceDatabase()
        self.telegram = TelegramNotifier()
        self.camera = None
        self.is_running = False
        self.last_detection_time = 0
        self.frame_callback = None
        self.consecutive_unknown_count = 0  # Ardışık bilinmeyen tespit sayısı
        self.last_unknown_state = False  # Son durumda bilinmeyen var mıydı
        self.photos_taken_today = 0  # Bugün çekilen fotoğraf sayısı
        self.last_photo_date = ""  # Son fotoğraf tarihi
        
        # Temp klasörü oluştur
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)
    
    def set_frame_callback(self, callback):
        """Frame callback fonksiyonunu ayarla"""
        self.frame_callback = callback
    
    def initialize_camera(self):
        """Kamerayı başlat"""
        try:
            self.camera = cv2.VideoCapture(CAMERA_INDEX)
            
            if not self.camera.isOpened():
                logging.error("Kamera açılamadı")
                return False
            
            # Kamera ayarları
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
            
            logging.info("Kamera başarıyla başlatıldı")
            return True
            
        except Exception as e:
            logging.error(f"Kamera başlatılırken hata: {str(e)}")
            return False
    
    def detect_and_recognize_faces(self, frame):
        """Yüzleri tespit et ve tanı (Lite Mod - OpenCV + LBPH)"""
        # Cascade classifier'ı başlat (ilk çalıştırmada)
        if not hasattr(self, 'face_cascade'):
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
            self._load_known_faces()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        results = []
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (100, 100))
            
            # Yüz tanıma
            if hasattr(self, 'model_trained') and self.model_trained:
                label, confidence = self.face_recognizer.predict(face_roi)
                
                if confidence < 80:  # Eşik değeri
                    name = self.face_labels.get(label, "Bilinmeyen")
                    is_known = True
                else:
                    name = "Bilinmeyen"
                    is_known = False
            else:
                name = "Bilinmeyen"
                is_known = False
            
            results.append({
                'name': name,
                'location': (x, y, x+w, y+h),
                'is_known': is_known
            })
        
        return results
    
    
    def _load_known_faces(self):
        """Kayıtlı yüzleri yükle ve modeli eğit"""
        try:
            from pathlib import Path
            known_faces_dir = Path(KNOWN_FACES_DIR)
            
            faces = []
            labels = []
            self.face_labels = {}
            label_counter = 0
            
            supported_formats = ('.jpg', '.jpeg', '.png', '.bmp')
            
            for image_file in known_faces_dir.glob("*"):
                if image_file.suffix.lower() in supported_formats:
                    try:
                        # İsmi dosya adından al (timestamp'i temizle)
                        name_parts = image_file.stem.split('_')
                        person_name = name_parts[0] if name_parts else image_file.stem
                        
                        # Resmi yükle
                        image = cv2.imread(str(image_file))
                        if image is None:
                            continue
                        
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        detected_faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                        
                        if len(detected_faces) > 0:
                            (x, y, w, h) = detected_faces[0]
                            face_roi = gray[y:y+h, x:x+w]
                            face_roi = cv2.resize(face_roi, (100, 100))
                            
                            faces.append(face_roi)

                            if person_name not in self.face_labels:
                                self.face_labels[person_name] = label_counter
                                label_counter += 1

                            labels.append(self.face_labels[person_name])
                            
                    except Exception as e:
                        logging.error(f"Hafif mod yüz yükleme hatası {image_file}: {e}")
            
            # Model eğit
            if len(faces) > 0:
                # Yeni recognizer oluştur (önceki modeli temizlemek için)
                self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
                self.face_recognizer.train(faces, np.array(labels))
                self.model_trained = True
                # Ters mapping
                self.face_labels = {v: k for k, v in self.face_labels.items()}
                # logging.info(f"✅ Yüz tanıma modeli {len(faces)} yüz ile eğitildi (Kişi sayısı: {len(set(labels))})")  # Gereksiz log
            else:
                self.model_trained = False
                self.face_labels = {}
                logging.warning("⚠️ Hiç kayıtlı yüz bulunamadı - Model devre dışı")
                
        except Exception as e:
            logging.error(f"Yüz yükleme hatası: {e}")
            self.model_trained = False
    
    def draw_face_boxes(self, frame, face_results):
        """Yüz kutularını çiz"""
        for result in face_results:
            left, top, right, bottom = result['location']
            name = result['name']
            is_known = result['is_known']
            
            # Kutu rengi belirle
            color = GREEN_COLOR if is_known else RED_COLOR
            
            # Kutuyu çiz
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # İsim etiketini çiz
            label = f"Known: {name}" if is_known else "Unknown"
            
            # Etiket arka planı
            label_size = cv2.getTextSize(label, FONT, FONT_SCALE, FONT_THICKNESS)[0]
            cv2.rectangle(frame, (left, top - 30), (left + label_size[0], top), color, -1)
            
            # Etiket metni
            cv2.putText(frame, label, (left, top - 10), FONT, FONT_SCALE, WHITE_COLOR, FONT_THICKNESS)
        
        return frame
    
    def save_detection_image(self, frame, face_results):
        """Tespit görüntüsünü kaydet (İyileştirilmiş)"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Bilinmeyen kişi sayısını say
            unknown_count = sum(1 for result in face_results if not result['is_known'])
            
            filename = f"unknown_{unknown_count}faces_{timestamp}.jpg"
            filepath = os.path.join(TEMP_DIR, filename)
            
            # Frame'e bilgi ekle
            info_frame = frame.copy()
            
            # Üst kısma bilgi yaz
            info_text = f"UNKNOWN DETECTION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            cv2.putText(info_frame, info_text, (10, 30), FONT, 0.7, (0, 0, 255), 2)
            
            faces_text = f"Unknown faces detected: {unknown_count}"
            cv2.putText(info_frame, faces_text, (10, 60), FONT, 0.6, (0, 0, 255), 2)
            
            # Kaydet
            cv2.imwrite(filepath, info_frame)
            logging.warning(f"🚨 Bilinmeyen kişi fotoğrafı kaydedildi: {filepath}")
            
            return filepath
            
        except Exception as e:
            logging.error(f"Görüntü kaydedilirken hata: {str(e)}")
            return None
    
    def handle_unknown_person(self, frame, face_results):
        """Bilinmeyen kişi işlemleri (Çok Sıkı Kontrol)"""
        current_time = time.time()
        today = datetime.now().strftime("%Y%m%d")
        
        # Günlük sayacı sıfırla
        if self.last_photo_date != today:
            self.photos_taken_today = 0
            self.last_photo_date = today
        
        # Günde maksimum 3 fotoğraf
        if self.photos_taken_today >= 3:
            return
        
        # Bilinmeyen kişi var mı kontrol et
        unknown_faces = [result for result in face_results if not result['is_known']]
        has_unknown = len(unknown_faces) > 0
        
        if has_unknown:
            # Bilinmeyen kişi var
            if not self.last_unknown_state:
                # İlk defa bilinmeyen kişi görüldü
                self.consecutive_unknown_count = 1
                self.last_unknown_state = True
                logging.info("🔍 Bilinmeyen kişi tespit edildi, kontrol ediliyor...")
            else:
                # Ardışık bilinmeyen tespit
                self.consecutive_unknown_count += 1
            
            # ÇOK SIKICI ŞARTLAR:
            # 1. En az 10 ardışık frame (yaklaşık 3-5 saniye)
            # 2. En az 60 saniye geçmiş olmalı
            # 3. Günde maksimum 3 fotoğraf
            if (self.consecutive_unknown_count >= 10 and 
                current_time - self.last_detection_time >= DETECTION_INTERVAL and
                self.photos_taken_today < 3):
                
                unknown_count = len(unknown_faces)
                logging.warning(f"🚨 ALARM: {unknown_count} bilinmeyen kişi tespit edildi! (Fotoğraf: {self.photos_taken_today + 1}/3)")
                
                # Görüntüyü kaydet
                image_path = self.save_detection_image(frame, face_results)
                
                if image_path:
                    self.photos_taken_today += 1
                    
                    # Telegram bildirimi gönder
                    self.telegram.notify_unknown_person(image_path)
                    logging.warning(f"📸 Fotoğraf kaydedildi. Bugün toplam: {self.photos_taken_today}/3")
                
                self.last_detection_time = current_time
                self.consecutive_unknown_count = 0  # Sayacı sıfırla
        else:
            # Bilinmeyen kişi yok
            if self.last_unknown_state:
                logging.info("✅ Bilinmeyen kişi alanı terk etti")
            
            self.last_unknown_state = False
            self.consecutive_unknown_count = 0
    
    def run_quick_scan(self, duration=5):
        """Hızlı tarama modu - Laptop açılışında 5 saniye çalışır"""
        if not self.initialize_camera():
            return False
        
        self.is_running = True
        start_time = time.time()
        
        logging.info(f"🚀 Hızlı güvenlik taraması başlatıldı ({duration} saniye)")
        print(f"🚀 Security scan started - {duration} seconds...")
        
        unknown_detected = False
        detection_count = 0
        
        try:
            while self.is_running and (time.time() - start_time) < duration:
                ret, frame = self.camera.read()
                
                if not ret:
                    logging.error("Kameradan görüntü alınamadı")
                    break
                
                # Yüzleri tespit et ve tanı
                face_results = self.detect_and_recognize_faces(frame)
                
                if face_results:
                    detection_count += 1
                    
                    # Bilinmeyen kişi kontrolü
                    unknown_faces = [result for result in face_results if not result['is_known']]
                    
                    if unknown_faces and not unknown_detected:
                        unknown_detected = True
                        unknown_count = len(unknown_faces)
                        
                        logging.warning(f"🚨 GÜVENLIK UYARISI: {unknown_count} bilinmeyen kişi tespit edildi!")
                        print(f"🚨 SECURITY ALERT: {unknown_count} unknown person detected!")
                        
                        # Fotoğraf çek ve kaydet
                        image_path = self.save_detection_image(frame, face_results)
                        
                        if image_path:
                            # Telegram bildirimi gönder (hızlı tarama modunda soğuma süresini atla)
                            self.telegram.notify_unknown_person(image_path, skip_cooldown=True)
                            logging.warning(f"📸 Güvenlik fotoğrafı kaydedildi ve Telegram'a gönderildi")
                            print("📸 Security photo saved and notification sent!")
                    
                    elif not unknown_faces:
                        # Sadece kayıtlı kişiler var
                        known_names = [result['name'] for result in face_results if result['is_known']]
                        if known_names:
                            logging.info(f"✅ Kayıtlı kişi tespit edildi: {', '.join(set(known_names))}")
                            print(f"✅ Registered person: {', '.join(set(known_names))}")
                
                # Kısa bekleme
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logging.info("Hızlı tarama kullanıcı tarafından durduruldu")
        
        finally:
            self.cleanup()
        
        # Sonuç raporu
        elapsed_time = time.time() - start_time
        if unknown_detected:
            logging.warning(f"⚠️ Hızlı tarama tamamlandı ({elapsed_time:.1f}s) - BİLİNMEYEN KİŞİ TESPİT EDİLDİ!")
            print(f"⚠️ Security scan completed - UNKNOWN PERSON DETECTED!")
        else:
            logging.info(f"✅ Hızlı tarama tamamlandı ({elapsed_time:.1f}s) - Güvenlik sorunu yok")
            print(f"✅ Security scan completed - No threats detected")
        
        return unknown_detected
    
    def run_detection(self):
        """Ana tespit döngüsü"""
        if not self.initialize_camera():
            return False
        
        self.is_running = True
        
        # Sistem başlangıç bildirimi
        self.telegram.notify_system_start()
        
        logging.info("Yüz tespiti başlatıldı. Çıkmak için 'q' tuşuna basın.")
        
        try:
            while self.is_running:
                ret, frame = self.camera.read()
                
                if not ret:
                    logging.error("Kameradan görüntü alınamadı")
                    break
                
                # Yüzleri tespit et ve tanı
                face_results = self.detect_and_recognize_faces(frame)
                
                # Kutuları çiz
                frame = self.draw_face_boxes(frame, face_results)
                
                # GUI'ye frame gönder
                if self.frame_callback:
                    self.frame_callback(frame.copy())
                
                # Bilinmeyen kişi kontrolü
                if face_results:
                    self.handle_unknown_person(frame, face_results)
                
                # Bilgi metni ekle (İngilizce - OpenCV uyumlu)
                info_text = f"Registered: {self.face_db.get_known_faces_count()} | Detected: {len(face_results)} faces"
                cv2.putText(frame, info_text, (10, 30), FONT, 0.5, WHITE_COLOR, 1)
                
                # Timestamp ekle
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), FONT, 0.4, WHITE_COLOR, 1)
                
                # Frame'i göster
                cv2.imshow('PC Security System - Face Recognition', frame)
                
                # Çıkış kontrolü
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except Exception as e:
            logging.error(f"Tespit döngüsünde hata: {str(e)}")
            
        finally:
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Kaynakları temizle"""
        self.is_running = False
        
        if self.camera:
            self.camera.release()
        
        cv2.destroyAllWindows()
        logging.info("Kamera ve pencereler kapatıldı")
    
    def add_known_person_interactive(self):
        """Interaktif kişi ekleme"""
        if not self.initialize_camera():
            return False
        
        print("\n=== Yeni Kişi Ekleme ===")
        name = input("Kişinin adını girin: ").strip()
        
        if not name:
            print("Geçersiz isim!")
            return False
        
        print("Kameraya bakın ve 's' tuşuna basarak fotoğraf çekin, 'q' ile çıkın...")
        
        try:
            while True:
                ret, frame = self.camera.read()
                
                if not ret:
                    break
                
                # Frame'i göster
                cv2.imshow('Fotoğraf Çekimi', frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('s'):
                    # Fotoğraf çek
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    # Türkçe karakter ve özel karakterleri temizle
                    safe_name = name.replace('ğ','g').replace('ü','u').replace('ş','s').replace('ı','i').replace('ö','o').replace('ç','c')
                    safe_name = safe_name.replace('Ğ','G').replace('Ü','U').replace('Ş','S').replace('İ','I').replace('Ö','O').replace('Ç','C')
                    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '-_')
                    filename = f"{safe_name}_{timestamp}.jpg"
                    filepath = os.path.join(KNOWN_FACES_DIR, filename)
                    
                    cv2.imwrite(filepath, frame)
                    
                    # Kişiyi veritabanına ekle
                    if self.face_db.add_person(filepath, name):
                        print(f"✅ {name} başarıyla eklendi!")
                        break
                    else:
                        print("❌ Yüz tespit edilemedi, tekrar deneyin.")
                        # Dosya varsa sil
                        if os.path.exists(filepath):
                            os.remove(filepath)
                
                elif key == ord('q'):
                    break
                    
        finally:
            self.cleanup()
        
        return True
