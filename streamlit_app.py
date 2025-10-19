# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col, when_matched

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input: Name on Smoothie
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit options (with SEARCH_ON) from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
pd_df = my_dataframe.to_pandas()
fruit_display_names = list(pd_df['FRUIT_NAME'])

# Multiselect with max_selections=5
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    options=fruit_display_names,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        # Look up SEARCH_ON term for API
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # Display nutrition header for each fruit
        st.subheader(f"{fruit_chosen} Nutrition Information")
        # Call API using SEARCH_ON value
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    st.write("Your insert statement will be:", my_insert_stmt)

    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")



import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)





