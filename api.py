from multiprocessing import Process
from flask import request
from flask import Flask
import time
import math
import var

app = Flask('app')

reload50 = '<script>setTimeout(function() { window.location = window.location }, 50)</script>'
reload250 = '<script>setTimeout(function() { window.location = window.location }, 250)</script>'
reload5000 = '<script>setTimeout(function() { window.location = window.location }, 5000)</script>'
viewport1 = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
appVer = '<br><br>API Version: ' + var.read('appVer')

def startWebserver():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port='7070')

def start():
    print('loading API')
    proc.start()
    time.sleep(2)
    print('API loaded, starting data stream')
    var.write('dataStrmStart','True')

proc = Process(target=startWebserver)

@app.route('/')
def mainEndpoint():
    if var.read('strmData') == 'None':
        return '<b><h3>Coronavirus API by VihangaTheTurtle</h3>The API server is currently offline, please check back later</b>' + viewport1
    elif var.read('strmData') == 'g':
        try:
            return '<b><h3>Coronavirus API by VihangaTheTurtle</h3>Gathering initial data: ' + str(math.floor((int(var.read('refreshes')) / 125) * 100)) + '% complete<br><progress id="file" value="' + str(math.floor((int(var.read('refreshes')) / 125) * 100)) + '" max="100"></progress><br>Initialization sequence: ' + str(math.floor(int(var.read('processingAmount')) / 2 + int(var.read('refreshes')) / 252 * 100)) + '% complete</b><br><progress id="file" value="' + str(math.floor(int(var.read('processingAmount')) / 2 + int(var.read('refreshes')) / 252 * 100)) + '" max="100"></progress>' + reload250 + appVer + viewport1
        except:
            return '<b><h3>Coronavirus API by VihangaTheTurtle</h3>An error occured</b>' + reload250 + appVer + viewport1
    elif var.read('strmData') == 'p':
        try:
            return '<b><h3>Coronavirus API by VihangaTheTurtle</h3>Processing initial data: ' + str(math.floor((int(var.read('processingAmount'))) / 125 * 100)) + '% complete<br><progress id="file" value="' + str(math.floor((int(var.read('processingAmount'))) / 125 * 100)) + '" max="100"></progress><br>Initialization sequence: ' + str(math.floor((int(var.read('processingAmount')) - 26) / 2 + int(var.read('refreshes')) / 252 * 100)) + '% complete</b><br><progress id="file" value="' + str(math.floor((int(var.read('processingAmount')) - 26) / 2 + int(var.read('refreshes')) / 252 * 100)) + '" max="100"></progress>' + reload250 + appVer + viewport1
        except:
            return '<b><h3>Coronavirus API by VihangaTheTurtle</h3>An error occured</b>' + reload250 + appVer + viewport1
    elif var.read('strmData') == 'e':
        return '<b><h3>Coronavirus API by VihangaTheTurtle</h3>An unknown error occured whilst processing the data</b>' + appVer + viewport1
    elif var.read('strmData') == 's':
        return '<b><h3>Coronavirus API by VihangaTheTurtle</h3>Slow down, the stream processor is still starting</b>' + appVer + viewport1
    elif var.read('strmData') == 'o':
        return '<b><h3>Coronavirus API by VihangaTheTurtle</h3>Data stream processor online, use <a href="/api/data">/api/data</a> to access data</b>' + appVer + viewport1
    elif var.read('strmData') == 'n':
        return '<b><h3>Coronavirus API by VihangaTheTurtle</h3>Data stream processor is offline, please try again later</b>' + appVer + viewport1
    elif var.read('strmData') == 'k':
        return '<b><h3>Coronavirus API by VihangaTheTurtle</h3>Data stream processor failed to establish a stable connection, retrying in 5 seconds</b>' + reload5000 + appVer + viewport1

@app.route('/api/data')
def apiDataMenu():
    return '<a href="data/lastCases">lastCases</a><br><a href="data/lastDeaths">lastDeaths</a><br><a href="data/highCases">highCases</a><br><a href="data/highDeaths">highDeaths</a><br><a href="data/avgCases">avgCases</a><br><a href="data/avgDeaths">avgDeaths</a>' + appVer + viewport1

@app.route('/api/data/avgCases')
def avgCases():
    return var.read('avgCases')
    
@app.route('/api/data/avgDeaths')
def avgDeaths():
    return var.read('avgDeaths')

@app.route('/api/data/custom')
def customData():
    q = request.args.get('q')
    return var.read(q)

@app.route('/api/data/highCases')
def highCases():
    return var.read('highCases')

@app.route('/api/data/highDeaths')
def highDeaths():
    return var.read('highDeaths')

@app.route('/api/data/lastCases')
def lastCases():
    return var.read('lastCases')

@app.route('/api/data/lastDeaths')
def lastDeaths():
    return var.read('lastDeaths')

@app.route('/api/')
def apiStatus():
    if var.read('strmData') == 'None':
        return '<b>Data stream is stopped</b>' + appVer + viewport1
    elif var.read('strmData') == 'g':
        try:
            return '<b>Gathering initial data: ' + str(math.floor((int(var.read('refreshes')) / 125) * 100)) + '% complete<br><progress id="file" value="' + str(math.floor((int(var.read('refreshes')) / 125) * 100)) + '" max="100"></progress><br>Initialization sequence: ' + str(math.floor(int(var.read('processingAmount')) / 2 + int(var.read('refreshes')) / 252 * 100)) + '% complete</b><br><progress id="file" value="' + str(math.floor(int(var.read('processingAmount')) / 2 + int(var.read('refreshes')) / 252 * 100)) + '" max="100"></progress>' + reload50 + appVer + viewport1
        except:
            return '<b>An error occured</b>' + reload50 + appVer + viewport1
    elif var.read('strmData') == 'p':
        try:
            return '<b>Processing initial data: ' + str(math.floor((int(var.read('processingAmount'))) / 125 * 100)) + '% complete<br><progress id="file" value="' + str(math.floor((int(var.read('processingAmount'))) / 125 * 100)) + '" max="100"></progress><br>Initialization sequence: ' + str(math.floor((int(var.read('processingAmount')) - 26) / 2 + int(var.read('refreshes')) / 252 * 100)) + '% complete</b><br><progress id="file" value="' + str(math.floor((int(var.read('processingAmount')) - 26) / 2 + int(var.read('refreshes')) / 252 * 100)) + '" max="100"></progress>' + reload50 + appVer + viewport1
        except:
            return '<b>An error occured</b>' + reload50 + appVer + viewport1
    elif var.read('strmData') == 'e':
        return '<b>An unknown error occured whilst processing the data</b>' + appVer + viewport1
    elif var.read('strmData') == 's':
        return '<b>Slow down, the stream processor is still starting</b>' + appVer + viewport1
    elif var.read('strmData') == 'o':
        return '<b>Data stream processor online, use <a href="data">/data</a> to access data</b>' + appVer + viewport1
    elif var.read('strmData') == 'n':
        return '<b>Data stream processor is offline, please try again later</b>' + appVer + viewport1
    elif var.read('strmData') == 'k':
        return '<b>Data stream processor failed to establish a stable connection, retrying in 5 seconds</b>' + reload5000 + appVer + viewport1