from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Data Simulasi Kain (Simulasi Database) ---
# Di dunia nyata, data ini akan diambil dari database
kain_data = [
    {"nama": "Katun Jepang Premium", "jenis": "katun", "warna": "putih", "motif": "polos", "kegunaan": "kemeja, dress", "harga": "Rp 45.000/m"},
    {"nama": "Sutra Satin Elegant", "jenis": "sutra", "warna": "emas", "motif": "polos", "kegunaan": "gaun malam, selendang", "harga": "Rp 75.000/m"},
    {"nama": "Linen Rami Alami", "jenis": "linen", "warna": "beige", "motif": "polos", "kegunaan": "celana, outer", "harga": "Rp 55.000/m"},
    {"nama": "Woolpeach Floral", "jenis": "wolfis", "warna": "biru", "motif": "bunga", "kegunaan": "gamis, tunik", "harga": "Rp 35.000/m"},
    {"nama": "Denim Strech", "jenis": "denim", "warna": "biru", "motif": "polos", "kegunaan": "jaket, jeans", "harga": "Rp 60.000/m"},
    {"nama": "Rayon Viscose Motif", "jenis": "rayon", "warna": "hijau", "motif": "abstrak", "kegunaan": "pajamas, daster", "harga": "Rp 30.000/m"},
    {"nama": "Brokat Semi-Prancis", "jenis": "brokat", "warna": "merah", "motif": "renda", "kegunaan": "kebaya, dress pesta", "harga": "Rp 90.000/m"},
]

# --- Simulasi Logika Rekomendasi (Simulasi AI) ---
def get_rekomendasi(preferensi_jenis):
    """
    Fungsi sederhana untuk merekomendasikan kain berdasarkan jenis yang disukai.
    Di dunia nyata, ini bisa berupa model Machine Learning (ML) yang lebih kompleks.
    """
    rekomendasi = []
    preferensi_jenis = preferensi_jenis.lower()
    
    # Kriteria utama: Cocokkan jenis kain
    for kain in kain_data:
        if preferensi_jenis in kain['jenis'].lower():
            rekomendasi.append(kain)
    
    # Jika tidak ada yang cocok, berikan rekomendasi populer/default
    if not rekomendasi:
        # Berikan 3 kain populer (misalnya, 3 kain pertama)
        return kain_data[:3]
    
    return rekomendasi

# --- Routing Flask ---

@app.route('/')
def index():
    """Menampilkan halaman utama dengan formulir input."""
    # Daftar jenis kain unik untuk dropdown
    jenis_kain_unik = sorted(list(set([kain['jenis'].title() for kain in kain_data])))
    return render_template('index.html', jenis_kain=jenis_kain_unik)

@app.route('/recommend', methods=['POST'])
def recommend():
    """Menerima input dari form dan mengembalikan rekomendasi."""
    # Ambil input dari form
    preferensi = request.form.get('preferensi_jenis')
    
    # Dapatkan rekomendasi
    hasil_rekomendasi = get_rekomendasi(preferensi)
    
    # Kembalikan hasilnya ke template untuk ditampilkan
    jenis_kain_unik = sorted(list(set([kain['jenis'].title() for kain in kain_data])))
    return render_template('index.html', 
                           rekomendasi=hasil_rekomendasi, 
                           jenis_kain=jenis_kain_unik,
                           preferensi_dipilih=preferensi)

# --- Jalankan Aplikasi ---
if __name__ == '__main__':
    # Saat deploy ke Render, Render akan menyediakan port-nya sendiri,
    # tapi untuk testing lokal, kita pakai port 5000.
    app.run(debug=True)