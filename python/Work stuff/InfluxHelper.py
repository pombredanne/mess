'''
Helper functions
'''
from datetime import datetime as dt
from datetime import timedelta as td
import re
from InfluxThreader import InfluxThreader

def getInfluxStr(**args):
    response = args['rsp']
    hostname = args['hst']
    nanodate = args['ndate']
    responsedb = args['measure']

    if args['log'] == "DB":
        operation = args['op']
        table = args['tbl']
        JSON = {
                "measurement" : responsedb,
                "tags": {
                    "host": hostname,
                    "operation" : operation,
                    "table": table
                },
                "time": nanodate,
                "fields": {
                    "value": int(response)
                }
                }
        #return JSON
    else:
        function = args['func']
        JSON = {
                "measurement" : responsedb,
                "tags": {
                    "host": hostname,
                    "function": function
                },
                "time": nanodate,
                "fields": {
                    "value": int(response)
                }
                }
    return JSON

def getFunction(line, log):
    function = re.sub(' ', '', line.split(log)[1].split("call")[0].split("(")[0])
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
    nanodate = re.sub('\n', '', convertDate(line.split("TIME")[1].split("DEBUG")[0]))

    for log in obj:
        if log in line:
            if log == "DB":
                operation, table = getDbStuff(line)
                influx = getInfluxStr(measure=measure[log], rsp=response, hst=hostname, ndate=nanodate, op=operation, tbl=table, log=log)
                return influx
                break
            else:
                function = getFunction(line, log)
                influx = getInfluxStr(measure=measure[log], rsp=response, hst=hostname, ndate=nanodate, func=function, log=log)
                return influx
                break

def processlines(obj, dbhost, dbport):
    logs = obj.logs
    measure = obj.dbDict
    dataList = []

    for line in obj.full:
        try:
            sendToInflux = getTheLine(logs, measure, line)
            dataList.append(sendToInflux)
        except Exception as e:
            print "ERROR in processlines(): %s" % e
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