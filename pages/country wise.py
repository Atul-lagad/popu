import streamlit as st
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import sklearn


#dataframe
from main import df
country = st.text_input('Enter a country')
country=country.title()
fl = pd.read_csv('flags_iso.csv')
fl = fl[['Country', 'URL']]
df = pd.merge(df, fl, on='Country', how='left')
df.loc[0, '1990 Population'] = 870452165
df.loc[0, '1980 Population'] = 696828385
df.loc[2, 'URL'] = 'https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg'
data=df[df['Country'] == country]

if country in df['Country'].values:
    col1, col2, col3 = st.columns(3)
    with col1:
        a = data['URL']
        url_value = a.iloc[0]
        if pd.isna(url_value):
            st.write("No image URL")
        else:
            st.image(url_value)
    with col2:
        a = data['2023 Population'].iloc[0]
        b = a / 1e7
        c=b.round(2)
        d=data['growthRate'].iloc[0]
        col2.metric("Population 2023", f"{c} crore", f"{d}%")
    with col3:
        a = data['2022 Population'].iloc[0]
        b = a / 1e7
        c=b.round(2)
        col3.metric("Population 2022", f"{c} crore")

    col1, col2, col3 = st.columns(3)
    with col1:
        a = data['Country'].iloc[0]
        col1.metric("Country",a)
    with col2:
        b=data['Capital'].iloc[0]
        col2.metric("Capital",b)
    with col3:
        c=data['Continent'].iloc[0]
        col3.metric("Continent",c)

    col1, col2, col3 = st.columns(3)
    with col1:
        a = data['rank'].iloc[0]
        col1.metric("Population rank", a)
    with col2:
        b = data['Area (km²)'].iloc[0]
        col2.metric("Area (km²)", b)
    with col3:
        c = data['density'].iloc[0]
        col3.metric("Density per Km", c)

    t = df.drop(
        columns=['rank', 'worldPercentage', 'growthRate', 'density', 'CCA3', 'Capital', 'Continent', 'Area (km²)','URL'])
    t = t.rename(columns=lambda x: x.split()[0] if 'Population' in x else x)
    df_transposed = t.set_index('Country').transpose()
    #df_transposed = df_transposed.sort_values('India')
    new=df_transposed[country].reset_index()
    new['index'] =new['index'].astype(str)
    new=new.sort_values(by='index')

    st.title(" ")
    st.subheader("Year wise population")

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(new['index'], new[country], label='Line Plot')
    ax.set_xlabel('year')
    ax.set_ylabel(f"Population {country}")
    ax.legend()
    # Display the Matplotlib plot using Streamlit
    st.pyplot(fig)

    st.title(" ")
    st.subheader("Predict data")
    yr = st.number_input('Enter a Year to Predit population', min_value=2024, max_value=2100)
    if yr>2023:
        X = new[['index']]
        y = new[country]
        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.34, random_state=42)
        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        # Fit the model to the training data
        model.fit(X_train, y_train)
        # Make predictions on the test set
        predictions = model.predict(X_test)
        # Evaluate the model
        # from sklearn.metrics import mean_squared_error
        # mse = mean_squared_error(y_test, predictions)
        # print(f'Mean Squared Error: {mse}')
        predictions_linear = model.predict([[yr]])
        predictions_linear=predictions_linear[0]
        a = predictions_linear / 1e7
        b = a.round(2)
        st.write(f"for '{country}' the predicted population in '{yr}' is")
        st.subheader(f'{b} crores')

        #for another graph whith predicte values
        #old data define as old
        new['Category'] = 'old'
        new_row = {'index': yr, country: predictions_linear, 'Category': 'pre'}
        new_row = pd.DataFrame([new_row])
        # Concatenating the new row to the existing DataFrame
        new = pd.concat([new_row, new], ignore_index=True)
        new['index'] = new['index'].astype(int)
        new = new.sort_values(by='index')

        #new dataset added with a year and pred value . now graph it
        st.title(" ")
        st.subheader("predicted population")
        new=new.drop([1,2,3])
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(new['index'], new[country], label='Line Plot predcted')
        ax.set_xlabel('year')
        ax.set_ylabel(f"Population {country}")
        ax.legend()
        # Display the Matplotlib plot using Streamlit
        st.pyplot(fig)
    else:
        st.write('enter year greater than 2023')





else:
    st.write("No such a country")

