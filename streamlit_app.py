import altair as alt
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from stock_analysis import get_stock_info, compare_stocks
from valuation import calculate_dtf_valuation, get_valuation_points
from financial_statements import display_financial_statements, get_color_style
from visualization import create_metrics_pie_chart
from dtf import calculate_advanced_dcf, calculate_wacc, get_risk_free_rate, get_industry_beta

# Show the page title and description.
st.set_page_config(page_title="Fundamental analysis", page_icon="&star;", layout="wide")
st.title("&star; Fundamental analysis Platform")
st.write(
    """
    Test demo app for fundamental analysis. WIP (Work in progress) \n
    Used for educational purposes only
    """
)

# Function to get stock data
# @st.cache_data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    return stock

stock_info={}
stock={}
if 'set_ticker' not in st.session_state:
    st.session_state.set_ticker = False

if 'stock' not in st.session_state:
    st.session_state.stock = {}

 # Sidebar for input
with st.sidebar:
    st.header("Stock Selection")
    ticker = st.text_input("Enter Stock Ticker:", value="").upper()

    if st.button("Analyze Stock"):
        st.session_state.set_ticker=True
        try:
            with st.spinner('Fetching stock data...'):
                # stock = yf.Ticker(ticker)
                stock = get_stock_data(ticker)
                st.session_state.stock=stock
                info = stock.info
                print(info)
                # Store analysis data for export
            stock_info = get_stock_info(stock)
            valuation_points = get_valuation_points(stock)

        except Exception as e:
            print(e)
            st.error(f"Error analyzing stock: {str(e)}")

if st.session_state.set_ticker:
# Main content area with two columns
    with st.container():
        stock = st.session_state.stock
        st.subheader("Basic Stock Information")
        info_df = pd.DataFrame(list(stock_info.items()), columns=["Metric", "Value"])
        st.dataframe(info_df, use_container_width=True, hide_index=True)

        # Financial Statements Section
        st.subheader("Financial Statements Analysis")
        display_financial_statements(stock)
        
        st.subheader("Advanced DCF Valuation with WACC")
        risk_free_rate = get_risk_free_rate()
        st.write(f"Current Risk-Free Rate (10Y Treasury): {risk_free_rate:.2%}")

        short_term_growth = st.slider("Short-term Growth Rate (5 years)", 0.0, 0.3, 0.1)
        long_term_growth = st.slider("Long-term Growth Rate", 0.0, 0.1, 0.02)
        market_risk_premium = st.slider("Market Risk Premium", 0.04, 0.08, 0.06)
        
        wacc, adjusted_beta = calculate_wacc(stock, risk_free_rate, market_risk_premium)
        st.write(f"Adjusted Beta (Company + Industry): {adjusted_beta:.2f}")
        st.write(f"Calculated WACC: {wacc:.2%}")
        
        fair_price, projected_fcfs, wacc = calculate_advanced_dcf(stock, short_term_growth, 
                                                                long_term_growth, wacc)
    
        if fair_price:
            st.write(f"Current Price: ${stock.info['currentPrice']:.2f}")
            # st.write(f"Potential Upside/Downside: {((fair_price/stock.info['currentPrice'])-1)*100:.2f}%")
            st.metric("Estimated Fair Value (DTF)", f"${fair_price:.2f}", f"{((fair_price/stock.info['currentPrice'])-1)*100:.2f}%")
           
            fig_dcf = go.Figure()
            fig_dcf.add_trace(go.Scatter(x=list(range(1, 11)), y=projected_fcfs, 
                                       mode='lines+markers', name='Projected FCF'))
            fig_dcf.update_layout(title="Projected Free Cash Flows (10 Years)", 
                                xaxis_title="Year", yaxis_title="FCF ($)")
            st.plotly_chart(fig_dcf)
        # try:
        #     dtf_value = calculate_dtf_valuation(stock)
        #     current_price = info['currentPrice']
        #     difference = ((dtf_value/current_price)-1)*100
        #     st.metric("Fair Value (DTF)", f"${dtf_value:.2f}", f"{difference:.1f}% from current price")

        # # Add DTF Model Explanation
        #     with st.expander("📊 Understanding DTF Valuation Model - Work In Progress"):
        #         st.markdown("""
        #         ### Discounted Cash Flow (DTF) Valuation Model

        #         The DTF model calculates a stock's intrinsic value based on projected future cash flows. Here's how we calculate it:

        #         #### 1. Initial Data Points
        #         - Free Cash Flow (FCF): Current free cash flow
        #         - Growth Rate: Company's earnings growth rate (default: 10% if unavailable)
        #         - Discount Rate: 10% (industry standard for equity investments)

        #         #### 2. Projection Steps
        #         1. **5-Year Cash Flow Projection**
        #             - Year 1-5: FCF × (1 + growth_rate)^year

        #         2. **Terminal Value Calculation**
        #             - Using 3% perpetual growth rate
        #             - Formula: Final Year FCF × (1 + 0.03) / (discount_rate - 0.03)

        #         3. **Present Value Calculation**
        #             - Discounts all future cash flows to present value
        #             - Formula: CF / (1 + discount_rate)^year

        #         4. **Per Share Value**
        #             - Total present value ÷ Shares outstanding

        #         #### Key Assumptions
        #             - Stable growth rate
        #             - Consistent profit margins
        #             - No major market disruptions

        #          The model provides a theoretical fair value that can be compared with current market price.
        #     """)
        # except Exception as e:
        #     st.error(f"Could not calculate DTF valuation: {str(e)}")

        # # Visualization Section
        # st.subheader("Financial Metrics Visualization")
        # try:
        #     metrics_fig = create_metrics_pie_chart(stock)
        #     st.plotly_chart(metrics_fig, use_container_width=True)
        # except Exception as e:
        #     st.error(f"Could not create visualization: {str(e)}")
else:
    with st.empty():
        st.subheader("Select a ticker for informations..")
    # with st.container():
        # st.subheader("Basic Stock Information")
        # st.subheader("Financial Statements Analysis")
        # st.subheader("Current Valuation")
        

# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
# @st.cache_data
# def load_data():
#     df = pd.read_csv("data/movies_genres_summary.csv")
#     return df


# df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
# genres = st.multiselect(
#     "Genres",
#     df.genre.unique(),
#     ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
# )

# Show a slider widget with the years using `st.slider`.
# years = st.slider("Years", 1986, 2006, (2000, 2016))

# # Filter the dataframe based on the widget input and reshape it.
# df_filtered = df[(df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))]
# df_reshaped = df_filtered.pivot_table(
#     index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
# )
# df_reshaped = df_reshaped.sort_values(by="year", ascending=False)


# Display the data as a table using `st.dataframe`.
# st.dataframe(
#     df_reshaped,
#     use_container_width=True,
#     column_config={"year": st.column_config.TextColumn("Year")},
# )

# # Display the data as an Altair chart using `st.altair_chart`.
# df_chart = pd.melt(
#     df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
# )
# chart = (
#     alt.Chart(df_chart)
#     .mark_line()
#     .encode(
#         x=alt.X("year:N", title="Year"),
#         y=alt.Y("gross:Q", title="Gross earnings ($)"),
#         color="genre:N",
#     )
#     .properties(height=320)
# )
# st.altair_chart(chart, use_container_width=True)
