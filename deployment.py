import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide", page_title="Deployment Module", page_icon="🚀")

t_col_1, t_col_2 = st.columns([0.8, 0.2], vertical_alignment="center")

t_col_1.markdown("""
    <div style="background-color:lightblue;padding:10px;border-radius:5px">
        <h1 style="color:black;text-align:center;">Deployment of Mid-Term Project</h1>
        <h2 style="color:black;text-align:center;">
            Data Visualization of the World Bank Group.
        </h2>
    </div>
""", unsafe_allow_html=True) 

# add image
t_col_2.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Logo_The_World_Bank.svg/2560px-Logo_The_World_Bank.svg.png", width=300)    


# read_df
df_data = pd.read_excel("dataset/ESGData_imputed.xlsx")
df_ind_info = pd.read_excel("dataset/ESG_translated_Series.xlsx")

# get country list
country_lst = df_data["Country Name"].unique().tolist()
default_index = country_lst.index("Egypt, Arab Rep.")  # Index of Eyft to set it as the default value

# get indicator list
indicator_lst = df_ind_info["Series Code"].tolist()

page = st.sidebar.radio('Pages', ['Home', "Check Indicators", "Comparisons"])


if page == 'Home':
    st.markdown("<h1 style='text-align: center; color: blue;'>Description of the World Bank Indicators</h1>", unsafe_allow_html= True)
    st.write("""
    The World Bank provides a comprehensive set of indicators that cover various aspects of global development. 
    These indicators are used to monitor and analyze economic, social, and environmental trends across countries. 
    They help policymakers, researchers, and the public understand development challenges and track progress 
    towards global goals such as poverty reduction, education, health, and sustainability.
    """)

    st.markdown("""    Some key categories of World Bank indicators include:
    - **Economic Indicators**: GDP, inflation rates, trade balances, and employment statistics. """)

    st.markdown("""- **Social Indicators**: Education enrollment rates, literacy rates, health outcomes, and demographic data.""")
    st.markdown("""- **Environmental Indicators**: Data on natural resources, pollution levels, and climate change impacts.""")
    st.markdown("""- **Poverty and Inequality Indicators**: Measures of income distribution, poverty rates, and social inclusion.""")
    st.markdown("""- **Infrastructure Indicators**: Access to clean water, sanitation, electricity, and transportation networks.""")    
    st.markdown("""- **Governance Indicators**: Data on political stability, government effectiveness, and regulatory quality.""")

    # Starting to show some indicators that have been used in this project
    st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
    st.markdown("""Our implementation includes a selection of these indicators to provide insights into global development trends and challenges.
                The selected indicators and their translation are presented below:""")
    
    for row_idx, row in df_ind_info.iterrows():
        # English line (left)
        st.markdown(f"""<div style="text-align:left; font-size:16px; font-weight:bold;">{row['Series Code']}: {row['Indicator Name']}</div>""", unsafe_allow_html=True)
        # Arabic line (right)
        st.markdown(f"""<div style="text-align:right; font-size:15px; direction:rtl;">{row['Arabic Indicator Name']}</div>""", unsafe_allow_html=True)
        # Add spacing
        st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

    # button to show samples of the data description
    if st.button("Show samples of the cleaned data and its description"):
        st.subheader("Sample of the Data Used in Deployment")
        st.dataframe(df_data.head())
        st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
        st.subheader("Data Description")
        st.write(df_data.describe())


elif page == "Check Indicators":
    st.header("Welcode to data visualization module")
    st.subheader("This page allows you to explore and visualize various World Bank indicators used in the project.")

    st.markdown("<h2 style='text-align: center; color: blue;'>Select a Country:</h2>", unsafe_allow_html= True)
    # Country selection
    country = st.selectbox("", options=country_lst, index=default_index)  
    st.subheader(f"Data for Country: {country}")

    st.write(df_data[df_data["Country Name"] == country])

    # Indicator selection
    st.markdown("<h2 style='text-align: center; color: blue;'>Select an Indicator:</h2>", unsafe_allow_html= True)
    indicator = st.selectbox("", options=indicator_lst)
    st.subheader(f"Data for Indicator: {indicator}")

    # English line (left)
    st.markdown(f"""<div style="text-align:left; font-size:16px; font-weight:bold;">{indicator}: 
                {df_ind_info.loc[df_ind_info["Series Code"] == indicator, 'Indicator Name'].values}</div>""", unsafe_allow_html=True)
    # Arabic line (right)
    st.markdown(f"""<div style="text-align:right; font-size:15px; direction:rtl;">{df_ind_info.loc[df_ind_info["Series Code"] == indicator, 'Arabic Indicator Name'].values}</div>""", unsafe_allow_html=True)


    if st.button("Visualize Indicator Data"):
        indicator_data = df_data[(df_data["Country Name"] == country)][["Year", indicator]].dropna()
        # indicator_data = df_data[(df_data["Country Name"] == country) & (df_data["Series Code"] == indicator)].dropna()
        if not indicator_data.empty:
            fig1 = px.line(indicator_data, x="Year", y=indicator, title=f"{indicator} over Years for {country}")
            fig2 = px.bar(indicator_data, x="Year", y=indicator, title=f"{indicator} over Years for {country} - Bar Chart")
            
            st.plotly_chart(fig1)
            st.plotly_chart(fig2)

        else:
            st.write("No data available for the selected indicator and country.")   



elif page == "Comparisons":
    st.header("Welcode to data visualization module")
    st.subheader("This page allows you to compare and visualize various World Bank indicators for 3 countries.")

    st.markdown("<h2 style='text-align: center; color: blue;'>Select a Countries:</h2>", unsafe_allow_html= True)
    # split to two columns
    comp_col1, comp_col2, comp_col3 = st.columns(3, vertical_alignment="center")

    # Country selection
    with comp_col1:
        country_1 = st.selectbox("select country 1", options=country_lst, index=default_index)  
        # st.write(f"##### Data for Country: {country_1}")

    with comp_col2:
        country_2 = st.selectbox("select country 2", options=country_lst, index=default_index)  
        # st.write(f"##### Data for Country: {country_2}")  

    with comp_col3:
        country_3 = st.selectbox("select country 3", options=country_lst, index=default_index)  
        # st.write(f"##### Data for Country: {country_3}")

    # Indicator selection
    st.markdown("<h2 style='text-align: center; color: blue;'>Select an Indicator:</h2>", unsafe_allow_html= True)
    indicator = st.selectbox("", options=indicator_lst)
    st.subheader(f"Data for Indicator: {indicator}")

    # English line (left)
    st.markdown(f"""<div style="text-align:left; font-size:16px; font-weight:bold;">{indicator}: 
                {df_ind_info.loc[df_ind_info["Series Code"] == indicator, 'Indicator Name'].values}</div>""", unsafe_allow_html=True)
    # Arabic line (right)
    st.markdown(f"""<div style="text-align:right; font-size:15px; direction:rtl;">{df_ind_info.loc[df_ind_info["Series Code"] == indicator, 'Arabic Indicator Name'].values}</div>""", unsafe_allow_html=True)

    if st.button("Visualize Indicator Data for Comparison"):
        comp_data_1 = df_data[(df_data["Country Name"] == country_1)][["Year", indicator]].dropna()
        comp_data_2 = df_data[(df_data["Country Name"] == country_2)][["Year", indicator]].dropna()
        comp_data_3 = df_data[(df_data["Country Name"] == country_3)][["Year", indicator]].dropna()

        fig = px.line(title=f"Comparison of {indicator} over Years")
        
        if not comp_data_1.empty:
            fig.add_scatter(x=comp_data_1["Year"], y=comp_data_1[indicator], mode='lines+markers', name=country_1)
        
        if not comp_data_2.empty:
            fig.add_scatter(x=comp_data_2["Year"], y=comp_data_2[indicator], mode='lines+markers', name=country_2)
        
        if not comp_data_3.empty:
            fig.add_scatter(x=comp_data_3["Year"], y=comp_data_3[indicator], mode='lines+markers', name=country_3)
        
        st.plotly_chart(fig)