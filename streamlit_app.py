import altair as alt
import pandas as pd
import streamlit as st
import yfinance as yf
from stock_analysis import get_stock_info, compare_stocks
from valuation import calculate_dtf_valuation, get_valuation_points

# Show the page title and description.
st.set_page_config(page_title="Fundamental analysis", page_icon="&star;", layout="wide")
st.title("&star; Fundamental analysis Platform")
st.write(
    """
    Test demo app for fundamental analysis
    """
)
stock_info={}

 # Sidebar for input
with st.sidebar:
    st.header("Stock Selection")
    ticker = st.text_input("Enter Stock Ticker:", value="AAPL").upper()

    if st.button("Analyze Stock"):
        try:
            with st.spinner('Fetching stock data...'):
                stock = yf.Ticker(ticker)
                info = stock.info
                print(info)

                # Store analysis data for export
            stock_info = get_stock_info(stock)
            valuation_points = get_valuation_points(stock)

        except Exception as e:
            st.error(f"Error analyzing stock: {str(e)}")

# Main content area with two columns
with st.container():  
    st.subheader("Basic Stock Information")
    info_df = pd.DataFrame(list(stock_info.items()), columns=["Metric", "Value"])
    st.table(info_df)


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
