# Import python packages
import streamlit as st
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

# Build ingredients string
if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    # Insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write("Your insert statement will be:", my_insert_stmt)

    # Submit order button
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")
