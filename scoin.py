import requests
import configparser
cf = configparser.ConfigParser()
cf.read('config.cfg')

# timestamp	최종 체결 시각.
# last	최종 체결 가격.
# bid	최우선 매수호가. 매수 주문 중 가장 높은 가격.
# ask	최우선 매도호가. 매도 주문 중 가장 낮은 가격.
# low	(최근 24시간) 저가. 최근 24시간 동안의 체결 가격 중 가장 낮 가격.
# high	(최근 24시간) 고가. 최근 24시간 동안의 체결 가격 중 가장 높은 가격.
# volume	거래량.
#etc (이더리움 클래식 거래 기준), eth (이더리움 거래 기준), xrp (리플 거래 기준), bch (비트코인 캐시 기준)
codes = {"BTC", "ETC", "ETH", "XRP", "BCH"}

def get_res(type, code):# type (TICKER, DETAILD)
    url = cf.get('KOR_BIT', type) + "?currency_pair=" + cf.get('KOR_BIT', code)
    res = requests.get(url)
    return res

def get_order_book(code):
    return get_res('ORDER_BOOK', code)

def get_transactions(code, time):
    url = cf.get('KOR_BIT', 'TRANSACTIONS') + "?currency_pair=" + cf.get('KOR_BIT', code) + "&time=" + time
    res = requests.get(url)
    return res


import time
import urllib
import json

post_data = {
    'nonce': int(time.time()*1000),
    'access_token': cf.get('COINONE', 'API_KEY'),

}


