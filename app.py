import streamlit as st
import heapq
import uuid
from datetime import datetime

# =====================================
# DATA USER
# =====================================
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "konsumen": {"password": "user123", "role": "user"}
}

if "pengiriman" not in st.session_state:
    st.session_state.pengiriman = []

# =====================================
# GRAPH
# =====================================
class Graph:
    def __init__(self):
        self.graph = {}

    def tambah_kota(self, kota):
        if kota not in self.graph:
            self.graph[kota] = []

    def hapus_kota(self, kota):
        if kota in self.graph:
            del self.graph[kota]

            for node in self.graph:
                self.graph[node] = [
                    (t, j)
                    for t, j in self.graph[node]
                    if t != kota
                ]

    def tambah_jalur(self, asal, tujuan, jarak):
        self.tambah_kota(asal)
        self.tambah_kota(tujuan)

        self.graph[asal].append((tujuan, jarak))
        self.graph[tujuan].append((asal, jarak))

    def hapus_jalur(self, asal, tujuan):

        if asal in self.graph:
            self.graph[asal] = [
                (n, d)
                for n, d in self.graph[asal]
                if n != tujuan
            ]

        if tujuan in self.graph:
            self.graph[tujuan] = [
                (n, d)
                for n, d in self.graph[tujuan]
                if n != asal
            ]

    def dijkstra(self, start, end):

        if start not in self.graph or end not in self.graph:
            return [], float("inf")

        distances = {
            city: float("inf")
            for city in self.graph
        }

        previous = {
            city: None
            for city in self.graph
        }

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

                    heapq.heappush(
                        pq,
                        (distance, neighbor)
                    )

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
# INISIALISASI GRAPH
# =====================================
if "navigator" not in st.session_state:

    navigator = Graph()

    jalur_awal = [
        ("Jakarta", "Bandung", 150),
        ("Jakarta", "Semarang", 440),
        ("Bandung", "Semarang", 290),
        ("Semarang", "Surabaya", 340),
        ("Bandung", "Yogyakarta", 360),
        ("Yogyakarta", "Surabaya", 315)
    ]

    for a, b, c in jalur_awal:
        navigator.tambah_jalur(a, b, c)

    st.session_state.navigator = navigator

navigator = st.session_state.navigator

# =====================================
# FUNGSI
# =====================================
def hitung_biaya(jarak, berat, kendaraan, prioritas):

    tarif = {
        "motor": 1000,
        "mobil": 2000,
        "truk": 3000
    }

    biaya = jarak * tarif[kendaraan]
    biaya += berat * 5000

    if prioritas == "express":
        biaya *= 1.5

    elif prioritas == "same_day":
        biaya *= 2

    return biaya


def estimasi(jarak, kendaraan):

    speed = {
        "motor": 40,
        "mobil": 60,
        "truk": 80
    }

    return round(jarak / speed[kendaraan], 2)


# =====================================
# LOGIN
# =====================================
st.set_page_config(
    page_title="Sistem Rute Pengiriman",
    layout="wide"
)

st.title("🚚 Sistem Rute Pengiriman Barang")

if "role" not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username in users and users[username]["password"] == password:

            st.session_state.role = users[username]["role"]
            st.rerun()

        else:
            st.error("Login gagal")

# =====================================
# ADMIN
# =====================================
elif st.session_state.role == "admin":

    menu = st.sidebar.selectbox(
        "Menu Admin",
        [
            "Tambah Kota",
            "Tambah Jalur",
            "Cari Rute",
            "Kirim Barang",
            "Tracking",
            "Update Status",
            "Statistik",
            "Logout"
        ]
    )

    if menu == "Tambah Kota":

        kota = st.text_input("Nama Kota")

        if st.button("Tambah Kota"):
            navigator.tambah_kota(kota)
            st.success("Kota berhasil ditambahkan")

    elif menu == "Tambah Jalur":

        asal = st.text_input("Kota Asal")
        tujuan = st.text_input("Kota Tujuan")
        jarak = st.number_input(
            "Jarak (KM)",
            min_value=1
        )

        if st.button("Tambah Jalur"):

            navigator.tambah_jalur(
                asal,
                tujuan,
                jarak
            )

            st.success("Jalur berhasil ditambahkan")

    elif menu == "Cari Rute":

        asal = st.text_input("Asal")
        tujuan = st.text_input("Tujuan")

        if st.button("Cari"):

            path, distance = navigator.dijkstra(
                asal,
                tujuan
            )

            if path:

                st.success(
                    f"Rute : {' ➜ '.join(path)}"
                )

                st.info(
                    f"Jarak : {distance} KM"
                )

            else:
                st.error("Rute tidak ditemukan")

    elif menu == "Kirim Barang":

        asal = st.text_input("Asal")
        tujuan = st.text_input("Tujuan")
        barang = st.text_input("Nama Barang")

        berat = st.number_input(
            "Berat (Kg)",
            min_value=1.0
        )

        kendaraan = st.selectbox(
            "Kendaraan",
            ["motor", "mobil", "truk"]
        )

        prioritas = st.selectbox(
            "Prioritas",
            ["reguler", "express", "same_day"]
        )

        if st.button("Kirim"):

            path, distance = navigator.dijkstra(
                asal,
                tujuan
            )

            if path:

                biaya = hitung_biaya(
                    distance,
                    berat,
                    kendaraan,
                    prioritas
                )

                resi = str(uuid.uuid4())[:8].upper()

                st.session_state.pengiriman.append({
                    "resi": resi,
                    "barang": barang,
                    "asal": asal,
                    "tujuan": tujuan,
                    "status": "Diproses",
                    "biaya": biaya,
                    "history": [
                        f"{datetime.now()} - Diproses"
                    ]
                })

                st.success(
                    f"Resi : {resi}"
                )

                st.write("Rute :", " ➜ ".join(path))
                st.write("Biaya : Rp", format(int(biaya), ","))
                st.write(
                    "Estimasi :",
                    estimasi(distance, kendaraan),
                    "Jam"
                )

            else:
                st.error("Rute tidak ditemukan")

    elif menu == "Tracking":

        st.dataframe(
            st.session_state.pengiriman,
            use_container_width=True
        )

    elif menu == "Update Status":

        resi = st.text_input("Nomor Resi")

        status = st.selectbox(
            "Status",
            [
                "Diproses",
                "Dijemput",
                "Di Gudang",
                "Dalam Perjalanan",
                "Sampai Tujuan",
                "Diantar Kurir",
                "Selesai"
            ]
        )

        if st.button("Update"):

            for p in st.session_state.pengiriman:

                if p["resi"] == resi:

                    p["status"] = status

                    p["history"].append(
                        f"{datetime.now()} - {status}"
                    )

                    st.success("Status diperbarui")

    elif menu == "Statistik":

        total = len(st.session_state.pengiriman)

        pemasukan = sum(
            p["biaya"]
            for p in st.session_state.pengiriman
        )

        st.metric(
            "Total Pengiriman",
            total
        )

        st.metric(
            "Total Pemasukan",
            f"Rp {int(pemasukan):,}"
        )

    elif menu == "Logout":

        st.session_state.role = None
        st.rerun()

# =====================================
# KONSUMEN
# =====================================
elif st.session_state.role == "user":

    st.sidebar.title("Menu Konsumen")

    menu = st.sidebar.selectbox(
        "Pilih",
        [
            "Cari Rute",
            "Lacak Pengiriman",
            "Logout"
        ]
    )

    if menu == "Cari Rute":

        asal = st.text_input("Asal")
        tujuan = st.text_input("Tujuan")

        if st.button("Cari Rute"):

            path, distance = navigator.dijkstra(
                asal,
                tujuan
            )

            if path:

                st.success(
                    f"{' ➜ '.join(path)}"
                )

                st.info(
                    f"Jarak {distance} KM"
                )

            else:
                st.error("Rute tidak ditemukan")

    elif menu == "Lacak Pengiriman":

        resi = st.text_input("Nomor Resi")

        if st.button("Lacak"):

            ditemukan = False

            for p in st.session_state.pengiriman:

                if p["resi"] == resi:

                    ditemukan = True

                    st.success(
                        f"Status : {p['status']}"
                    )

                    st.write("Riwayat")

                    for h in p["history"]:
                        st.write("•", h)

            if not ditemukan:
                st.error("Resi tidak ditemukan")

    elif menu == "Logout":

        st.session_state.role = None
        st.rerun()