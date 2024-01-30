from flask import Flask, render_template,request,jsonify, redirect, url_for
from jugaad_data.nse import stock_df
from dateutil.relativedelta import relativedelta
import pandas as pd
import cufflinks as cf
import yfinance as yf
from datetime import date,datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random,requests,time
app = Flask(__name__)

# Download data and set up cufflinks configuration
cf.set_config_file(theme='pearl', world_readable=False)
cf.go_offline()

current_stock_symbol="SBIN"
current_stock_series="EQ"
current_plot_type="Candle"
current_range="5 years"
current_filter_status=0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot1')
def plot1():
    single_stock = yf.download('MSFT', start="2020-05-27", end="2021-05-27")
    chart_data = single_stock['Adj Close'].iplot(asFigure=True, title='MSFT Adjusted Close', colors=['red'])
    return render_template('plot.html', chart_data=chart_data)

# def plot_stock_candlestick(symbol, series, start_date, end_date):
#     stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
#     stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
#     stock_data.set_index('DATE', inplace=True)
    
#     chart_data = stock_data.iplot(kind='candle', asFigure=True, gridcolor='rgba(0,0,0,0)', zerolinecolor='rgba(0,0,0,0)')
    
#     chart_data.update_layout(
#         paper_bgcolor='black',
#         plot_bgcolor='black',
#         xaxis=dict(
#             title_font=dict(color='white'),
#             tickfont=dict(color='white')
#         )
#     )
    
#     chart_data.update_yaxes(title_text='Stock Price', title_font=dict(color='white'), tickfont=dict(color='white'))
    
#     return chart_data


# def plot_stock_candlestick(symbol, series, start_date, end_date):
#     stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
#     stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
#     stock_data.set_index('DATE', inplace=True)
    
#     chart_data = go.Figure(go.Candlestick(x=stock_data.index,
#                     open=stock_data['OPEN'], high=stock_data['HIGH'],
#                     low=stock_data['LOW'], close=stock_data['CLOSE']))
    
#     chart_data.update_layout(
#         paper_bgcolor='black',
#         plot_bgcolor='black',
#         xaxis=dict(
#             title_font=dict(color='white'),
#             tickfont=dict(color='white')
#         )
#     )
    
#     chart_data.update_yaxes(title_text='Stock Price', title_font=dict(color='white'), tickfont=dict(color='white'))
    
#     # Change candlestick color here
#     chart_data.data[0].increasing.fillcolor = 'lawngreen'  # Change to desired color
#     chart_data.data[0].increasing.line.color = 'lawngreen'  # Change to desired color
#     chart_data.data[0].decreasing.fillcolor = 'red'  # Change to desired color
#     chart_data.data[0].decreasing.line.color = 'red'  # Change to desired color
    
#     return chart_data

def datetotimestamp(date):
    time_tuple = date.timetuple()
    timestamp = round(time.mktime(time_tuple))
    return timestamp

def timestamptodate(timestamp):
    return datetime.fromtimestamp(timestamp)


def fetch_data(symbol):
    start = datetotimestamp(datetime.now() - relativedelta(days=1))
    end = datetotimestamp(datetime.now())
    url = 'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol=' + symbol + '&resolution=1&from='+ str(start) +'&to='+ str(end) +'&countback=329&currencyCode=INR'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print('Failed to retrieve content. Status code:', response.status_code)
        return None
    
    resp = response.json()
    data = pd.DataFrame(resp)
    
    date = []
    for dt in data['t']:
        date.append({'Date': timestamptodate(dt)})
    dt = pd.DataFrame(date)
    intraday_data = pd.concat([dt, data['o'], data['h'], data['l'], data['c'], data['v']], axis=1).rename(columns={'o':'OPEN', 'h':'HIGH', 'l':'LOW', 'c':'CLOSE', 'v':'VOLUME'})
    
    return intraday_data.set_index('Date')  # Setting Date as index for cufflinks compatibility

def Loading():
    # create a sample dataframe
    df = pd.DataFrame({'x': [], 'y': []})

    # create a plotly figure object
    fig = df.iplot(kind='scatter', x='x', y='y', mode='lines+markers', asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')

    # add an annotation with the word 'welcome' in bold and red color
    fig.add_annotation(
        x=3, y=20,
        text="<b>Loading...</b>",
        showarrow=False,
        font=dict(family="Arial",size=100, color='red')
    )
        
    fig.update_layout(
            paper_bgcolor='rgba(34, 46, 50, 0.8)',
            plot_bgcolor='rgba(34, 46, 50, 0.5)',
            xaxis=dict(
                title_font=dict(color='white'),
                tickfont=dict(color='white')
            )
        )
        
    fig.update_yaxes(title_text='Stock Price', title_font=dict(color='white'), tickfont=dict(color='white'))

    return fig

def Welcome():
    # create a sample dataframe
    df = pd.DataFrame({'x': [], 'y': []})

    # create a plotly figure object
    fig = df.iplot(kind='scatter', x='x', y='y', mode='lines+markers', asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')

    # add an annotation with the word 'welcome' in bold and red color
    fig.add_annotation(
        x=3, y=20,
        text="<b>Welcome!</b>",
        showarrow=False,
        font=dict(family="Arial",size=100, color='red')
    )
        
    fig.update_layout(
            paper_bgcolor='rgba(34, 46, 50, 0.8)',
            plot_bgcolor='rgba(34, 46, 50, 0.5)',
            xaxis=dict(
                title_font=dict(color='white'),
                tickfont=dict(color='white')
            )
        )
        
    fig.update_yaxes(title_text='Stock Price', title_font=dict(color='white'), tickfont=dict(color='white'))

    return fig

def plot_stock_candlestick(symbol, series, start_date, end_date,f,r):
    if(r=="1 Week"):
        symbol=symbol+".NS"
        stock=yf.Ticker(symbol)
        stock_data=stock.history(period='1wk')
        #stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        #stock_data.set_index('Date', inplace=True)
    elif(r=="1 Day"):
        stock_data=fetch_data(symbol)
    else:
        stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
        stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
        stock_data.set_index('DATE', inplace=True)
    if(f==1):
        stock_data = cf.QuantFig(stock_data, title='Stock Analysis', legend='top', name=symbol)
        stock_data.add_sma([50, 200], width=2, color=['green', 'lightgreen'], legendgroup=True)
        stock_data.add_bollinger_bands()
        stock_data.add_ema()
        stock_data.add_dmi()
        stock_data.add_volume()
        stock_data.add_rsi()
        chart_data = stock_data.iplot(kind='candle', asFigure=True,layout=dict(height=1500))
        chart_data.update_layout(
                      xaxis_rangeslider_visible=False,
                      paper_bgcolor='rgba(34, 46, 50, 0.8)',
                      plot_bgcolor='rgba(34, 46, 50, 0.5)',
                      xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white')),
                      legend=dict(title='Stock Symbols', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),legend_font_color='red')
        chart_data.update_yaxes(title_font=dict(color='white'),showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white') )
    else:
        chart_data = stock_data.iplot(kind='candle', asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        chart_data.update_layout(
            paper_bgcolor='rgba(34, 46, 50, 0.8)',
            plot_bgcolor='rgba(34, 46, 50, 0.5)',
            xaxis=dict(
                title_font=dict(color='white'),
                tickfont=dict(color='white')
            )
        )
        chart_data.update_yaxes(title_text='Stock Price', title_font=dict(color='white'), tickfont=dict(color='white'))
        chart_data.data[0].increasing.fillcolor = 'rgba(0, 255, 0, 0.3)'  # Green with glowing effect
        chart_data.data[0].increasing.line.color = 'lawngreen'  # Green with glowing effect
        chart_data.data[0].decreasing.fillcolor = 'rgba(255, 0, 0, 0.3)'  # Red with glowing effect
        chart_data.data[0].decreasing.line.color = 'rgba(255, 0, 0 ,0.7)'  # Red with glowing effect    
    
    return chart_data

def plot_stock_area(symbol, series, start_date, end_date,f,r):
    if(r=="1 Week"):
        symbol=symbol+".NS"
        stock=yf.Ticker(symbol)
        stock_data=stock.history(period='1wk')
        fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
        chart_data = stock_data['Close'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
    elif(r=="1 Day"):
        stock_data=fetch_data(symbol)
        fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
        chart_data = stock_data['CLOSE'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
    else:        
        stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
        stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
        stock_data.set_index('DATE', inplace=True)
        fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
        if(r!="1 Month"):
            chart_data = stock_data['CLOSE'].iplot(fill=True,color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        else:
            chart_data = stock_data['CLOSE'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
    if(f==1):
        return plot_stock_candlestick(symbol,series,start_date,end_date,f,r)
    chart_data.update_layout(
        paper_bgcolor='rgba(34, 46, 50, 0.8)',
        plot_bgcolor='rgba(34, 46, 50, 0.5)',
        xaxis=dict(
            title_font=dict(color='white'),
            tickfont=dict(color='white')
        )
    )
    
    chart_data.update_yaxes(title_text='Stock Price', title_font=dict(color='white'), tickfont=dict(color='white'))
    
    return chart_data



def reset_global_variables():
    global current_stock_symbol, current_stock_series, current_plot_type, current_range,current_stock_list,current_series_list,length,current_multi_plot_type,current_merged_status,current_multi_range,current_filter_status,current_multi_filter_status
    current_stock_symbol = "SBIN"
    current_stock_series = "EQ"
    current_plot_type = "Candle"
    current_range = "5 years"
    current_stock_list=[]
    current_series_list=[]
    length=0
    current_multi_plot_type="Candle"
    current_merged_status="No"
    current_multi_range="5 years"
    current_filter_status=0
    current_multi_filter_status=0


@app.route('/candlestick',methods=['GET', 'POST'])
def candlestick():
    if request.method == 'POST':
        reset_global_variables()
        return 'Global variables reset successfully.'
    
    chart_data = Welcome()
    Loading_data=Loading()
    
    return render_template('dashboard1.html', chart_data=chart_data,Loading_data=Loading_data)


@app.route('/process', methods=['POST']) 
def process():
    global current_stock_symbol
    global current_stock_series
    global current_range
    global current_plot_type
    global current_filter_status
    data = request.get_json()
    stock_symbol = data['currsymbol']
    stock_series = data['currseries']
    current_stock_symbol=stock_symbol
    current_stock_series=stock_series
    current_range="5 years"
    current_plot_type="Candle"
    current_filter_status=0
    today = date.today()
    start_date = today - relativedelta(years=5)   
    chart_data = plot_stock_candlestick(symbol=current_stock_symbol, series=current_stock_series, start_date=start_date, end_date=today,f=current_filter_status,r=current_range) 
    chart_data_json = chart_data.to_json()
    return chart_data_json


@app.route('/processrange', methods=['POST']) 
def processrange():
    global current_stock_symbol
    global current_stock_series
    global current_range
    global current_plot_type 
    global current_filter_status   
    data = request.get_json()
    diffintime=data['currRange']
    current_range=diffintime
    today = date.today()
    if(current_range=="5 years"):
        start_date = today - relativedelta(years=5)   
    elif(current_range=="1 year"):
        start_date = today - relativedelta(years=1)
    elif(current_range=="1 Month"):
        start_date = today - relativedelta(months=1)#################
    elif(current_range=="1 Week"):
        start_date = today - relativedelta(years=1)##################
    elif(current_range=="1 Day"):
        start_date = today - relativedelta(years=1)    ###########    
    elif(current_range=="Overall"):
        start_date = today - relativedelta(years=50)   ##################                   
    if(current_plot_type=="Candle"):
        chart_data = plot_stock_candlestick(symbol=current_stock_symbol, series=current_stock_series, start_date=start_date, end_date=today, f=current_filter_status,r=current_range) 
    else:
        chart_data = plot_stock_area(symbol=current_stock_symbol, series=current_stock_series, start_date=start_date, end_date=today, f=current_filter_status,r=current_range) 
    chart_data_json = chart_data.to_json()
    return chart_data_json    


@app.route('/processplottype', methods=['POST']) 
def processplottype():
    global current_stock_symbol
    global current_stock_series
    global current_range
    global current_plot_type  
    global current_filter_status  
    data = request.get_json()
    plottype=data['currPlot']
    current_plot_type=plottype
    today = date.today()
    if(current_range=="5 years"):
        start_date = today - relativedelta(years=5)   
    elif(current_range=="1 year"):
        start_date = today - relativedelta(years=1)
    elif(current_range=="1 Month"):
        start_date = today - relativedelta(months=1)#################
    elif(current_range=="1 Week"):
        start_date = today - relativedelta(years=1)##################
    elif(current_range=="1 Day"):
        start_date = today - relativedelta(years=1)    ###########    
    elif(current_range=="Overall"):
        start_date = today - relativedelta(years=50)   ##################                   
    if(current_plot_type=="Candle"):
        chart_data = plot_stock_candlestick(symbol=current_stock_symbol, series=current_stock_series, start_date=start_date, end_date=today, f=current_filter_status,r=current_range) 
    else:
        chart_data = plot_stock_area(symbol=current_stock_symbol, series=current_stock_series, start_date=start_date, end_date=today, f=current_filter_status,r=current_range) 
    chart_data_json = chart_data.to_json()
    return chart_data_json    


@app.route('/processfilter', methods=['POST']) 
def processfilter():
    global current_stock_symbol
    global current_stock_series
    global current_range
    global current_plot_type    
    global current_filter_status
    if(current_filter_status==1):
        current_filter_status=0
    else:
        current_filter_status=1
    today = date.today()
    if(current_range=="5 years"):
        start_date = today - relativedelta(years=5)   
    elif(current_range=="1 year"):
        start_date = today - relativedelta(years=1)
    elif(current_range=="1 Month"):
        start_date = today - relativedelta(months=1)#################
    elif(current_range=="1 Week"):
        start_date = today - relativedelta(years=1)##################
    elif(current_range=="1 Day"):
        start_date = today - relativedelta(years=1)    ###########    
    elif(current_range=="Overall"):
        start_date = today - relativedelta(years=50)   ##################                   
    if(current_plot_type=="Candle"):
        chart_data = plot_stock_candlestick(symbol=current_stock_symbol, series=current_stock_series, start_date=start_date, end_date=today, f=current_filter_status,r=current_range) 
    else:
        chart_data = plot_stock_area(symbol=current_stock_symbol, series=current_stock_series, start_date=start_date, end_date=today, f=current_filter_status,r=current_range) 
    chart_data_json = chart_data.to_json()
    return chart_data_json    

def plot_4_stock_candlestick(symbols, series_list, start_date, end_date,f,r):
    fig = make_subplots(rows=2, cols=2, subplot_titles=[f"<b><span style='color:red;'>{symbol}</span></b>" for symbol in symbols])

    for i, (symbol, series) in enumerate(zip(symbols, series_list), 1):
        
        # stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
        # stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
        # stock_data.set_index('DATE', inplace=True)

        # chart_data = stock_data.iplot(kind='candle', asFigure=True)
 
        # # Change candlestick colors with glowing effect
        # chart_data.data[0].increasing.fillcolor = 'rgba(0, 255, 0, 0.3)'  # Green with glowing effect
        # chart_data.data[0].increasing.line.color = 'lawngreen'  # Green with glowing effect
        # chart_data.data[0].decreasing.fillcolor = 'rgba(255, 0, 0, 0.3)'  # Red with glowing effect
        # chart_data.data[0].decreasing.line.color = 'rgba(255, 0, 0 ,0.7)'  # Red with glowing effect     

        if(r=="1 Week"):
            symbol=symbol+".NS"
            stock=yf.Ticker(symbol)
            stock_data=stock.history(period='1wk')
            #stock_data['Date'] = pd.to_datetime(stock_data['Date'])
            #stock_data.set_index('Date', inplace=True)
        elif(r=="1 Day"):
            stock_data=fetch_data(symbol)
        else:
            stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
            stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
            stock_data.set_index('DATE', inplace=True)
        if(f==1):
            stock_data = cf.QuantFig(stock_data, title='Stock Analysis', legend='top', name=symbol)
            stock_data.add_sma([50, 200], width=2, color=['green', 'lightgreen'], legendgroup=True)
            stock_data.add_bollinger_bands()
            stock_data.add_ema()
            stock_data.add_dmi()
            stock_data.add_volume()
            stock_data.add_rsi()
            chart_data = stock_data.iplot(kind='candle', asFigure=True,layout=dict(height=1500))
            chart_data.update_layout(
                        xaxis_rangeslider_visible=False,
                        paper_bgcolor='rgba(34, 46, 50, 0.8)',
                        plot_bgcolor='rgba(34, 46, 50, 0.5)',
                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white')),
                        legend=dict(title='Stock Symbols', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),legend_font_color='red')
            chart_data.update_yaxes(title_font=dict(color='white'),showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white') )
        else:
            chart_data = stock_data.iplot(kind='candle', asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
            chart_data.update_layout(
                paper_bgcolor='rgba(34, 46, 50, 0.8)',
                plot_bgcolor='rgba(34, 46, 50, 0.5)',
                xaxis=dict(
                    title_font=dict(color='white'),
                    tickfont=dict(color='white')
                )
            )
            chart_data.update_yaxes(title_text='Stock Price', title_font=dict(color='white'), tickfont=dict(color='white'))
            chart_data.data[0].increasing.fillcolor = 'rgba(0, 255, 0, 0.3)'  # Green with glowing effect
            chart_data.data[0].increasing.line.color = 'lawngreen'  # Green with glowing effect
            chart_data.data[0].decreasing.fillcolor = 'rgba(255, 0, 0, 0.3)'  # Red with glowing effect
            chart_data.data[0].decreasing.line.color = 'rgba(255, 0, 0 ,0.7)'  # Red with glowing effect               

        # Update layout directly on the figure object
        fig.append_trace(chart_data.data[0], row=(i+1)//2, col=(i+1)%2 + 1)
        fig.update_layout(
            paper_bgcolor='rgba(34, 46, 50, 0.8)',
            plot_bgcolor='rgba(34, 46, 50, 0.5)'
        )


        # Remove grid and zeroline
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=(i+1)//2, col=(i+1)%2 if (i+1)%2 != 0 else 2, tickfont=dict(color='white'))
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=(i+1)//2, col=(i+1)%2 if (i+1)%2 != 0 else 2, tickfont=dict(color='white'))

        # Disable x-axis range slider
        fig.update_xaxes(rangeslider_visible=False, row=(i+1)//2, col=(i+1)%2 + 1)

    return fig

def plot_3_stock_candlestick(symbols, series_list, start_date, end_date,f,r):
    fig = make_subplots(rows=3, cols=1, subplot_titles=[f"<b><span style='color:red;'>{symbol}</span></b>" for symbol in symbols])

    for i, (symbol, series) in enumerate(zip(symbols, series_list), 1):
        # stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
        # stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
        # stock_data.set_index('DATE', inplace=True)

        # chart_data = stock_data.iplot(kind='candle', asFigure=True)


        # # Change candlestick colors with glowing effect
        # chart_data.data[0].increasing.fillcolor = 'rgba(0, 255, 0, 0.3)'  # Green with glowing effect
        # chart_data.data[0].increasing.line.color = 'lawngreen'  # Green with glowing effect
        # chart_data.data[0].decreasing.fillcolor = 'rgba(255, 0, 0, 0.3)'  # Red with glowing effect
        # chart_data.data[0].decreasing.line.color = 'rgba(255, 0, 0 ,0.7)'  # Red with glowing effect       
        if(r=="1 Week"):
            symbol=symbol+".NS"
            stock=yf.Ticker(symbol)
            stock_data=stock.history(period='1wk')
            #stock_data['Date'] = pd.to_datetime(stock_data['Date'])
            #stock_data.set_index('Date', inplace=True)
        elif(r=="1 Day"):
            stock_data=fetch_data(symbol)
        else:
            stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
            stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
            stock_data.set_index('DATE', inplace=True)
        if(f==1):
            stock_data = cf.QuantFig(stock_data, title='Stock Analysis', legend='top', name=symbol)
            stock_data.add_sma([50, 200], width=2, color=['green', 'lightgreen'], legendgroup=True)
            stock_data.add_bollinger_bands()
            stock_data.add_ema()
            stock_data.add_dmi()
            stock_data.add_volume()
            stock_data.add_rsi()
            chart_data = stock_data.iplot(kind='candle', asFigure=True,layout=dict(height=1500))
            chart_data.update_layout(
                        xaxis_rangeslider_visible=False,
                        paper_bgcolor='rgba(34, 46, 50, 0.8)',
                        plot_bgcolor='rgba(34, 46, 50, 0.5)',
                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white')),
                        legend=dict(title='Stock Symbols', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),legend_font_color='red')
            chart_data.update_yaxes(title_font=dict(color='white'),showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white') )
        else:
            chart_data = stock_data.iplot(kind='candle', asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
            chart_data.update_layout(
                paper_bgcolor='rgba(34, 46, 50, 0.8)',
                plot_bgcolor='rgba(34, 46, 50, 0.5)',
                xaxis=dict(
                    title_font=dict(color='white'),
                    tickfont=dict(color='white')
                )
            )
            chart_data.update_yaxes(title_text='Stock Price', title_font=dict(color='white'), tickfont=dict(color='white'))
            chart_data.data[0].increasing.fillcolor = 'rgba(0, 255, 0, 0.3)'  # Green with glowing effect
            chart_data.data[0].increasing.line.color = 'lawngreen'  # Green with glowing effect
            chart_data.data[0].decreasing.fillcolor = 'rgba(255, 0, 0, 0.3)'  # Red with glowing effect
            chart_data.data[0].decreasing.line.color = 'rgba(255, 0, 0 ,0.7)'  # Red with glowing effect              

        # Update layout directly on the figure object
        fig.append_trace(chart_data.data[0], row=i, col=1)
        fig.update_layout(
            paper_bgcolor='rgba(34, 46, 50, 0.8)',
            plot_bgcolor='rgba(34, 46, 50, 0.5)'
        )


        # Remove grid and zeroline
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=i, col=1, tickfont=dict(color='white'))
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=i, col=1, tickfont=dict(color='white'))

        # Disable x-axis range slider
        fig.update_xaxes(rangeslider_visible=False, row=i, col=1)

    return fig

def plot_2_stock_candlestick(symbols, series_list, start_date, end_date,f,r):
    if(f==0):
        fig = make_subplots(rows=1, cols=2, subplot_titles=[f"<b><span style='color:red;'>{symbol}</span></b>" for symbol in symbols])
    else:
        fig = make_subplots(rows=8, cols=2, subplot_titles=[f"<b><span style='color:red;'>{symbol}</span></b>" for symbol in symbols])
    for i, (symbol, series) in enumerate(zip(symbols, series_list), 1):
        # stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
        # stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
        # stock_data.set_index('DATE', inplace=True)

        # chart_data = stock_data.iplot(kind='candle', asFigure=True)

        # # Change candlestick colors with glowing effect
        # chart_data.data[0].increasing.fillcolor = 'rgba(0, 255, 0, 0.3)'  # Green with glowing effect
        # chart_data.data[0].increasing.line.color = 'lawngreen'  # Green with glowing effect
        # chart_data.data[0].decreasing.fillcolor = 'rgba(255, 0, 0, 0.3)'  # Red with glowing effect
        # chart_data.data[0].decreasing.line.color = 'rgba(255, 0, 0 ,0.7)'  # Red with glowing effect        

        if(r=="1 Week"):
            symbol=symbol+".NS"
            stock=yf.Ticker(symbol)
            stock_data=stock.history(period='1wk')
            #stock_data['Date'] = pd.to_datetime(stock_data['Date'])
            #stock_data.set_index('Date', inplace=True)
        elif(r=="1 Day"):
            stock_data=fetch_data(symbol)
        else:
            stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
            stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
            stock_data.set_index('DATE', inplace=True)
        if(f==1):
            stock_data = cf.QuantFig(stock_data, title='Stock Analysis', legend='top', name=symbol)
            stock_data.add_sma([50, 200], width=2, color=['green', 'lightgreen'], legendgroup=True)
            stock_data.add_bollinger_bands()
            stock_data.add_ema()
            stock_data.add_dmi()
            stock_data.add_volume()
            stock_data.add_rsi()
            chart_data = stock_data.iplot(kind='candle', asFigure=True)
            chart_data.update_layout(
                        
                        paper_bgcolor='rgba(34, 46, 50, 0.8)',
                        plot_bgcolor='rgba(34, 46, 50, 0.5)',
                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white')),
                        legend=dict(title='Stock Symbols', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),legend_font_color='red')
            chart_data.update_yaxes(title_font=dict(color='white'),showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white') )

            fig.append_trace(chart_data.data[0], row=2, col=i)
            fig.append_trace(chart_data.data[1], row=2, col=i)
            fig.append_trace(chart_data.data[2], row=1, col=i)
            fig.append_trace(chart_data.data[3], row=1, col=i)
            fig.append_trace(chart_data.data[4],row=2,col=i)
            fig.append_trace(chart_data.data[5],row=3,col=i)
            fig.append_trace(chart_data.data[6],row=3,col=i)
            fig.append_trace(chart_data.data[7],row=5,col=i)
            fig.append_trace(chart_data.data[8],row=5,col=i)
            fig.append_trace(chart_data.data[9],row=3,col=i) 
            fig.append_trace(chart_data.data[10],row=6,col=i)
            fig.append_trace(chart_data.data[11],row=6,col=i)
            fig.append_trace(chart_data.data[12],row=6,col=i)
            fig.append_trace(chart_data.data[13],row=1,col=i)                    

        else:
            chart_data = stock_data.iplot(kind='candle', asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
            chart_data.update_layout(
                paper_bgcolor='rgba(34, 46, 50, 0.8)',
                plot_bgcolor='rgba(34, 46, 50, 0.5)',
                xaxis=dict(
                    title_font=dict(color='white'),
                    tickfont=dict(color='white')
                )
            )
            chart_data.update_yaxes(title_text='Stock Price', title_font=dict(color='white'), tickfont=dict(color='white'))
            chart_data.data[0].increasing.fillcolor = 'rgba(0, 255, 0, 0.3)'  # Green with glowing effect
            chart_data.data[0].increasing.line.color = 'lawngreen'  # Green with glowing effect
            chart_data.data[0].decreasing.fillcolor = 'rgba(255, 0, 0, 0.3)'  # Red with glowing effect
            chart_data.data[0].decreasing.line.color = 'rgba(255, 0, 0 ,0.7)'  # Red with glowing effect      
            fig.append_trace(chart_data.data[0], row=1, col=i)
     

        # Update layout directly on the figure object
        #fig.append_trace(chart_data.data[0], row=1, col=i)

        fig.update_layout(
            paper_bgcolor='rgba(34, 46, 50, 0.8)',
            plot_bgcolor='rgba(34, 46, 50, 0.5)',
        )
        if(f==1):
            fig.update_layout(
                legend_font_color='red'
                ,height=1500
            )


        # Remove grid and zeroline
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=1, col=i, tickfont=dict(color='white'))
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=1, col=i, tickfont=dict(color='white'))

        # Disable x-axis range slider
        fig.update_xaxes(rangeslider_visible=False, row=1, col=i)


    return fig


def plot_merged_stock_candlestick(symbols, series_list, start_date, end_date,r):
    # Generate random line and fill colors for each stock
    num_stocks = len(symbols)
    line_colors = [f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})' for _ in range(num_stocks)]
    fill_colors = [f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.3)' for _ in range(num_stocks)]
    decreasing_line_colors = [f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.7)' for _ in range(num_stocks)]
    decreasing_fill_colors = [f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.3)' for _ in range(num_stocks)]

    fig = go.Figure()

    for i, (symbol, series) in enumerate(zip(symbols, series_list)):
        # stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
        # stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
        # stock_data.set_index('DATE', inplace=True)
        if(r=="1 Week"):
            symbol=symbol+".NS"
            stock=yf.Ticker(symbol)
            stock_data=stock.history(period='1wk')
            fig.add_trace(go.Candlestick(x=stock_data.index,
                                        open=stock_data['Open'],
                                        high=stock_data['High'],
                                        low=stock_data['Low'],
                                        close=stock_data['Close'],
                                        increasing_line_color=line_colors[i],
                                        decreasing_line_color=decreasing_line_colors[i],
                                        increasing_fillcolor=fill_colors[i],
                                        decreasing_fillcolor=decreasing_fill_colors[i],
                                        name=f"{symbol}"))            
            #stock_data['Date'] = pd.to_datetime(stock_data['Date'])
            #stock_data.set_index('Date', inplace=True)
        elif(r=="1 Day"):
            stock_data=fetch_data(symbol)
            fig.add_trace(go.Candlestick(x=stock_data.index,
                                        open=stock_data['OPEN'],
                                        high=stock_data['HIGH'],
                                        low=stock_data['LOW'],
                                        close=stock_data['CLOSE'],
                                        increasing_line_color=line_colors[i],
                                        decreasing_line_color=decreasing_line_colors[i],
                                        increasing_fillcolor=fill_colors[i],
                                        decreasing_fillcolor=decreasing_fill_colors[i],
                                        name=f"{symbol}"))            
        else:
            stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
            stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
            stock_data.set_index('DATE', inplace=True)
            fig.add_trace(go.Candlestick(x=stock_data.index,
                                        open=stock_data['OPEN'],
                                        high=stock_data['HIGH'],
                                        low=stock_data['LOW'],
                                        close=stock_data['CLOSE'],
                                        increasing_line_color=line_colors[i],
                                        decreasing_line_color=decreasing_line_colors[i],
                                        increasing_fillcolor=fill_colors[i],
                                        decreasing_fillcolor=decreasing_fill_colors[i],
                                        name=f"{symbol}"))

    # Update layout
    fig.update_layout(
                      xaxis_rangeslider_visible=False,
                      paper_bgcolor='rgba(34, 46, 50, 0.8)',
                      plot_bgcolor='rgba(34, 46, 50, 0.5)',
                      xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white')),
                      yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white')),
                      legend=dict(title='Stock Symbols', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),legend_font_color='red')

    return fig

def plot_4_stock_area(symbols, series_list, start_date, end_date,f,r):
    fig = make_subplots(rows=2, cols=2, subplot_titles=[f"<b><span style='color:red;'>{symbol}</span></b>" for symbol in symbols])

    for i, (symbol, series) in enumerate(zip(symbols, series_list), 1):
        # stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
        # stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
        # stock_data.set_index('DATE', inplace=True)
        # fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
        # chart_data = stock_data['CLOSE'].iplot(fill=True,color=fill_gradient_color, asFigure=True)
        if(r=="1 Week"):
            symbol=symbol+".NS"
            stock=yf.Ticker(symbol)
            stock_data=stock.history(period='1wk')
            fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            chart_data = stock_data['Close'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        elif(r=="1 Day"):
            stock_data=fetch_data(symbol)
            fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            chart_data = stock_data['CLOSE'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        else:        
            stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
            stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
            stock_data.set_index('DATE', inplace=True)
            fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            if(r!="1 Month"):
                chart_data = stock_data['CLOSE'].iplot(fill=True,color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
            else:
                chart_data = stock_data['CLOSE'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        if(f==1):
            return plot_4_stock_candlestick(symbol,series,start_date,end_date,f,r)
        # Update layout directly on the figure object
        fig.append_trace(chart_data.data[0], row=(i+1)//2, col=(i+1)%2 + 1)
        fig.update_layout(
            paper_bgcolor='rgba(34, 46, 50, 0.8)',
            plot_bgcolor='rgba(34, 46, 50, 0.5)'
        )

        # Remove grid and zeroline
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=(i+1)//2, col=(i+1)%2 if (i+1)%2 != 0 else 2, tickfont=dict(color='white'))
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=(i+1)//2, col=(i+1)%2 if (i+1)%2 != 0 else 2, tickfont=dict(color='white'))

        # Disable x-axis range slider
        fig.update_xaxes(rangeslider_visible=False, row=(i+1)//2, col=(i+1)%2 + 1)

        # Hide legend
        fig.update_traces(showlegend=False)

    return fig

def plot_3_stock_area(symbols, series_list, start_date, end_date,f,r):
    fig = make_subplots(rows=3, cols=1, subplot_titles=[f"<b><span style='color:red;'>{symbol}</span></b>" for symbol in symbols])

    for i, (symbol, series) in enumerate(zip(symbols, series_list), 1):
        # stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
        # stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
        # stock_data.set_index('DATE', inplace=True)

        # fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
        # chart_data = stock_data['CLOSE'].iplot(fill=True,color=fill_gradient_color, asFigure=True)        
        if(r=="1 Week"):
            symbol=symbol+".NS"
            stock=yf.Ticker(symbol)
            stock_data=stock.history(period='1wk')
            fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            chart_data = stock_data['Close'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        elif(r=="1 Day"):
            stock_data=fetch_data(symbol)
            fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            chart_data = stock_data['CLOSE'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        else:        
            stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
            stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
            stock_data.set_index('DATE', inplace=True)
            fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            if(r!="1 Month"):
                chart_data = stock_data['CLOSE'].iplot(fill=True,color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
            else:
                chart_data = stock_data['CLOSE'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        if(f==1):
            return plot_3_stock_candlestick(symbol,series,start_date,end_date,f,r)
        # Update layout directly on the figure object
        fig.append_trace(chart_data.data[0], row=i, col=1)
        fig.update_layout(
            paper_bgcolor='rgba(34, 46, 50, 0.8)',
            plot_bgcolor='rgba(34, 46, 50, 0.5)'
        )

        # Remove grid and zeroline
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=i, col=1, tickfont=dict(color='white'))
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=i, col=1, tickfont=dict(color='white'))

        # Disable x-axis range slider
        fig.update_xaxes(rangeslider_visible=False, row=i, col=1)

        fig.update_traces(showlegend=False)

    return fig

def plot_2_stock_area(symbols, series_list, start_date, end_date,f,r):
    fig = make_subplots(rows=1, cols=2, subplot_titles=[f"<b><span style='color:red;'>{symbol}</span></b>" for symbol in symbols])

    for i, (symbol, series) in enumerate(zip(symbols, series_list), 1):
        # stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
        # stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
        # stock_data.set_index('DATE', inplace=True)

        # fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
        # chart_data = stock_data['CLOSE'].iplot(fill=True,color=fill_gradient_color, asFigure=True)
        if(r=="1 Week"):
            symbol=symbol+".NS"
            stock=yf.Ticker(symbol)
            stock_data=stock.history(period='1wk')
            fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            chart_data = stock_data['Close'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        elif(r=="1 Day"):
            stock_data=fetch_data(symbol)
            fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            chart_data = stock_data['CLOSE'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        else:        
            stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
            stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
            stock_data.set_index('DATE', inplace=True)
            fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            if(r!="1 Month"):
                chart_data = stock_data['CLOSE'].iplot(fill=True,color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
            else:
                chart_data = stock_data['CLOSE'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        if(f==1):
            return plot_2_stock_candlestick(symbol,series,start_date,end_date,f,r)        

        # Update layout directly on the figure object
        fig.append_trace(chart_data.data[0], row=1, col=i)

        fig.update_layout(
            paper_bgcolor='rgba(34, 46, 50, 0.8)',
            plot_bgcolor='rgba(34, 46, 50, 0.5)'
        )

        # Remove grid and zeroline
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=1, col=i, tickfont=dict(color='white'))
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', row=1, col=i, tickfont=dict(color='white'))

        # Disable x-axis range slider
        fig.update_xaxes(rangeslider_visible=False, row=1, col=i)

        fig.update_traces(showlegend=False)

    return fig


def plot_merged_stock_area(symbols, series_list, start_date, end_date,r):
    fig = go.Figure()

    for symbol, series in zip(symbols, series_list):
        # stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
        # stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
        # stock_data.set_index('DATE', inplace=True)
        if(r=="1 Week"):
            symbol=symbol+".NS"
            stock=yf.Ticker(symbol)
            stock_data=stock.history(period='1wk')
            fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], fill='tozeroy', mode='lines', name=symbol))
            # fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            #chart_data = stock_data['Close'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        elif(r=="1 Day"):
            stock_data=fetch_data(symbol)
            fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['CLOSE'], fill='tozeroy', mode='lines', name=symbol))
            # fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            #chart_data = stock_data['CLOSE'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
        else:        
            stock_data = stock_df(symbol=symbol, from_date=start_date, to_date=end_date, series=series)
            stock_data['DATE'] = pd.to_datetime(stock_data['DATE'])
            stock_data.set_index('DATE', inplace=True)
            # fill_gradient_color = 'rgba(0, 255, 0, 0.3)'
            # if(r!="1 Month"):
            #     chart_data = stock_data['CLOSE'].iplot(fill=True,color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')
            # else:
            #     chart_data = stock_data['CLOSE'].iplot(color=fill_gradient_color, asFigure=True, gridcolor='rgba(0,0,0,0.5)', zerolinecolor='rgba(0,0,0,0.5)')        
            fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['CLOSE'], fill='tozeroy', mode='lines', name=symbol))

    fig.update_layout(
        paper_bgcolor='rgba(34, 46, 50, 0.8)',
        plot_bgcolor='rgba(34, 46, 50, 0.5)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white')),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.5)', zeroline=True, zerolinecolor='rgba(0,0,0,0.5)', tickfont=dict(color='white')),
        xaxis_rangeslider_visible=False,
        showlegend=True,
        legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0.5)")
    )
    return fig

current_stock_list=[]
current_series_list=[]
length=0
current_multi_plot_type="Candle"
current_merged_status="No"
current_multi_range="5 years"

@app.route('/multicandlestick',methods=['GET', 'POST'])
def multicandlestick():
    if request.method == 'POST':
        reset_global_variables()
        return 'Global variables reset successfully.'
    
    chart_data = Welcome()
    Loading_data=Loading()
    
    return render_template('multidashboard1.html', chart_data=chart_data,Loading_data=Loading_data)

@app.route('/multiprocesspush', methods=['POST']) 
def multiprocesspush():
    global current_stock_list
    global current_series_list
    global length
    global current_multi_plot_type
    global current_merged_status
    global current_multi_range
    global current_multi_filter_status
    data = request.get_json()
    stock_symbol = data['currsymbol']
    stock_series = data['currseries']
    current_multi_range="5 years"
    current_multi_plot_type="Candle"
    current_multi_filter_status=0
    today = date.today()
    start_date = today - relativedelta(years=5)   
    if(current_merged_status=="No"):
            current_stock_list.append(stock_symbol)
            current_series_list.append(stock_series)
            length=len(current_stock_list)
            if(length==4):
                chart_data=plot_4_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==3):
                chart_data=plot_3_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==2):
                chart_data=plot_2_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            else:
                chart_data=plot_stock_candlestick(current_stock_list[0],current_series_list[0],start_date,today,current_multi_filter_status,current_multi_range)
    else:
        current_stock_list.append(stock_symbol)
        current_series_list.append(stock_series)
        length=len(current_stock_list)
        chart_data=plot_merged_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_range)       
    chart_data_json = chart_data.to_json()
    return chart_data_json    
         
@app.route('/multiprocesspop', methods=['POST']) 
def multiprocesspop():
    global current_stock_list
    global current_series_list
    global length
    global current_multi_plot_type
    global current_merged_status
    global current_multi_range
    data = request.get_json()
    print(data)
    stock_symbol = data['currsymbol']
    stock_series = data['currseries']
    current_multi_range="5 years"
    current_multi_plot_type="Candle"
    current_multi_filter_status=0
    today = date.today()
    start_date = today - relativedelta(years=5)   
    if(current_merged_status=="No"):
            current_stock_list.remove(stock_symbol)
            current_series_list.remove(stock_series)
            length=len(current_stock_list)
            if(length==3):
                chart_data=plot_3_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==2):
                chart_data=plot_2_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==1):
                chart_data=plot_stock_candlestick(current_stock_list[0],current_series_list[0],start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==0):
                chart_data = Welcome()
    else:
        current_stock_list.remove(stock_symbol)
        current_series_list.remove(stock_series)
        length=len(current_stock_list)
        chart_data=plot_merged_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_range)       
    chart_data_json = chart_data.to_json()
    return chart_data_json    
    # current_stock_symbol=stock_symbol
    # current_stock_series=stock_series
    # current_range="5 years"
    # current_plot_type="Candle"
    # today = date.today()
    # start_date = today - relativedelta(years=5)   
    # chart_data = plot_stock_candlestick(symbol=current_stock_symbol, series=current_stock_series, start_date=start_date, end_date=today) 
    # chart_data_json = chart_data.to_json()
    # return chart_data_json

@app.route('/multimergetosinglegraph', methods=['POST']) 
def multimergetosinglegraph():
    global current_stock_list
    global current_series_list
    global length
    global current_multi_plot_type
    global current_merged_status
    global current_multi_range
    global current_multi_filter_status
    if (current_merged_status=="Yes"):
        current_merged_status="No"
    else:
        current_merged_status="Yes"
    today = date.today()
    if(current_multi_range=="5 years"):
        start_date = today - relativedelta(years=5)   
    elif(current_multi_range=="1 year"):
        start_date = today - relativedelta(years=1)
    elif(current_multi_range=="1 Month"):
        start_date = today - relativedelta(months=1)#################
    elif(current_multi_range=="1 Week"):
        start_date = today - relativedelta(years=1)##################
    elif(current_multi_range=="1 Day"):
        start_date = today - relativedelta(years=1)    ###########    
    elif(current_multi_range=="Overall"):
        start_date = today - relativedelta(years=50)   ##################                   
    if(current_multi_plot_type=="Candle"):
        if(current_merged_status=="Yes"):
            chart_data = plot_merged_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_range)  
        else:
            if(length==4):
                chart_data=plot_4_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==3):
                chart_data=plot_3_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==2):
                chart_data=plot_2_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            else:
                chart_data=plot_stock_candlestick(current_stock_list[0],current_series_list[0],start_date,today,current_multi_filter_status,current_multi_range)

    else:
        if(current_merged_status=="Yes"):
            chart_data = plot_merged_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_range)  
        else:
            if(length==4):
                chart_data=plot_4_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==3):
                chart_data=plot_3_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==2):
                chart_data=plot_2_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            else:
                chart_data=plot_stock_area(current_stock_list[0],current_series_list[0],start_date,today,current_multi_filter_status,current_multi_range)           
    chart_data_json = chart_data.to_json()
    return chart_data_json   

@app.route('/multiprocessplottype', methods=['POST']) 
def multiprocessplottype():
    global current_stock_list
    global current_series_list
    global length
    global current_multi_plot_type
    global current_merged_status
    global current_multi_range
    global current_multi_filter_status
    if(current_multi_plot_type=="Candle"):
        current_multi_plot_type="Area"
    elif(current_multi_plot_type=="Area"):
        current_multi_plot_type="Candle"
    today = date.today()
    if(current_multi_range=="5 years"):
        start_date = today - relativedelta(years=5)   
    elif(current_multi_range=="1 year"):
        start_date = today - relativedelta(years=1)
    elif(current_multi_range=="1 Month"):
        start_date = today - relativedelta(months=1)#################
    elif(current_multi_range=="1 Week"):
        start_date = today - relativedelta(years=1)##################
    elif(current_multi_range=="1 Day"):
        start_date = today - relativedelta(years=1)    ###########    
    elif(current_multi_range=="Overall"):
        start_date = today - relativedelta(years=50)   ##################      
    if(current_multi_plot_type=="Candle"):
        if(current_merged_status=="Yes"):
            chart_data = plot_merged_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_range)  
        else:
            if(length==4):
                chart_data=plot_4_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==3):
                chart_data=plot_3_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==2):
                chart_data=plot_2_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            else:
                chart_data=plot_stock_candlestick(current_stock_list[0],current_series_list[0],start_date,today,current_multi_filter_status,current_multi_range)

    else:
        if(current_merged_status=="Yes"):
            chart_data = plot_merged_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_range)  
        else:
            if(length==4):
                chart_data=plot_4_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==3):
                chart_data=plot_3_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==2):
                chart_data=plot_2_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            else:
                chart_data=plot_stock_area(current_stock_list[0],current_series_list[0],start_date,today,current_multi_filter_status,current_multi_range)           
    chart_data_json = chart_data.to_json()
    return chart_data_json      

@app.route('/multiprocessrange', methods=['POST']) 
def multiprocessplotrange():
    global current_stock_list
    global current_series_list
    global length
    global current_multi_plot_type
    global current_merged_status
    global current_multi_range
    global current_multi_filter_status
    data=request.get_json()
    current_multi_range=data['currRange']
    today = date.today()
    if(current_multi_range=="5 years"):
        start_date = today - relativedelta(years=5)   
    elif(current_multi_range=="1 year"):
        start_date = today - relativedelta(years=1)
    elif(current_multi_range=="1 Month"):
        start_date = today - relativedelta(months=1)#################
    elif(current_multi_range=="1 Week"):
        start_date = today - relativedelta(years=1)##################
    elif(current_multi_range=="1 Day"):
        start_date = today - relativedelta(years=1)    ###########    
    elif(current_multi_range=="Overall"):
        start_date = today - relativedelta(years=50)   ##################      
    if(current_multi_plot_type=="Candle"):
        if(current_merged_status=="Yes"):
            chart_data = plot_merged_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_range)  
        else:
            if(length==4):
                chart_data=plot_4_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==3):
                chart_data=plot_3_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==2):
                chart_data=plot_2_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            else:
                chart_data=plot_stock_candlestick(current_stock_list[0],current_series_list[0],start_date,today,current_multi_filter_status,current_multi_range)

    else:
        if(current_merged_status=="Yes"):
            chart_data = plot_merged_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_range)  
        else:
            if(length==4):
                chart_data=plot_4_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==3):
                chart_data=plot_3_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==2):
                chart_data=plot_2_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            else:
                chart_data=plot_stock_area(current_stock_list[0],current_series_list[0],start_date,today,current_multi_filter_status,current_multi_range)           
    chart_data_json = chart_data.to_json()
    return chart_data_json     


@app.route('/multiprocessfilter', methods=['POST']) 
def multiprocessfilter():
    global current_stock_list
    global current_series_list
    global length
    global current_multi_plot_type
    global current_merged_status
    global current_multi_range
    global current_multi_filter_status
    if(current_multi_filter_status==1):
        current_multi_filter_status=0
    else:
        current_multi_filter_status=1
    today = date.today()
    if(current_multi_range=="5 years"):
        start_date = today - relativedelta(years=5)   
    elif(current_multi_range=="1 year"):
        start_date = today - relativedelta(years=1)
    elif(current_multi_range=="1 Month"):
        start_date = today - relativedelta(months=1)#################
    elif(current_multi_range=="1 Week"):
        start_date = today - relativedelta(years=1)##################
    elif(current_multi_range=="1 Day"):
        start_date = today - relativedelta(years=1)    ###########    
    elif(current_multi_range=="Overall"):
        start_date = today - relativedelta(years=50)   ##################      
    if(current_multi_plot_type=="Candle"):
        if(current_merged_status=="Yes"):
            chart_data = plot_merged_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_range)  
        else:
            if(length==4):
                chart_data=plot_4_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==3):
                chart_data=plot_3_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==2):
                chart_data=plot_2_stock_candlestick(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            else:
                chart_data=plot_stock_candlestick(current_stock_list[0],current_series_list[0],start_date,today,current_multi_filter_status,current_multi_range)

    else:
        if(current_merged_status=="Yes"):
            chart_data = plot_merged_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_range)  
        else:
            if(length==4):
                chart_data=plot_4_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==3):
                chart_data=plot_3_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            elif(length==2):
                chart_data=plot_2_stock_area(current_stock_list,current_series_list,start_date,today,current_multi_filter_status,current_multi_range)
            else:
                chart_data=plot_stock_area(current_stock_list[0],current_series_list[0],start_date,today,current_multi_filter_status,current_multi_range)           
    chart_data_json = chart_data.to_json()
    return chart_data_json     


# @app.route('/redirect_to_single_stock')
# def redirect_to_single_stock():
#     return redirect(url_for('dashboard'))

# @app.route('/redirect_to_multiple_stock')
# def redirect_to_multiple_stock():
#     return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

