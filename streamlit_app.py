import altair as alt
import pandas as pd
import streamlit as st
import yfinance as yf
from stock_analysis import get_stock_info, compare_stocks
from valuation import calculate_dtf_valuation, get_valuation_points
from financial_statements import display_financial_statements
from visualization import create_metrics_pie_chart

# Show the page title and description.
st.set_page_config(page_title="Fundamental analysis", page_icon="&star;", layout="wide")
st.title("&star; Fundamental analysis Platform")
st.write(
    """
    Test demo app for fundamental analysis. WIP (Work in progress) \n
    Used for educational purposes only
    """
)
stock_info={}
stock={}
if 'set_ticker' not in st.session_state:
    st.session_state.set_ticker = False

 # Sidebar for input
with st.sidebar:
    st.header("Stock Selection")
    ticker = st.text_input("Enter Stock Ticker:", value="").upper()

    if st.button("Analyze Stock"):
        st.session_state.set_ticker=True
        try:
            with st.spinner('Fetching stock data...'):
                stock = yf.Ticker(ticker)
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
        st.subheader("Basic Stock Information")
        info_df = pd.DataFrame(list(stock_info.items()), columns=["Metric", "Value"])
        st.dataframe(info_df, use_container_width=True, hide_index=True)

        # Financial Statements Section
        st.subheader("Financial Statements Analysis")
        display_financial_statements(stock)
        
        st.subheader("Current Valuation")
        try:
            dtf_value = calculate_dtf_valuation(stock)
            current_price = info['currentPrice']
            difference = ((dtf_value/current_price)-1)*100
            st.metric("Fair Value (DTF)", f"${dtf_value:.2f}", f"{difference:.1f}% from current price")

        # Add DTF Model Explanation
            with st.expander("📊 Understanding DTF Valuation Model - Work In Progress"):
                st.markdown("""
                ### Discounted Cash Flow (DTF) Valuation Model

                The DTF model calculates a stock's intrinsic value based on projected future cash flows. Here's how we calculate it:

                #### 1. Initial Data Points
                - Free Cash Flow (FCF): Current free cash flow
                - Growth Rate: Company's earnings growth rate (default: 10% if unavailable)
                - Discount Rate: 10% (industry standard for equity investments)

                #### 2. Projection Steps
                1. **5-Year Cash Flow Projection**
                    - Year 1-5: FCF × (1 + growth_rate)^year

                2. **Terminal Value Calculation**
                    - Using 3% perpetual growth rate
                    - Formula: Final Year FCF × (1 + 0.03) / (discount_rate - 0.03)

                3. **Present Value Calculation**
                    - Discounts all future cash flows to present value
                    - Formula: CF / (1 + discount_rate)^year

                4. **Per Share Value**
                    - Total present value ÷ Shares outstanding

                #### Key Assumptions
                    - Stable growth rate
                    - Consistent profit margins
                    - No major market disruptions

                 The model provides a theoretical fair value that can be compared with current market price.
            """)
        except Exception as e:
            st.error(f"Could not calculate DTF valuation: {str(e)}")

        # Visualization Section
        st.subheader("Financial Metrics Visualization")
        try:
            metrics_fig = create_metrics_pie_chart(stock)
            st.plotly_chart(metrics_fig, use_container_width=True)
        except Exception as e:
            st.error(f"Could not create visualization: {str(e)}")
else:
    with st.container():
        st.subheader("Basic Stock Information")
        st.subheader("Financial Statements Analysis")
        st.subheader("Current Valuation")
        

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
