#very bad python code.
import shutil
import os
import subprocess
import datetime
import json
import config
os.chdir(config.whereami)
d = datetime.datetime.now()
delta = datetime.timedelta(days=1)
deltaweek = datetime.timedelta(days=7)
dp = d - delta
dw = d - deltaweek
year = int(d.strftime("%y"))
month = int(d.strftime("%m"))
day = int(d.strftime("%d"))
lastyear = int(dp.strftime("%y"))
lastmonth = int(dp.strftime("%m"))
lastday = int(dp.strftime("%d"))
weekyear = int(dw.strftime("%y"))
weekmonth = int(dw.strftime("%m"))
weekday = int(dw.strftime("%d"))




def dd(a):
    if a < 10:
        return "0{0}".format(a)
    else:
        return str(a)

md = "{0}{1}".format(dd(month), dd(day))
mdp = "{0}{1}".format(dd(lastmonth), dd(lastday))
todayago = "20{0}-{1}-{2}".format(year, dd(month), dd(day))
yesterdayago = "20{0}-{1}-{2}".format(lastyear, dd(lastmonth), dd(lastday))
aweekago = "20{0}-{1}-{2}".format(weekyear, dd(weekmonth), dd(weekday))
slurmactt = config.slurmactt
compdir = "."
userinfo = config.userinfo
def check_call(arguments, shell=False):
    try:
        return subprocess.check_output(arguments, stderr=subprocess.STDOUT, shell=shell, env=os.environ).decode()
    except subprocess.CalledProcessError as e:
        raise e


def get_avgwait_last_seven_days():
    check_call([slurmactt, "-w", "-n", "-r", "."])
    ret = check_call(["grep", "TOTAL", ".Last_week"])
    clear = [x for x in ret.split(" ") if x != '']
    avgwait = float(clear[-5])
    return avgwait * 3600
def get_avgwait_yesterday():
    check_call([slurmactt, "-s",mdp, "-e", md, "-n", "-r", "."])
    ret = (check_call(["grep", "TOTAL", ".{0}_{1}".format(mdp,md)]))
    clear = [x for x in ret.split(" ") if x != '']
    avgwait = float(clear[-5])
    return avgwait * 3600


def alloc_down_idle_week():
    ret = check_call(["sreport", "cluster", "Utlization", "-n", "start={0}".format(yesterdayago), "end={0}".format(aweekago)])
    erm = [x for x in ret.split(" ") if x != '']
    alloc = int(erm[1])
    down = int(erm[2])
    idle = int(erm[4])
    reported = int(erm[6])
    return ([alloc/reported * 100, down/reported * 100, idle/reported * 100])

def alloc_down_idle_day():
    ret = check_call(["sreport", "cluster", "Utlization", "-n", "start={0}".format(yesterdayago), "end={0}".format(todayago)])
    erm = [x for x in ret.split(" ") if x != '']
    alloc = int(erm[1])
    down = int(erm[2])
    idle = int(erm[4])
    reported = int(erm[6])
    return ([alloc/reported * 100, down/reported * 100, idle/reported * 100])
def top_users(yesaweek=False):
    if yesaweek:
        ret = check_call([userinfo, yesterdayago, todayago])
    else:
        ret = check_call([userinfo, aweekago, todayago])
    ret = check_call(["cat", "log"])
    rets = []
    for p in ret.split("\n"):
        try:
            name = p.split(" ")[0]
            percent = p.split(" ")[1]
            rets.append("{0} ({1})".format(name, percent))
        except:
            break
    return rets


ret = {}

ret["avgwait_yesterday"] = get_avgwait_yesterday()
ret["avgwait_last_week"] = get_avgwait_last_seven_days()
lastday = alloc_down_idle_day()
lastweek = alloc_down_idle_week()
ret["alloc_last_day"] = lastday[0]
ret["down_last_day"] = lastday[1]
ret["idle_last_day"] = lastday[2]
ret["alloc_last_week"] = lastweek[0]
ret["down_last_week"] = lastweek[1]
ret["idle_last_week"] = lastweek[2]
ret["last_updated"] = todayago
ret["top_users_last_day"] = top_users(yesaweek=True)
ret["top_users_last_week"] = top_users()

print("callback({0})".format(ret))
