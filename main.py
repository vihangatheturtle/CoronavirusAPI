from requests import get
import time
from datetime import datetime
import sys
import os
import atexit
import api
import var

data = None
dataArrayInit = [None]
dataArrayInit0 = [None]
delay = 0
same = True

if __name__ == '__main__':
  def dataStrm():
      global delay
      global same
      var.write('strmData','s')
      while True:
        def reset():
            global data
            global dataArrayInit
            global dataArrayInit0
            global delay
            global same
            data = None
            dataArrayInit = [None]
            dataArrayInit0 = [None]
            delay = 0
            same = True
            var.write('dataStrmStart','False')
            var.write('strmData','n')
            var.write('refreshes','0')
            var.write('processingAmount','0')
        try:
            f = open("var/processingAmount.dat", "r")
            f.close()
        except:
            var.write('processingAmount','0')
            delay = 0
        if var.read('refreshes') == 'err0':
            var.write('refreshes','0')
        if int(var.read('refreshes')) >= 125:
            var.write('strmData','o')
            if int(var.read('refreshes')) == 125:
                var.write('strmData','p')
                dataArrayInit0[0] = dataArrayInit0[1]
                same = True
                prev = dataArrayInit0[0][0].split('!')[3]
                i = 0
                for x in dataArrayInit0:
                  try:
                    if int(x[0].split('!')[3]) == int(prev):
                        if int(i) <= 128:
                            prev = int(x[0].split('!')[3])
                            print('Processed stream ' + str(i) + ', success')
                        else:
                            print('Processing anomaly found, attempting to recover from this')
                            var.write('processingAmount','0')
                            same = False
                    else:
                        print('Processed stream ' + str(i) + ', fail, prev: ' + prev + ', curr: ' + str(x[0].split('!')[3]))
                  except Exception as e:
                    print('Processed stream ' + str(i) + ', fail, prev: ' + prev + ', curr: ' + str(x[0].split('!')[3]))
                    print('Furthermore, an error also occured whilst processing stream ' + str(i))
                    print(e)
                    same = False
                  try:
                    var.write('processingAmount',str(int(var.read('processingAmount')) + 1))
                  except Exception as ex:
                    same = False
                    print('An error occured (' + str(ex) + '), attempting to recover from this')
                    var.write('processingAmount','0')
                  time.sleep(0.05)
                  i = i + 1
                if same == True:
                    print('Successfully processed all initial data streams, increasing rescan delay to 2 seconds')
                    delay = 2
                else:
                    print('Failed to verify a stable data stream, retrying in 5 seconds')
                    reset()
                    var.write('strmData','k')
                    time.sleep(5)
        else:
            var.write('strmData','g')
            
        def exitFunc():
          print('\nPlease press start')

        var.write('refreshes',str(int(var.read('refreshes')) + 1))
        print('data checks: ' + var.read('refreshes'))
        today = datetime.today()
        dataArray = []

        def get_data(url):
            response = get(endpoint, timeout=10)
            
            if response.status_code >= 400:
                raise RuntimeError(f'Request failed: { response.text }')
                
            return response.json()

        endpoint = 'https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=nation;areaName=england&structure={"date":"date","name":"areaName","code":"areaCode","cases":{"daily":"newCasesByPublishDate","cumulative":"cumCasesByPublishDate"},"deaths":{"daily":"newDeathsByDeathDate","cumulative":"cumDeathsByDeathDate"}}'
        
        data = str(get_data(endpoint)).split("'data':")[1].replace('[', '').replace('{', '').replace(", 'da", 'da').replace("'", '').replace(' ', '').split('],pagi')[0].replace(',', '!').replace('date:', '').replace('name:', '').replace('code:', '').replace('cases:daily:', '').replace('cumulative:', '').replace('deaths:daily:', '').replace('None', '0').split('}}')
        dataArrayInit0.append(data)
        for d in data:
            #print(d)
            dataArray.append(d.replace('}', ''))
            
        avg = 0
        avgD = 0
        try:
          for x in dataArray:
              #print(x)
              avg = avg + int(x.split('!')[3])
              avgD = avgD + int(x.split('!')[5])
              #print(x.split('!')[3])
        except:
          pass
        
        highC = '0!0'
        highD = '0!0'
        for x in dataArray:
          try:
            if int(x.split('!')[3]) > int(highC.split('!')[0]):
              highC = x.split('!')[3] + '!' + x.split('!')[0]
            if int(x.split('!')[5]) > int(highD.split('!')[0]):
              highD = x.split('!')[5] + '!' + x.split('!')[0]
          except:
            pass
        
        highC = highC.split('!')
        highD = highD.split('!')
        
        trendC = int((int(dataArray[1].split('!')[3]) + int(dataArray[2].split('!')[3]) + int(dataArray[3].split('!')[3]) + int(dataArray[4].split('!')[3]) + int(dataArray[5].split('!')[3]) + int(dataArray[6].split('!')[3]) + int(dataArray[7].split('!')[3])) / 7)
        trendD = int((int(dataArray[3].split('!')[5]) + int(dataArray[4].split('!')[5]) + int(dataArray[5].split('!')[5]) + int(dataArray[6].split('!')[5]) + int(dataArray[7].split('!')[5]) + int(dataArray[8].split('!')[5]) + int(dataArray[9].split('!')[5])) / 7)
        avg = int(avg / len(dataArray))
        avgD = int(avgD / len(dataArray))

        var.write('avgCases',str(avg))
        var.write('avgDeaths',str(avgD))
        var.write('lastCases',str([dataArray[0].split('!')[3],dataArray[0].split('!')[0]]))
        if int(dataArray[0].split('!')[5]) == 0:
            if int(dataArray[1].split('!')[5]) != 0:
                var.write('lastDeaths',str([dataArray[1].split('!')[5],dataArray[1].split('!')[0]]))
            else:
                var.write('lastDeaths',str([dataArray[0].split('!')[5],dataArray[0].split('!')[0]]))
        else:
            var.write('lastDeaths',str([dataArray[0].split('!')[5],dataArray[0].split('!')[0]]))
        var.write('highCases',str(highC))
        var.write('highDeaths',str(highD))

        try:
          if (int(dataArray[0].split('!')[3]) > int(trendC)):
            trendStateC = '▲ - cases increasing'
          elif (int(dataArray[2].split('!')[3]) < int(trendC)):
            trendStateC = '▼ - cases decreasing'
          elif (int(dataArray[2].split('!')[3]) == int(trendC)):
            trendStateC = '■ - cases stabilising'
          else:
            trendStateC = '✘ - A unknown error occured'
        except:
            trendStateC = '✘ - A unknown error occured'

        try:
          if (int(dataArray[2].split('!')[5]) > int(trendD)):
            trendStateD = '▲ - deaths increasing'
          elif (int(dataArray[2].split('!')[5]) < int(trendD)):
            trendStateD = '▼ - deaths decreasing'
          elif (int(dataArray[2].split('!')[5]) == int(trendD)):
            trendStateD = '■ - deaths stabilising'
          else:
            trendStateD = '✘ - A unknown error occured'
        except:
          trendStateD = '✘ - A unknown error occured'

        time.sleep(delay)
    
  var.write('dataStrmStart','False')
  var.write('strmData','n')
  var.write('refreshes','0')
  var.write('processingAmount','0')
  var.write('appVer','1.0.2')
  api.start()
  
  while True:
    if var.read('dataStrmStart') == 'True':
        dataStrm()
    #print('')
    #print('See Coronavirus statistics for a specific day in the year. Use the date format: yyyy-mm-dd, for days or months with only 1 digit, put a 0 in front, for example: 2020-09-20. Data for weekends may be inaccurate for a couple days')
    #print('')
    #while True:
    #  try:
    #    req = input('See information for a date (UK): ')
    #    if int(req.split('-')[0]) == today.year:
    #      for x in dataArray:
    #        if req in x:
    #          print('Date: ' + x.split('!')[0])
    #          print('    Recorded cases: ' + x.split('!')[3])
    #          print('    Recorded deaths: ' + x.split('!')[5])
    #          print('')
    #    else:
    #      if int(req.split('-')[0]) < 2020:
    #        print('Dates before 2020 are not currently indexed')
    #      if int(req.split('-')[0]) > today.year:
    #        print("Are you sure you're from the future?")
    #  except:
    #    print('That date is either invalid or there is no data for it')