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
codes = {"BTC", "ETC", "ETH", "XRP", "BCH"}


def get_res(type, code):  # type (TICKER, DETAILD)
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
