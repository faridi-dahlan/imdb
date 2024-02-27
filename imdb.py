import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


#interface
st.set_page_config(
    page_title="IMDB Top 400 Movies",
    layout="centered"
)

# 1. as sidebar menu
with st.sidebar:
    selected = option_menu("Menu", ["Home", 'Analyze'], 
        icons=['house', 'graph-up-arrow'], menu_icon="cast", default_index=0)
if selected == 'Home':
    st.markdown("## Tentang IMDB")
    st.image('image/imdb.jpg')
    st.write('**IMDb (singkatan dari Internet Movie Database)** adalah basis data online yang berisi informasi terkait film, serial televisi, podcast, video rumahan, video game, dan konten streaming online - termasuk pemeran, kru produksi, dan biografi pribadi, ringkasan plot, trivia, peringkat, serta ulasan penggemar dan kritikus. IMDb dimulai sebagai basis data film yang dioperasikan oleh penggemar di grup Usenet "rec.arts.movies" pada tahun 1990, dan pindah ke Web pada tahun 1993. Sejak tahun 1998, situs ini dimiliki dan dioperasikan oleh IMDb.com, Inc, anak perusahaan Amazon. Hingga Oktober 2018, IMDb memiliki kira-kira 5.3 juta film/acara (termasuk episode masing-masing) dan 9.3 tokoh di basis data tersebut. IMDb juga memiliki 83 juta pengguna terdaftar.')
    st.write('Pada project kali ini, kita akan melihat Top 400+ Movies All Time. Dataset saya ambil dari melakukan scrapping ke website [**IMDB**](https://www.imdb.com/) menggunakan Octoparse Apps.')
    st.write('-'*100)
    st.markdown("## Alur Pengerjaan Project")
    st.image('image/Body.png')
    st.write('-'*100)
    st.markdown("## Penjelasan Dataset")
    st.write('**Data yang akan kita analisa :**')
    st.write('1. title : judul dari film')
    st.write('2. release_year : tahun rilis film')
    st.write('3. type : rating film')
    st.write('4. duration : durasi film')
    st.write('5. rating : rating nilai film')
    st.write('6. total_user_rating : total user yang memberikan rating pada film tersebut')
    st.write('7. genre : genre film')
    st.write('8. director : direktur film')
    st.write('9. writers : penulis film')
    st.write('10. stars : bintang (aktor/aktris) film')
    st.write('11. achiement : pencapaian (nominasi dan menang piala)')
    st.write('12. first_language : bahasa utama yang digunakan pada film tersebut')
    st.write('13. country : negara asal film tersebut')
    st.write('14. budget dan gross worldwide : biaya pembuatan film dan pendapatan kotor film')
else :
    st.markdown("## Analisa")
    st.write("""Berikut merupakan dataframe yang akan kita gunakan :""")
    df_imdb = pd.read_csv('dataset streamlit/imdb.csv')
    df_imdb['profit'] = df_imdb['gross_worldwide']-df_imdb['budget']
    st.write(df_imdb)
    st.write("-"*100)
    st.markdown("### Analisa 1 : Negara manakah yang mempunyai profit terbesar dari industri film?")
    df_country = df_imdb.groupby('country').agg({'profit':'sum'})
    df_country = df_country.reset_index()
    df_country = df_country.sort_values(by="profit", ascending=False)
    fig1 = px.bar(df_country, x='country', y='profit')
    st.write(fig1)
    st.write("""Berdasarkan grafik diatas, kita bisa melihat bahwa united states (us) mendominasi pasar perfilman dunia, lalu disusul oleh united kingdom (uk) yang memiliki perbedaan nilai profit cukup jauh. Bahkan keseluruhan profit dari film seluruh negara diatas jika diagregasi belum bisa menyamai profit yang didapat us.""")
    st.write("""Kita patut berbangga, dikarenakan negara kita (Indonesia) masuk dalam top 400 film of all time. Bahkan kita hanya memiliki perbedaan 2 juta dollar dari korea selatan secara profit. """)
    st.write("""Lantas, apa film dari negara kita yang masuk ke dalam top 400?""")
    df_indo = df_imdb[df_imdb['country']=='Indonesia']
    st.write(df_indo)
    st.write("-"*100)
    st.markdown("### Analisa 2 : Film apa yang memiliki profit terbesar?")
    df_imdb["ranking"] = df_imdb["profit"].rank(method="min", ascending=False)
    df_imdb_5 = df_imdb[df_imdb["ranking"]<=5]
    df_imdb_5 = df_imdb_5.sort_values(by='ranking')
    fig2 = px.bar(df_imdb_5, x='title', y=['profit','rating','achievements'])
    st.write(fig2)
    st.write("""Secara profit, nilai yang tertinggi adalah Avatar dengan 2.6B dollar. Namun, bukan berarti film ini mendapatkan rating tertinggi. Justru, film lord of the rings yang menduduki posisi 5 menjadi film dengan rating yang tinggi (9.0) diantara film-film di grafik tersebut.""")
    st.write("""Kira-kira apa yang menjadikan suatu film itu menadapat profit begitu besar dibanding film lainnya? Kemungkinan akan banyak faktor. Tetapi dari data tersebut mengatakan jika tidak selalu film yang punya rating tertinggi, dan memiliki achievement yang banyak bisa mendapatkan profit yang juga tinggi""")
    st.write("""Berdasarkan artikel dari [**Kincir**](https://kincir.com/movie/cinema/review-film-avatar-2009-rilis-ulang-xQmpdTCaUmcOQ/) mengatakan film avatar bisa sukses dikarenakan visual yang canggih dan akting yang cukup baik.""")
    st.write("-"*100)
    st.markdown("### Analisa 3 : Bagaimana trend rata-rata profit dari industri film dari tahun ke tahun?")
    df_trends = df_imdb.groupby('release_year')['profit'].mean()
    df_trends = df_trends.reset_index()
    fig3 = px.line(df_trends, x="release_year", y="profit")
    st.write(fig3)
    st.write("""Trend dari tahun ke tahun di grafik menunjukkan bahwa kita tidak bisa memastikan secara pasti untuk pendapatan rata-rata tiap tahunnya. Ini juga bisa diartikan bahwasanya rerata pendapatan untuk industri film memang tidak stabil, dan cukup riskan untuk investasi di industri film.""")
    st.write("""Tentunya ini cukup masuk akal. Mengingat industri film adalah industri yang memiliki banyak faktor kesuksesan dan bukan hanya 1 ataupun 2 faktor saja.""")
    st.write("-"*100)
    st.markdown("### Analisa 4 : Top 5 Director Film by Profit")
    df_director = df_imdb.groupby('director').agg({'profit':'sum','achievements':'sum','title':'count'})
    df_director['ranking'] = df_director['profit'].rank(method="min",ascending=False)
    df_director_5 = df_director[df_director['ranking']<=5]
    df_director_5 = df_director_5.reset_index() 
    fig4 = px.bar(df_director_5, x='director', y=['profit','achievements','title'])
    st.write(fig4)
    st.write("""Director dengan pendapatan profit tertinggi ada di James Cameroon. Namun, bukan berarti dia memiliki achievements terbanyak (nominasi dan win). Hal ini juga sama seperti analisa 2. Tidak selalu director dengan profit tinggi memiliki achievement tinggi dan tidak juga berarti menukangi banyak film.""")
    st.write("""Pendapatan profit film terbesar yang didapatkan James Cameroon juga berasal dari Top 1 Profit Film (Avatar) yang dikomando oleh dirinya.""")
    st.write("-"*100)
    st.markdown("### Apa bahasa yang sering digunakan?")
    df_language = df_imdb.groupby('first_language').agg(language=('first_language','count'))
    df_language = df_language.reset_index()
    fig5 = px.bar(df_language, x='first_language', y='language')
    st.write(fig5)
    st.write("""Tentu hasil grafik tersebut tidaklah mengejutkan. Mengingat bahasa inggris sebagai bahasa internasional yang digunakan oleh seluruh dunia. Produser film pun harus bisa menyesuaikan penggunaan bahasa dialog dalam film agar nantinya bisa lebih dinikmati oleh banyak khalayak dan go internasional.""")






    

