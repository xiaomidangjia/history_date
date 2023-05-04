# coding: utf-8

import json
import base64
from flask import Flask, request
import requests
import numpy as np
import pandas as pd
import csv

app = Flask(__name__)


@app.route("/keep_date", methods=['post'])
def keep_date():
    order_date = request.form.get('order_date')
    order_type = request.form.get('order_type')
    order_multi = request.form.get('order_multi')
    order_value = request.form.get('order_value')
    order_id = request.form.get('order_id')
    order_price = request.form.get('order_price')
    order_win = request.form.get('order_win')

    sub_df = pd.DataFrame({'order_date':order_date,'order_type':order_type,'order_multi':order_multi,'order_value':order_value,'order_id':order_id,'order_price':order_price,'order_win':order_win},index=[0])

    # 读取历史开单记录
    p = []
    with open("/root/history_date/量化机器人历史开单记录明细.csv", 'r', encoding="UTF-8") as fr:
        reader = csv.reader(fr)
        for index, line in enumerate(reader):
            if index == 0:
                continue
            p.append(line)
    res_data = pd.DataFrame(p)
    res_data['order_date'] = res_data.iloc[:,0]
    res_data['order_type'] = res_data.iloc[:,1]
    res_data['order_multi'] = res_data.iloc[:,2]
    res_data['order_value'] = res_data.iloc[:,3]
    res_data['order_id'] = res_data.iloc[:,4]
    res_data['order_price'] = res_data.iloc[:,5]
    res_data['order_win'] = res_data.iloc[:,6]

    res_data = res_data[['order_date','order_type','order_multi','order_value','order_id','order_price','order_win']]

    ins = pd.concat([res_data,sub_df])
    ins['order_date'] = pd.to_datetime(ins['order_date'])

    ins = ins.sort_values(by=['order_date'])
    ins = ins[['order_date','order_type','order_multi','order_value','order_id','order_price','order_win']]
    ins.to_csv('history_date.csv',encoding='utf-8-sig',index=False)
    import telegram
    bot = telegram.Bot(token='6219784883:AAE3YXlXvxNArWJu-0qKpKlhm4KaTSHcqpw')
    bot.sendDocument(chat_id='-840309715', document=open('/root/history_date/量化机器人历史开单记录明细.csv', 'rb'))

    res = {'value':'Finish'}
    return res

if __name__ == '__main__':
    app.run("0.0.0.0", port=80)


