# Predicting the Future of Hotel Bookings: A Strategic Plan to Prevent Cancellations and Increase Revenue
---

## 1. Business Understanding
Pembatalan reservasi yang mendadak dapat menurunkan pendapatan dan menimbulkan kerugian pada hotel, karena kamar yang sudah dipesan menjadi kosong dan sulit diisi kembali dalam waktu singkat. Untuk mengantisipasi hal ini, hotel ingin memanfaatkan data historis, seperti informasi pelanggan, tipe kamar, segmen pasar, dan variabel terkait lainnya, untuk memprediksi kemungkinan pembatalan reservasi. Dengan mengetahui reservasi yang berisiko tinggi dibatalkan, hotel dapat mengambil langkah preventif guna meminimalkan dampak negatif.

## 2. Problem Statment
Proses pembatalan reservasi dapat berdampak langsung pada pendapatan hotel. Tanpa adanya informasi atau prediksi mengenai kemungkinan pembatalan, hotel akan kesulitan dalam mengelola tingkat hunian kamar secara efisien dan merancang strategi untuk mengantisipasi pembatalan mendadak, selain itu hotel juga gagal memperoleh 100% pendapatan dari reservasi tersebut. Hotel ingin memprediksi kemungkinan pembatalan reservasi agar dapat mengurangi potensi kerugian dan meningkatkan efisiensi operasional. Dengan memanfaatkan data yang tersedia, seperti asal negara pelanggan, segmen pasar, riwayat pembatalan sebelumnya, perubahan dalam reservasi, serta permintaan khusus, hotel berharap dapat membuat keputusan yang lebih baik sebelum pembatalan terjadi.

Contoh Kasus: <br>
Seorang pelanggan memesan kamar seharga IDR 400k per malam untuk satu malam. Jika pelanggan membatalkan reservasi tersebut, hotel akan kehilangan pendapatan IDR 400k dan tetap menanggung biaya operasional. Selain itu, hotel perlu mengalokasikan waktu dan sumber daya untuk mengisi kembali kamar kosong tersebut, yang tidak selalu mudah jika waktu pembatalan terlalu mendadak. Oleh karena itu, kemampuan untuk memprediksi pembatalan akan sangat membantu hotel dalam mengambil tindakan antisipatif, seperti memberikan promo khusus atau menyesuaikan strategi pemasaran.

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
| **Model**               | **Resampling Method** | **Mean F2** | **Std Dev** | **Catatan**                                                          |
| ----------------------- | --------------------- | ----------- | ----------- | -------------------------------------------------------------------- |
| **KNN Classifier**      | Tanpa Resample        | 0.359       | 0.025       | Performa rendah, tidak cocok untuk data imbalance                    |
| **Stacking Classifier** | Tanpa Resample        | 0.357       | 0.025       | Kompleks tapi tidak memberikan peningkatan performa                  |
| **XGBoost Classifier**  | Tanpa Resample        | 0.354       | 0.022       | Eksekusi cepat namun tidak efektif menangani ketidakseimbangan kelas |
| **SVM Classifier**      | ADASYN                | **0.717**   | 0.011       | F2 tertinggi, sangat stabil, cocok untuk fokus recall & F2           |
| **Gradient Boosting**   | Random Undersampling  | 0.711       | 0.007       | Kompetitif dan cepat, hasil konsisten across fold                    |
| **SVM Classifier**      | SMOTEENN              | 0.707       | 0.013       | Kinerja kuat, meski sedikit fluktuatif antar fold                    |


Model tanpa resampling menunjukkan performa F2 Score yang rendah (< 0.36), menandakan ketidakefisienannya dalam menangani masalah kelas tidak seimbang seperti prediksi pembatalan. Sebaliknya, pendekatan dengan teknik resampling khususnya **SVM dengan ADASYN** secara signifikan meningkatkan performa dengan **F2 Score mencapai 0.717**, menjadikannya pilihan paling tepat untuk kasus yang menekankan recall dan pengurangan False Negative.


## 6. Hyperparameter Tuning Summary
| **Model**              | **F2 Score (Train)** | **F2 Score (Test)** | **Recall (Test)** | **Precision (Test)** |
| ---------------------- | -------------------- | ------------------- | ----------------- | -------------------- |
| **SVM Setelah Tuning** | 0.756                | 0.743               | 0.902             | 0.440                |
| **SVM Sebelum Tuning** | 0.732                | 0.744               | 0.898             | 0.444                |


Tuning pada SVM Classifier berhasil meningkatkan F2 Score di training set dan mempertahankan performa di test set. Model tetap sangat baik dalam mengenali pembatalan (recall tinggi), tanpa overfitting, dan F2 Score yang optimal menegaskan model ini cocok untuk kasus dengan fokus pada kelas positif.


## 7. Model Evaluation Summary

**Model terbaik: SVM Classifier dengan 0.21 Treshold**


* **True Negative (TN) = 865** → Tamu yang **tidak membatalkan booking** dan **diprediksi tidak membatalkan**. Ini adalah prediksi yang tepat dan tidak perlu intervensi dari bisnis.

* **False Positive (FP) = 640** → Tamu yang **sebenarnya tidak membatalkan**, tetapi **diprediksi akan membatalkan**. Hal ini bisa menyebabkan tindakan pencegahan yang tidak perlu, seperti promosi yang memboroskan sumber daya.

* **False Negative (FN) = 15** → Tamu yang **membatalkan booking**, tetapi **tidak terdeteksi oleh model**. Ini berarti bisnis kehilangan kesempatan untuk mencegah pembatalan.

* **True Positive (TP) = 450** → Tamu yang **akan membatalkan booking** dan **berhasil terdeteksi** oleh model. Ini merupakan peluang bagi bisnis untuk melakukan intervensi dan mengurangi pembatalan.

**Summary**

1. **Threshold 0.21 menghasilkan F2 Score tertinggi sebesar 0.763**, dibandingkan threshold default yang hanya mencapai sekitar 0.744. Ini menunjukkan peningkatan signifikan dalam keseimbangan antara recall dan precision dengan penekanan pada recall (sesuai bobot F2).

2. Pada threshold ini, **True Positive (TP) meningkat menjadi 450** dari sebelumnya 417, dan **False Negative (FN) menurun drastis menjadi 15** dari 48. Ini berarti model jauh lebih baik dalam mengenali pelanggan yang benar-benar akan membatalkan (kelas 1).

3. Peningkatan recall ini datang dengan trade-off berupa **kenaikan False Positive (FP) menjadi 640**, yang berarti lebih banyak prediksi salah terhadap pelanggan yang seharusnya tidak membatalkan. Namun, berdasarkan skor F2 tertinggi, threshold 0.21 adalah titik optimal jika fokus utama adalah meminimalkan kasus pembatalan yang terlewat.



## 8. Conclusion

1. **Support Vector Classifier (SVC) dengan Threshold 0.21 adalah Model Terbaik secara Bisnis dan Teknikal**   
   Model SVC memberikan performa **F2 Score tertinggi (0.74)** dan Recall yang sangat tinggi (**0.90**) setelah threshold diturunkan ke **0.21**. Hal ini memungkinkan model menangkap hampir semua reservasi yang berisiko batal, sekaligus **menghemat Rp 154 juta (83%)** dibandingkan skenario tanpa intervensi.

2. **Model Memahami Pola Nyata Pembatalan Reservasi**   
   Berdasarkan analisis SHAP, fitur-fitur seperti `market_segment_Online TA`, `customer_type_Transient`, dan `required_car_parking_spaces` adalah pendorong utama prediksi pembatalan. Ini menunjukkan bahwa model SVC **tidak hanya akurat**, tapi juga **mampu menangkap dinamika perilaku pelanggan** secara realistis, dan **mudah dijelaskan ke tim bisnis atau pemasaran**.

3. **Fokus pada F2 Score Memberikan Keseimbangan Terbaik untuk Tujuan Bisnis**   
   Dalam konteks prediksi pembatalan, **F2 Score menjadi metrik paling relevan** karena menekankan Recall lebih besar daripada Precision. Model SVC yang dioptimalkan untuk F2 memastikan **lebih banyak pembatalan bisa dicegah**, tanpa mengorbankan efisiensi secara drastis. Pendekatan ini sejalan dengan prioritas hotel: **meminimalkan kehilangan pendapatan**, bukan sekadar meningkatkan akurasi.


## 9.  Recomendation

1. **Terapkan Model SVC di Sistem Reservasi Secara Real-Time**   
   Integrasikan model ke dalam alur pemesanan agar setiap reservasi baru langsung dievaluasi risikonya. Prediksi pembatalan bisa digunakan sebagai dasar pengambilan keputusan intervensi seperti penawaran diskon, upgrade, atau reminder otomatis.

2. **Gunakan Threshold 0.21 untuk Intervensi**   
   Threshold ini terbukti memberikan **F2 Score tertinggi**, menjaga sensitivitas model terhadap pembatalan. Terapkan threshold ini saat menentukan siapa yang layak menerima insentif pencegahan.

3. **Fokuskan Intervensi ke Segmen Berisiko Tinggi**   
   Prioritaskan upaya pemasaran ke pelanggan dengan ciri `market_segment_Online TA`, `customer_type_Transient`, dan tanpa kebutuhan parkir karena mereka terbukti paling berkontribusi terhadap pembatalan. 


## 10. How to use 

### A. Requirements:
* Python 3.13 atau lebih tinggi
* Jupyter Notebook

### B. Installation:
```
git clone https://github.com/Meowstronot/hotel__booking_predict
cd hotel__booking_predict
pip install -r requirements.txt
```

### C. Run Analysis:
* Buka file `Revisi_hotel_booking_cancelation.ipynb` dengan Jupyter Notebook.
* Jalankan setiap sel untuk melihat analisis dan hasil prediksi.

## 11. Contact 
* **Nama**: Moh. Khisanul Fakhrudin Akbar
* **Email**: shinaruikhisan@gmail.com
* **LinkedIn**: [linkedin.com/in/muhammad-khisanul-fakhrudin-akbar](https://www.linkedin.com/in/muhammad-khisanul-fakhrudin-akbar/)

