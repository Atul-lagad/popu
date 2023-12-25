import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import sklearn


#dataframe
from main import df
fl = pd.read_csv('flags_iso.csv')
fl = fl[['Country', 'URL']]
df = pd.merge(df, fl, on='Country', how='left')
#stetting flag of us
df.loc[2, 'URL'] = 'https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg'

year = st.selectbox(
    'select an year',
    ('select an option','2023', '2022', '2020', '2015', '2010', '2000', '1990', '1980', '1970')
)

if year != 'select an option':
    df = df.drop(columns=['rank', 'worldPercentage', 'growthRate', 'density', 'CCA3', 'Capital', 'Area (km²)'])
    df = df.rename(columns=lambda x: x.split()[0] if 'Population' in x else x)
    df = df.loc[:, ['Country', 'Continent', year, 'URL']]
    top5 = df.sort_values(by=year, ascending=False).head()

    sum = df[year].sum()
    b = sum / 1e7
    c = b.round(2)
    st.subheader(f"total world population in {year}")
    st.write(f"{c} crores")

    st.subheader(f"top 5 populated countries in {year}")

    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    for i, col in enumerate(columns):
        with col:
            st.write("")  # Optional empty space between images
            url_value = top5.iloc[i]['URL']
            if pd.isna(url_value):
                st.write("No image URL")
                st.write(" ")
                st.subheader(top5.iloc[i]['Country'])
                a = top5.iloc[i][year]
                b = a / 1e7
                c = b.round(2)
                st.write(f"{c} crores")
            else:
                st.image(url_value)
                st.subheader(top5.iloc[i]['Country'])
                a = top5.iloc[i][year]
                b = a / 1e7
                c = b.round(2)
                st.write(f"{c} crores")
    d=df
    st.subheader("Continent Population")
    dff=df.groupby('Continent').sum()[year].reset_index()
    st.dataframe(dff,use_container_width=True)
    x = dff[['Continent', year]]
    st.bar_chart(x.set_index('Continent'))


    #country ip
    country = st.text_input(f'Enter a country to show data of {year}')
    country = country.title()
    if country:
        data = d[d['Country'] == country][year]
        data=data.iloc[0]
        b = data / 1e7
        c = b.round(2)
        st.subheader(f"{c} crores")

