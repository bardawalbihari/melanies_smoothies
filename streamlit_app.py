# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col, when_matched

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

order_filled = st.checkbox('Order Filled?')  # Add this to mark as FILLED

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
pd_df = my_dataframe.to_pandas()
fruit_display_names = list(pd_df['FRUIT_NAME'])

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients (order matters):',
    options=fruit_display_names,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Comma separated, ordered
    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled)
        VALUES ('{ingredients_string}', '{name_on_order}', {'TRUE' if order_filled else 'FALSE'})
    """

    st.write("Your insert statement will be:", my_insert_stmt)

    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")



import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

