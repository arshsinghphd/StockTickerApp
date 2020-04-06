from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from flask import Flask,render_template,request,redirect,session
#import os
import pandas as pd
import quandl
import requests
import simplejson as json

app = Flask(__name__)
app.vars={}
@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/graph', methods=['POST'])
def graph():
  if request.method == 'POST':
    app.vars['ticker'] = request.form['ticker']
    quandl.ApiConfig.api_key ="SV_rnAS4EL65RG_ZMHGh"
    df=quandl.get("WIKI/%s" % app.vars['ticker'])
    df.reset_index(inplace=True)
    pd.to_datetime(df['Date'],infer_datetime_format=True)

    p = figure(title='Stock prices for %s' % app.vars['ticker'], x_axis_label='Date', x_axis_type='datetime')
    if request.form.get('Close'):
        p.line(df.get('Date'), df.get('Close'), line_width=2, line_color="green", legend_label='Close')
    if request.form.get('Adj. Close'):
        p.line(df.get('Date'), df.get('Adj. Close'), line_width=2, line_color="black", legend_label='Adj. Close')
    if request.form.get('Open'):
        p.line(df.get('Open'), df.get('Open'), line_width=2, line_color="red", legend_label='Open')
    if request.form.get('Adj. Open'):
        p.line(df.get('Adj. Open'), df.get('Adj. Open'), line_width=2, line_color="blue", legend_label='Adj. Open')

###   Plotting using ColumnDataSource       
##    source=ColumnDataSource(df)
##    p = figure(title='Stock prices for %s' % app.vars['ticker'], x_axis_label='Date', x_axis_type='datetime')
##    if request.form.get('Close'):
##        p.line(x='Date', y='Close',source=source, line_width=2, line_color="green", legend_label='Close')
##    if request.form.get('Adj. Close'):
##        p.line(x='Date', y='Adj. Close',source=source, line_width=2, line_color="black", legend_label='Adj. Close')
##    if request.form.get('Open'):
##        p.line(x='Date', y='Open',source=source, line_width=2, line_color="red", legend_label='Open')
##    if request.form.get('Adj. Open'):
##        p.line(x='Date', y='Adj. Open',source=source, line_width=2, line_color="blue", legend_label='Adj. Open') 

###  Earlier plotting
##    source=ColumnDataSource(df)
##    p = figure(title='Stock prices for %s' % app.vars['ticker'], x_axis_label='Date', x_axis_type='datetime')
##    if request.form.get('Close'):
##        p.line(x=df['Date'].values, y=df['Close'].values,line_width=2, line_color="green", legend_label='Close')
##    if request.form.get('Adj. Close'):
##        p.line(x=df['Date'].values, y=df['Adj. Close'].values,line_width=2, line_color="green", legend_label='Adj. Close')
##    if request.form.get('Open'):
##        p.line(x=df['Date'].values, y=df['Open'].values,line_width=2, line_color="red", legend_label='Open')
##    if request.form.get('Adj. Open'):
##        p.line(x=df['Date'].values, y=df['Adj. Open'].values,line_width=2, line_color="purple", legend_label='Adj. Open')


    script, div = components(p)
    return render_template('graph.html', script=script, div=div)
  
if __name__ == '__main__':
  # myport = int(os.environ.get("PORT", 5000))
  # myhost='0.0.0.0'
  # app.run(host=myhost, port=myport, debug=True)
  app.run()
