def calculate_dtf_valuation(stock):
    """Calculate Discounted Cash Flow (DTF) valuation with comprehensive financial data."""
    info = stock.info

    # Get comprehensive financial data
    free_cash_flow = info.get('freeCashflow', 0)
    operating_cash_flow = info.get('operatingCashflow', 0)
    historical_growth = info.get('earningsGrowth', 0)
    profit_margin = info.get('profitMargins', 0)

    # Use the better of operating cash flow or free cash flow
    base_cash_flow = max(free_cash_flow, operating_cash_flow)

    # Adjust growth rate based on historical performance and margins
    base_growth_rate = historical_growth if historical_growth > 0 else 0.1
    adjusted_growth_rate = min(base_growth_rate * (1 + profit_margin), 0.15)  # Cap at 15%

    # Risk-adjusted discount rate based on company metrics
    base_discount_rate = 0.1  # 10% base rate
    risk_premium = 0.02 if info.get('beta', 1) > 1.5 else 0  # Add premium for high beta
    debt_premium = 0.01 if info.get('debtToEquity', 0) > 2 else 0  # Add premium for high debt
    discount_rate = base_discount_rate + risk_premium + debt_premium

    # Project cash flows for 5 years with adjusted growth
    projected_cf = []
    for i in range(1, 6):
        cf = base_cash_flow * (1 + adjusted_growth_rate)**i
        projected_cf.append(cf)

    # Calculate terminal value with conservative growth
    terminal_growth = min(0.03, adjusted_growth_rate / 2)  # More conservative terminal growth
    terminal_value = (projected_cf[-1] * (1 + terminal_growth)) / (discount_rate - terminal_growth)

    # Calculate present value of projected cash flows
    present_value = 0
    for i, cf in enumerate(projected_cf):
        present_value += cf / (1 + discount_rate)**(i+1)

    # Add present value of terminal value
    present_value += terminal_value / (1 + discount_rate)**5

    # Calculate per share value with margin of safety
    shares_outstanding = info.get('sharesOutstanding', 1)
    fair_value = present_value / shares_outstanding

    # Apply a margin of safety based on company quality metrics
    quality_score = (
        (1 if info.get('returnOnEquity', 0) > 0.15 else 0) +  # Good ROE
        (1 if info.get('currentRatio', 0) > 1.5 else 0) +     # Good liquidity
        (1 if info.get('debtToEquity', 0) < 1 else 0) +       # Low debt
        (1 if profit_margin > 0.1 else 0)                      # Good margins
    ) / 4.0

    margin_of_safety = 0.7 + (0.3 * quality_score)  # 70-100% based on quality

    return fair_value * margin_of_safety

def get_valuation_points(stock):
    """Get 8-point valuation analysis with enhanced financial metrics."""
    info = stock.info

    # Calculate key growth metrics
    revenue_growth = info.get('revenueGrowth', 0) * 100
    earnings_growth = info.get('earningsGrowth', 0) * 100

    # Get industry averages (example values, could be fetched from sector data)
    industry_pe = 20  # Example industry P/E
    industry_pb = 2.5  # Example industry P/B

    return {
        "1. Price to Earnings": f"P/E ratio is {info.get('trailingPE', 0):.2f} vs industry average of {industry_pe}",
        "2. Price to Book": f"P/B ratio is {info.get('priceToBook', 0):.2f} vs industry average of {industry_pb}",
        "3. Debt Levels": (f"Debt to Equity ratio is {info.get('debtToEquity', 0):.2f} "
                          f"{'(High Risk)' if info.get('debtToEquity', 0) > 2 else '(Moderate Risk)' if info.get('debtToEquity', 0) > 1 else '(Low Risk)'}"),
        "4. Profit Margins": (f"Net profit margin is {info.get('profitMargins', 0)*100:.2f}% "
                             f"{'(Strong)' if info.get('profitMargins', 0) > 0.2 else '(Average)' if info.get('profitMargins', 0) > 0.1 else '(Weak)'}"),
        "5. Growth Metrics": f"Revenue growth: {revenue_growth:.1f}%, Earnings growth: {earnings_growth:.1f}%",
        "6. Cash Flow Quality": (f"Operating cash flow is {format_currency(info.get('operatingCashflow', 0))} vs "
                                f"Net Income of {format_currency(info.get('netIncome', 0))}"),
        "7. Returns": f"ROE: {info.get('returnOnEquity', 0)*100:.1f}%, ROA: {info.get('returnOnAssets', 0)*100:.1f}%",
        "8. Financial Health": f"Current Ratio: {info.get('currentRatio', 0):.2f}, Quick Ratio: {info.get('quickRatio', 0):.2f}"
    }

def format_currency(value):
    """Format large currency values with B/M suffix."""
    if abs(value) >= 1e9:
        return f"${value/1e9:.1f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.1f}M"
    else:
        return f"${value:.2f}"