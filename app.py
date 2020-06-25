import streamlit as st
from bs4 import BeautifulSoup


st.title("Mathematics Applications")
st.sidebar.checkbox("Merchant's and USA rules")

interest_rate = st.number_input("How many partial payments do you have" , 0.0)
due_date = st.date_input("Due date" )
date_taking = st.date_input("Due date" )
amount = st.number_input("Amount")
num = st.number_input("How many partial payments do you have" , 1)


html = [] 
for i in range(int(num)):
    date = st.date_input("Date of partial payment"  , key=i)
    val = st.number_input("amount of parital payment" , 1.0 , key=i)
    html.append("""<p class="val-inputs" >{val} </p>
                   <p class="date-inputs" >{date} </p>
    """.format(val=val , date=date))

html = " ".join(html)


st.html(html)
if st.checkbox("show result", False ):
    soup = BeautifulSoup(html , "lxml")
    inputs = list(map(lambda x: float(x.string) , soup.find_all("p" , {"class":"val-inputs"})))
    result = sum(inputs)
    st.markdown("result of sum : {}".format(result))