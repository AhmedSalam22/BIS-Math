import streamlit as st
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta 
from dateutil import parser

import numpy as np
import pandas as pd
from datetime import date as date_
from datetime import datetime


st.title("Mathematics Applications")


options = st.radio("Select the method" , ["Merchant's rule Method(simple interests Method)" , "USA's rule (Compound interest Method)"])
interest_rate = st.number_input("interest rate" , 0.0)
due_date = st.date_input("Date of final settlement" )
date_taking = st.date_input("date of taking" )
amount = st.number_input("Original debt")
num = st.number_input("How many partial payments do you have" , 1)


html = [] 
for i in range(int(num)):
    date = st.date_input("Date of partial payment for payment number {}".format(i+1)  , key=i+1)
    val = st.number_input("amount of parital payment  for payment number {}".format(i+1) , 1.0 , key=i+1)
    html.append("""<p class="val-inputs" >{val} </p>
                   <p class="date-inputs" >{date} </p>
    """.format(val=val , date=date))

html = " ".join(html)


if st.checkbox("show result", False ):
    if options == "Merchant's rule Method(simple interests Method)":

        difference_in_years = due_date - date_taking
        difference_in_years =  difference_in_years.days / 365
        result = {
            "Original debt": amount , 
            "interest on {amount} for {due_date}".format(amount=amount , due_date = due_date) : amount  * interest_rate * difference_in_years , 

            "Total": amount * ( 1 + interest_rate * difference_in_years) , 
        }
        soup = BeautifulSoup(html , "lxml")
        dates =list(map(lambda x: x.string , soup.find_all("p" , {"class":"date-inputs"})))
        inputs = np.array(list(map(lambda x: float(x.string) , soup.find_all("p" , {"class":"val-inputs"}))))
        delta = np.array(list(map(lambda x: (pd.Timestamp(due_date) -  pd.Timestamp(parser.parse(x))).days  , dates)))
        interest_on_payments = inputs  * interest_rate  * delta /365

       
        for i in range(num):
            result["partial payment Num:{}".format(i+1)] = inputs[i] 
            result["interest on {} from {} to {}".format(inputs[i] , dates[i] , due_date)] = interest_on_payments[i]
            result["Total for payment Num:{}".format(i+1)] = interest_on_payments[i] + inputs[i]
        
        result["sum of partial payments"] = np.sum((interest_on_payments + inputs))
        result["Balance"] =  result["Total"] - result["sum of partial payments"]


            
        st.table(pd.Series(result))