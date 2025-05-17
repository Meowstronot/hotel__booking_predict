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
| **Balancing Method** | **Model Terbaik**   | **Recall CV** | **Std Recall CV** | **Recall Test** | **Recall Gap** | **Catatan**                                                           |
| -------------------- | ------------------- | ------------- | ----------------- | --------------- | -------------- | --------------------------------------------------------------------- |
| **Undersampling**    | LightGBM            | 0.8266        | 0.0269            | 0.8415          | -0.0149        | Recall test tertinggi, generalisasi cukup baik, performa masih stabil |
| **Oversampling**     | LightGBM            | 0.8111        | 0.0166            | 0.8351          | -0.0240        | Performa tinggi dan stabil, meskipun gap sedikit lebih besar          |
| **SMOTE**            | Logistic Regression | 0.7812        | 0.0131            | 0.7859          | -0.0047        | Performa paling stabil, gap kecil, model sederhana dan robust         |


Berdasarkan hasil evaluasi dari tiga metode penyeimbangan data **undersampling, oversampling, dan SMOTE**, `LightGBM` menunjukkan performa terbaik pada undersampling dan oversampling, dengan nilai recall test tertinggi (hingga 0.84) dan recall gap negatif yang menandakan generalisasi yang baik. Sementara itu, Logistic Regression unggul dalam skenario SMOTE dengan performa paling stabil dan hampir tanpa gap, namun dengan recall yang sedikit lebih rendah dibanding `LightGBM`. Mengingat pentingnya recall tinggi dalam kasus ketidakseimbangan kelas dan performa generalisasi yang kuat, `LightGBM` dengan teknik undersampling dipilih sebagai model terbaik untuk dilakukan hyperparameter tuning selanjutnya.

## 6. Hyperparameter Tuning Summary
| **Model**           | **Accuracy Test** | **Recall Test** | **Precision Test** | **F1 Score Test** |
| ------------------- | ----------------- | --------------- | ------------------ | ----------------- |
| **LGBM 1st Tuning** | 0.712114          | 0.867238        | 0.444566           | 0.587808          |
| **LGBM 2nd Tuning** | 0.700456          | 0.860814        | 0.433190           | 0.576344          |
| **LGBM Default**    | 0.706031          | 0.841542        | 0.437152           | 0.575403          |
| **Logistic Reg Tuning** | 0.709579      | 0.790150        | 0.437204           | 0.562929          |
| **Logistic Reg Default** | 0.712620     | 0.785867        | 0.440048           | 0.564181          |


Berdasarkan hasil perbandingan antara model terbaik (LGBM Default dan Logistic Regression Default) dengan model setelah tuning (LGBM 1st Tuning, LGBM 2nd Tuning, dan Logistic Reg Tuning), model *LGBM 1st Tuning* menunjukkan hasil terbaik dalam hal **Recall Test** dengan skor 0.8672. Ini mengindikasikan bahwa *LGBM 1st Tuning* berhasil menangkap lebih banyak kelas positif dibandingkan model lainnya. Meskipun model *Logistic Regression Tuning* memiliki skor recall yang baik (0.7901), performa recall *LGBM 1st Tuning* tetap lebih unggul, menandakan bahwa tuning pada model *LGBM* memberikan peningkatan signifikan dalam kemampuan deteksi kelas positif.



## 7. Model Evaluation Summary

**Model terbaik: LGBM 1st Tuning**

* Memiliki **False Negative (FN) terendah**, yaitu **62**, menunjukkan kemampuannya yang paling baik dalam mendeteksi reservasi yang akan dibatalkan. Ini sangat penting karena pembatalan yang tidak terdeteksi dapat menyebabkan kerugian pendapatan bagi hotel.

* Mencapai **True Positive (TP) tertinggi**, yakni **405**, yang berarti model ini paling akurat dalam mengidentifikasi kasus pembatalan secara benar.

* **False Positive (FP)** sebesar **506**, lebih rendah dibandingkan LGBM 2nd Tuning, dan masih dalam batas yang dapat ditoleransi mengingat fokus utama adalah meminimalkan kerugian dari FN.

* **True Negative (TN)** sebanyak **1000**, menandakan bahwa model juga cukup andal dalam mengenali reservasi yang tidak dibatalkan.

* **Kesimpulan:** Dengan kombinasi FN yang rendah dan TP yang tinggi, LGBM 1st Tuning memberikan keseimbangan terbaik antara efektivitas dalam mendeteksi pembatalan dan kestabilan model, menjadikannya pilihan yang paling optimal untuk diterapkan dalam konteks bisnis hotel.


## 8. Conclusion
Dengan menggunakan model machine learning, hotel berhasil memprediksi dan mengurangi kerugian akibat pembatalan yang tidak terdeteksi secara signifikan, meskipun masih ada biaya terkait dengan prediksi yang salah. Dalam skenario tanpa machine learning, hotel harus menanggung kerugian sebesar 186.800.000 IDR karena tidak dapat melakukan antisipasi terhadap pembatalan. Namun, dengan model machine learning, kerugian dapat dikurangi menjadi 60.760.000 IDR, yang menunjukkan pengurangan kerugian sebesar **67%**. Meskipun ada biaya terkait dengan diskon untuk pelanggan yang salah diprediksi (False Positive) dan kerugian akibat pembatalan yang terlewat (False Negative), penggunaan machine learning memungkinkan hotel untuk lebih efisien mengelola risiko pembatalan, mengurangi kerugian, dan meningkatkan pendapatan yang hilang.

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
* Python 3.13 atau lebih tinggi
* Jupyter Notebook

### B. Installation:
```
git clone https://github.com/Meowstronot/hotel__booking_predict
cd hotel__booking_predict
pip install -r requirements.txt
```

### C. Run Analysis:
* Buka file `hotel_booking_cancelation.ipynb` dengan Jupyter Notebook.
* Jalankan setiap sel untuk melihat analisis dan hasil prediksi.

## 11. Contact 
* **Nama**: Moh. Khisanul Fakhrudin Akbar
* **Email**: shinaruikhisan@gmail.com
* **LinkedIn**: [linkedin.com/in/muhammad-khisanul-fakhrudin-akbar](https://www.linkedin.com/in/muhammad-khisanul-fakhrudin-akbar/)

