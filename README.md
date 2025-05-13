# Predicting the Future of Hotel Bookings: A Strategic Plan to Prevent Cancellations and Increase Revenue
---

## 1. Business Understanding
Pembatalan reservasi yang mendadak dapat menurunkan pendapatan dan menimbulkan kerugian pada hotel, karena kamar yang sudah dipesan menjadi kosong dan sulit diisi kembali dalam waktu singkat. Untuk mengantisipasi hal ini, hotel ingin memanfaatkan data historis, seperti informasi pelanggan, tipe kamar, segmen pasar, dan variabel terkait lainnya, untuk memprediksi kemungkinan pembatalan reservasi. Dengan mengetahui reservasi yang berisiko tinggi dibatalkan, hotel dapat mengambil langkah preventif guna meminimalkan dampak negatif.

## 2. Problem Statment
Proses pembatalan reservasi dapat berdampak langsung pada pendapatan hotel. Tanpa adanya informasi atau prediksi mengenai kemungkinan pembatalan, hotel akan kesulitan dalam mengelola tingkat hunian kamar secara efisien dan merancang strategi untuk mengantisipasi pembatalan mendadak, selain itu hotel juga gagal memperoleh 100% pendapatan dari reservasi tersebut. Hotel ingin memprediksi kemungkinan pembatalan reservasi agar dapat mengurangi potensi kerugian dan meningkatkan efisiensi operasional. Dengan memanfaatkan data yang tersedia, seperti asal negara pelanggan, segmen pasar, riwayat pembatalan sebelumnya, perubahan dalam reservasi, serta permintaan khusus, hotel berharap dapat membuat keputusan yang lebih baik sebelum pembatalan terjadi.

Contoh Kasus: <br>
Seorang pelanggan memesan kamar seharga $150 per malam untuk satu malam. Jika pelanggan membatalkan reservasi tersebut, hotel akan kehilangan pendapatan $150 dan tetap menanggung biaya operasional. Selain itu, hotel perlu mengalokasikan waktu dan sumber daya untuk mengisi kembali kamar kosong tersebut, yang tidak selalu mudah jika waktu pembatalan terlalu mendadak. Oleh karena itu, kemampuan untuk memprediksi pembatalan akan sangat membantu hotel dalam mengambil tindakan antisipatif, seperti memberikan promo khusus atau menyesuaikan strategi pemasaran.

## 3. Goals
Hotel ingin memiliki kemampuan untuk memprediksi kemungkinan pembatalan setiap reservasi yang masuk. Informasi ini akan membantu tim pemasaran untuk lebih fokus pada pelanggan yang berisiko tinggi membatalkan reservasi dan mengambil langkah preventif yang tepat, seperti memberikan penawaran khusus, diskon, atau pengingat yang dipersonalisasi, guna mengurangi kemungkinan pembatalan.

Selain itu, hotel juga ingin memahami faktor-faktor utama yang memengaruhi keputusan pelanggan dalam membatalkan reservasi. Wawasan ini akan menjadi dasar bagi tim pemasaran dalam merancang strategi promosi dan kebijakan harga yang lebih efektif, serta menciptakan pengalaman pelanggan yang lebih baik guna meningkatkan loyalitas dan menurunkan tingkat pembatalan di masa mendatang.

## 4. Data Sources 
* Dataset berasal dari [Hotel Booking Demand Data Set - Kaggle](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) yang berisi lebih dari 119.000 entri pemesanan hotel antara tahun 2015 dan 2017.
* Fitur utama mencakup:
  - Tipe hotel, negara asal, channel pemesanan
  - Jumlah tamu, tanggal check-in/out, jumlah hari menginap
  - Tipe kamar, harga per malam, permintaan khusus
  - Status pembatalan (target variabel)

## 5. Model Benchmarking Summary
| Balancing Method  | Model Terbaik       | Recall CV | Std Recall CV | Recall Test | Recall Gap | Catatan                                                            |
| ----------------- | ------------------- | --------- | ------------- | ----------- | ---------- | ------------------------------------------------------------------ |
| **Undersampling** | LightGBM            | 0.8247    | 0.0167        | 0.8628      | -0.0381    | Recall test tertinggi, generalisasi baik, performa stabil          |
| **Oversampling**  | LightGBM            | 0.8024    | 0.0190        | 0.8254      | -0.023    | Konsisten performa tinggi, gap kecil, stabil                       |
| **SMOTE**         | Logistic Regression | 0.7639    | 0.0295        | 0.7651      | -0.001    | Performa paling stabil, nyaris tanpa gap, model sederhana & robust |

Berdasarkan hasil evaluasi dari tiga metode penyeimbangan data **undersampling, oversampling, dan SMOTE**, `LightGBM` menunjukkan performa terbaik pada undersampling dan oversampling, dengan nilai recall test tertinggi (hingga 0.8628) dan recall gap negatif yang menandakan generalisasi yang baik. Sementara itu, Logistic Regression unggul dalam skenario SMOTE dengan performa paling stabil dan hampir tanpa gap, namun dengan recall yang sedikit lebih rendah dibanding `LightGBM`. Mengingat pentingnya recall tinggi dalam kasus ketidakseimbangan kelas dan performa generalisasi yang kuat, `LightGBM` dengan teknik undersampling dipilih sebagai model terbaik untuk dilakukan hyperparameter tuning selanjutnya.

## 6. Hyperparameter Tuning Summary
| Model             | Accuracy Test | Recall Test | Precision Test | F1 Score Test |
|------------------|---------------|-------------|----------------|----------------|
| LGBM Default     | 0.724752      | 0.862786    | 0.458564       | 0.598846       |
| LGBM 1st Tuning  | 0.706436      | 0.891892    | 0.442268       | 0.591316       |
| LGBM 2nd Tuning  | 0.698020      | 0.912682    | 0.435948       | 0.590054       |

Setelah dilakukan dua tahap tuning terhadap model `LightGBM`, terjadi peningkatan recall yang signifikan dari 0.86 (default) menjadi 0.89 setelah tuning pertama, dan meningkat lagi menjadi 0.91 setelah tuning kedua. Peningkatan ini menunjukkan bahwa model semakin mampu mengenali kelas minoritas (kelas 1), yang terlihat dari recall kelas 1 yang naik dari **0.86** menjadi **0.91**. Meski akurasi dan precision kelas 1 sedikit menurun, hal ini merupakan trade-off yang umum ketika memaksimalkan recall pada dataset yang tidak seimbang. Secara keseluruhan, tuning kedua berhasil meningkatkan kemampuan deteksi positif (recall) tanpa penurunan drastis pada metrik lainnya, menjadikannya strategi yang efektif untuk masalah klasifikasi dengan fokus pada deteksi kelas minoritas.

## 7. Model Evaluation Summary

- LGBM 2nd Tuning adalah model terbaik berdasarkan confusion matrix.
- Memiliki False Negative (FN) paling rendah (42), yang berarti lebih banyak pembatalan berhasil terdeteksi.
- Dalam konteks bisnis, FN lebih merugikan dibandingkan False Positive (FP), karena berdampak pada hilangnya pendapatan penuh.
- Meskipun FP model ini lebih tinggi (568), dampaknya relatif kecil dan dapat ditoleransi.
- Model ini juga memiliki 439 True Positives (TP) dan 971 True Negatives (TN), menunjukkan akurasi yang baik dalam dua kelas.
- Secara keseluruhan, model ini paling efektif dalam meminimalkan kerugian akibat pembatalan yang tidak terdeteksi.

## 8. Conclusion
Dengan menggunakan model machine learning, hotel berhasil memprediksi dan mengurangi kerugian akibat pembatalan yang tidak terdeteksi secara signifikan, meskipun masih ada biaya terkait dengan prediksi yang salah. Dalam skenario tanpa machine learning, hotel harus menanggung kerugian sebesar 192.400.000 IDR karena tidak dapat melakukan antisipasi terhadap pembatalan. Namun, dengan model machine learning, kerugian dapat dikurangi menjadi 57.080.000 IDR, yang menunjukkan pengurangan kerugian sebesar **70,3%**. Meskipun ada biaya terkait dengan diskon untuk pelanggan yang salah diprediksi (False Positive) dan kerugian akibat pembatalan yang terlewat (False Negative), penggunaan machine learning memungkinkan hotel untuk lebih efisien mengelola risiko pembatalan, mengurangi kerugian, dan meningkatkan pendapatan yang hilang.

## 9.  Recomendation
1. **Fokus pada Pelanggan Berisiko Pembatalan** <br>
Dengan menggunakan model prediksi, tim pemasaran dapat mengidentifikasi pelanggan yang berisiko tinggi membatalkan reservasi. Dengan demikian, hotel bisa mengambil langkah-langkah proaktif seperti memberikan diskon, upgrade kamar, atau penawaran khusus sebelum pembatalan terjadi.

1. **Meningkatkan Pengelolaan Hunian Kamar** <br>
Prediksi pembatalan memungkinkan hotel untuk mengelola tingkat hunian kamar secara lebih efisien. Dengan mengetahui kemungkinan pembatalan lebih awal, hotel dapat melakukan penyesuaian harga dinamis, mengisi kembali kamar kosong dengan lebih cepat, atau menawarkan penawaran promosi khusus untuk menarik pelanggan baru. Ini akan mengurangi dampak dari kerugian pendapatan akibat pembatalan mendadak dan memastikan bahwa kamar terisi dengan lebih efisien.

1. **Mengurangi Potensi Kerugian Melalui Pemberian Insentif yang Terencana** <br>
Memberikan insentif kepada pelanggan dengan risiko pembatalan lebih tinggi bisa meminimalkan kerugian dari pembatalan mendadak. Misalnya, jika sistem memprediksi pembatalan pada pelanggan tertentu, tim pemasaran bisa langsung menawarkan promo waktu terbatas atau diskon tertentu untuk memastikan pelanggan tetap melanjutkan reservasi mereka. 

1. **Optimalisasi Strategi Pemasaran** <br>
Berdasarkan hasil feature importances, tim marketing dapat memanfaatkan fitur-fitur seperti asal negara pelanggan, segmen pasar, dan riwayat perubahan dalam reservasi, sehingga dapat menyusun kampanye pemasaran yang lebih terfokus. Misalnya, pelanggan dari segmen Online TA atau pelanggan dengan permintaan khusus lebih berisiko membatalkan. Dengan data ini, pemasaran dapat menyesuaikan penawaran mereka untuk meminimalkan pembatalan mendadak.


## 10. How to use 

### A. Requirements:
* Python 3.9 atau lebih tinggi
* Jupyter Notebook

### B. Installation:
```
git clone https://github.com/username/hotel-booking-cancellation
cd hotel-booking-cancellation
pip install -r requirements.txt
```

### C. Run Analysis:
* Buka file `hotel_booking_cancelation.ipynb` dengan Jupyter Notebook.
* Jalankan setiap sel untuk melihat analisis dan hasil prediksi.

## 11. Contact 
* **Nama**: Moh. Khisanul Fakhrudin Akbar
* **Email**: shinaruikhisan@gmail.com
* **LinkedIn**: [linkedin.com/in/muhammad-khisanul-fakhrudin-akbar](https://www.linkedin.com/in/muhammad-khisanul-fakhrudin-akbar/)

