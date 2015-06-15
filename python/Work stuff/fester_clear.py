from datetime import date, timedelta as td
import datetime
import subprocess


def bashing(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = process.stdout.readline()
    print output


def deletefolder(folder):
    main = "/opt/livelogs/fester-*/"
    deleteme = "rm -rf " + main + folder

    try:
        bashing(deleteme)
    except:
        pass


def main():
    today = date.today() + datetime.timedelta(-7)
    oneweek = today + datetime.timedelta(-7)

    delta = today - oneweek

    for day in range(delta.days + 1):
        remove = today - td(days=day)
        deletefolder(remove.strftime("%Y/%m/%d"))

if __name__ == '__main__':
    main()
