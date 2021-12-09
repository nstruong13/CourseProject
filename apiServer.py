from flask import Flask, make_response, request, send_file
from scrapeGoogle import get_text_data
import ScrapeMineVizScholar 

app = Flask(__name__)
@app.route('/query', methods=['GET'])

def query():
	#TODO: change to read in the query. Below was just a test of the server.
	response = make_response(send_file("heatmap.png", mimetype='image/png'))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response
	# inputQuery = request.args.get('query')
	# get_text_data("text mining")
	# lines = []
	# with open('scrapedtext.dat','r',encoding='utf-8') as file:
	# 	for line in file:
	# 		lines.append(line)
	# return str(lines)


@app.route('/query2', methods=['GET'])

def query2():
	# response = make_response('<style type="text/css">\n#T_c445c_row0_col1 {\n  background-color: #fff7fb;\n  color: #000000;\n}\n</style>\n<table id="T_c445c_">\n  <caption>file</caption>\n  <thead>\n    <tr>\n      <th class="col_heading level0 col0" >Document Number</th>\n      <th class="col_heading level0 col1" >Frequency</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td id="T_c445c_row0_col0" class="data row0 col0" >2</td>\n      <td id="T_c445c_row0_col1" class="data row0 col1" >6</td>\n    </tr>\n  </tbody>\n</table>\n')
	inputQuery = request.args.get('query')
	response = make_response(ScrapeMineVizScholar.main(inputQuery))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=105)
