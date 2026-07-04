import os
import pickle

# PC Güvenlik Sistemi - Lite Mod (Dosya tabanlı yönetim)
print("🗃️ FaceDatabase: Lite Mod aktif (Dosya tabanlı)")
import logging
from config import KNOWN_FACES_DIR

class FaceDatabase:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_data_file = "face_data.pkl"
        
        # Klasör oluştur
        if not os.path.exists(KNOWN_FACES_DIR):
            os.makedirs(KNOWN_FACES_DIR)
        
        self.load_known_faces()
    
    def add_person(self, image_path, person_name):
        """Yeni kişi ekle (Lite Mod - Dosya tabanlı)"""
        try:
            # Dosya zaten known_faces klasöründeyse sadece onay ver
            if os.path.dirname(image_path) == KNOWN_FACES_DIR:
                logging.info(f"✅ Kişi dosyası zaten doğru konumda: {person_name}")
                return True
            else:
                # Dosyayı kopyala
                import shutil
                target_path = os.path.join(KNOWN_FACES_DIR, f"{person_name}.jpg")
                shutil.copy2(image_path, target_path)
                logging.info(f"✅ Kişi dosyası kopyalandı: {person_name}")
                return True
                
        except Exception as e:
            logging.error(f"❌ Kişi eklenirken hata: {str(e)}")
            return False
    
    def load_known_faces(self):
        """Kayıtlı yüzleri yükle"""
        try:
            # Pickle dosyasından yükle
            if os.path.exists(self.face_data_file):
                with open(self.face_data_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data['encodings']
                    self.known_face_names = data['names']
                logging.info(f"Kayıtlı {len(self.known_face_names)} kişi yüklendi")
            else:
                # known_faces klasöründen yükle
                self.load_from_directory()
                
        except Exception as e:
            logging.error(f"Yüzler yüklenirken hata: {str(e)}")
            self.known_face_encodings = []
            self.known_face_names = []
    
    def load_from_directory(self):
        """Klasörden yüzleri yükle"""
        for filename in os.listdir(KNOWN_FACES_DIR):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                person_name = os.path.splitext(filename)[0]
                image_path = os.path.join(KNOWN_FACES_DIR, filename)
                self.add_person(image_path, person_name)
    
    def save_face_data(self):
        """Yüz verilerini kaydet"""
        try:
            data = {
                'encodings': self.known_face_encodings,
                'names': self.known_face_names
            }
            with open(self.face_data_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            logging.error(f"Veri kaydedilirken hata: {str(e)}")
    
    def get_known_faces_count(self):
        """Kayıtlı yüz sayısını döndür"""
        return len(self.get_known_names())
    
    def get_known_names(self):
        """Kayıtlı isimleri döndür (Lite Mod - Dosya tabanlı)"""
        names = []
        try:
            for filename in os.listdir(KNOWN_FACES_DIR):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # Timestamp'i temizle
                    name_parts = os.path.splitext(filename)[0].split('_')
                    person_name = name_parts[0] if name_parts else os.path.splitext(filename)[0]
                    if person_name not in names:
                        names.append(person_name)
        except Exception as e:
            logging.error(f"❌ İsim listesi hatası: {e}")
        return names
    
    def delete_person(self, person_name):
        """Kişiyi veritabanından sil (Lite Mod - Dosya tabanlı)"""
        try:
            logging.warning(f"🔍 Kişi silme işlemi başlatıldı: '{person_name}'")
            
            # Klasör varlığını kontrol et
            if not os.path.exists(KNOWN_FACES_DIR):
                logging.error(f"❌ Klasör bulunamadı: {KNOWN_FACES_DIR}")
                return False, f"Klasör bulunamadı: {KNOWN_FACES_DIR}"
            
            # Kişiye ait tüm dosyaları bul ve sil
            deleted_files = []
            files_to_delete = []
            all_files = []
            
            # Klasördeki tüm dosyaları listele
            try:
                all_files = os.listdir(KNOWN_FACES_DIR)
            except Exception as list_error:
                logging.error(f"❌ Klasör listeleme hatası: {list_error}")
                return False, f"Klasör listeleme hatası: {str(list_error)}"
            
            # Önce silinecek dosyaları belirle
            for filename in all_files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # Dosya adından kişi ismini al
                    name_parts = os.path.splitext(filename)[0].split('_')
                    file_person_name = name_parts[0] if name_parts else os.path.splitext(filename)[0]
                    
                    if file_person_name == person_name:
                        files_to_delete.append(filename)
            
            # Dosyaları sil
            for filename in files_to_delete:
                file_path = os.path.join(KNOWN_FACES_DIR, filename)
                try:
                    # Dosya varlığını kontrol et
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        deleted_files.append(filename)
                    else:
                        logging.warning(f"⚠️ Dosya zaten yok: {filename}")
                except Exception as file_error:
                    logging.error(f"❌ Dosya silinemedi {filename}: {file_error}")
            
            # Pickle dosyasını da güncelle/sil
            try:
                if os.path.exists(self.face_data_file):
                    os.remove(self.face_data_file)
            except Exception as pickle_error:
                logging.warning(f"⚠️ Pickle dosyası silinemedi: {pickle_error}")
            
            if deleted_files:
                logging.warning(f"✅ Toplam silinen dosyalar: {deleted_files}")
                return True, f"{len(deleted_files)} dosya başarıyla silindi:\n{chr(10).join(deleted_files)}"
            else:
                logging.warning(f"⚠️ '{person_name}' adında kişi bulunamadı")
                return False, f"'{person_name}' adında hiçbir dosya bulunamadı"
                
        except Exception as e:
            logging.error(f"❌ Kişi silme hatası: {e}")
            return False, f"Silme hatası: {str(e)}"
