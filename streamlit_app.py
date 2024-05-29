# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

import streamlit as st

title = st.text_input("Name on Smoothie: ")
st.write("The name on your smoothie will be: ", title)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
import streamlit as st

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',my_dataframe,max_selections=5)

ingredients_string= ''

if ingredients_list:
  for fruit_chosen in ingredients_list:
      ingredients_string += fruit_chosen + ' '

  my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','"""+title+"""')"""


  time_to_insert = st.button("Submit Order", type="primary")
  if(time_to_insert):
      session.sql(my_insert_stmt).collect()
      st.success('Your Smoothie is ordered, '+title+'!', icon="✅")
