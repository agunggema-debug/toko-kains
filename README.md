# 🛍️ Toko Kain Pintar: Aplikasi Rekomendasi Kain Personal (Simulasi AI)

Aplikasi web prototipe yang dibangun menggunakan Flask dan Tailwind CSS untuk mensimulasikan sistem rekomendasi produk personal (kain) berdasarkan preferensi pengguna (Jenis, Warna, Motif). Sistem rekomendasi ini didukung oleh logika *scoring* berbasis bobot yang dapat dikonfigurasi secara dinamis.

---

## ✨ Fitur Utama

* **Rekomendasi Personal:** Algoritma sederhana berbasis bobot (simulasi AI) memberikan skor relevansi untuk setiap kain.
* **Filter Dinamis:** Pengguna dapat memfilter berdasarkan Jenis, Warna, dan Motif kain.
* **Bobot Dinamis:** Prioritas *scoring* (bobot Jenis, Warna, Motif) dapat diubah melalui file `config.json` tanpa mengubah kode Python.
* **Manajemen Keranjang:** Fungsionalitas dasar keranjang belanja (Tambah, Kurangi, Hapus Item, Kosongkan Keranjang) menggunakan *Cookies* peramban.
* **Detail Produk:** Halaman detail untuk setiap kain termasuk gambar (placeholder) dan spesifikasi.
* **Tampilan Modern & Responsif:** Menggunakan Tailwind CSS untuk antarmuka web yang bersih dan *mobile-friendly*.

---

## 🛠️ Teknologi yang Digunakan

* **Backend:** Python 3.x, Flask
* **Frontend:** HTML5, Jinja2 Templating, Tailwind CSS (via CDN)
* **Manajemen Paket:** `pip`
* **Penyimpanan Data:** Python List (simulasi database), JSON (untuk konfigurasi bobot), Browser Cookies (untuk keranjang)
* **Deployment:** Siap untuk di-*deploy* di platform seperti Render atau Heroku.

---

