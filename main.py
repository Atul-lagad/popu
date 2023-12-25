import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.title('World Population Analysis 🌏📊')

#dataset
df=pd.read_csv("population_final.csv")
df.loc[0, '1990 Population'] = 870452165
df.loc[0, '1980 Population'] = 696828385
#for blank of india
#total population in 2023
total_world_population23=df['2023 Population'].sum()
total_world_population23=(total_world_population23/1e7).round(2)
#total population in 2022
total_world_population22=df['2022 Population'].sum()
total_world_population22=(total_world_population22/1e7).round(2)
#total population in increment from 22 to 23
inc_22to23=(total_world_population23-total_world_population22)/total_world_population22*100
inc_22to23=inc_22to23.round(2)

col1, col2= st.columns(2)
col1.metric("Population 2023",f"{total_world_population23} crore",f"{inc_22to23}%")
col2.metric("Population 2022", f"{total_world_population22} crore")

#dataframe print
st.subheader("Continent wise population")
Continent_wise_popu=df.groupby(['Continent'])[['2022 Population','2023 Population','Area (km²)']].sum()
Continent_wise_popu=Continent_wise_popu.reset_index()
Continent_wise_popu['Increment']=(Continent_wise_popu['2023 Population']-Continent_wise_popu['2022 Population'])/Continent_wise_popu['2022 Population']*100
Continent_wise_popu['Increment'] = Continent_wise_popu['Increment'].apply(lambda x: f'{x:.2f}%')
st.dataframe(Continent_wise_popu,use_container_width=True)

#pip plot
st.subheader("Pie charts")
col1, col2= st.columns(2)

with col1:
    st.write("continent population")
    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie(Continent_wise_popu['2023 Population'], labels=Continent_wise_popu['Continent'], autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Display the pie chart in Streamlit
    st.pyplot(fig)

with col2:
    st.write("continent area")
    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie(Continent_wise_popu['Area (km²)'], labels=Continent_wise_popu['Continent'], autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Display the pie chart in Streamlit
    st.pyplot(fig,use_container_width=True)

#barplot of inc
st.write("")
st.subheader("Increment of population from 2022 to 2023 (in %)")
Continent_wise_popu['Increment'] =(Continent_wise_popu['2023 Population']-Continent_wise_popu['2022 Population'])/Continent_wise_popu['2022 Population']*100
x=Continent_wise_popu[['Continent','Increment']]
st.bar_chart(x.set_index('Continent'))





