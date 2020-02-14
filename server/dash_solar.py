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
	html.H2( children = "charge-con graph" ),
	dcc.Graph( id = "live-graph-soc" ),
	dcc.Graph( id = "live-graph-load" ),
	dcc.Graph( id = "live-graph-solar" ),
	dcc.Graph( id = "live-graph-battery" ),
	dcc.Interval(
		id = "interval-component",
		interval = 60000 * param_server.WEB_INTERVAL_SOL,
		n_intervals = 0
	)
])

def getData(start_day, end_day, id):
	sql = 	"SELECT "\
				+ "DATE_FORMAT(time, '%Y/%m/%d %H:%i'),"\
				+ "AVG(solarVoltage),"\
				+ "AVG(solarCurrent),"\
				+ "AVG(solarPower),"\
				+ "AVG(batteryVoltage),"\
				+ "AVG(batteryCurrent),"\
				+ "AVG(batteryPower),"\
				+ "AVG(batterySOC),"\
				+ "AVG(loadVoltage),"\
				+ "AVG(loadCurrent),"\
				+ "AVG(loadPower) "\
			+ "FROM solar_tb "\
			+ "WHERE "\
				+ "time "\
				+ "BETWEEN '"\
				+ start_day + "' and '" + end_day\
			+ "' AND "\
				+ "id=" + str(id)\
			+ " GROUP BY "\
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
	print(sql)
	fetch = c.fetchall()
	conn.close()

	li = [list(x) for x in zip(*fetch)]

	return li

def printTime(str):
	print(str + ":" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.callback(Output('live-graph-soc', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_soc(n):
	printTime("SOC1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li = getData(start_day, end_day, 1)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li[0], "y":li[7], "type":"line", "name":"Power"},
		],
		"layout": {
			"title":"SOC info"
		}
	}
	printTime("SOC2")

	return fig

@app.callback(Output('live-graph-load', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_load(n):
	printTime("liad1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li = getData(start_day, end_day, 1)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li[0], "y":li[8], "type":"line", "name":"Voltage"},
			{"x":li[0], "y":li[9], "type":"line", "name":"Current"},
			{"x":li[0], "y":li[10], "type":"line", "name":"Power"},
		],
		"layout": {
			"title":"load info"
		}
	}
	t1 = datetime.datetime.now()
	t1 = t1.strftime("%Y-%m-%d %H:%M:%S")

	printTime("load2")
	return fig

@app.callback(Output('live-graph-solar', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_solar(n):
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li = getData(start_day, end_day, 1)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li[0], "y":li[1], "type":"line", "name":"Voltage"},
			{"x":li[0], "y":li[2], "type":"line", "name":"Current"},
			{"x":li[0], "y":li[3], "type":"line", "name":"Power"},
		],
		"layout": {
			"title":"solar info"
		}
	}

	printTime("solar2")
	return fig

@app.callback(Output('live-graph-battery', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_battery(n):
	printTime("battery1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li = getData(start_day, end_day, 1)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li[0], "y":li[4], "type":"line", "name":"Voltage"},
			{"x":li[0], "y":li[5], "type":"line", "name":"Current"},
			{"x":li[0], "y":li[6], "type":"line", "name":"Power"},
		],
		"layout": {
			"title":"battery info"
		}
	}

	printTime("battery2")
	return fig


if __name__ == "__main__":
	app.run_server(debug=True, host=param_server.ADDRESS, port=param_server.WEB_PORT_SOL)