import datetime
import os
import requests
from requests.cookies import extract_cookies_to_jar
import simplejson as json
from pmb_py import PmbError
from pmb_py.domain.query_result import QueryResult

_session = None

PMBAPI_URL = os.environ['PMB_API_URL']


class Session:
    service_root = PMBAPI_URL
    if os.environ.get('DEBUG') in ('True', 'true', True):
        service_root = os.environ.get('PMB_API_URL_DEBUG', 'http://127.0.0.1:5000') 
    headers = {'user-agent': 'pmb-py 0.4.1',
               'accept': '*/*',
               'content-type': 'application/json'}

    def __init__(self):
        self.cookies = requests.cookies.RequestsCookieJar()
        self.user = None
        self.auth_status = False

    def authorization(self, user, pw):
        '''get token, presver token in cookie

        Args:
            user(str): user name
            pw(str): password

        Returns:
            bool: bool
        '''

        
        url = '/'.join([PMBAPI_URL, 'login'])
        try:
            resp = requests.post(url, auth=(user, pw), headers=self.headers)
        except requests.ConnectionError as _:
            raise PmbError(
                'Services seems not available, Please connect administrator')

        if resp.status_code == 200 and resp.text:
            cookies_data = resp.headers.get('Set-Cookie')
            if cookies_data:
                self.__set_cookie(cookies_data)


            self.auth_status = True
            self.user = user
            return True
        else:
            return False




    def __set_cookie(self, set_cookie_info):
        if not set_cookie_info:
            return

        cookie_item = set_cookie_info.split(';')[0]
        cookie_key, cookie_value = cookie_item.split('=')
        self.cookies.set(cookie_key, cookie_value, path='/')

    def get(self, api, params={}, kwargs={}):
        return self.__request('get', api, params, kwargs=kwargs)

    def post(self, api, params={}, data={}, kwargs={}):
        return self.__request('post', api, params, data, kwargs)

    def put(self, api, params={}, data={}, kwargs={}):
        return self.__request('put', api, params, data, kwargs)

    def patch(self, api, params={}, data={}, kwargs={}):
        return self.__request('patch', api, params, data, kwargs)

    def delete(self, api, params={}, data={}, kwargs={}):
        return self.__request('delete', api, params, data, kwargs)

    def __request(self, method, api, params={}, data={}, kwargs={}):
        url = '/'.join([self.service_root, api])
        dumped_data = json.dumps(data)
        request_kargs = {
            'headers': self.headers,
            'cookies': self.cookies,
            'params': params,
            'data': dumped_data
        }
        if kwargs:
            request_kargs['allow_redirects'] = kwargs.get(
                'allow_redirects', True)

        resp = requests.request(method, url, **request_kargs)
        if 'access_token' not in self.cookies.items():
            extract_cookies_to_jar(self.cookies, resp.request, resp.raw)
        else:
            for cookie in self.cookies:
                if cookie.name == 'access_token':
                    if cookie.expires <= datetime.datetime.now():
                        self.cookies.pop('access_token')

        # 處理 responds 的 access_token,拿到新 access_token 就加入，沒日到新的代表有舊的，就看看過期了沒

        self.__check_response_stat(resp)
        if resp.status_code == requests.codes['NOT_FOUND']:
            if method == 'delete':
                return False
            try:
                int(resp.url.split('/')[-1])  # 看看網址最後帶的是不是整數來判斷是不是 id, 如果是 id，又是 not found, 就是報錯
            except ValueError:
                return QueryResult()
            raise PmbError('Not Found')
        
        if method == 'delete'and resp.status_code == requests.codes['NO_CONTENT']:
            return True
        j_obj = self.__parse_json(resp.text)
        if 'next' in j_obj and j_obj['next'] is not None:
            return QueryResult(j_obj['limit'], j_obj['next'], j_obj['previous'], j_obj['results'], j_obj['start'], j_obj['total_count'])
        # 如果是 pagenation 的呼叫就回傳 QueryResult
        
        return j_obj

    def __check_response_stat(self, resp):
        if resp.status_code not in [requests.codes['ok'], requests.codes['NOT_FOUND'], requests.codes['created'], requests.codes['NO_CONTENT']]:
            if resp.status_code == 500:
                msg = "The Monkey working in server do some thing wrong:"
                msg += resp.text
                raise PmbError(msg)
            else:
                msg = 'status: {}, text: {},\nurl: {}'.format(resp.status_code, resp.text, resp.url)
                raise PmbError(msg)

    def __parse_json(self, json_str):
        try:
            j_obj = json.loads(json_str)
            return j_obj
        except ValueError as e:
            raise PmbError(e)

    def log_out(self):
        global _session
        _session = None
        return True


def log_in(ac, pw):
    '''log in to pmb

        ac: user accout
        pw: passworb
        mode: 'ad' or 'pmb', switch difference log in method
    '''
    from pmb_py.core import Session
    global _session
    if _session and _session.user:
        return _session
    else:
        _session = Session()
        if not _session.authorization(ac, pw):
            return False
        return True


def log_out():
    global _session
    if _session and _session.user:
        return _session.log_out()
    else:
        raise PmbError('Not In Log-in Status')
