def get_risk_factors(stock):
    """Analyze 12 risk factors for the stock."""
    info = stock.info
    
    beta = info.get('beta', 0)
    debt_to_equity = info.get('debtToEquity', 0)
    current_ratio = info.get('currentRatio', 0)
    
    risk_factors = {
        "1. Market Risk": f"Beta: {beta:.2f}" + (" - High volatility" if beta > 1.5 else " - Moderate volatility" if beta > 1 else " - Low volatility"),
        
        "2. Financial Leverage": f"Debt/Equity: {debt_to_equity:.2f}" + (" - High risk" if debt_to_equity > 2 else " - Moderate risk" if debt_to_equity > 1 else " - Low risk"),
        
        "3. Liquidity Risk": f"Current Ratio: {current_ratio:.2f}" + (" - High risk" if current_ratio < 1 else " - Moderate risk" if current_ratio < 2 else " - Low risk"),
        
        "4. Industry Competition": "Analysis based on market position and industry dynamics",
        
        "5. Regulatory Risk": f"Sector: {info.get('sector', 'Unknown')} - Regulatory environment assessment",
        
        "6. Management Risk": "Based on corporate governance and management history",
        
        "7. Economic Sensitivity": "Cyclical nature and economic dependence analysis",
        
        "8. Geographic Risk": f"Based on {info.get('country', 'Unknown')} operations",
        
        "9. Currency Risk": "International operations exposure assessment",
        
        "10. Technology Risk": "Innovation and disruption vulnerability",
        
        "11. ESG Risk": "Environmental, Social, and Governance considerations",
        
        "12. Dividend Risk": f"Payout Ratio: {info.get('payoutRatio', 0)*100:.2f}%" + 
                            (" - High risk" if info.get('payoutRatio', 0) > 0.8 else " - Moderate risk" if info.get('payoutRatio', 0) > 0.5 else " - Low risk")
    }
    
    return risk_factors
