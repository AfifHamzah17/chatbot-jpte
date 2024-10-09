# Chatbot-PTIK 🤖

Selamat datang di **Chatbot-PTIK**, proyek yang dirancang untuk mempermudah komunikasi antara mahasiswa dan pihak kampus. Chatbot ini berfungsi sebagai platform digital yang menyediakan informasi dan bantuan dengan cepat, khususnya terkait dengan berbagai aspek kehidupan akademik di PTIK.

## 📝 Deskripsi Proyek

Chatbot-PTIK adalah aplikasi yang memanfaatkan teknologi AI, khususnya model GPT-3.5 dari OpenAI, untuk memberikan jawaban yang akurat dan relevan berdasarkan konteks yang diberikan. Proyek ini bertujuan untuk menjawab pertanyaan-pertanyaan yang sering diajukan oleh mahasiswa, sehingga meminimalkan kebingungan dan meningkatkan efisiensi dalam mencari informasi.

### Fitur Utama

- **Informasi Jurusan**: Chatbot dapat menjawab pertanyaan seputar pendaftaran KRS, KKN, PLP, dan sidang PKLI.
- **Dukungan Multi Bahasa**: Mampu menjawab dalam berbagai bahasa, memberikan kemudahan bagi pengguna dengan latar belakang bahasa yang berbeda.
- **Mode Malam**: Pengguna dapat memilih tampilan gelap untuk kenyamanan saat menggunakan aplikasi di malam hari.
- **Antarmuka Interaktif**: Desain antarmuka yang intuitif dan menarik memudahkan pengguna dalam berinteraksi dengan chatbot.

## 🎨 Estetika dan Desain

Antarmuka pengguna dirancang dengan mempertimbangkan aspek estetika. Dengan penggunaan palet warna yang lembut dan elemen interaktif, pengguna dapat merasa nyaman saat berinteraksi. Di sidebar, pengguna dapat menemukan informasi lebih lanjut mengenai proyek, serta fitur tambahan yang dapat meningkatkan pengalaman pengguna.

## ⚙️ Teknologi yang Digunakan

- **Streamlit**: Digunakan untuk membangun antarmuka aplikasi web.
- **Langchain**: Untuk mengelola alur percakapan dan penyimpanan konteks.
- **OpenAI API**: Menggunakan model GPT-3.5 untuk memproses pertanyaan dan memberikan jawaban.
- **Pinecone**: Digunakan sebagai penyimpanan vektor untuk melakukan pencarian informasi yang relevan dari dokumen PDF.

## 📁 Struktur Proyek

- `app.py`: File utama yang menjalankan aplikasi chatbot.
- `utils.py`: Berisi fungsi-fungsi pendukung untuk memproses dokumen dan mencari informasi.
- `.env`: File konfigurasi untuk menyimpan kunci API dan variabel penting lainnya (jangan diunggah ke repositori publik).

## 🔧 Cara Menggunakan

1. **Clone Repository**: Mulai dengan mengkloning repositori ini ke dalam komputer Anda.
   ```bash
   git clone https://github.com/AfifHamzah17/chatbot-ptik.git
   cd chatbot-ptik
   ```

2. **Install Dependencies**: Pastikan Anda memiliki semua dependensi yang diperlukan dengan menjalankan:
   ```bash
   pip install -r requirements.txt
   ```

3. **Konfigurasi .env**: Buat file `.env` di root direktori proyek Anda dan tambahkan kunci API yang diperlukan:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   ```

4. **Jalankan Aplikasi**: Terakhir, jalankan aplikasi dengan perintah:
   ```bash
   streamlit run app.py
   ```

5. **Interaksi dengan Chatbot**: Buka browser dan kunjungi `http://localhost:8501` untuk mulai berinteraksi dengan chatbot.

## 🌟 Kontribusi

Kami terbuka untuk kontribusi dari semua pihak yang ingin membantu mengembangkan proyek ini. Jika Anda memiliki ide atau fitur baru yang ingin ditambahkan, silakan buat issue atau pull request di repositori ini.

## 📞 Dukungan

Jika Anda mengalami kesulitan atau memiliki pertanyaan, jangan ragu untuk menghubungi tim pengembang:

Afif Hamzah** (5213151004)

## 🎉 Kesimpulan

Dengan Chatbot-PTIK, kami berharap dapat menjawab semua pertanyaan Anda dan memberikan informasi yang Anda butuhkan dengan cepat dan efisien. Mari bergabung dalam perjalanan ini dan tingkatkan pengalaman akademik Anda di PTIK! Terima kasih telah mengunjungi proyek kami. 🌟

---

Silakan sesuaikan isi dan format sesuai kebutuhan Anda. Jika ada tambahan atau perubahan, beri tahu saya!
