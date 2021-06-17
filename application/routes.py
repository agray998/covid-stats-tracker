from application import app
from flask import Flask, request, render_template, url_for
import requests, json
from datetime import date
from matplotlib import pyplot as plt
import numpy as np

@app.route('/')
def home():
    response = requests.get('https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&areaCode=E08000009&metric=newCasesByPublishDateChange&format=json')
    resp_json = response.json()
    dates = []
    newCasesByPublishDateChange = []
    for entry in resp_json['body']:
        dates.append(entry['date'])
        newCasesByPublishDateChange.append(entry['newCasesByPublishDateChange'])
    dates[56:] = []
    newCasesByPublishDateChange[56:] = []
    dates.reverse()
    newCasesByPublishDateChange.reverse()
    seven_day_averages = []
    averages_dates = []
    for i in range(3, len(newCasesByPublishDateChange)-3):
        seven_day_averages.append(sum(newCasesByPublishDateChange[i-3:i+4])/7)
        averages_dates.append(dates[i])
    index = np.arange(len(seven_day_averages)) + 0.3
    plot = plt.bar(index, seven_day_averages, tick_label = averages_dates)
    plt.savefig(f"/static/output_graph{date.today()}.png")
    return render_template('home.html', imgname=f"output_graph{date.today()}.png")
