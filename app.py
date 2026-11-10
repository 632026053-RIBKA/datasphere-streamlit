

import streamlit as st
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import uuid
from datetime import datetime, timezone

# ==========================================
# KONEKSI MONGODB
# ==========================================

@st.cache_resource
def koneksi_mongodb():
    client = MongoClient(
        st.secrets["MONGO_URI"],
        serverSelectionTimeoutMS=5000
    )
    client.admin.command("ping")
    return client

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="DataSphere | Streamlit Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# CUSTOM CSS - DATASPHERE PROFESSIONAL
# ==========================================

st.markdown("""
<style>

/* IMPORT FONT */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* GLOBAL */
html, body, [class*="css"], button, input, textarea {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #0b1020, #111a33);
    color: #f1f5f9;
    font-size: 17px;
}

/* MAIN CONTENT */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #10182b !important;
    border-right: 1px solid #263653;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #f1f5f9 !important;
    font-size: 16px !important;
    font-weight: 500;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* HERO SECTION */
.hero {
    background: linear-gradient(120deg, #172554, #312e81, #164e63);
    padding: 42px;
    border-radius: 20px;
    border: 1px solid #3b82f6;
    margin-bottom: 28px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

.hero h1 {
    color: #ffffff !important;
    font-size: 42px !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    margin-bottom: 12px;
}

.hero p {
    color: #dbeafe !important;
    font-size: 18px !important;
    line-height: 1.8;
}

/* DASHBOARD CARDS */
.card {
    background: #17233b;
    border: 1px solid #293d5c;
    border-radius: 18px;
    padding: 25px;
    min-height: 180px;
    margin-bottom: 18px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.15);
    transition: 0.3s ease;
}

.card:hover {
    border-color: #38bdf8;
    transform: translateY(-3px);
}

.card h3 {
    color: #67e8f9 !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    margin-bottom: 12px;
}

.card p {
    color: #cbd5e1 !important;
    font-size: 16px !important;
    line-height: 1.8;
}

/* SECTION TITLE */
.section-title {
    color: #ffffff !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    margin-top: 30px;
    margin-bottom: 20px;
}

/* GENERAL HEADINGS */
h1 {
    color: #ffffff !important;
    font-size: 38px !important;
    font-weight: 800 !important;
    letter-spacing: -0.7px;
}

h2 {
    color: #ffffff !important;
    font-size: 29px !important;
    font-weight: 700 !important;
}

h3 {
    color: #ffffff !important;
    font-size: 23px !important;
    font-weight: 700 !important;
}

h4 {
    color: #e2e8f0 !important;
    font-size: 19px !important;
    font-weight: 600 !important;
}

/* PARAGRAPH */
.stMarkdown p,
.stMarkdown li {
    color: #e2e8f0 !important;
    font-size: 17px !important;
    line-height: 1.8 !important;
}



/* ==========================================
   ALERT - FIX WARNA TULISAN
========================================== */

[data-testid="stAlert"] {
    background-color: #E0F2FE !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 12px !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div,
[data-testid="stAlert"] li,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    line-height: 1.7 !important;
}

[data-testid="stAlert"] svg {
    color: #0369A1 !important;
}

/* METRICS */
[data-testid="stMetric"] {
    background: #17233b;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #293d5c;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
    font-size: 16px !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #67e8f9 !important;
    font-size: 32px !important;
    font-weight: 800 !important;
}

/* INPUT */
.stTextInput label,
.stSelectbox label,
.stNumberInput label,
.stFileUploader label,
.stTextArea label {
    color: #f1f5f9 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* BUTTON */
.stButton > button {
    border-radius: 10px;
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 10px 20px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border-color: #67e8f9;
    color: #67e8f9;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid #293d5c;
    border-radius: 12px;
}

/* DIVIDER */
hr {
    border-color: #334155 !important;
}

/* HEADER */
[data-testid="stHeader"] {
    background-color: #0b1020 !important;
}

/* HIDE DEFAULT MENU */
#MainMenu, footer {
    visibility: hidden;
}

/* ==========================================
   FIX TEKS DAFTAR COLLECTION
========================================== */

/* Deskripsi collection */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: #CBD5E1 !important;
    -webkit-text-fill-color: #CBD5E1 !important;
    font-size: 16px !important;
}

/* Label radio button */
[data-testid="stRadio"] label,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] label span,
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] {
    color: #F1F5F9 !important;
    -webkit-text-fill-color: #F1F5F9 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* Teks pilihan student_data dan comments */
[data-testid="stRadio"] [role="radiogroup"] label * {
    color: #F1F5F9 !important;
    -webkit-text-fill-color: #F1F5F9 !important;
}

/* Teks seluruh widget radio */
[data-testid="stRadio"] {
    color: #F1F5F9 !important;
}

/* ==========================================
   SIDEBAR NAVIGATION - IMPROVED CONTRAST
========================================== */

[data-testid="stSidebar"] {
    background: #071426 !important;
}

/* Tombol navigasi */
[data-testid="stSidebar"] [data-testid="stButton"] button {
    background: #142b45 !important;
    color: #ffffff !important;
    border: 1px solid #294766 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    min-height: 44px !important;
}

/* Hover */
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background: #164e70 !important;
    border-color: #38bdf8 !important;
    color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("# 🌌 DataSphere")
    st.title("Streamlit Dashboard")
    
st.markdown("""
<style>
/* Kolom nama dan komentar */
.stTextInput input,
.stTextArea textarea {
    color: #222222 !important;
    background-color: #ffffff !important;
    caret-color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}

/* Placeholder */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #777777 !important;
    -webkit-text-fill-color: #777777 !important;
}
</style>

""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigasi",
    [
        "🏠 Home",
        "📂 Dataset Explorer",
        "🤖 ML Laboratory",
        "🎯 Classification",
        "🔮 Clustering Studio",
        "🗄️ MongoDB Hub",
        "💬 Community",
        "ℹ️ About"
    ]
)

st.markdown("---")
st.caption("DataSphere v1.0")
st.caption("Powered by Python & Streamlit")

# ==========================================
# HALAMAN HOME
# ==========================================
if menu == "🏠 Home":

    st.markdown("""
    <div class="hero">
        <h1>Welcome to DataSphere 🌌</h1>
        <p>
            Explore data, build machine learning models,
            discover patterns, and transform information
            into intelligent insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Dashboard Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Machine Learning", "2 Models", "Regression & Classification")

    with col2:
        st.metric("Data Analysis", "3 Modules", "Explore & Process Data")

    with col3:
        st.metric("Database", "MongoDB", "Data Storage")

    st.markdown(
        '<div class="section-title">Explore Your Workspace</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>📂 Dataset Explorer</h3>
            <p>Upload, preview, and understand your dataset
            through interactive data exploration.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>🔮 Clustering Studio</h3>
            <p>Discover hidden patterns and group similar
            data using clustering algorithms.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>💬 Community & Feedback</h3>
            <p>Share comments, feedback, and ideas
            with other DataSphere users.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>🤖 ML Laboratory</h3>
            <p>Build and evaluate regression and
            classification machine learning models.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>🗄️ MongoDB Hub</h3>
            <p>Store datasets, manage records,
            and support model retraining.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>ℹ️ About DataSphere</h3>
            <p>Learn about the platform, its features,
            and the technology behind it.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("© 2026 DataSphere | AI Intelligence Dashboard")

# ==========================================

# ==========================================

# ==========================================
# DATASET EXPLORER
# ==========================================
elif menu == "📂 Dataset Explorer":

    st.title("📂 Dataset Explorer")
    st.write("Upload and explore your dataset.")

    uploaded_file = st.file_uploader(
        "Upload dataset CSV",
        type=["csv"],
        key="upload_dataset"
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep=";")

        st.session_state["dataset"] = df
        st.session_state["dataset_name"] = uploaded_file.name

    st.divider()
    st.subheader("📥 Muat Dataset Tersimpan")

    try:
        client = koneksi_mongodb()
        db = client["datasphere"]

        metadata_collection = db["dataset_metadata"]
        records_collection = db["dataset_records"]

        daftar_dataset = list(
            metadata_collection.find().sort("created_at", -1)
        )

        if daftar_dataset:

            pilihan_dataset = {
                (
                    f"{item.get('dataset_name', 'Tanpa nama')} | "
                    f"{item.get('row_count', 0)} baris | "
                    f"ID: {item['dataset_id'][:8]}"
                ): item["dataset_id"]
                for item in daftar_dataset
            }

            nama_pilihan = st.selectbox(
                "Pilih dataset yang ingin dimuat",
                list(pilihan_dataset.keys())
            )

            if st.button("📂 Muat Dataset"):
                dataset_id = pilihan_dataset[nama_pilihan]

                data = list(
                    records_collection.find(
                        {"dataset_id": dataset_id},
                        {"_id": 0, "dataset_id": 0, "row_index": 0}
                    ).sort("row_index", 1)
                )

                if data:
                    st.session_state["dataset"] = pd.DataFrame(data)

                    metadata_terpilih = next(
                        item for item in daftar_dataset
                        if item["dataset_id"] == dataset_id
                    )

                    st.session_state["dataset_name"] = (
                        metadata_terpilih.get(
                            "dataset_name", "Dataset tanpa nama"
                        )
                    )

                    st.success("Dataset berhasil dimuat!")
                    st.rerun()
                else:
                    st.warning("Data tidak ditemukan.")

        else:
            st.info("Belum ada dataset yang tersimpan di MongoDB.")

    except Exception as e:
        st.error(f"Gagal memuat dataset: {e}")

    if "dataset" in st.session_state:

        df = st.session_state["dataset"]

        st.success("Dataset berhasil ditemukan!")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Jumlah Baris", df.shape[0])

        with col2:
            st.metric("Jumlah Kolom", df.shape[1])

        with col3:
            st.metric("Data Kosong", int(df.isnull().sum().sum()))

        st.subheader("Preview Dataset")
        st.dataframe(df, use_container_width=True)

        st.subheader("Informasi Dataset")
        st.write("Nama Kolom:")
        st.write(list(df.columns))

        st.subheader("Visual Analytics")

        if "G3" in df.columns:

            import numpy as np
            import plotly.graph_objects as go

            nilai = pd.to_numeric(
                df["G3"], errors="coerce"
            ).dropna()

            bins = np.arange(-0.5, 21.5, 1)
            counts, edges = np.histogram(nilai, bins=bins)

            colors = [
                "#312e81", "#3730a3", "#4338ca",
                "#4f46e5", "#6366f1", "#7c3aed",
                "#8b5cf6", "#a855f7", "#c026d3",
                "#d946ef", "#c026d3", "#a855f7",
                "#8b5cf6", "#6366f1", "#4f46e5",
                "#3b82f6", "#2563eb", "#0891b2",
                "#06b6d4", "#22d3ee", "#67e8f9"
            ]

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=list(range(21)),
                y=counts,
                marker=dict(
                    color=colors,
                    line=dict(color="#0f172a", width=1.5)
                ),
                hovertemplate=(
                    "Nilai: %{x}<br>"
                    "Jumlah siswa: %{y}<extra></extra>"
                )
            ))

            fig.update_layout(
                title=dict(
                    text="Distribusi Nilai Akhir Siswa (G3)",
                    font=dict(size=22, color="#ffffff")
                ),
                xaxis_title="Nilai Akhir Siswa",
                yaxis_title="Jumlah Siswa",
                template="plotly_dark",
                paper_bgcolor="#17233b",
                plot_bgcolor="#17233b",
                font=dict(
                    family="Arial",
                    size=13,
                    color="#ffffff"
                ),
                xaxis=dict(
                    tickmode="linear",
                    dtick=1,
                    gridcolor="#334155"
                ),
                yaxis=dict(
                    gridcolor="#334155"
                ),
                margin=dict(l=20, r=20, t=70, b=40),
                height=450,
                bargap=0.18
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="grafik_distribusi_nilai_g3"
            )

        else:
            st.warning("Kolom G3 tidak ditemukan dalam dataset.")

    else:
        st.info("Silakan unggah file CSV untuk mulai mengeksplorasi data.")

# ==========================================
# MACHINE LEARNING LABORATORY
# ==========================================
elif menu == "🤖 ML Laboratory":

    st.title("🤖 Machine Learning Laboratory")
    st.write("Prediksi nilai akhir siswa menggunakan Linear Regression.")

    if "dataset" not in st.session_state:
        st.warning(
            "Silakan unggah dataset terlebih dahulu melalui Dataset Explorer."
        )

    else:
        df = st.session_state["dataset"]

        st.subheader("Konfigurasi Model")

        fitur = ["studytime", "absences", "G1", "G2"]
        target = "G3"

        if all(kolom in df.columns for kolom in fitur + [target]):

            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import (
                mean_absolute_error,
                mean_squared_error,
                r2_score
            )

            data_ml = df[fitur + [target]].copy()

            for kolom in fitur + [target]:
                data_ml[kolom] = pd.to_numeric(
                    data_ml[kolom], errors="coerce"
                )

            data_ml = data_ml.dropna()

            X = data_ml[fitur]
            y = data_ml[target]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            model = LinearRegression()
            model.fit(X_train, y_train)

            prediksi = model.predict(X_test)

            st.success("Model Linear Regression berhasil dilatih!")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "MAE",
                f"{mean_absolute_error(y_test, prediksi):.3f}"
            )

            col2.metric(
                "RMSE",
                f"{mean_squared_error(y_test, prediksi) ** 0.5:.3f}"
            )

            col3.metric(
                "R² Score",
                f"{r2_score(y_test, prediksi):.3f}"
            )

            hasil = pd.DataFrame({
                "Nilai Aktual": y_test.values,
                "Nilai Prediksi": prediksi
            })

            st.subheader("Hasil Prediksi")
            st.dataframe(hasil, use_container_width=True)

            import plotly.express as px

            fig = px.scatter(
                hasil,
                x="Nilai Aktual",
                y="Nilai Prediksi",
                title="Perbandingan Nilai Aktual dan Prediksi"
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#17233b",
                plot_bgcolor="#17233b"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="grafik_regresi_linear"
            )

        else:
            st.warning("Dataset tidak memiliki kolom yang dibutuhkan.")

# ==========================================
# CLASSIFICATION
# ==========================================
elif menu == "🎯 Classification":

    
    if "dataset" not in st.session_state:
        st.warning("Silakan unggah dataset melalui Dataset Explorer.")

    else:
        df = st.session_state["dataset"]

        fitur = ["studytime", "absences", "G1", "G2"]
        target = "G3"

        if all(k in df.columns for k in fitur + [target]):

            from sklearn.model_selection import train_test_split
            from sklearn.tree import DecisionTreeClassifier
            from sklearn.metrics import (
                accuracy_score,
                classification_report,
                confusion_matrix
            )

            data_ml = df[fitur + [target]].copy()

            for kolom in fitur + [target]:
                data_ml[kolom] = pd.to_numeric(
                    data_ml[kolom], errors="coerce"
                )

            data_ml = data_ml.dropna()

            data_ml["Kategori"] = pd.cut(
                data_ml["G3"],
                bins=[-float("inf"), 10, 15, float("inf")],
                labels=["Rendah", "Sedang", "Tinggi"],
                right=False
            )

            X = data_ml[fitur]
            y = data_ml["Kategori"]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y,
                test_size=0.2,
                random_state=42,
                stratify=y
            )

            model = DecisionTreeClassifier(
                max_depth=4,
                random_state=42
            )

            model.fit(X_train, y_train)
            prediksi = model.predict(X_test)

            st.success("Decision Tree berhasil dilatih!")

            st.subheader("Evaluasi Model")

            akurasi = accuracy_score(y_test, prediksi)
            st.metric("Accuracy Score", f"{akurasi:.3f}")

            st.subheader("Classification Report")

            laporan = classification_report(
                y_test,
                prediksi,
                labels=["Rendah", "Sedang", "Tinggi"],
                output_dict=True,
                zero_division=0
            )

            st.dataframe(
                pd.DataFrame(laporan).transpose().round(3),
                use_container_width=True
            )

            st.subheader("Confusion Matrix")

            cm = confusion_matrix(
                y_test,
                prediksi,
                labels=["Rendah", "Sedang", "Tinggi"]
            )

            import plotly.express as px

            fig = px.imshow(
                cm,
                x=["Rendah", "Sedang", "Tinggi"],
                y=["Rendah", "Sedang", "Tinggi"],
                text_auto=True,
                color_continuous_scale="Blues",
                title="Confusion Matrix"
            )

            fig.update_layout(template="plotly_dark")

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="grafik_classification"
            )

        else:
            st.warning("Dataset tidak memiliki kolom yang dibutuhkan.")

    if "dataset" not in st.session_state:
        st.warning("Silakan unggah dataset terlebih dahulu melalui Dataset Explorer.")

    else:
        df = st.session_state["dataset"]

    
# ==========================================
# CLUSTERING STUDIO
# ==========================================
elif menu == "🔮 Clustering Studio":

    st.title("🔮 Student Clustering Studio")
    st.write("Mengelompokkan siswa berdasarkan kemiripan pola belajar.")

    if "dataset" not in st.session_state:
        st.warning("Silakan unggah dataset melalui Dataset Explorer.")

    else:
        df = st.session_state["dataset"]

        fitur = ["studytime", "absences", "G1", "G2"]

        if all(k in df.columns for k in fitur):

            from sklearn.preprocessing import StandardScaler
            from sklearn.cluster import KMeans
            from sklearn.decomposition import PCA
            from sklearn.metrics import silhouette_score

            data_cluster = df[fitur].copy()

            for kolom in fitur:
                data_cluster[kolom] = pd.to_numeric(
                    data_cluster[kolom], errors="coerce"
                )

            data_cluster = data_cluster.dropna()

            if len(data_cluster) < 3:
                st.warning("Data terlalu sedikit untuk membuat 3 cluster.")

            else:
                # Standardisasi data
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(data_cluster)

                # Membuat model K-Means
                model_cluster = KMeans(
                    n_clusters=3,
                    random_state=42,
                    n_init=10
                )

                cluster = model_cluster.fit_predict(X_scaled)

                hasil_cluster = data_cluster.copy()
                hasil_cluster["Cluster"] = cluster

                st.success("K-Means Clustering berhasil dijalankan!")

                # Evaluasi clustering
                skor_silhouette = silhouette_score(
                    X_scaled, cluster
                )

                st.subheader("Evaluasi Clustering")

                col1, col2 = st.columns(2)

                col1.metric(
                    "Jumlah Cluster",
                    "3"
                )

                col2.metric(
                    "Silhouette Score",
                    f"{skor_silhouette:.3f}"
                )

                # Jumlah anggota setiap cluster
                st.subheader("Distribusi Anggota Cluster")

                jumlah_cluster = (
                    hasil_cluster["Cluster"]
                    .value_counts()
                    .sort_index()
                )

                st.bar_chart(jumlah_cluster)

                # Visualisasi PCA
                st.subheader("Visualisasi Cluster")

                pca = PCA(n_components=2)
                hasil_pca = pca.fit_transform(X_scaled)

                visualisasi = pd.DataFrame({
                    "PCA 1": hasil_pca[:, 0],
                    "PCA 2": hasil_pca[:, 1],
                    "Cluster": cluster.astype(str)
                })

                import plotly.express as px

                fig = px.scatter(
                    visualisasi,
                    x="PCA 1",
                    y="PCA 2",
                    color="Cluster",
                    title="Visualisasi Pengelompokan Siswa",
                    color_discrete_sequence=[
                        "#00D4FF",
                        "#A855F7",
                        "#22C55E"
                    ]
                )

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#17233b",
                    plot_bgcolor="#17233b"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key="grafik_clustering"
                )

                # Tabel hasil
                st.subheader("Hasil Pengelompokan Siswa")

                st.dataframe(
                    hasil_cluster,
                    use_container_width=True
                )

        else:
            st.warning("Dataset tidak memiliki kolom yang dibutuhkan.")



elif menu == "🗄️ MongoDB Hub":

    st.title("🗄️ MongoDB Hub")
    st.write("Mengelola database siswa menggunakan MongoDB Atlas.")

    st.subheader("Status Koneksi Database")

    try:
        # Menghubungkan ke MongoDB
        client = koneksi_mongodb()
        db = client["datasphere"]

        st.success("Berhasil terhubung ke MongoDB Atlas!")
        st.metric("Status Database", "Connected")
        st.write("Nama Database: datasphere")

        # Membuat collection
        if "student_data" not in db.list_collection_names():
            db.create_collection("student_data")

        if "comments" not in db.list_collection_names():
            db.create_collection("comments")

        # Menyimpan dataset
        st.divider()


        st.subheader("💾 Simpan Dataset ke MongoDB")

        if "dataset" in st.session_state:
            df = st.session_state["dataset"]

            st.write(f"Jumlah data: {len(df)} baris")

            if st.button("💾 Simpan Dataset ke MongoDB"):

                dataset_id = str(uuid.uuid4())
                records_collection = db["dataset_records"]

                try:
                    metadata_collection = db["dataset_metadata"]

                    clean_df = df.astype(object).where(
                        pd.notna(df), None
                    )
                    records = clean_df.to_dict(orient="records")

                    for index, record in enumerate(records):
                        record["dataset_id"] = dataset_id
                        record["row_index"] = index

                        for key, value in record.items():
                            if hasattr(value, "item"):
                                record[key] = value.item()

                    for start in range(0, len(records), 1000):
                        records_collection.insert_many(
                            records[start:start + 1000]
                        )

                    metadata_collection.insert_one({
                        "dataset_id": dataset_id,
                        "dataset_name": st.session_state.get(
                            "dataset_name", "Dataset tanpa nama"
                        ),
                        "created_at": datetime.now(timezone.utc),
                        "row_count": len(df),
                        "column_count": len(df.columns),
                        "columns": [str(col) for col in df.columns]
                    })

                    st.success(
                        "Dataset berhasil disimpan secara permanen!"
                    )

                except Exception as e:
                    records_collection.delete_many(
                        {"dataset_id": dataset_id}
                    )
                    st.error(f"Gagal menyimpan dataset: {e}")

        else:
            st.warning(
                "Silakan unggah dataset terlebih dahulu melalui Dataset Explorer."
            )

        # Menampilkan collection yang interaktif
        st.divider()
        st.subheader("📁 Daftar Collection")

        daftar_collection = db.list_collection_names()

        if daftar_collection:

            pilihan_collection = st.radio(
                "Pilih collection untuk melihat data:",
                daftar_collection,
                horizontal=True,
                key="pilihan_collection"
            )

            st.subheader(f"Isi Collection: {pilihan_collection}")

            jumlah_data = db[pilihan_collection].count_documents({})

            st.metric("Jumlah Dokumen", jumlah_data)

            data_collection = list(
                db[pilihan_collection].find(
                    {},
                    {"_id": 0}
                ).limit(100)
            )

            if data_collection:
                import pandas as pd

                df_collection = pd.DataFrame(data_collection)

                st.dataframe(
                    df_collection,
                    use_container_width=True
                )
            else:
                st.info("Collection ini belum memiliki data.")

        else:
            st.info("Belum ada collection.")

        # Retraining Machine Learning
        st.divider()
        st.subheader("🤖 Retraining Machine Learning")

        if st.button("🔄 Latih Ulang Model dari MongoDB"):

            import pandas as pd
            import numpy as np

            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import (
                mean_absolute_error,
                mean_squared_error,
                r2_score
            )

            # Mengambil data dari MongoDB
            data_mongodb = list(
                db["student_data"].find({}, {"_id": 0})
            )

            if len(data_mongodb) > 0:

                df_mongodb = pd.DataFrame(data_mongodb)

                fitur = ["studytime", "absences", "G1", "G2"]
                target = "G3"

                if all(
                    kolom in df_mongodb.columns
                    for kolom in fitur + [target]
                ):

                    # Memastikan data numerik
                    df_mongodb[fitur + [target]] = (
                        df_mongodb[fitur + [target]]
                        .apply(pd.to_numeric, errors="coerce")
                    )

                    df_mongodb = df_mongodb.dropna(
                        subset=fitur + [target]
                    )

                    if len(df_mongodb) >= 2:

                        X = df_mongodb[fitur]
                        y = df_mongodb[target]

                        X_train, X_test, y_train, y_test = train_test_split(
                            X,
                            y,
                            test_size=0.2,
                            random_state=42
                        )

                        # Melatih model
                        model_baru = LinearRegression()
                        model_baru.fit(X_train, y_train)

                        prediksi = model_baru.predict(X_test)

                        # Evaluasi model
                        mae = mean_absolute_error(y_test, prediksi)

                        rmse = np.sqrt(
                            mean_squared_error(y_test, prediksi)
                        )

                        r2 = r2_score(y_test, prediksi)

                        st.success(
                            "Model berhasil dilatih ulang dari MongoDB!"
                        )

                        col1, col2, col3 = st.columns(3)

                        col1.metric("MAE", f"{mae:.3f}")
                        col2.metric("RMSE", f"{rmse:.3f}")
                        col3.metric("R² Score", f"{r2:.3f}")

                        st.write(
                            f"Jumlah data pelatihan: {len(X_train)}"
                        )

                        st.write(
                            f"Jumlah data pengujian: {len(X_test)}"
                        )

                    else:
                        st.warning("Data valid tidak mencukupi untuk pelatihan.")

                else:
                    st.error("Kolom dataset tidak sesuai.")

            else:
                st.warning("Belum ada data di MongoDB.")

    except KeyError:
        st.error(
            "MONGO_URI belum ditemukan. Periksa file secrets.toml."
        )

    except Exception as e:
        st.error("Terjadi kesalahan pada MongoDB.")
        st.code(f"{type(e).__name__}: {e}")


elif menu == "💬 Community":

    st.title("💬 DataSphere Community")
    st.write("Tempat berbagi pengalaman dan berdiskusi tentang pembelajaran.")

    st.divider()
    st.subheader("✍️ Tulis Komentar")

    try:
        client = koneksi_mongodb()
        db = client["datasphere"]

        with st.form("form_komentar"):
            nama = st.text_input("Nama Pengguna")
            komentar = st.text_area("Tulis komentar kamu...")
            kirim = st.form_submit_button("📨 Kirim Komentar")

        if kirim:
            if nama.strip() and komentar.strip():
                from datetime import datetime

                db["comments"].insert_one({
                    "nama": nama.strip(),
                    "komentar": komentar.strip(),
                    "created_at": datetime.now()
                })

                st.success("Komentar berhasil dikirim!")
            else:
                st.warning("Nama dan komentar harus diisi.")

        st.divider()
        st.subheader("📢 Komentar Pengguna")

        daftar_komentar = list(
            db["comments"].find().sort("created_at", -1).limit(50)
        )

        if daftar_komentar:
            for item in daftar_komentar:
                with st.container(border=True):
                    st.markdown(f"**👤 {item.get('nama', 'Pengguna')}**")
                    st.write(item.get("komentar", ""))

                    waktu = item.get("created_at")
                    if waktu:
                        st.caption(waktu.strftime("%d-%m-%Y %H:%M"))
        else:
            st.info("Belum ada komentar.")

    except Exception as e:
        st.error("Tidak dapat mengakses Community.")
        st.code(f"{type(e).__name__}: {e}")


elif menu == "ℹ️ About":

    st.title("ℹ️ About DataSphere")

    st.markdown("""
    ### 🌌 DataSphere – Streamlit Dashboard

    DataSphere merupakan aplikasi berbasis web yang dikembangkan
    menggunakan Python dan Streamlit untuk membantu pengguna
    memahami pengolahan data dan penerapan Machine Learning.

    """)

    st.divider()

    st.subheader("🎯 Tujuan Aplikasi")

    st.write("""
    - Memahami proses eksplorasi dan analisis data.
    - Melakukan prediksi menggunakan Machine Learning.
    - Mengelompokkan data menggunakan algoritma clustering.
    - Mengelola data menggunakan MongoDB.
    - Menyediakan ruang diskusi melalui fitur Community.
    """)

    st.divider()

    st.subheader("🛠️ Teknologi yang Digunakan")

    col1, col2, col3 = st.columns(3)

    col1.metric("Bahasa Pemrograman", "Python")
    col2.metric("Framework", "Streamlit")
    col3.metric("Database", "MongoDB")

    st.divider()

    st.subheader("📌 Fitur Utama")

    fitur = [
        "Dataset Explorer",
        "Machine Learning Laboratory",
        "Classification",
        "Clustering Studio",
        "MongoDB Hub",
        "Community"
    ]

    for item in fitur:
        st.markdown(f"- ✅ {item}")

    st.divider()

    st.caption("DataSphere v1.0 | Built with Python & Streamlit")