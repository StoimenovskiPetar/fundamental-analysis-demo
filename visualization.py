import plotly.graph_objects as go

def create_metrics_pie_chart(stock):
    """Create pie charts for key financial metrics."""
    info = stock.info
    
    # Financial metrics for pie chart
    revenue = info.get('totalRevenue', 0)
    costs = revenue - info.get('grossProfits', 0)
    operating_income = info.get('operatingIncome', 0)
    net_income = info.get('netIncomeToCommon', 0)

    print(costs)
    
    # Create pie chart
    labels = ['Costs', 'Operating Income', 'Net Income']
    values = [costs, operating_income - net_income, net_income]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        textinfo='label+percent',
        marker_colors=['#ff9999', '#66b3ff', '#99ff99']
    )])
    
    fig.update_layout(
        title="Revenue Breakdown",
        annotations=[dict(text=f'Total Revenue<br>${revenue:,.0f}', 
                        x=0.5, y=0.5, font_size=12, showarrow=False)],
        showlegend=True,
        width=600,
        height=400
    )
    
    return fig
