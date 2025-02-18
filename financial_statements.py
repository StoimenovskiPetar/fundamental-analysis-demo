import pandas as pd
import yfinance as yf
import streamlit as st
import numpy as np

def format_currency(value):
    """Format currency values with B/M suffix."""
    if np.isnan(value):
        return "-"
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    elif value <= -1e9:
        return f"${value/1e9:.2f}B"
    elif value <= -1e6:
        return f"${value/1e6:.2f}M"
    else:
        return f"${value:.2f}"

def get_color_style(value):
    """Return CSS style for positive/negative values."""
    if value > 0:
        return 'color: green'
    elif value < 0:
        return 'color: red'
    return 'color: white'

def get_income_statement(ticker):
    """Get and format income statement data."""
    stock = yf.Ticker(ticker)
    print(stock.income_stmt)
    income_stmt = stock.income_stmt

    if income_stmt.empty:
        return pd.DataFrame()
    
    # Convert index to dates and sort columns
    income_stmt.columns = pd.to_datetime(income_stmt.columns).strftime('%Y-%m-%d')
    income_stmt = income_stmt.sort_index()

        # Format values
    formatted_income_stmt = income_stmt.map(format_currency)

    # Store original values for coloring
    return income_stmt, formatted_income_stmt


def get_balance_sheet(ticker):
    """Get and format balance sheet data."""
    stock = yf.Ticker(ticker)
    bs = stock.balance_sheet
    
    if bs.empty:
        return pd.DataFrame()
        
    # Convert index to dates and sort columns
    bs.columns = pd.to_datetime(bs.columns).strftime('%Y-%m-%d')
    bs = bs.sort_index()
    
    # Format values
    formatted_bs = bs.map(format_currency)
    
    # Store original values for coloring
    return bs, formatted_bs

def get_cash_flow(ticker):
    """Get and format cash flow statement."""
    stock = yf.Ticker(ticker)
    cf = stock.cashflow
    
    if cf.empty:
        return pd.DataFrame()
        
    # Convert index to dates and sort columns
    cf.columns = pd.to_datetime(cf.columns).strftime('%Y-%m-%d')
    cf = cf.sort_index()
    
    # Format values
    formatted_cf = cf.applymap(format_currency)
    
    return cf, formatted_cf

def get_financial_ratios(ticker):
    """Calculate and format key financial ratios."""
    stock = yf.Ticker(ticker)
    info = stock.info
    
    ratios = {
        'Profitability Ratios': {
            'Gross Margin': info.get('grossMargins', 0) * 100,
            'Operating Margin': info.get('operatingMargins', 0) * 100,
            'Net Profit Margin': info.get('profitMargins', 0) * 100,
            'ROE': info.get('returnOnEquity', 0) * 100,
            'ROA': info.get('returnOnAssets', 0) * 100
        },
        'Liquidity Ratios': {
            'Current Ratio': info.get('currentRatio', 0),
            'Quick Ratio': info.get('quickRatio', 0),
            'Operating Cash Flow Ratio': info.get('operatingCashflow', 0) / info.get('totalCurrentLiabilities', 1)
        },
        'Efficiency Ratios': {
            'Asset Turnover': info.get('totalRevenue', 0) / info.get('totalAssets', 1),
            'Inventory Turnover': info.get('totalRevenue', 0) / info.get('inventory', 1) if info.get('inventory', 0) != 0 else 0,
            'Receivables Turnover': info.get('totalRevenue', 0) / info.get('netReceivables', 1) if info.get('netReceivables', 0) != 0 else 0
        }
    }
    
    # Convert to DataFrame
    ratios_df = pd.DataFrame({
        'Category': [cat for cat, metrics in ratios.items() for _ in metrics],
        'Metric': [metric for _, metrics in ratios.items() for metric in metrics.keys()],
        'Value': [value for _, metrics in ratios.items() for value in metrics.values()]
    })
    
    return ratios_df

def display_financial_statements(ticker):
    """Display all financial statements in a tabbed interface."""
    st.subheader("Financial Statements Analysis")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Income Statement","Balance Sheet", "Cash Flow", "Financial Ratios"])
    
    with tab1:
        st.write("### Income Statement")
        try:
            income_stmt, formatted_income_stmt = get_income_statement(ticker)
            if not income_stmt.empty:
                # Apply color styling
                st.dataframe(
                    formatted_income_stmt.style.apply(lambda x: [get_color_style(v) for v in income_stmt[x.name]], axis=0),
                    use_container_width=True
                )
            else:
                st.warning("No Income Statement data available")
        except Exception as e:
            st.error(f"Error loading income statement sheet: {str(e)}")

    with tab2:
        st.write("### Balance Sheet")
        try:
            bs, formatted_bs = get_balance_sheet(ticker)
            if not bs.empty:
                # Apply color styling
                st.dataframe(
                    formatted_bs.style.apply(lambda x: [get_color_style(v) for v in bs[x.name]], axis=0),
                    use_container_width=True
                )
            else:
                st.warning("No balance sheet data available")
        except Exception as e:
            st.error(f"Error loading balance sheet: {str(e)}")
    
    with tab3:
        st.write("### Cash Flow Statement")
        try:
            cf, formatted_cf = get_cash_flow(ticker)
            if not cf.empty:
                # Apply color styling
                st.dataframe(
                    formatted_cf.style.apply(lambda x: [get_color_style(v) for v in cf[x.name]], axis=0),
                    use_container_width=True
                )
            else:
                st.warning("No cash flow data available")
        except Exception as e:
            st.error(f"Error loading cash flow statement: {str(e)}")
    
    with tab4:
        st.write("### Financial Ratios")
        try:
            ratios_df = get_financial_ratios(ticker)
            if not ratios_df.empty:
                # Format and display ratios
                st.dataframe(
                    ratios_df.style.apply(lambda x: ['color: green' if v > 0 else 'color: red' if v < 0 else 'color: black' for v in x], 
                    subset=['Value']),
                    use_container_width=True
                )
            else:
                st.warning("No ratio data available")
        except Exception as e:
            st.error(f"Error calculating ratios: {str(e)}")
