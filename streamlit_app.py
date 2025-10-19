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
# Connect to Snowflake

# Load fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Multiselect with max_selections
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    options=fruit_list,
    max_selections=5
)

# Build ingredients string and call API for each ingredient (following screenshot logic)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen.lower()}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Insert statement (same as before)
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    st.write("Your insert statement will be:", my_insert_stmt)

    # Submit order button
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
