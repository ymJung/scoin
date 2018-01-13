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
# etc (이더리움 클래식 거래 기준), eth (이더리움 거래 기준), xrp (리플 거래 기준), bch (비트코인 캐시 기준)
coin_fields = ['btc_krw', 'etc_krw', 'eth_krw', 'xrp_krw', 'bch_krw']
def get_res(type, code):  # type (TICKER, DETAILD)
    if code not in coin_fields:
        raise Exception('code field is not found. use only ', coin_fields)
    url = cf.get('KOR_BIT', type) + "?currency_pair=" + cf.get('KOR_BIT', code)
    res = requests.get(url)
    return res


def get_order_book(code):
    return get_res('ORDER_BOOK', code)


def get_transactions(code, time):
    url = cf.get('KOR_BIT', 'TRANSACTIONS') + "?currency_pair=" + cf.get('KOR_BIT', code) + "&time=" + time
    res = requests.get(url)
    return res


def get_access_payload(grant_type, token):
    payload = {
        'client_id': cf.get('KOR_BIT', 'ACC-KEY'),
        'client_secret': cf.get('KOR_BIT', 'SEC-KEY'),
        'grant_type': grant_type  # refresh_token #password
    }
    if grant_type is 'password':
        payload['grant_type'] = "password"
        payload['username'] = cf.get('KOR_BIT', 'USER_NAME')
        payload['password'] = cf.get('KOR_BIT', 'SEC-USER_PWD')
    elif grant_type is 'refresh_token':
        payload['refresh_token'] = token['refresh_token']
    return payload


def create_acc_token():
    return post_acc_request(get_access_payload('password', token=None))


def refresh(token):
    return post_acc_request(get_access_payload('refresh_token', token))


def post_acc_request(payload):
    return requests.post(url=cf.get('KOR_BIT', 'ACCESS_URL'), data=payload)

def get_headers(token):
    return {'Accept': 'application/json',
               'Authorization': "{} {}".format(token['token_type'], token['access_token'])}

def get_user_info(token):
    return requests.get(url=cf.get('KOR_BIT', 'USER_URL'), headers=get_headers(token))

import time
def get_nonce():
    return int(time.time() * 1000)
# currency_pair	비트코인 거래 기준으로 필드값을 가져온다.
# ## etc_krw(이더리움 클래식 거래 기준), eth_krw(이더리움 거래 기준), xrp_krw(리플 거래 기준), bch_krw(비트코인 캐시 기준)를 지정할 수 있으며, 이 외에 다른 코인은 지원하지 않는다.
# type	주문 형태. “limit” : 지정가 주문, “market” : 시장가 주문.
# price	비트코인의 가격(원화). 500원 단위로만 가능하다. 지정가 주문(type=limit)인 경우에만 유효하다. ETH는 50원 단위, ETC는 10원 단위로 가격을 설정할 수 있다.
# coin_amount
# ## 매수하고자 하는 코인의 수량. 정가 주문인 경우에는 해당 수량을 price 파라미터에 지정한 가격으로 구매하는 주문을 생성한다. 시장가 주문인 경우에는 해당 수량을 시장가에 구매하는 주문을 생성하며,
# ## price 파라미터와 coin_amount 파라미터는 사용되지 않는다.
# fiat_amount	코인을 구매하는데 사용하고자 하는 금액(원화). 시장가 주문(type=market)인 경우에만 유효하며, 이 파라미터를 사용할 경우 price 파라미터와 coin_amount 파라미터는 사용할 수 없다.

 currency_pairs = ['etc_krw', #(이더리움 클래식 거래 기준)
                   'eth_krw', #(이더리움 거래 기준)
                   'xrp_krw', #(리플 거래 기준),
                   'bch_krw' ]#(비트코인 캐시 기준)

def get_order_payload(bid_type, currency_pair, price=None, coin_amount=None, fiat_amount=None): #price 우선.
    if currency_pair not in currency_pairs:
        raise Exception('code field is not found. use only ', currency_pairs)
    if price is not None:
        coin_amount = None
    if bid_type in ['limit', 'market'] is False:
        raise Exception('invalid param')
    if fiat_amount is not None:
        if bid_type is not 'market' or price is not None or coin_amount is not None:
            raise Exception('use fiat amount. it is only use "market" bid_type. So does not use "price" and "coin_amount". (set to None) ')
    # bid_types = ['limit', 'market']
    return {
        'currency_pair': currency_pair,
        'type': bid_type,
        'price': price,
        'coin_amount': coin_amount,
        'fiat_amount': fiat_amount,
        'nonce': get_nonce()
    }

def order_buy_price(price, ):
    requests.post(url=cf.get('KOR_BIT', 'ORDER_BUY'), get_order_payload(bid_type='limit', currency_pair=)
