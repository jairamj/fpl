# -*- coding: utf-8 -*-
"""
Created on Friday 3 September 2021
@author: Jitesh Jairam
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np


st.set_page_config(
    page_title="Financial Planning Calculator 2")

st.title("Financial Planning Calculator")

with st.sidebar.form(key ='Form1'):

        Name=st.text_input("First Name: ")
        Surname=st.text_input("Last Name: ")
        Email=st.text_input("Email: ")
        submitted1 = st.form_submit_button(label='Submit')
        submitted1 = False

if submitted1 == False:

    st.write ("Please enter your details on the sidebar.")    

if submitted1 == True:
    st.header("**Welcome!:sunglasses:**")
  
    st.subheader("Introduction ")


colAge, colMarital_Status = st.columns(2)
with colAge:
        Age=st.number_input(f"{Name}, what's your age?: ", min_value=0, format='%d' )
with colMarital_Status:
        Marital_Status = st.selectbox(
                             'What is your marital regime?',
                                            ('Single', 'In Community of Property', 'Out of Community of Property'))

st.header("**Total Cost of Employment**")
st.subheader("Salary")

colMonthSal, colRetire = st.columns(2)

with colMonthSal:
    salary = st.number_input("Enter your monthly total cost to company /  salary(R): ", min_value=0.00, format='%f')
    st.write('Include all benefits such as pension, provident fund, allowances, bonuses, etc')
with colRetire:    
    retirement1 = st.number_input("Enter your monthly contribution to retirement(R): ", min_value=0.00, format='%f')
    
    if salary-retirement1 < 0 :
        st.write ("Your retirement contribution can not be greater than your salary!")
    else:
        st.write("Add your contribution to prension or provident funds with your company's. Exclude RA's.")
          
    if retirement1*12<=350000:
        r12=round(retirement1*12,2)
    else:
        r12=350000

    salary12 = round (salary*12,2)
    TaxableIncome = salary12 - r12
    
    if (Age < 65 and salary12 < 87300) or (Age>= 65 and salary12 < 135150) or (Age >= 75 and salary12 < 151100):
                
                tax_rate =0
                salary_after_taxes = salary12-r12

    elif TaxableIncome <= 216200: 
                tax_rate = TaxableIncome * 0.18

    elif TaxableIncome <= 337800: 
                tax_rate = (TaxableIncome - 216201) * 0.26 + 38916 

    elif TaxableIncome <= 467500:
                tax_rate = (TaxableIncome- 337801) * 0.31 + 70532 

    elif TaxableIncome <= 613600: 
                tax_rate = (TaxableIncome - 467501) * 0.36 + 110739 

    elif TaxableIncome <= 782200:
                tax_rate = (TaxableIncome - 613601) * 0.39 + 163335 

    elif TaxableIncome <= 1656600:
                tax_rate = (TaxableIncome - 782201) * 0.41 + 229089 
    else:
                tax_rate = (TaxableIncome - 1656601) * 0.45 + 587593

   
    if (Age < 65 and tax_rate>0):
        salary_after_taxes = TaxableIncome - tax_rate + 15714
    elif (Age < 75 and tax_rate>0):
        salary_after_taxes = TaxableIncome - tax_rate + 8613
    elif (Age >= tax_rate>0) :
        salary_after_taxes = TaxableIncome - tax_rate + 2871    
    else:
        salary_after_taxes = TaxableIncome - tax_rate

monthly_takehome_salary = round(salary_after_taxes / 12.00, 2)

with colMonthSal:
    
    st.subheader("Annual Salary is: R" + str(round(salary12)))

with colRetire: 
   if monthly_takehome_salary >= 0: 
    st.subheader("Monthly Take Home Salary: ~R" + str(round(monthly_takehome_salary,2)))
   else:
    st.subheader("Please check your input. Deductions can not be greater than Income!")


st.header("**Monthly Expenses**")
colExpenses1, colExpenses2 = st.columns(2)

with colExpenses1:
    st.subheader("Monthly Rental")
    monthly_rental = st.number_input("Enter your monthly rental(R): ", min_value=0.0,format='%f' )
    
    st.subheader("Daily Food Budget")
    daily_food = st.number_input("Enter your daily food budget (R): ", min_value=0.0,format='%f' )
    monthly_food = daily_food * 30
    
    st.subheader("Monthly Unforeseen Expenses")
    monthly_unforeseen = st.number_input("Enter your monthly unforeseen expenses (R): ", min_value=0.0,format='%f' ) 
    
with colExpenses2:
    st.subheader("Monthly Transport")
    monthly_transport = st.number_input("Enter your monthly transport fee (R): ", min_value=0.0,format='%f' )   
    
    st.subheader("Monthly Utilities Fees")
    monthly_utilities = st.number_input("Enter your monthly utilities fees (R): ", min_value=0.0,format='%f' )
    
    st.subheader("Monthly Entertainment Budget")
    monthly_entertainment = st.number_input("Enter your monthly entertainment budget (R): ", min_value=0.0,format='%f' )   

monthly_expenses = monthly_rental + monthly_food + monthly_transport + monthly_entertainment + monthly_utilities + monthly_unforeseen
monthly_savings = monthly_takehome_salary - monthly_expenses 

st.header("**Savings**")

st.subheader("Monthly Expenses: R" + str(round(monthly_expenses, 2)))
st.subheader("Monthly Savings: R" + str(round(monthly_savings, 2)))

st.markdown("---")

st.header("**Forecast Savings**")
colForecast1, colForecast2 = st.columns(2)
with colForecast1:
    st.subheader("Forecast Year")
    forecast_year = st.number_input("Enter your forecast year (Min 1 year): ", min_value=0,format='%d')
    forecast_months = 12 * forecast_year 
    
    st.subheader("Annual Inflation Rate")
    annual_inflation = st.number_input("Enter annual inflation rate (%): ", min_value=0.0,format='%f')
    monthly_inflation = (1+annual_inflation)**(1/12) - 1
    cumulative_inflation_forecast = np.cumprod(np.repeat(1 + monthly_inflation, forecast_months))
    forecast_expenses = monthly_expenses*cumulative_inflation_forecast
with colForecast2:
    st.subheader("Annual Salary Growth Rate")
    annual_growth = st.number_input("Enter your expected annual salary growth (%): ", min_value=0.0,format='%f')
    monthly_growth = (1 + annual_growth) ** (1/12) - 1
    cumulative_salary_growth = np.cumprod(np.repeat(1 + monthly_growth, forecast_months))
    forecast_salary = monthly_takehome_salary * cumulative_salary_growth 
    
forecast_savings = forecast_salary - forecast_expenses 
cumulative_savings = np.cumsum(forecast_savings)

x_values = np.arange(forecast_year + 1)

fig = go.Figure()
fig.add_trace(
        go.Scatter(
            x=x_values, 
            y=forecast_salary,
            name="Forecast Salary"
        )
    )

fig.add_trace(
        go.Scatter(
            x=x_values,
            y=forecast_expenses,
            name= "Forecast Expenses"
        )
    )

fig.add_trace(
        go.Scatter(
                x=x_values, 
                y=cumulative_savings,
                name= "Forecast Savings"
            )
    )
fig.update_layout(title='Forecast Salary, Expenses & Savings Over the Years',
                   xaxis_title='Year',
                   yaxis_title='Amount(R)')

st.plotly_chart(fig, use_container_width=True)

