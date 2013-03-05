import urllib2
import urllib
import ast

def get_taobao_api_data(app_para_dct):
    content = ""
    if app_para_dct:
        # para_dct = {}
        # para_dct['a'] = 'a'
        # para_dct['b'] = 'b'
        para_str = "{'a': 'a', 'b', 'b'}"

        para_dct = ast.literal_eval(para_str)

        url = """http://gw.api.taobao.com/router/rest"""
        para_data = urllib.urlencode(para_dct)
        f = urllib2.urlopen(url, para_data)
        content = f.read()
    return content

if __name__ == '__main__':
    print get_taobao_api_data(1)