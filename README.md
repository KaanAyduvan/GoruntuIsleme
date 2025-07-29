
<img width="1414" height="2000" alt="GÖRÜNTÜ İŞLEME İLE EL HAREKETLERİNDEN OYUN" src="https://github.com/user-attachments/assets/4f9496a1-4ac1-4fe0-bb9a-0b8c4046493f" />


# Görüntü İşleme - El işaretleri ile Tetris ve Jetpack Joyride

Bu proje, basit sayılabilecek bir el işareti algılama modelinin ürünleştirilme ve model kurulumu projesidir.

## Kullanılan Veri Seti

https://github.com/hukenovs/hagrid

Fazlaca el görseli bulunan HaGRID veri setinden:

- **like**
- **dislike**
- **palm**
- **fist**
- **one**
- **timeout**
- **no_gesture**

sınıfları kullanılmıştır.

## Kullanılan Kütüphaneler ve Yöntem

- **OpenCV**
- **MediaPipe**
- **MobileNetv2**
- **Tensorflow**

Modeli eğitirken TransferredLearning yöntemi kullanıldı. MobileNet gibi daha hafif ve verimli çalışan bir modelin her bir katmanını tekrardan eğitmek yerine, son katmanına kendi görsellerimiz ile eğitim gerçekleştirildi.

**Başarı Metrikleri:** 
Epoch 1: loss: 0.7426 - accuracy: 0.7681 - val_loss: 0.4681 - val_accuracy: 0.8543
Epoch 2: loss: 0.4264 - accuracy: 0.8648 - val_loss: 0.3829 - val_accuracy: 0.8796
Epoch 3: loss: 0.3739 - accuracy: 0.8809 - val_loss: 0.3668 - val_accuracy: 0.8859
Epoch 4: loss: 0.3471 - accuracy: 0.8874 - val_loss: 0.3586 - val_accuracy: 0.8832
Epoch 5: loss: 0.3301 - accuracy: 0.8926 - val_loss: 0.3324 - val_accuracy: 0.8933

## Nasıl Kullanılır?
elyakalama.ipynb notebook'unu açtığınızda 4 hücre göreceksiniz. Projeyi çalıştırmak için şu adımları izleyin:

- Gereksinimlerin yüklü olduğundan emin olun.
- Kütüphanelerin bulunduğu ilk hücreyi çalıştırın.
- 3. ve 4. hücrelerde bulunan oyunlardan birini seçip çalıştırın.
- Hücresini çalıştırdığınız oyunun kod dosyasını açıp çalıştırın.

sonrasında hem oyun hem de kamera ekranınızda belirecektir.

## Alıntı Oyunlar
Jetpack Joyride klonu için @Gustavo-Pauli'ye https://github.com/Gustavo-Pauli/Jetpack-Goodride
Tetris klonu için ise @rajat https://github.com/rajatdiptabiswas
Teşekkürlerimi sunarım. Oyunları geliştiren ve açık kaynaklı paylaşan geliştiricilerdir.

