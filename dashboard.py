import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

# Load data
day_df = pd.read_csv("day.csv")

# Streamlit sidebar setup
with st.sidebar:
    #Menampilkan logo
    st.image("logo.png")  

# Mapping nama musim
nama_musim = {
    1: 'Musim Semi',
    2: 'Musim Panas',
    3: 'Musim Gugur',
    4: 'Musim Dingin'
}
day_df['season'] = day_df['season'].map(nama_musim)

# Sidebar untuk multi-select filter
st.sidebar.header("Filter Data")
selected_season = st.sidebar.multiselect("Pilih Musim", options=day_df['season'].unique(), default=day_df['season'].unique())

# Menambahkan option 'All' untuk tipe penyewa
selected_user_type = st.sidebar.multiselect(
    "Pilih Tipe Penyewa", 
    options=['casual', 'registered', 'All'], 
    default=['casual', 'registered']
)

# Memfilter data berdasarkan pilihan musim
filtered_df = day_df[day_df['season'].isin(selected_season)]

# Membuat kondisi 'All' tipe penyewa dengan menghitung total dari tipe penyewa casual dan registered
if 'All' in selected_user_type:
    filtered_df['total'] = filtered_df['casual'] + filtered_df['registered']
    selected_user_type = ['total']

# Memfilter dan mengelompokkan data berdasarkan bulan dan musim, serta menjumlahkan jenis pengguna yang dipilih
filtered_df = filtered_df[['mnth', 'season'] + selected_user_type]
kategori_penyewa = filtered_df.groupby(['mnth', 'season'])[selected_user_type].sum().reset_index()

# Menampilkan visualisasinya
st.subheader("Jumlah Penyewa per Bulan Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(12, 6))

# Plot untuk setiap tipe pengguna yang dipilih
for user_type in selected_user_type:
    sns.barplot(data=kategori_penyewa, x='mnth', y=user_type, hue='season', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewa")
ax.set_title("Distribusi Penyewa per Bulan Berdasarkan Musim")
ax.legend(title="Musim")
st.pyplot(fig)

#Menampilkan jumlah rental sepeda perBulan
day_df['dteday'] = pd.to_datetime(day_df['dteday'], errors='coerce')
bulan = day_df[(day_df['dteday'].dt.year >= 2011) & (day_df['dteday'].dt.year <= 2012)]
bulan['Year'] = bulan['dteday'].dt.year
bulan['Month'] = bulan['dteday'].dt.month

rental_bulanan = bulan.groupby(['Year', 'Month'])['cnt'].sum().reset_index()
rental_bulanan = rental_bulanan.sort_values(by=['Year', 'Month'])
st.title('Bike Sharing Data Dashboard')

total_rentals = rental_bulanan['cnt'].sum()
st.metric('Total Rentals (2011-2012)', total_rentals)

# Menampilkan Jumlah Rental Sepeda per Bulan (2011-2012)
st.subheader('Jumlah Rental Sepeda per Bulan (2011-2012)')
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(rental_bulanan['Month'].astype(str) + '-' + rental_bulanan['Year'].astype(str), 
        rental_bulanan['cnt'], marker='o', color='blue')
ax.set_title('Jumlah Rental Sepeda per Bulan (2011-2012)')
ax.set_xlabel('Bulan-Tahun')
ax.set_ylabel('Total Rentals')
ax.set_xticklabels(rental_bulanan['Month'].astype(str) + '-' + rental_bulanan['Year'].astype(str), rotation=90)
ax.grid(True)
st.pyplot(fig)

#Insight
st.markdown("""
**Tren jumlah penyewaan sepeda per bulan (2011-2012)** menunjukan bahwa jumlah penyewaan sepeda meningkat pesat dari awal tahun 2011 hingga puncaknya pada pertengahan 2012, kemudian mengalami penurunan yang signifikan setelahnya. 
  Peningkatan yang tajam pada bulan bulan tertentu menunjukkan adanya musim atau peristiwa yang mendorong lebih banyak orang untuk menyewa sepeda.
""")

# Menampilkan tabel berisi data rental sepeda per bulan
st.subheader('Data Rental Sepeda Bulanan')
st.dataframe(rental_bulanan)


# Membuat filter data untuk menentukan cuaca ekstrem atau normal
cuaca_ekstrem = day_df[(day_df['weathersit'] == 3) & (day_df['temp'] > 0.4)]  
cuaca_normal = day_df[(day_df['weathersit'] != 3) & (day_df['temp'] <= 0.4)] 

rental_ekstrem = cuaca_ekstrem['cnt'].sum()
rental_normal = cuaca_normal['cnt'].sum()
st.subheader('Perbandingan Sewa Sepeda pada Cuaca Ekstrem vs Normal')
categories = ['Cuaca Ekstrem', 'Cuaca Normal']
rentals = [rental_ekstrem, rental_normal]

# Memvisualisasikannya kedalam bentuk bar plot
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.bar(categories, rentals, color=['red', 'green'])
ax2.set_ylim(0, max(rentals) * 1.1)
ax2.set_title('Perbandingan Jumlah Penyewaan Sepeda pada Cuaca Ekstrem vs Normal', fontsize=16)
ax2.set_xlabel('Kategori Cuaca', fontsize=14)
ax2.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
ax2.tick_params(axis='both', which='major', labelsize=12)
plt.tight_layout()
st.pyplot(fig2)
st.write(f'Jumlah penyewaan sepeda pada cuaca ekstrem: {rental_ekstrem}')
st.write(f'Jumlah penyewaan sepeda pada cuaca normal: {rental_normal}')

#Insight
st.markdown("""
            **Grafik perbandingan jumlah penyewaan sepeda pada cuaca ekstrem dengan cuaca normal** menunjukkan bahwa 
            jumlah penyewaan sepeda pada cuaca normal sangat tinggi dibandingkan dengan cuaca ekstrem. Cuaca ekstrem ini
            seperti hujan lebat atau suhu yang tinggi, dan hanya menghasilkan sedikit terhadap total penyewaan sepeda.
            """)


# Mengubah kolom "season" menjadi nama musim berdasarkan mapping "nama_musim" 
def process_season_data(day_df):
    day_df['season'] = day_df['season'].map(nama_musim)
    season_counts = day_df['season'].value_counts()
    
    return day_df

day_df = process_season_data(day_df)

#Menghitung total rental per bulan berdasarkan cuaca dan musim
rental_bulanan = day_df.groupby(['mnth', 'weathersit', 'season'])['cnt'].sum().reset_index()

# Menampilkan bulan dengan penyewaan tertinggi dan terrendah
rental_tertinggi = rental_bulanan[rental_bulanan['cnt'] == rental_bulanan['cnt'].max()]
rental_terendah = rental_bulanan[rental_bulanan['cnt'] == rental_bulanan['cnt'].min()]
st.subheader('Total Penyewaan Sepeda per Bulan Berdasarkan Cuaca dan Musim')

# Visualisasi total penyewaan sepeda per bulan dengan cuaca dan musim
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='mnth', y='cnt', data=rental_bulanan, hue='season', palette='coolwarm', ax=ax)
ax.set_title('Total Penyewaan Sepeda per Bulan Berdasarkan Cuaca dan Musim', fontsize=16)
ax.set_xlabel('Bulan', fontsize=14)
ax.set_ylabel('Total Penyewaan', fontsize=14)
ax.legend(title='Musim', loc='upper left', fontsize=12, title_fontsize=14, bbox_to_anchor=(1, 1))
st.pyplot(fig)

# Insight
st.markdown("""
            **Grafik total penyewaan sepeda berdasarkan cuaca dan musim** terlihat bahwa pada musim panas 
            dan musim gugur, jumlah penyewaan sepeda lebih tinggi, sementara pada musim semi dan musim dingin, 
            penyewaan sepeda lebih rendah. Keberadaan variasi ini menjelaskan bahwa cuaca memainkan peran penting 
            dalam keputusan penyewaan sepeda, dengan musim panas cenderung meningkatkan aktifitas penyewaan sepeda.
""")

st.subheader('Jumlah Sewa Sepeda Tertinggi dan Terendah Berdasarkan Musim')
if not rental_tertinggi.empty:
    highest_season = rental_tertinggi[['season', 'cnt']].iloc[0]
    st.write(f"Penyewaan sepeda tertinggi terjadi pada musim {highest_season['season']} dengan jumlah {highest_season['cnt']:,} penyewaan.")
else:
    st.write("Tidak ada data untuk penyewaan tertinggi.")

if not rental_terendah.empty:
    lowest_season = rental_terendah[['season', 'cnt']].iloc[0]
    st.write(f"Penyewaan sepeda terendah terjadi pada musim {lowest_season['season']} dengan jumlah {lowest_season['cnt']:,} penyewaan.")
else:
    st.write("Tidak ada data untuk penyewaan terendah.")

# Menampilkan dalam bentuk tabel
st.subheader('Data Rental Sepeda Bulanan Berdasarkan Cuaca dan Musim')
st.dataframe(rental_bulanan)


# Membuat fungsi untuk mengkategorikan penyewaan berdasarkan frekuensi
def kategori_penyewa(row):
    if row['cnt'] > 1000:
        return 'Cluster A (Tinggi)'
    elif 700 <= row['cnt'] <= 1000:
        return 'Cluster B (Sedang)'
    else:
        return 'Cluster C (Rendah)'

# Hanya menampilkan tanggal
day_df['dteday'] = day_df['dteday'].dt.date

# Menambahkan kolom 'Cluster' 
day_df['Cluster'] = day_df.apply(kategori_penyewa, axis=1)

# Mengelompokkan data berdasarkan tanggal dan cluster untuk menghitung jumlah sewa sepeda percluster
cluster_per_day = day_df.groupby(['dteday', 'Cluster'])['cnt'].sum().reset_index()
st.subheader('Distribusi Penyewaan Sepeda Berdasarkan Cluster Sepanjang Waktu')

# Menampilkan visualisasi distribusi penyewaan sepeda per cluster sepanjang waktu menggunakan line plot
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dteday', y='cnt', hue='Cluster', data=cluster_per_day, marker='o', ax=ax)
ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Cluster Sepanjang Waktu', fontsize=16)
ax.set_xlabel('Tanggal', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)
st.subheader('Data Penyewaan Sepeda per Cluster')
st.write(day_df[['dteday', 'cnt', 'Cluster']])

#Kesimpulan
st.markdown("""
            Terlihat jelas dari visualisasi **distribusi penyewaan sepeda dari waktu ke waktu**, yang dibagi
            menjadi tiga klaster bahwa Klaster A (Tinggi) memiliki jumlah penyewaan terbanyak, dengan jumlah 
            yang meningkat dari waktu ke waktu. Hal ini menunjukkan bahwa penyewaan sepeda dengan frekuensi tinggi 
            lebih sering terjadi pada waktu yang berbeda, terutama antara pertengahan tahun 2011 dan 2012. 
            Namun, Klaster B (Sedang) dan Klaster C (Rendah) menunjukkan tingkat penyewaan yang lebih rendah, 
            sedangkan tingkat penyewaan Klaster B sedikit meningkat pada waktu-waktu tertentu. Sementara tingkat 
            penyewaan Klaster C tetap rendah sepanjang waktu. Klaster B dan Klaster C menunjukkan pola yang lebih konsisten, 
            penyewaan sepeda di Klaster A dipengaruhi oleh kondisi musiman atau acara tertentu.""")