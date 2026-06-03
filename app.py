import streamlit as st
import heapq
import uuid
from datetime import datetime

# ─────────────────────────────────────────
#  CSS GLOBAL
# ─────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* ── reset & base ── */
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .stApp {
        background: #0A0E1A;
        color: #E8EAF0;
    }

    /* ── sidebar ── */
    [data-testid="stSidebar"] {
        background: #0F1422 !important;
        border-right: 1px solid #1E2535;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #8892AA !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: #161C2E !important;
        border: 1px solid #1E2535 !important;
        border-radius: 10px !important;
        color: #E8EAF0 !important;
    }

    /* ── nav brand ── */
    .brand {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 22px;
        color: #5B8EF0;
        letter-spacing: -0.5px;
        padding: 8px 0 24px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand span { color: #E8EAF0; }

    /* ── page title ── */
    .page-title {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 28px;
        color: #FFFFFF;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .page-sub {
        font-size: 14px;
        color: #5A6478;
        margin-bottom: 32px;
    }

    /* ── card ── */
    .card {
        background: #111827;
        border: 1px solid #1E2A3F;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .card-title {
        font-family: 'Syne', sans-serif;
        font-weight: 600;
        font-size: 13px;
        color: #4A5568;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 16px;
    }

    /* ── metric cards ── */
    .metric-row { display: flex; gap: 16px; margin-bottom: 24px; }
    .metric-card {
        flex: 1;
        background: #111827;
        border: 1px solid #1E2A3F;
        border-radius: 14px;
        padding: 20px 24px;
    }
    .metric-label {
        font-size: 11px;
        color: #4A5568;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }
    .metric-value {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 28px;
        color: #FFFFFF;
    }
    .metric-accent { color: #5B8EF0; }

    /* ── inputs ── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: #161C2E !important;
        border: 1px solid #1E2535 !important;
        border-radius: 10px !important;
        color: #E8EAF0 !important;
        padding: 10px 14px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #5B8EF0 !important;
        box-shadow: 0 0 0 3px rgba(91,142,240,0.15) !important;
    }
    .stTextInput label, .stNumberInput label,
    .stSelectbox label {
        color: #8892AA !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }
    .stSelectbox > div > div {
        background: #161C2E !important;
        border: 1px solid #1E2535 !important;
        border-radius: 10px !important;
        color: #E8EAF0 !important;
    }

    /* ── buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #5B8EF0, #3B6FD4) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 28px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        letter-spacing: 0.03em;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 20px rgba(91,142,240,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 28px rgba(91,142,240,0.45) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ── alerts ── */
    .stSuccess > div {
        background: rgba(52,211,153,0.1) !important;
        border: 1px solid rgba(52,211,153,0.3) !important;
        border-radius: 10px !important;
        color: #34D399 !important;
    }
    .stError > div {
        background: rgba(239,68,68,0.1) !important;
        border: 1px solid rgba(239,68,68,0.3) !important;
        border-radius: 10px !important;
        color: #EF4444 !important;
    }
    .stInfo > div {
        background: rgba(91,142,240,0.1) !important;
        border: 1px solid rgba(91,142,240,0.3) !important;
        border-radius: 10px !important;
        color: #5B8EF0 !important;
    }
    .stWarning > div {
        background: rgba(251,191,36,0.1) !important;
        border: 1px solid rgba(251,191,36,0.3) !important;
        border-radius: 10px !important;
        color: #FBBF24 !important;
    }

    /* ── dataframe ── */
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    [data-testid="stDataFrame"] > div {
        border: 1px solid #1E2A3F !important;
        border-radius: 12px !important;
        background: #111827 !important;
    }

    /* ── divider ── */
    hr { border-color: #1E2535 !important; margin: 24px 0 !important; }

    /* ── resi badge ── */
    .resi-badge {
        display: inline-block;
        background: rgba(91,142,240,0.15);
        border: 1px solid rgba(91,142,240,0.35);
        color: #7EB0FF;
        font-family: 'Syne', monospace;
        font-weight: 700;
        font-size: 20px;
        letter-spacing: 0.12em;
        padding: 12px 28px;
        border-radius: 12px;
        margin: 12px 0;
    }

    /* ── route pill ── */
    .route-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #161C2E;
        border: 1px solid #1E2535;
        border-radius: 50px;
        padding: 8px 20px;
        font-size: 14px;
        color: #C4CCE0;
        margin: 4px 2px;
        font-weight: 500;
    }
    .route-arrow { color: #5B8EF0; font-size: 16px; }

    /* ── status badge ── */
    .status-diproses   { color:#FBBF24; background:rgba(251,191,36,0.12);  border:1px solid rgba(251,191,36,0.3);  }
    .status-selesai    { color:#34D399; background:rgba(52,211,153,0.12);  border:1px solid rgba(52,211,153,0.3);  }
    .status-perjalanan { color:#5B8EF0; background:rgba(91,142,240,0.12); border:1px solid rgba(91,142,240,0.3); }
    .status-other      { color:#C4CCE0; background:rgba(196,204,224,0.08);border:1px solid rgba(196,204,224,0.2);}
    .status-pill {
        display:inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    /* ── history timeline ── */
    .timeline-item {
        display: flex;
        gap: 14px;
        margin-bottom: 14px;
        align-items: flex-start;
    }
    .timeline-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #5B8EF0;
        margin-top: 5px;
        flex-shrink: 0;
        box-shadow: 0 0 8px rgba(91,142,240,0.6);
    }
    .timeline-dot.done { background: #34D399; box-shadow: 0 0 8px rgba(52,211,153,0.5); }
    .timeline-text { font-size: 13px; color: #8892AA; line-height: 1.5; }
    .timeline-text strong { color: #C4CCE0; font-weight: 500; }

    /* ── login page ── */
    .login-wrap {
        max-width: 420px;
        margin: 80px auto;
    }
    .login-logo {
        font-family: 'Syne', sans-serif;
        font-size: 38px;
        font-weight: 800;
        color: #5B8EF0;
        text-align: center;
        margin-bottom: 8px;
    }
    .login-tagline {
        text-align: center;
        font-size: 14px;
        color: #4A5568;
        margin-bottom: 40px;
        letter-spacing: 0.03em;
    }
    .login-card {
        background: #111827;
        border: 1px solid #1E2A3F;
        border-radius: 20px;
        padding: 36px 32px;
    }
    .login-hint {
        font-size: 11px;
        color: #2E3A52;
        margin-top: 16px;
        text-align: center;
        font-family: monospace;
        letter-spacing: 0.05em;
    }

    /* ── graph network visual ── */
    .graph-node {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px; height: 40px;
        border-radius: 50%;
        background: #161C2E;
        border: 2px solid #5B8EF0;
        color: #7EB0FF;
        font-family: 'Syne', sans-serif;
        font-size: 10px;
        font-weight: 700;
        margin: 4px;
        letter-spacing: 0.03em;
    }

    /* ── hide streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }
    .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
#  GRAPH  (Dijkstra)
# ─────────────────────────────────────────
class Graph:
    def __init__(self):
        self.graph: dict[str, list[tuple[str, int]]] = {}

    def tambah_kota(self, kota: str):
        if kota not in self.graph:
            self.graph[kota] = []

    def hapus_kota(self, kota: str):
        if kota in self.graph:
            del self.graph[kota]
            for node in self.graph:
                self.graph[node] = [(t, j) for t, j in self.graph[node] if t != kota]

    def tambah_jalur(self, asal: str, tujuan: str, jarak: int):
        self.tambah_kota(asal)
        self.tambah_kota(tujuan)
        self.graph[asal].append((tujuan, jarak))
        self.graph[tujuan].append((asal, jarak))

    def hapus_jalur(self, asal: str, tujuan: str):
        if asal in self.graph:
            self.graph[asal] = [(n, d) for n, d in self.graph[asal] if n != tujuan]
        if tujuan in self.graph:
            self.graph[tujuan] = [(n, d) for n, d in self.graph[tujuan] if n != asal]

    def dijkstra(self, start: str, end: str) -> tuple[list, float]:
        if start not in self.graph or end not in self.graph:
            return [], float("inf")
        dist = {c: float("inf") for c in self.graph}
        prev = {c: None for c in self.graph}
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            cd, cc = heapq.heappop(pq)
            if cd > dist[cc]:
                continue
            for nb, w in self.graph[cc]:
                nd = cd + w
                if nd < dist[nb]:
                    dist[nb] = nd
                    prev[nb] = cc
                    heapq.heappush(pq, (nd, nb))
        if dist[end] == float("inf"):
            return [], float("inf")
        path, cur = [], end
        while cur:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path, dist[end]

    def semua_kota(self) -> list[str]:
        return sorted(self.graph.keys())

    def semua_jalur(self) -> list[tuple[str, str, int]]:
        seen, result = set(), []
        for asal, neighbors in self.graph.items():
            for tujuan, jarak in neighbors:
                key = tuple(sorted([asal, tujuan]))
                if key not in seen:
                    seen.add(key)
                    result.append((asal, tujuan, jarak))
        return result


# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
TARIF = {"motor": 1_000, "mobil": 2_000, "truk": 3_000}
SPEED = {"motor": 40,    "mobil": 60,    "truk": 80}

STATUS_LIST = ["Diproses", "Dijemput", "Di Gudang",
               "Dalam Perjalanan", "Sampai Tujuan", "Diantar Kurir", "Selesai"]

def hitung_biaya(jarak, berat, kendaraan, prioritas) -> float:
    biaya = jarak * TARIF[kendaraan] + berat * 5_000
    if prioritas == "express":   biaya *= 1.5
    elif prioritas == "same_day": biaya *= 2.0
    return biaya

def estimasi_jam(jarak, kendaraan) -> float:
    return round(jarak / SPEED[kendaraan], 2)

def status_class(status: str) -> str:
    s = status.lower()
    if "diproses" in s or "dijemput" in s or "gudang" in s: return "status-diproses"
    if "selesai" in s:   return "status-selesai"
    if "perjalanan" in s or "antar" in s or "tujuan" in s: return "status-perjalanan"
    return "status-other"

def render_route(path: list[str]):
    pills = ""
    for i, kota in enumerate(path):
        pills += f'<span class="route-pill">{kota}</span>'
        if i < len(path) - 1:
            pills += '<span class="route-arrow">→</span>'
    st.markdown(f'<div style="margin:12px 0 8px">{pills}</div>', unsafe_allow_html=True)

def render_timeline(history: list[str]):
    for i, item in enumerate(history):
        done = "done" if i < len(history) - 1 else ""
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-dot {done}"></div>
            <div class="timeline-text">{item}</div>
        </div>
        """, unsafe_allow_html=True)

def section(title: str):
    st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────
USERS = {
    "admin":    {"password": "admin123", "role": "admin"},
    "konsumen": {"password": "user123",  "role": "user"},
}

def init_state():
    if "role" not in st.session_state:
        st.session_state.role = None
    if "pengiriman" not in st.session_state:
        st.session_state.pengiriman = []
    if "navigator" not in st.session_state:
        nav = Graph()
        for a, b, c in [
            ("Jakarta",    "Bandung",    150),
            ("Jakarta",    "Semarang",   440),
            ("Bandung",    "Semarang",   290),
            ("Semarang",   "Surabaya",   340),
            ("Bandung",    "Yogyakarta", 360),
            ("Yogyakarta", "Surabaya",   315),
        ]:
            nav.tambah_jalur(a, b, c)
        st.session_state.navigator = nav


# ─────────────────────────────────────────
#  PAGES — ADMIN
# ─────────────────────────────────────────
def page_tambah_kota(nav: Graph):
    st.markdown('<div class="page-title">Tambah Kota</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Tambahkan node baru ke jaringan graf pengiriman</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Node Baru")
        kota = st.text_input("Nama Kota", placeholder="contoh: Malang")
        if st.button("➕ Tambah Kota"):
            if kota.strip():
                nav.tambah_kota(kota.strip())
                st.success(f"✓ Kota **{kota}** berhasil ditambahkan ke graf")
            else:
                st.error("Nama kota tidak boleh kosong")
        st.markdown('</div>', unsafe_allow_html=True)

    if nav.semua_kota():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Node dalam Graf")
        cols = st.columns(6)
        for i, k in enumerate(nav.semua_kota()):
            cols[i % 6].markdown(
                f'<div style="background:#161C2E;border:1px solid #1E2535;border-radius:10px;'
                f'padding:10px 14px;text-align:center;font-size:13px;color:#7EB0FF;'
                f'font-family:\'Syne\',sans-serif;font-weight:600;margin-bottom:8px">{k}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)


def page_tambah_jalur(nav: Graph):
    st.markdown('<div class="page-title">Tambah Jalur</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Tambahkan edge (bobot jarak) antara dua node di graf</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Edge Baru")
        c1, c2, c3 = st.columns([2, 2, 1])
        asal   = c1.text_input("Kota Asal",   placeholder="Jakarta")
        tujuan = c2.text_input("Kota Tujuan", placeholder="Surabaya")
        jarak  = c3.number_input("Jarak (KM)", min_value=1, value=100)
        if st.button("➕ Tambah Jalur"):
            if asal.strip() and tujuan.strip():
                nav.tambah_jalur(asal.strip(), tujuan.strip(), int(jarak))
                st.success(f"✓ Jalur {asal} ↔ {tujuan} ({jarak} KM) ditambahkan")
            else:
                st.error("Asal dan tujuan tidak boleh kosong")
        st.markdown('</div>', unsafe_allow_html=True)

    jalur_list = nav.semua_jalur()
    if jalur_list:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        section("Semua Edge dalam Graf")
        for a, b, d in jalur_list:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:10px 0;border-bottom:1px solid #1A2035">'
                f'<span style="color:#C4CCE0;font-size:14px">'
                f'<span style="color:#5B8EF0">{a}</span> ↔ <span style="color:#5B8EF0">{b}</span>'
                f'</span>'
                f'<span style="font-family:\'Syne\',sans-serif;font-weight:700;color:#FBBF24;font-size:13px">'
                f'{d} KM</span></div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)


def page_cari_rute(nav: Graph):
    st.markdown('<div class="page-title">Cari Rute Optimal</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Algoritma Dijkstra mencari jalur terpendek di graf</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("Input Rute")
    c1, c2 = st.columns(2)
    asal   = c1.text_input("Kota Asal",   placeholder="Jakarta")
    tujuan = c2.text_input("Kota Tujuan", placeholder="Surabaya")
    if st.button("🔍 Cari Rute Terpendek"):
        if asal.strip() and tujuan.strip():
            path, dist = nav.dijkstra(asal.strip(), tujuan.strip())
            if path:
                st.success(f"✓ Rute ditemukan — total {int(dist)} KM")
                render_route(path)
                st.markdown(
                    f'<div style="margin-top:16px;padding:16px 20px;background:#0F1832;'
                    f'border-radius:12px;border-left:3px solid #5B8EF0">'
                    f'<span style="font-size:12px;color:#4A5568;text-transform:uppercase;'
                    f'letter-spacing:.1em">Total Jarak</span><br>'
                    f'<span style="font-family:Syne,sans-serif;font-weight:700;font-size:26px;'
                    f'color:#7EB0FF">{int(dist)} KM</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            else:
                st.error("Rute tidak ditemukan. Periksa nama kota atau tambahkan jalur.")
        else:
            st.warning("Isi asal dan tujuan terlebih dahulu")
    st.markdown('</div>', unsafe_allow_html=True)


def page_kirim_barang(nav: Graph):
    st.markdown('<div class="page-title">Buat Pengiriman</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Buat order pengiriman baru dengan kalkulasi biaya otomatis</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("Detail Pengiriman")

    c1, c2 = st.columns(2)
    asal   = c1.text_input("Kota Asal",   placeholder="Jakarta")
    tujuan = c2.text_input("Kota Tujuan", placeholder="Surabaya")
    barang = st.text_input("Nama Barang", placeholder="Laptop, Paket Elektronik, dll")

    c3, c4, c5 = st.columns(3)
    berat    = c3.number_input("Berat (Kg)", min_value=0.1, value=1.0, step=0.5)
    kendaraan = c4.selectbox("Kendaraan", ["motor", "mobil", "truk"],
                              format_func=lambda x: {"motor":"🏍 Motor","mobil":"🚗 Mobil","truk":"🚚 Truk"}[x])
    prioritas = c5.selectbox("Prioritas", ["reguler", "express", "same_day"],
                              format_func=lambda x: {"reguler":"📦 Reguler","express":"⚡ Express","same_day":"🔥 Same Day"}[x])

    if st.button("🚀 Buat Pengiriman"):
        if asal.strip() and tujuan.strip() and barang.strip():
            path, dist = nav.dijkstra(asal.strip(), tujuan.strip())
            if path:
                biaya = hitung_biaya(dist, berat, kendaraan, prioritas)
                jam   = estimasi_jam(dist, kendaraan)
                resi  = str(uuid.uuid4())[:8].upper()
                st.session_state.pengiriman.append({
                    "resi":     resi,
                    "barang":   barang,
                    "asal":     asal.strip(),
                    "tujuan":   tujuan.strip(),
                    "rute":     " → ".join(path),
                    "jarak":    int(dist),
                    "status":   "Diproses",
                    "biaya":    biaya,
                    "kendaraan":kendaraan,
                    "prioritas":prioritas,
                    "history":  [f"{datetime.now().strftime('%d %b %Y %H:%M')} — Diproses"],
                })
                st.success("✓ Pengiriman berhasil dibuat!")
                st.markdown(
                    f'<div style="text-align:center"><div class="resi-badge">{resi}</div>'
                    f'<div style="font-size:12px;color:#4A5568;margin-top:4px">Nomor Resi</div></div>',
                    unsafe_allow_html=True
                )
                render_route(path)
                m1, m2, m3 = st.columns(3)
                m1.metric("Jarak", f"{int(dist)} KM")
                m2.metric("Estimasi", f"{jam} Jam")
                m3.metric("Biaya", f"Rp {int(biaya):,}")
            else:
                st.error("Rute tidak ditemukan. Periksa nama kota.")
        else:
            st.warning("Lengkapi semua field pengiriman")
    st.markdown('</div>', unsafe_allow_html=True)


def page_tracking():
    st.markdown('<div class="page-title">Semua Pengiriman</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Pantau seluruh status pengiriman aktif</div>', unsafe_allow_html=True)

    pengiriman = st.session_state.pengiriman
    if not pengiriman:
        st.markdown(
            '<div style="text-align:center;padding:60px;color:#2E3A52;font-size:15px">'
            '📭 Belum ada pengiriman</div>',
            unsafe_allow_html=True
        )
        return

    for p in reversed(pengiriman):
        sc = status_class(p["status"])
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px">
            <div>
              <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:18px;
                color:#FFFFFF;letter-spacing:.05em">{p['resi']}</span>
              <span style="font-size:13px;color:#4A5568;margin-left:12px">{p['barang']}</span>
            </div>
            <span class="status-pill {sc}">{p['status']}</span>
          </div>
          <div style="display:flex;gap:24px;font-size:13px;color:#8892AA">
            <span>📍 {p['asal']} → {p['tujuan']}</span>
            <span>📏 {p.get('jarak','—')} KM</span>
            <span>💰 Rp {int(p['biaya']):,}</span>
            <span>🚗 {p.get('kendaraan','—')}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)


def page_update_status():
    st.markdown('<div class="page-title">Update Status</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Perbarui status pengiriman berdasarkan nomor resi</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("Cari & Update")
    resi   = st.text_input("Nomor Resi", placeholder="contoh: A1B2C3D4")
    status = st.selectbox("Status Baru", STATUS_LIST)
    if st.button("✏️ Update Status"):
        if resi.strip():
            found = False
            for p in st.session_state.pengiriman:
                if p["resi"] == resi.strip().upper():
                    p["status"] = status
                    p["history"].append(f"{datetime.now().strftime('%d %b %Y %H:%M')} — {status}")
                    st.success(f"✓ Status resi **{resi.upper()}** diperbarui → {status}")
                    found = True
                    break
            if not found:
                st.error("Nomor resi tidak ditemukan")
        else:
            st.warning("Masukkan nomor resi")
    st.markdown('</div>', unsafe_allow_html=True)


def page_statistik():
    pengiriman = st.session_state.pengiriman
    total      = len(pengiriman)
    pemasukan  = sum(p["biaya"] for p in pengiriman)
    selesai    = sum(1 for p in pengiriman if p["status"] == "Selesai")
    aktif      = total - selesai

    st.markdown('<div class="page-title">Statistik</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Ringkasan performa sistem pengiriman</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card">
        <div class="metric-label">Total Pengiriman</div>
        <div class="metric-value">{total}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Total Pemasukan</div>
        <div class="metric-value metric-accent">Rp {int(pemasukan):,}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Selesai</div>
        <div class="metric-value" style="color:#34D399">{selesai}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Aktif</div>
        <div class="metric-value" style="color:#FBBF24">{aktif}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    nav = st.session_state.navigator
    st.markdown('<div class="card">', unsafe_allow_html=True)
    section("Struktur Graf")
    kota_list  = nav.semua_kota()
    jalur_list = nav.semua_jalur()
    st.markdown(
        f'<div style="font-size:13px;color:#8892AA;margin-bottom:12px">'
        f'{len(kota_list)} node · {len(jalur_list)} edge</div>',
        unsafe_allow_html=True
    )
    cols = st.columns(min(len(kota_list), 6)) if kota_list else []
    for i, k in enumerate(kota_list):
        cols[i % len(cols)].markdown(
            f'<div style="background:#161C2E;border:1px solid #1E2535;border-radius:10px;'
            f'padding:8px 12px;text-align:center;font-size:12px;color:#7EB0FF;'
            f'font-family:\'Syne\',sans-serif;font-weight:700;margin-bottom:8px">{k}</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────
#  PAGES — KONSUMEN
# ─────────────────────────────────────────
def page_cari_rute_user(nav: Graph):
    st.markdown('<div class="page-title">Cek Rute Pengiriman</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Temukan jalur terpendek untuk pengirimanmu</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    asal   = c1.text_input("Kota Asal",   placeholder="Jakarta")
    tujuan = c2.text_input("Kota Tujuan", placeholder="Surabaya")
    if st.button("🔍 Cari Rute"):
        path, dist = nav.dijkstra(asal.strip(), tujuan.strip())
        if path:
            st.success(f"✓ Rute optimal ditemukan — {int(dist)} KM")
            render_route(path)
        else:
            st.error("Rute tidak ditemukan")
    st.markdown('</div>', unsafe_allow_html=True)


def page_lacak_user():
    st.markdown('<div class="page-title">Lacak Pengiriman</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Pantau status paketmu secara real-time</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    resi = st.text_input("Nomor Resi", placeholder="contoh: A1B2C3D4")
    if st.button("🔎 Lacak"):
        if resi.strip():
            found = False
            for p in st.session_state.pengiriman:
                if p["resi"] == resi.strip().upper():
                    found = True
                    sc = status_class(p["status"])
                    st.markdown(f"""
                    <div style="margin:16px 0">
                      <div style="font-size:12px;color:#4A5568;text-transform:uppercase;
                        letter-spacing:.1em;margin-bottom:6px">Status saat ini</div>
                      <span class="status-pill {sc}" style="font-size:15px;padding:8px 20px">
                        {p['status']}
                      </span>
                    </div>
                    <div style="display:flex;gap:20px;font-size:13px;color:#8892AA;margin:16px 0">
                      <span>📦 {p['barang']}</span>
                      <span>📍 {p['asal']} → {p['tujuan']}</span>
                      <span>💰 Rp {int(p['biaya']):,}</span>
                    </div>
                    <div style="font-size:12px;color:#4A5568;text-transform:uppercase;
                      letter-spacing:.1em;margin:20px 0 12px">Riwayat</div>
                    """, unsafe_allow_html=True)
                    render_timeline(p["history"])
                    break
            if not found:
                st.error("Nomor resi tidak ditemukan")
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────
def page_login():
    st.markdown("""
    <div class="login-wrap">
      <div class="login-logo">⬡ KIRIM.ID</div>
      <div class="login-tagline">Sistem Rute Pengiriman Berbasis Graf Dijkstra</div>
      <div class="login-card">
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-weight:600;font-size:16px;'
                'color:#FFFFFF;margin-bottom:20px">Masuk ke Sistem</div>', unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="admin / konsumen")
    password = st.text_input("Password", type="password", placeholder="••••••••")

    if st.button("→ Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.role = USERS[username]["role"]
            st.rerun()
        else:
            st.error("Username atau password salah")

    st.markdown(
        '<div class="login-hint">admin/admin123 · konsumen/user123</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────
def render_sidebar_brand(role: str):
    label = "Admin Panel" if role == "admin" else "Konsumen"
    st.sidebar.markdown(
        f'<div class="brand">⬡ <span>KIRIM.ID</span></div>'
        f'<div style="font-size:11px;color:#2E3A52;text-transform:uppercase;'
        f'letter-spacing:.1em;margin-bottom:24px;padding-left:2px">{label}</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="KIRIM.ID — Sistem Rute Pengiriman",
        page_icon="⬡",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()
    init_state()

    nav: Graph = st.session_state.navigator

    # ── LOGIN ──
    if st.session_state.role is None:
        page_login()
        return

    # ── ADMIN ──
    if st.session_state.role == "admin":
        render_sidebar_brand("admin")
        menu = st.sidebar.selectbox("", [
            "🏙  Tambah Kota",
            "🔗  Tambah Jalur",
            "🗺  Cari Rute",
            "📦  Kirim Barang",
            "📋  Tracking",
            "✏️  Update Status",
            "📊  Statistik",
            "🚪  Logout",
        ])
        st.sidebar.markdown("<hr>", unsafe_allow_html=True)

        if   "Tambah Kota"    in menu: page_tambah_kota(nav)
        elif "Tambah Jalur"   in menu: page_tambah_jalur(nav)
        elif "Cari Rute"      in menu: page_cari_rute(nav)
        elif "Kirim Barang"   in menu: page_kirim_barang(nav)
        elif "Tracking"       in menu: page_tracking()
        elif "Update Status"  in menu: page_update_status()
        elif "Statistik"      in menu: page_statistik()
        elif "Logout"         in menu:
            st.session_state.role = None
            st.rerun()

    # ── KONSUMEN ──
    elif st.session_state.role == "user":
        render_sidebar_brand("user")
        menu = st.sidebar.selectbox("", [
            "🗺  Cari Rute",
            "🔎  Lacak Pengiriman",
            "🚪  Logout",
        ])
        st.sidebar.markdown("<hr>", unsafe_allow_html=True)

        if   "Cari Rute"        in menu: page_cari_rute_user(nav)
        elif "Lacak Pengiriman" in menu: page_lacak_user()
        elif "Logout"           in menu:
            st.session_state.role = None
            st.rerun()


if __name__ == "__main__":
    main()