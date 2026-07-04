import requests
import logging
import time
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, CHAT_ID, NOTIFICATION_COOLDOWN

class TelegramNotifier:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = CHAT_ID
        self.last_notification_time = {}
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message):
        """Telegram mesajı gönder"""
        if not self.bot_token or self.bot_token == "YOUR_BOT_TOKEN_HERE" or self.bot_token.strip() == "":
            logging.warning("Telegram bot token ayarlanmamış")
            return False
        
        if not self.chat_id or self.chat_id == "YOUR_CHAT_ID_HERE" or self.chat_id.strip() == "":
            logging.warning("Telegram chat ID ayarlanmamış")
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                # logging.info("Telegram bildirimi gönderildi")  # Gereksiz log
                return True
            else:
                logging.error(f"Telegram API hatası: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Telegram bildirimi gönderilirken hata: {str(e)}")
            return False
    
    def send_photo(self, photo_path, caption=""):
        """Telegram fotoğrafı gönder"""
        if not self.bot_token or self.bot_token == "YOUR_BOT_TOKEN_HERE" or self.bot_token.strip() == "":
            logging.warning("Telegram bot token ayarlanmamış")
            return False
        
        if not self.chat_id or self.chat_id == "YOUR_CHAT_ID_HERE" or self.chat_id.strip() == "":
            logging.warning("Telegram chat ID ayarlanmamış")
            return False
        
        # Dosya varlığını kontrol et
        import os
        if not os.path.exists(photo_path):
            logging.error(f"Fotoğraf dosyası bulunamadı: {photo_path}")
            return False
        
        try:
            url = f"{self.base_url}/sendPhoto"
            
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    # logging.info(f"✅ Telegram fotoğrafı başarıyla gönderildi: {photo_path}")  # Gereksiz log
                    return True
                else:
                    logging.error(f"❌ Telegram API hatası: {result.get('description', 'Bilinmeyen hata')}")
                    return False
            else:
                logging.error(f"❌ Telegram fotoğraf API hatası: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Telegram fotoğrafı gönderilirken hata: {str(e)}")
            return False
    
    def notify_unknown_person(self, photo_path=None, skip_cooldown=False):
        """Bilinmeyen kişi bildirimi"""
        current_time = time.time()
        
        # Soğuma süresi kontrolü (hızlı tarama modunda atla)
        if not skip_cooldown and 'unknown_person' in self.last_notification_time:
            time_diff = current_time - self.last_notification_time['unknown_person']
            if time_diff < NOTIFICATION_COOLDOWN:
                logging.info(f"⏰ Bildirim soğuma süresi aktif: {NOTIFICATION_COOLDOWN - time_diff:.0f} saniye kaldı")
                return False
        
        # Bildirim mesajı
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        message = f"""
🚨 <b>GÜVENLİK UYARISI</b> 🚨

⚠️ Bilinmeyen kişi tespit edildi!
📅 Tarih: {timestamp}
💻 Cihaz: {self.get_computer_name()}

Lütfen durumu kontrol edin.
        """.strip()
        
        # Mesajı gönder
        message_success = self.send_message(message)
        photo_success = False
        
        # Fotoğraf varsa gönder (mesaj başarısız olsa bile)
        if photo_path:
            photo_success = self.send_photo(photo_path, "🔴 Tespit edilen bilinmeyen kişi")
            if not photo_success:
                logging.error("❌ Güvenlik fotoğrafı gönderilemedi")
        else:
            logging.warning("⚠️ Fotoğraf yolu belirtilmedi")
        
        # En az biri başarılıysa soğuma süresini başlat
        if message_success or photo_success:
            self.last_notification_time['unknown_person'] = current_time
            logging.info("✅ Güvenlik bildirimi gönderildi")
            return True
        else:
            logging.error("❌ Hiçbir bildirim gönderilemedi")
            return False
    
    def notify_system_start(self):
        """Sistem başlangıç bildirimi"""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        message = f"""
✅ <b>Güvenlik Sistemi Aktif</b>

📅 Başlangıç: {timestamp}
💻 Cihaz: {self.get_computer_name()}
🎥 Kamera izleme başladı

Sistem güvenlik modunda çalışıyor.
        """.strip()
        
        return self.send_message(message)
    
    def get_computer_name(self):
        """Bilgisayar adını al"""
        try:
            import socket
            return socket.gethostname()
        except (socket.error, OSError):
            return "Bilinmeyen PC"
    
    def test_connection(self):
        """Telegram bağlantısını test et"""
        if not self.bot_token or self.bot_token == "YOUR_BOT_TOKEN_HERE" or self.bot_token.strip() == "":
            logging.warning("Telegram bot token ayarlanmamış")
            return False
        
        if not self.chat_id or self.chat_id == "YOUR_CHAT_ID_HERE" or self.chat_id.strip() == "":
            logging.warning("Telegram chat ID ayarlanmamış")
            return False
            
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get('ok'):
                    bot_name = bot_info['result'].get('first_name', 'Bot')
                    # logging.info(f"✅ Telegram bot bağlantısı başarılı: {bot_name}")  # Gereksiz log
                    return True
            
            logging.error("❌ Telegram bot bağlantısı başarısız")
            return False
            
        except Exception as e:
            logging.error(f"❌ Telegram bağlantısı test edilirken hata: {str(e)}")
            return False
    
    def test_photo_sending(self, test_image_path=None):
        """Telegram fotoğraf gönderme testi"""
        try:
            # Test resmi oluştur (eğer belirtilmemişse)
            if not test_image_path:
                import cv2
                import numpy as np
                import os
                
                # Basit test resmi oluştur
                test_image = np.zeros((200, 300, 3), dtype=np.uint8)
                test_image[:] = (0, 100, 200)  # Mavi arka plan
                cv2.putText(test_image, "TEST IMAGE", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(test_image, "Telegram Test", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                test_image_path = "telegram_test_image.jpg"
                cv2.imwrite(test_image_path, test_image)
                logging.info(f"📸 Test resmi oluşturuldu: {test_image_path}")
            
            # Fotoğrafı gönder
            success = self.send_photo(test_image_path, "🧪 Telegram Fotoğraf Testi")
            
            # Test resmini sil
            if test_image_path == "telegram_test_image.jpg" and os.path.exists(test_image_path):
                os.remove(test_image_path)
                logging.info("🗑️ Test resmi temizlendi")
            
            if success:
                # logging.info("✅ Telegram fotoğraf testi başarılı!")  # Gereksiz log
                return True
            else:
                logging.error("❌ Telegram fotoğraf testi başarısız!")
                return False
                
        except Exception as e:
            logging.error(f"❌ Telegram fotoğraf testi hatası: {str(e)}")
            return False
