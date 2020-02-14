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
	dcc.Graph( id = "live-graph-load-v" ),
	dcc.Graph( id = "live-graph-load-i" ),
	dcc.Graph( id = "live-graph-load-p" ),
	dcc.Graph( id = "live-graph-solar-v" ),
	dcc.Graph( id = "live-graph-solar-i" ),
	dcc.Graph( id = "live-graph-solar-p" ),
	dcc.Graph( id = "live-graph-battery-v" ),
	dcc.Graph( id = "live-graph-battery-i" ),
	dcc.Graph( id = "live-graph-battery-p" ),
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

	ret = [list(x) for x in zip(*fetch)]

	return ret

def printTime(str):
	print(str + ":" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.callback(Output('live-graph-soc', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_soc(n):
	printTime("SOC-1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li1 = getData(start_day, end_day, 1)
	li2 = getData(start_day, end_day, 2)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li1[0], "y":li1[7], "type":"line", "name":"ID1"},
			{"x":li1[0], "y":li1[7], "type":"line", "name":"ID2"},
		],
		"layout": {
			"title":"SOC info"
		}
	}
	printTime("SOC-2")

	return fig

#####################
# load graph
#####################
@app.callback(Output('live-graph-load-v', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_load_v(n):
	printTime("load_v-1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li1 = getData(start_day, end_day, 1)
	li2 = getData(start_day, end_day, 2)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li1[0], "y":li1[8], "type":"line", "name":"ID1"},
			{"x":li2[0], "y":li2[8], "type":"line", "name":"ID2"},
		],
		"layout": {
			"title":"load voltage info"
		}
	}
	t1 = datetime.datetime.now()
	t1 = t1.strftime("%Y-%m-%d %H:%M:%S")

	printTime("load_v-2")
	return fig

@app.callback(Output('live-graph-load-i', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_load_i(n):
	printTime("load_i-1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li1 = getData(start_day, end_day, 1)
	li2 = getData(start_day, end_day, 2)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li1[0], "y":li1[9], "type":"line", "name":"ID1"},
			{"x":li2[0], "y":li2[9], "type":"line", "name":"ID2"},
		],
		"layout": {
			"title":"load current info"
		}
	}
	t1 = datetime.datetime.now()
	t1 = t1.strftime("%Y-%m-%d %H:%M:%S")

	printTime("load_i-2")
	return fig

@app.callback(Output('live-graph-load-p', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_load_p(n):
	printTime("load_p-1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li1 = getData(start_day, end_day, 1)
	li2 = getData(start_day, end_day, 2)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li1[0], "y":li1[10], "type":"line", "name":"ID1"},
			{"x":li2[0], "y":li2[10], "type":"line", "name":"ID2"},
		],
		"layout": {
			"title":"load power info"
		}
	}
	t1 = datetime.datetime.now()
	t1 = t1.strftime("%Y-%m-%d %H:%M:%S")

	printTime("load_p-2")
	return fig

#####################
# solar graph
#####################
@app.callback(Output('live-graph-solar-v', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_solar_v(n):
	printTime("solar_v-1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li1 = getData(start_day, end_day, 1)
	li2 = getData(start_day, end_day, 2)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li1[0], "y":li1[1], "type":"line", "name":"ID1"},
			{"x":li2[0], "y":li2[1], "type":"line", "name":"ID2"},
		],
		"layout": {
			"title":"solar voltage info"
		}
	}

	printTime("solar_v-2")
	return fig

@app.callback(Output('live-graph-solar-i', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_solar_i(n):
	printTime("solar_i-1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li1 = getData(start_day, end_day, 1)
	li2 = getData(start_day, end_day, 2)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li1[0], "y":li1[2], "type":"line", "name":"ID1"},
			{"x":li2[0], "y":li2[2], "type":"line", "name":"ID2"},
		],
		"layout": {
			"title":"solar current info"
		}
	}

	printTime("solar_i-2")
	return fig

@app.callback(Output('live-graph-solar-p', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_solar_p(n):
	printTime("solar_p-1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li1 = getData(start_day, end_day, 1)
	li2 = getData(start_day, end_day, 2)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li1[0], "y":li1[3], "type":"line", "name":"ID1"},
			{"x":li2[0], "y":li2[3], "type":"line", "name":"ID2"},
		],
		"layout": {
			"title":"solar power info"
		}
	}

	printTime("solar_p-2")
	return fig

#####################
# battery graph
#####################
@app.callback(Output('live-graph-battery-v', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_battery_v(n):
	printTime("battery_v-1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li1 = getData(start_day, end_day, 1)
	li2 = getData(start_day, end_day, 2)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li1[0], "y":li1[4], "type":"line", "name":"ID1"},
			{"x":li2[0], "y":li2[4], "type":"line", "name":"ID2"},
		],
		"layout": {
			"title":"battery voltage info"
		}
	}

	printTime("battery_v-2")
	return fig

@app.callback(Output('live-graph-battery-i', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_battery_i(n):
	printTime("battery_i-1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li1 = getData(start_day, end_day, 1)
	li2 = getData(start_day, end_day, 2)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li1[0], "y":li1[4], "type":"line", "name":"ID1"},
			{"x":li2[0], "y":li2[4], "type":"line", "name":"ID2"},
		],
		"layout": {
			"title":"battery current info"
		}
	}

	printTime("battery_i-2")
	return fig

@app.callback(Output('live-graph-battery-p', 'figure'),
			[Input('interval-component', 'n_intervals')])
def update_live_graph_battery_p(n):
	printTime("battery_p-1")
	# 現在までの湿度データを取得するSQLを生成
	end_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	start_day = (datetime.datetime.now() - datetime.timedelta(days=param_server.WEB_DELTA_SOL)).strftime("%Y-%m-%d %H:%M:%S")
	li1 = getData(start_day, end_day, 1)
	li2 = getData(start_day, end_day, 2)

	# dcc.Graphに渡すfigureの作成
	fig = {
		"data":[
			{"x":li1[0], "y":li1[4], "type":"line", "name":"ID1"},
			{"x":li2[0], "y":li2[4], "type":"line", "name":"ID2"},
		],
		"layout": {
			"title":"battery power info"
		}
	}

	printTime("battery_p-2")
	return fig


if __name__ == "__main__":
	app.run_server(debug=True, host=param_server.ADDRESS, port=param_server.WEB_PORT_SOL)