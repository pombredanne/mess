'''
Helper functions
'''
from datetime import datetime as dt
from datetime import timedelta as td
import re
from InfluxThreader import InfluxThreader
from InfluxThreader import InfluxClientSender
import traceback

from influxdb import InfluxDBClient


def getInfluxStr(**args):
    response = args['rsp']
    hostname = args['hst']
    system = args['stm']
    nanodate = args['ndate']
    responsedb = args['measure']

    if args['log'] == "DB":
        operation = args['op']
        table = args['tbl']
        JSON = {
                "measurement" : responsedb,
                "tags": {
                    "host": hostname,
		    "system": system,
                    "operation" : operation,
                    "table": table
                },
                "time": nanodate,
                "fields": {
                    "value": int(response)
                }
                }
    elif args['log'] == "VODS":
        function = args['func']
        category = args['cat']
        JSON = {
                "measurement" : responsedb,
                "tags": {
                    "host": hostname,
                    "function": function,
		    "system": system,
                    "category": category
                },
                "time": nanodate,
                "fields": {
                    "value": int(response)
                }
                }
    else:
        function = args['func']
        JSON = {
                "measurement" : responsedb,
                "tags": {
                    "host": hostname,
		    "system": system,
                    "function": function
                },
                "time": nanodate,
                "fields": {
                    "value": int(response)
                }
                }
    print JSON
    return JSON

def getFunction(line, log):
    line = line.replace('[', '(')
    if "call" in line.split(log)[1]:
        function = re.sub(' ', '', line.split(log)[1].split("call")[0].split("(")[0])
    else:
        function = re.sub(' ', '', line.split(log)[2].split("call")[0].split("(")[0])
    return function

def getDbStuff(line):
    dbOps = {'insert': 'into', 'select': 'from', 'delete': 'from', 'update': 'update'}
    for ops in dbOps.keys():
        if ops in line:
            operation = ops
            table = line.split(dbOps[ops])[1].split()[0].split("(")[0].split(")")[0]
            break
    return operation, table

def convertDate(dateStr):
    dateFormat = "%Y-%m-%d %H:%M:%S,%f"
    influxFormat = "%Y-%m-%dT%H:%M:%S.%fZ"
    myDate = dateStr[1:-1]
    influxDate = (dt.strptime(myDate, dateFormat) - td(hours=2)).strftime(influxFormat)
    return influxDate

def getTheLine(obj, measure, line):
    response = re.sub('ms', '', line.rsplit(None, 1)[-1])
    hostname = line.split()[3]
    system = hostname.split('-')[1]
    splitStr = "MSG" if "_MSG " in line else "TIME"
    nanodate = re.sub('\n', '', convertDate(line.split(splitStr)[1].split("DEBUG")[0]))

    for log in obj:
        if log in line:
            if log == "DB":
                operation, table = getDbStuff(line)
                influx = getInfluxStr(measure=measure[log], rsp=response, hst=hostname, stm=system, ndate=nanodate, op=operation, tbl=table, log=log)
                return influx
                break
            elif log == "VODS" and 'XAVIER' not in line:
                function = getFunction(line, log)
                category = function.split('.')[0][:3].lower()
                influx = getInfluxStr(measure=measure[log], rsp=response, hst=hostname, stm=system, ndate=nanodate, cat=category, func=function, log=log)
                return influx
                break
            else:
                function = getFunction(line, log)
                influx = getInfluxStr(measure=measure[log], rsp=response, hst=hostname, stm=system, ndate=nanodate, func=function, log=log)
                return influx
                break

def processlines(obj, dbhost, dbport):
    #logs = [XAVIER, VODS, etc]
    #measure = {VODS: vodsresponses, CYCLOPS: cyclopsresponses, etc}
    logs = obj.logs
    measure = obj.dbDict
    dataList = []

    for line in obj.full:
        try:
            sendToInflux = getTheLine(logs, measure, line)
            dataList.append(sendToInflux)
        except Exception as e:
            print "ERROR in processlines(): %s\n" % e
            print "--- %s" % line
            #traceback.print_exc(file=sys.stdout)
            #raise e
            pass
    try:
        threading = InfluxThreader(dbhost, dbport, dataList)

    except Exception as e:
        print "ERROR in processlines().threader: %s" % e

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
