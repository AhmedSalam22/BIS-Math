import streamlit as st
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta 
from dateutil import parser

import numpy as np
import pandas as pd
from datetime import date as date_
from datetime import datetime


st.title("Mathematics Applications")
if st.sidebar.checkbox("Merchant's and USA rules" , False):


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
        else:
            result = {
                "Original debt on {}".format(date_taking): amount , 

            }
            soup = BeautifulSoup(html , "lxml")
            dates =list(map(lambda x: x.string , soup.find_all("p" , {"class":"date-inputs"})))
            inputs = np.array(list(map(lambda x: float(x.string) , soup.find_all("p" , {"class":"val-inputs"}))))


            previous_amount = 0.0
            for i in range(num):
               
                if i == 0 :
                    result["{} Payment on {}".format(i+1 , dates[i])] = inputs[i]
                    differ = pd.Timestamp(parser.parse(dates[i])) - pd.Timestamp(date_taking)  
                    result["interest on {} from {} to {}".format(amount , date_taking , dates[i])] = amount * interest_rate * differ.days / 365
                    previous_amount = amount - inputs[i] + amount * interest_rate * differ.days / 365
                    result["Balance on {}".format(dates[i])] = previous_amount
                else:
                    result["{} Payment on {}".format(i+1 , dates[i])] = inputs[i]
                    differ = pd.Timestamp(parser.parse(dates[i])) - pd.Timestamp(parser.parse(dates[i-1]))  
                    result["interest on {} from {} to {}".format(previous_amount , dates[i-1] , dates[i])] = previous_amount * interest_rate * differ.days / 365
                    previous_amount = previous_amount - inputs[i] + previous_amount * interest_rate * differ.days / 365
                    result["Balance on {}".format(dates[i])] = previous_amount

            differ = pd.Timestamp(due_date) - pd.Timestamp(parser.parse(dates[-1]))

            result["interest on {} from {} to {}".format(previous_amount , dates[-1] , due_date)] = previous_amount * interest_rate * differ.days / 365
            result["Balance on {}".format(due_date)] = previous_amount + (previous_amount * interest_rate * differ.days / 365)
            st.table(pd.Series(result))
