import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to get industry-specific beta (simplified mapping)
@st.cache_data
def get_industry_beta(industry):
    industry_betas = {
        'Technology': 1.25, 'Financial Services': 1.15, 'Healthcare': 0.95,
        'Consumer Goods': 0.85, 'Industrials': 1.05, 'Energy': 1.10,
        'Utilities': 0.75, 'Default': 1.0
    }
    return industry_betas.get(industry, industry_betas['Default'])

# Function to get risk-free rate (10-year Treasury yield)
@st.cache_data
def get_risk_free_rate():
    try:
        url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx?data=yield"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 't-chart'})
        latest_yield = float(table.find_all('tr')[-1].find_all('td')[-1].text) / 100
        return latest_yield
    except:
        return 0.03  # Default to 3% if scraping fails

# Calculate WACC
def calculate_wacc(stock, risk_free_rate, market_risk_premium=0.06):
    try:
        company_beta = stock.info.get('beta', 1.0)
        industry_beta = get_industry_beta(stock.info.get('industry', 'Default'))
        adjusted_beta = (company_beta + industry_beta) / 2
        cost_of_equity = risk_free_rate + (adjusted_beta * market_risk_premium)
        
        total_debt = stock.info.get('totalDebt', 0)
        interest_expense = stock.financials.loc['Interest Expense'].iloc[0] if 'Interest Expense' in stock.financials.index else 0
        cost_of_debt = abs(interest_expense / total_debt) if total_debt > 0 else 0.05
        tax_rate = stock.info.get('effectiveTaxRate', 0.21)
        
        market_cap = stock.info.get('marketCap', 0)
        total_value = market_cap + total_debt
        equity_weight = market_cap / total_value if total_value > 0 else 0.8
        debt_weight = total_debt / total_value if total_value > 0 else 0.2
        
        wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
        return wacc if wacc > 0 else 0.08, adjusted_beta
    except Exception as e:
        st.warning(f"WACC calculation failed: {str(e)}. Using default 8%")
        return 0.08, 1.0

# Enhanced DCF Valuation
def calculate_advanced_dcf(stock, short_term_growth, long_term_growth, wacc, years_short=5, years_total=10):
    print("Inside calc advanced dcf")
    print(stock.cashflow)
    cash_flow = stock.cashflow.loc['Free Cash Flow'].dropna()
    if len(cash_flow) < 1:
        return None, None, None
    
    latest_fcf = cash_flow.iloc[0]
    projected_fcfs = []
    present_values = []
    current_fcf = latest_fcf
    
    for year in range(years_short):
        current_fcf *= (1 + short_term_growth)
        pv = current_fcf / ((1 + wacc) ** (year + 1))
        projected_fcfs.append(current_fcf)
        present_values.append(pv)
    
    for year in range(years_short, years_total):
        growth_rate = short_term_growth - ((short_term_growth - long_term_growth) * 
                                          (year - years_short + 1) / (years_total - years_short))
        current_fcf *= (1 + growth_rate)
        pv = current_fcf / ((1 + wacc) ** (year + 1))
        projected_fcfs.append(current_fcf)
        present_values.append(pv)
    
    terminal_value = projected_fcfs[-1] * (1 + long_term_growth) / (wacc - long_term_growth)
    pv_terminal = terminal_value / ((1 + wacc) ** years_total)
    
    enterprise_value = sum(present_values) + pv_terminal
    net_debt = stock.info.get('totalDebt', 0) - stock.info.get('totalCash', 0)
    equity_value = enterprise_value - net_debt
    fair_price = equity_value / stock.info['sharesOutstanding']
    
    return fair_price, projected_fcfs, wacc