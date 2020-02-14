# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import numpy as np
import datetime
import pymysql.cursors
import param_server

app = dash.Dash()
app.layout =  html.Div( children = [
	html.H2( children = "sensor graph" ),
	dcc.Graph( id = "live-graph-soil" ),
	dcc.Graph( id = "live-graph-temp" ),
	dcc.Graph( id = "live-graph-hum" ),
	dcc.Graph( id = "live-graph-lux" ),
	dcc.Interval(
		id = "interval-component",
		interval = 60000 * param_server.WEB_INTERVAL_TWE,
		n_intervals = 0
	)
])
def getData(start_day, end_day, twe_id):
	sql = 	"SELECT "\
				+ "DATE_FORMAT(time, '%Y/%m/%d %H:%i'),"\
				+ "AVG(ba),"\
				+ "AVG(a1),"\
				+ "AVG(a2),"\
				+ "AVG(te),"\
				+ "AVG(hu)"\
			+ "FROM sensor_tb "\
			+ "WHERE "\
				+ "time "\
				+ "BETWEEN '"\
				+ start_day + "' and '" + end_day\
				+ "' and ed='" + twe_id\
			+ "' GROUP BY "\
				+ "DATE_FORMAT(time, '%Y-%m-%d %H:%i') "\
			+ "ORDER BY "\
				+ "time "\
				+ "ASC;"\

	conn = pymysql.connect(
		user="ubuntu",
		passwd="ubuntu",
		host="localhost",
		db="sensor_db"
	)
	c = conn.cursor()
	c.execute( sql )
	print( sql )
	fetch = c.fetchall()
	conn.close()

	li = [list(x) for x in zip(*fetch)]
#	print(li)
#	print(fetch)

	return li

def printTime(str):
	print(str + ":" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.callback(Output('live-graph-soil', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_soil(n):
	printTime("soil1:")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
	li = getData(start_day, end_day, param_server.ID_SOIL)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li[0], "y":li[2], "type":"line", "name":"soil"},
		],
		"layout": {
			"title":"土中水分"
		}
	}

	printTime("soil2:")
	return fig

@app.callback(Output('live-graph-temp', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_temp(n):
	printTime("temp:1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
	li = getData(start_day, end_day, param_server.ID_TEMP)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li[0], "y":li[4], "type":"line", "name":"temp"},
		],
		"layout": {
			"title":"窓際温度"
		}
	}
	printTime("temp2:")

	return fig

@app.callback(Output('live-graph-hum', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_hum(n):
	printTime("hum:1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
	li = getData(start_day, end_day, param_server.ID_TEMP)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li[0], "y":li[5], "type":"line", "name":"hum"},
		],
		"layout": {
			"title":"窓際湿度"
		}
	}
	printTime("hum3:")

	return fig

@app.callback(Output('live-graph-lux', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_lux(n):
	printTime("lux:1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
	li = getData(start_day, end_day, param_server.ID_LUX)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li[0], "y":li[3], "type":"line", "name":"lux"},
		],
		"layout": {
			"title":"窓際照度"
		}
	}
	printTime("lux3:")

	return fig

if __name__ == "__main__":
	app.run_server(debug=True, host=param_server.ADDRESS, port=param_server.WEB_PORT_TWE)
