#!/usr/bin/env python
# -*- coding: UTF8 -*-
import codecs;
import os;
import datetime;
import re;
import bitly;
import subprocess;
import time;

##########
# This script will look for an event matching today's date and will tuit it
#
# Requires https://github.com/sferik/t twitter's client
##########

# t update "mi primer tuit"

# api details for bitly
API_USERNAME = 'Usar tu propio username'
API_KEY      = 'Usar tu propia api_key para bitly'

# get current date mm-dd
today = str(datetime.date.today());
today = re.sub("^[0-9]{4}-", "", today);

# create a log file
file_log = open("log.txt", "a");

# read data
file = "coincidencias.txt";
data_file = codecs.open(file, "r", encoding="utf-8");

def format_date(date):
    date = date.strip()
    d = datetime.datetime.strptime(date, "%Y-%m-%d")
    try:
        return d.strftime("%d de %b %Y");
    except:
        date = date.split("-");
        if date[1] == "07":
            month = "Jul";
        return re.sub("^0", "", date[2]) + " de " + month + " " + date[0]

tuits = []

# process data
for line in data_file:
    line = line.split("|");
    # date as mm-dd
    date = re.sub("^[0-9]{4}-", "", line[0].strip())
    if date == today:
        event = line[1].strip()

        link = line[2].strip();
        shortUrl = bitly.Api(login=API_USERNAME, apikey=API_KEY).shorten(link)

        formatted_date = format_date(line[0]);
        f.write(formatted_date + "\n")

        tuit = formatted_date + ": " + event + " " + shortUrl;

        cmd = '/usr/local/bin/t update "' + tuit + '"';
        tuits.append(cmd)

# count number of tuits for today
n_tuits = len(tuits)
if n_tuits > 0:
    timeToSleep = 6.0*60*60/n_tuits
else:
    timeToSleep = 1;

print "N tuits: " + str(n_tuits)
file_log.write("N tuits: " + str(n_tuits) + "\n");

print "Time to sleep between tuits: " + str(timeToSleep)
file_log.write("Time to sleep between tuits: " + str(timeToSleep) + "\n");

for cmd in tuits:
    p = subprocess.check_call(cmd, shell=True);

    if p == 0:
        # sleep for some time within 6 hour shift
        time.sleep(timeToSleep)

data_file.close();
file_log.close();

