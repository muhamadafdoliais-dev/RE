from datetime import datetime
import heapq
import streamlit as st
import uuid

# =====================================
# DATA USER & KONFIGURASI HALAMAN
# =====================================
st.set_page_config(
    page_title="LogiRoute - Logistik Pintar",
    page_icon="🚚",
    layout="wide",
)

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "konsumen": {"password": "user123", "role": "user"},
}

if "pengiriman" not in st.session_state:
    st.session_state.pengiriman = []


# =====================================
# GRAPH STRUCTURE
# =====================================
class Graph:

    def __init__(self):
        self.graph = {}

    def get_semua_kota(self):
        return sorted(list(self.graph.keys()))

    def tambah_kota(self, kota):
        if kota and kota not in self.graph:
            self.graph[kota] = []
            return True
        return False

    def tambah_jalur(self, asal, tujuan, jarak):
        if not asal or not tujuan:
            return False
        self.tambah_kota(asal)
        self.tambah_kota(tujuan)

        # Cek apakah jalur sudah ada untuk menghindari duplikasi
        if not any(t == tujuan for t, _ in self.graph[asal]):
            self.graph[asal].append((tujuan, jarak))
            self.graph[tujuan].append((asal, jarak))
            return True
        return False

    def dijkstra(self, start, end):
        if start not in self.graph or end not in self.graph:
            return [], float("inf")

        distances = {city: float("inf") for city in self.graph}
        previous = {city: None for city in self.graph}

        distances[start] = 0
        pq = [(0, start)]

        while pq:
            current_distance, current_city = heapq.heappop(pq)

            if current_distance > distances[current_city]:
                continue

            for neighbor, weight in self.graph[current_city]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_city
                    heapq.heappush(pq, (distance, neighbor))

        if distances[end] == float("inf"):
            return [], float("inf")

        path = []
        current = end
        while current:
            path.append(current)
            current = previous[current]

        path.reverse()
        return path, distances[end]


# =====================================
# INISIALISASI GRAPH STATE (DENGAN PENGECEKAN AMAN)
# =====================================
# Jika navigator belum ada, ATAU objek di state adalah objek versi lama (tidak punya fungsi get_semua_kota)
if "navigator" not in st.session_state or not hasattr(st.session_state.navigator, "get_semua_kota"):
    navigator = Graph()
    jalur_awal = [
        ("Jakarta", "Bandung", 150),
        ("Jakarta", "Semarang", 440),
        ("Bandung", "Semarang", 290),
        ("Semarang", "Surabaya", 340),
        ("Bandung", "Yogyakarta", 360),
        ("Yogyakarta", "Surabaya", 315),
    ]
    for a, b, c in jalur_awal:
        navigator.tambah_jalur(a, b, c)
    st.session_state.navigator = navigator

navigator = st.session_state.navigator


# =====================================
# UTILITY FUNCTIONS
# =====================================
def hitung_biaya(jarak, berat, kendaraan, prioritas):
    tarif = {"motor": 1000, "mobil": 2000, "truk": 3000}
    biaya = (jarak * tarif[kendaraan]) + (berat * 5000)

    if prioritas == "express":
        biaya *= 1.5
    elif prioritas == "same_day":
        biaya *= 2.0
    return biaya


def estimasi(jarak, kendaraan):
    speed = {"motor": 40, "mobil": 60, "truk": 80}
    return round(jarak / speed[kendaraan], 1)


# =====================================
# CUSTOM CSS FOR MODERN LOOK
# =====================================
st.markdown(
    """
    <style>
    .main-title { font-size: 2.5rem; font-weight: 700; color: #1E293B; margin-bottom: 2rem; }
    .card { background-color: #F8FAFC; padding: 1.5rem; border-radius: 0.75rem; border: 1px solid #E2E8F0; margin-bottom: 1rem; }
    .status-badge { padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600; display: inline-block; }
    .status-process { background-color: #DBEAFE; color: #1E40AF; }
    .status-done { background-color: #DCFCE7; color: #14532D; }
    .status-transit { background-color: #FEF3C7; color: #78350F; }
    </style>
""",
    unsafe_allow_html=True,
)

# =====================================
# UI ROUTING & LOGIN
# =====================================
if "role" not in st.session_state:
    st.session_state.role = None

# Sidebar Global (Selalu tampil jika sudah login)
if st.session_state.role:
    with st.sidebar:
        st.markdown(f"### 👤 Logged in as: **{st.session_state.role.upper()}**")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.role = None
            st.rerun()

# --- HALAMAN LOGIN ---
if st.session_state.role is None:
    st.markdown("<h1 class='main-title'>🚚 LogiRoute Dashboard</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            """
            ### Sistem Navigasi & Pengiriman Logistik Berbasis Struktur Data Graf.
            Aplikasi ini menggunakan **Algoritma Dijkstra** untuk mencari rute distribusi barang terpendek antar kota secara *real-time*, menghemat biaya operasional, dan menghitung estimasi waktu secara akurat.
        """
        )

    with col2:
        with st.form("login_form"):
            st.markdown("### 🔐 Masuk ke Sistem")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In", use_container_width=True)

            if submit:
                if username in users and users[username]["password"] == password:
                    st.session_state.role = users[username]["role"]
                    st.rerun()
                else:
                    st.error("Username atau password salah.")

# --- HALAMAN ADMIN ---
elif st.session_state.role == "admin":
    st.markdown("<h1 class='main-title'>⚙️ Panel Kendali Admin Logistik</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Ringkasan & Statistik",
        "📦 Buat Pengiriman",
        "🗺️ Kelola Peta Rute",
        "📍 Update Tracking",
        "🔍 Cek Rute Terpendek",
    ])

    # 1. TAB STATISTIK
    with tab1:
        st.subheader("Performa Bisnis Saat Ini")
        total_kirim = len(st.session_state.pengiriman)
        total_pendapatan = sum(p["biaya"] for p in st.session_state.pengiriman)

        m1, m2 = st.columns(2)
        m1.metric(label="Total Order Pengiriman", value=f"{total_kirim} Paket")
        m2.metric(label="Total Pendapatan Operasional", value=f"Rp {int(total_pendapatan):,}")

        st.markdown("---")
        st.subheader("📋 Manifes Semua Pengiriman")
        if st.session_state.pengiriman:
            st.dataframe(st.session_state.pengiriman, use_container_width=True)
        else:
            st.info("Belum ada data transaksi pengiriman hari ini.")

    # 2. TAB BUAT PENGIRIMAN
    with tab2:
        st.subheader("Formulir Manifes Pengiriman Baru")
        daftar_kota = navigator.get_semua_kota()

        if len(daftar_kota) < 2:
            st.warning("Tambahkan minimal 2 kota di tab 'Kelola Peta Rute' terlebih dahulu.")
        else:
            with st.form("form_pengiriman"):
                col1, col2 = st.columns(2)
                with col1:
                    asal = st.selectbox("Kota Asal Distribusi", daftar_kota)
                    barang = st.text_input("Nama/Jenis Barang", placeholder="Contoh: Elektronik")
                    kendaraan = st.selectbox("Armada Kendaraan", ["motor", "mobil", "truk"])
                with col2:
                    tujuan = st.selectbox("Kota Tujuan Pengiriman", daftar_kota, index=1 if len(daftar_kota) > 1 else 0)
                    berat = st.number_input("Berat Muatan (Kg)", min_value=1.0, step=0.5)
                    prioritas = st.selectbox("Tingkat Prioritas", ["reguler", "express", "same_day"])

                submit_kirim = st.form_submit_button("Proses Pengiriman & Terbitkan Resi", use_container_width=True)

                if submit_kirim:
                    if asal == tujuan:
                        st.error("Kota asal dan tujuan tidak boleh sama.")
                    else:
                        path, distance = navigator.dijkstra(asal, tujuan)
                        if path:
                            biaya = hitung_biaya(distance, berat, kendaraan, prioritas)
                            resi = f"LR-{str(uuid.uuid4())[:8].upper()}"

                            st.session_state.pengiriman.append({
                                "resi": resi,
                                "barang": barang,
                                "asal": asal,
                                "tujuan": tujuan,
                                "status": "Diproses",
                                "biaya": biaya,
                                "history": [f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - Paket Diproses di {asal}"],
                            })

                            st.success(f"✅ Pengiriman Berhasil Dibuat! Nomor Resi: **{resi}**")
                            c1, c2, c3 = st.columns(3)
                            c1.info(f"🛣️ **Rute Tercepat:** {' ➔ '.join(path)}")
                            c2.info(f"💰 **Total Biaya:** Rp {int(biaya):,}")
                            c3.info(f"⏱️ **Estimasi Tiba:** {estimasi(distance, kendaraan)} Jam")
                        else:
                            st.error("Gagal memproses. Tidak ada jalur graf yang menghubungkan kedua kota tersebut.")

    # 3. TAB KELOLA PETA RUTE
    with tab3:
        st.subheader("Modifikasi Struktur Jaringan Distribusi (Graf)")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🏢 Tambah Node (Kota Baru)")
            kota_baru = st.text_input("Nama Kota Baru").strip()
            if st.button("Daftarkan Kota", use_container_width=True):
                if navigator.tambah_kota(kota_baru):
                    st.success(f"Kota '{kota_baru}' berhasil ditambahkan ke dalam sistem.")
                    st.rerun()
                else:
                    st.error("Kota kosong atau sudah terdaftar.")

        with col2:
            st.markdown("### 🛣️ Hubungkan Jalur Baru (Edge Waktu/Jarak)")
            daftar_kota = navigator.get_semua_kota()
            if len(daftar_kota) >= 2:
                c1, c2, c3 = st.columns(3)
                c_asal = c1.selectbox("Dari Kota", daftar_kota, key="c_asal")
                c_tujuan = c2.selectbox("Ke Kota", daftar_kota, key="c_tujuan")
                c_jarak = c3.number_input("Jarak (KM)", min_value=1, value=50)

                if st.button("Hubungkan Rute", use_container_width=True):
                    if c_asal == c_tujuan:
                        st.error("Tidak bisa menghubungkan kota yang sama.")
                    else:
                        if navigator.tambah_jalur(c_asal, c_tujuan, c_jarak):
                            st.success(f"Jalur baru {c_asal} ⬌ {c_tujuan} ({c_jarak} KM) aktif.")
                            st.rerun()
            else:
                st.info("Minimal harus ada 2 kota terdaftar untuk membuat jalur penghubung.")

    # 4. TAB UPDATE STATUS
    with tab4:
        st.subheader("Pembaruan Status Perjalanan Logistik")
        if not st.session_state.pengiriman:
            st.info("Belum ada manifes pengiriman untuk di-update.")
        else:
            daftar_resi = [p["resi"] for p in st.session_state.pengiriman]
            selected_resi = st.selectbox("Pilih Nomor Resi yang Akan Diperbarui", daftar_resi)

            status_opsi = ["Diproses", "Dijemput", "Di Gudang", "Dalam Perjalanan", "Sampai Tujuan", "Diantar Kurir", "Selesai"]
            selected_status = st.selectbox("Ubah Status Menjadi", status_opsi)

            if st.button("Perbarui Manifes Perjalanan", use_container_width=True):
                for p in st.session_state.pengiriman:
                    if p["resi"] == selected_resi:
                        p["status"] = selected_status
                        p["history"].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {selected_status}")
                        st.success(f"Resi {selected_resi} berhasil diperbarui ke status: **{selected_status}**")
                        st.rerun()

    # 5. TAB CEK RUTE TERPENDEK
    with tab5:
        st.subheader("Simulator Rute Terpendek (Dijkstra Solver)")
        daftar_kota = navigator.get_semua_kota()
        col1, col2 = st.columns(2)
        t_asal = col1.selectbox("Titik Awal Navigasi", daftar_kota, key="t_asal")
        t_tujuan = col2.selectbox("Titik Akhir Navigasi", daftar_kota, key="t_tujuan")

        if st.button("Kalkulasi Rute", use_container_width=True):
            path, distance = navigator.dijkstra(t_asal, t_tujuan)
            if path:
                st.markdown(
                    f"""
                <div class="card">
                    <h4>Hasil Optimal Jalur Distribusi:</h4>
                    <p style="font-size:1.25rem; color:#0EA5E9;"><b>{' ➜ '.join(path)}</b></p>
                    <p>Total Akumulasi Jarak: <b>{distance} KM</b></p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.error("Kedua area/kota ini terisolasi. Tidak ditemukan jalur penghubung di dalam Graf.")

# --- HALAMAN KONSUMEN ---
elif st.session_state.role == "user":
    st.markdown("<h1 class='main-title'>📦 Portal Pelacakan Mandiri Konsumen</h1>", unsafe_allow_html=True)

    menu_user = st.tabs(["🔍 Lacak Paket Real-Time", "🗺️ Cek Jangkauan & Estimasi Rute"])

    # USER TAB 1: LACAK
    with menu_user[0]:
        st.subheader("Masukkan Nomor Resi Anda")
        input_resi = st.text_input("Nomor Resi Pengiriman", placeholder="Contoh: LR-ABC12345").strip().upper()

        if st.button("Lacak Keberadaan Paket", use_container_width=True):
            paket_ditemukan = None
            for p in st.session_state.pengiriman:
                if p["resi"] == input_resi:
                    paket_ditemukan = p
                    break

            if paket_ditemukan:
                badge_class = "status-transit"
                if paket_ditemukan["status"] == "Diproses":
                    badge_class = "status-process"
                elif paket_ditemukan["status"] == "Selesai":
                    badge_class = "status-done"

                st.markdown(
                    f"""
                    <div class="card">
                        <h3>📋 Informasi Paket: {paket_ditemukan['barang']}</h3>
                        <p>Status Terkini: <span class="status-badge {badge_class}">{paket_ditemukan['status']}</span></p>
                        <p>Pengiriman: <b>{paket_ditemukan['asal']}</b> menuju <b>{paket_ditemukan['tujuan']}</b></p>
                        <p>Total Administrasi: <b>Rp {int(paket_ditemukan['biaya']):,}</b></p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                st.markdown("### 🕒 Garis Waktu Riwayat Perjalanan (Log)")
                for h in reversed(paket_ditemukan["history"]):
                    st.markdown(f"- {h}")
            else:
                st.error("Nomor resi tidak valid atau tidak terdaftar di sistem kami.")

    # USER TAB 2: ESTIMASI
    with menu_user[1]:
        st.subheader("Cek Estimasi Jarak Antar Kota Mandiri")
        daftar_kota = navigator.get_semua_kota()
        c1, c2 = st.columns(2)
        u_asal = c1.selectbox("Kota Asal Penjemputan", daftar_kota, key="u_asal")
        u_tujuan = c2.selectbox("Kota Tujuan Pengantaran", daftar_kota, key="u_tujuan")

        if st.button("Cek Jalur Logistik", use_container_width=True):
            path, distance = navigator.dijkstra(u_asal, u_tujuan)
            if path:
                st.info(f"Jalur Distribusi Kami: {' ➜ '.join(path)} (Jarak Tempuh: {distance} KM)")
            else:
                st.error("Maaf, rute pengiriman ke area tersebut belum tersedia saat ini.")