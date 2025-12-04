from flask import Flask, render_template, request, make_response
import json

app = Flask(__name__)

# --- Data Simulasi Kain (Simulasi Database) ---
# Di dunia nyata, data ini akan diambil dari database
kain_data = [
    {"nama": "Katun Jepang Premium", "jenis": "katun", "warna": "putih", "motif": "polos", "kegunaan": "kemeja, dress", "harga": "Rp 45.000/m", "image_url": "https://picsum.photos/seed/katun/300/200"},
    {"nama": "Sutra Satin Elegant", "jenis": "sutra", "warna": "emas", "motif": "polos", "kegunaan": "gaun malam, selendang", "harga": "Rp 75.000/m", "image_url": "https://picsum.photos/seed/sutra/300/200"},
    {"nama": "Linen Rami Alami", "jenis": "linen", "warna": "beige", "motif": "polos", "kegunaan": "celana, outer", "harga": "Rp 55.000/m", "image_url": "https://picsum.photos/seed/linen/300/200"},
    {"nama": "Woolpeach Floral", "jenis": "wolfis", "warna": "biru", "motif": "bunga", "kegunaan": "gamis, tunik", "harga": "Rp 35.000/m", "image_url": "https://picsum.photos/seed/woolpeach/300/200"},
    {"nama": "Denim Strech", "jenis": "denim", "warna": "biru", "motif": "polos", "kegunaan": "jaket, jeans", "harga": "Rp 60.000/m", "image_url": "https://picsum.photos/seed/denim/300/200"},
    {"nama": "Rayon Viscose Motif", "jenis": "rayon", "warna": "hijau", "motif": "abstrak", "kegunaan": "pajamas, daster", "harga": "Rp 30.000/m", "image_url": "https://picsum.photos/seed/rayon/300/200"},
    {"nama": "Brokat Semi-Prancis", "jenis": "brokat", "warna": "merah", "motif": "renda", "kegunaan": "kebaya, dress pesta", "harga": "Rp 90.000/m", "image_url": "https://picsum.photos/seed/brokat/300/200"},
    {"nama": "Katun Motif Garis", "jenis": "katun", "warna": "abu-abu", "motif": "garis", "kegunaan": "kemeja, rok", "harga": "Rp 40.000/m", "image_url": "https://picsum.photos/seed/katunmotif/300/200"},
]
# --- Muat Bobot dari File Konfigurasi ---
def load_weights():
    """Memuat bobot dari file konfigurasi JSON."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config.get('rekomendasi_bobot', {})
    except FileNotFoundError:
        print("PERINGATAN: config.json tidak ditemukan. Menggunakan bobot default.")
        return {'jenis': 5, 'warna': 3, 'motif': 2}
    except json.JSONDecodeError:
        print("ERROR: config.json tidak valid. Menggunakan bobot default.")
        return {'jenis': 5, 'warna': 3, 'motif': 2}

# Muat bobot saat aplikasi dimulai
BOBOT = load_weights()
TOTAL_BOBOT_MAX = sum(BOBOT.values()) # Hitung total bobot maksimum secara dinamis

# --- Fungsi Utilitas untuk Opsi Filter ---
def get_unique_options(key):
    """Mengambil daftar unik dari nilai 'key' (jenis, warna, atau motif)."""
    return sorted(list(set([kain[key].title() for kain in kain_data])))

# --- Fungsi Utilitas untuk Mencari Kain ---
def find_kain_by_name(kain_name):
    """Mencari objek kain berdasarkan nama yang di-URL-kan."""
    # Ubah nama_kain menjadi format yang mudah dibandingkan (misal: lowercase, ganti spasi jadi strip)
    target_slug = kain_name.lower().replace(' ', '-')
    
    for kain in kain_data:
        kain_slug = kain['nama'].lower().replace(' ', '-')
        if kain_slug == target_slug:
            return kain
    return None

# --- Simulasi Logika Rekomendasi (Simulasi AI) ---
# --- Logika Rekomendasi (Diperbarui dengan Scoring) ---
def calculate_score_and_recommend(preferensi_jenis, preferensi_warna, preferensi_motif):
    """
    Menghitung skor kecocokan setiap kain berdasarkan preferensi dan bobot.
    """
    skor_kain = []
    
    # Normalisasi input
    jenis_target = preferensi_jenis.lower() if preferensi_jenis else None
    warna_target = preferensi_warna.lower() if preferensi_warna else None
    motif_target = preferensi_motif.lower() if preferensi_motif else None
    
    # Cek apakah ada preferensi yang diisi
    ada_preferensi = jenis_target or warna_target or motif_target

    for kain in kain_data:
        current_score = 0
        
        # 1. Scoring Jenis Kain
        if jenis_target and jenis_target in kain['jenis'].lower():
            current_score += BOBOT.get('jenis', 0)

        # 2. Scoring Warna Kain
        if warna_target and warna_target in kain['warna'].lower():
            current_score += BOBOT.get('warna', 0)

        # 3. Scoring Motif Kain
        if motif_target and motif_target in kain['motif'].lower():
            current_score += BOBOT.get('motif', 0)
            
        # Tambahkan skor ke data kain
        kain_dengan_skor = kain.copy()
        kain_dengan_skor['skor'] = str(current_score)
        skor_kain.append(kain_dengan_skor)

    # Filter dan urutkan berdasarkan skor
    if ada_preferensi:
        # Hanya tampilkan kain yang memiliki skor lebih besar dari 0 (minimal 1 kecocokan)
        skor_kain.sort(key=lambda x: int(x['skor']), reverse=True)
        rekomendasi_final = [kain for kain in skor_kain if int(kain['skor']) > 0]
    else:
        # Jika tidak ada input, tampilkan semua kain tanpa pengurutan skor
        rekomendasi_final = skor_kain


    # Jika setelah filter tidak ada hasil, kembalikan semua data awal (atau data populer)
    if not rekomendasi_final:
        return skor_kain # Mengembalikan semua kain (semuanya memiliki skor 0)

    return rekomendasi_final

# --- Routing Flask ---

@app.route('/')
def index():
    """Menampilkan halaman utama dengan semua opsi filter."""
    
    default_preferensi = {
        'jenis': '',
        'warna': '',
        'motif': '',
    }

    context = {
        'jenis_kain': get_unique_options('jenis'),
        'warna_kain': get_unique_options('warna'),
        'motif_kain': get_unique_options('motif'),
        'preferensi_dipilih': default_preferensi,
        'total_bobot_max': TOTAL_BOBOT_MAX # Kirim variabel ini ke template
    }
    return render_template('index.html', **context)

#--- Routing Flask untuk Rekomendasi ---
@app.route('/recommend', methods=['POST'])
def recommend():
    """Menerima input dari form (jenis, warna, motif) dan mengembalikan rekomendasi."""
    
    # Ambil input dari form
    preferensi_jenis = request.form.get('preferensi_jenis')
    preferensi_warna = request.form.get('preferensi_warna')
    preferensi_motif = request.form.get('preferensi_motif')
    
    # Dapatkan rekomendasi
    hasil_rekomendasi = calculate_score_and_recommend(preferensi_jenis, preferensi_warna, preferensi_motif)
    
    # Siapkan konteks untuk template
    context = {
        'jenis_kain': get_unique_options('jenis'),
        'warna_kain': get_unique_options('warna'),
        'motif_kain': get_unique_options('motif'),
        'rekomendasi': hasil_rekomendasi,
        # Untuk mempertahankan pilihan pengguna di form setelah submit
        'preferensi_dipilih': {
            'jenis': preferensi_jenis,
            'warna': preferensi_warna,
            'motif': preferensi_motif,
        },
        'total_bobot_max': TOTAL_BOBOT_MAX # Kirim variabel ini ke template
    }
    return render_template('index.html', **context)

#--- Routing Flask untuk Halaman Detail Produk ---
@app.route('/product/<kain_name>')
def product_detail(kain_name):
    """Menampilkan halaman detail produk."""
    kain = find_kain_by_name(kain_name)
    
    if kain:
        # Untuk halaman detail, kita tidak perlu skor relevansi, 
        # tapi kita kirim semua data yang ada.
        return render_template('detail.html', kain=kain)
    else:
        # Jika kain tidak ditemukan, kembali ke halaman utama atau tampilkan 404
        return "Produk tidak ditemukan!", 404

#
@app.route('/add_to_cart/<kain_name>')
def add_to_cart(kain_name):
    """Menambahkan item ke keranjang (disimpan di cookie) dan mengarahkan kembali ke detail produk."""
    kain = find_kain_by_name(kain_name)
    
    if not kain:
        return "Produk tidak ditemukan!", 404
        
    # 1. Ambil data keranjang yang sudah ada dari cookie
    cart_items_str = request.cookies.get('cart', '[]')
    try:
        cart_items = json.loads(cart_items_str)
    except json.JSONDecodeError:
        cart_items = []

    # 2. Tambahkan item baru
    item_id = kain_name.lower().replace(' ', '-')
    
    # Cek apakah item sudah ada di keranjang (kita hanya tambahkan 1 unit untuk kesederhanaan)
    found = False
    for item in cart_items:
        if item['id'] == item_id:
            item['qty'] += 1
            found = True
            break
    
    if not found:
        cart_items.append({
            'id': item_id,
            'name': kain['nama'],
            'price': kain['harga'],
            'qty': 1
        })

    # 3. Simpan kembali ke cookie
    response = make_response(redirect(url_for('product_detail', kain_name=kain_name)))
    response.set_cookie('cart', json.dumps(cart_items), max_age=60*60*24*7) # Cookie berlaku 7 hari
    
    return response

@app.route('/cart')
def cart_summary():
    """Menampilkan ringkasan isi keranjang."""
    cart_items_str = request.cookies.get('cart', '[]')
    try:
        cart_items = json.loads(cart_items_str)
    except json.JSONDecodeError:
        cart_items = []
    
    total_belanja = 0

    # Hitung total belanja
    for item in cart_items:
        # Ambil harga (misal: "Rp 45.000/m")
        price_str = item.get('price', 'Rp 0/m')
        
        # Bersihkan string harga untuk mendapatkan angka
        # Hapus "Rp", hapus "/m", hapus titik, lalu konversi ke integer
        cleaned_price = price_str.replace('Rp', '').replace('/m', '').replace('.', '').strip()
        try:
            unit_price = int(cleaned_price)
        except ValueError:
            unit_price = 0 # Jika konversi gagal, anggap harganya 0

        item_qty = item.get('qty', 0)
        total_belanja += (unit_price * item_qty)
    
    # Konversi total belanja ke format rupiah
    # Gunakan format string Python untuk pemisah ribuan
    total_belanja_formatted = "Rp {:,}".format(total_belanja).replace(',', '.') # ubah koma jadi titik

    return render_template('cart.html', 
                           cart_items=cart_items, 
                           total_belanja=total_belanja_formatted)

# --- Pastikan Anda mengimpor 'redirect' dan 'url_for' di bagian atas app.py ---
# from flask import Flask, render_template, request, make_response, redirect, url_for
# Jika belum, tambahkan:
from flask import redirect, url_for

#--- Routing Flask untuk Mengelola Keranjang ---
@app.route('/clear_cart')
def clear_cart():
    """Menghapus cookie keranjang (cart) untuk mengosongkan keranjang belanja."""
    
    # Membuat respons yang akan mengarahkan pengguna kembali ke halaman keranjang
    response = make_response(redirect(url_for('cart_summary')))
    
    # Menghapus cookie 'cart' dengan menyetel nilainya ke kosong dan mengatur max_age=0
    # Ini memberi tahu browser untuk segera menghapus cookie tersebut.
    response.set_cookie('cart', '', max_age=0) 
    
    return response

#--- Routing Flask untuk Memperbarui Isi Keranjang ---
@app.route('/update_cart/<item_id>/<action>')
def update_cart(item_id, action):
    """
    Memperbarui isi keranjang (menghapus item atau mengurangi kuantitas)
    item_id: ID produk (slug)
    action: 'remove' atau 'decrement'
    """
    cart_items_str = request.cookies.get('cart', '[]')
    try:
        cart_items = json.loads(cart_items_str)
    except json.JSONDecodeError:
        cart_items = []
        
    new_cart_items = []
    
    for item in cart_items:
        if item['id'] == item_id:
            if action == 'remove':
                # Jangan tambahkan item ini ke new_cart_items (efeknya dihapus)
                continue 
            
            elif action == 'decrement':
                if item['qty'] > 1:
                    item['qty'] -= 1
                    new_cart_items.append(item)
                # Jika qty = 1, dan kita decrement, item akan dihapus (tidak ditambahkan ke new_cart_items)
            
            else:
                # Jika aksi tidak valid, kembalikan item seperti semula
                new_cart_items.append(item)
        else:
            # Item yang tidak diubah, tetap dimasukkan
            new_cart_items.append(item)

    # 1. Buat respons yang mengarahkan kembali ke halaman keranjang
    response = make_response(redirect(url_for('cart_summary')))
    
    # 2. Simpan keranjang baru ke cookie
    if new_cart_items:
        response.set_cookie('cart', json.dumps(new_cart_items), max_age=60*60*24*7)
    else:
        # Jika keranjang kosong, hapus cookie
        response.set_cookie('cart', '', max_age=0)
        
    return response



# --- Jalankan Aplikasi ---
if __name__ == '__main__':
    app.run(debug=True)