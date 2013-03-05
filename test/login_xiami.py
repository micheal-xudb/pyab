#!/usr/bin/python
#coding=utf-8

import urllib
import urllib2


def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    #enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()


def main():
    posturl = "http://www.xiami.com/member/login"
    data = {'email': 'micheal.xudb@foxmail.com', 'password': 'Micheal123$', 'autologin': '1', 'submit': '登 录', 'type': ''}
    print post(posturl, data)

if __name__ == '__main__':
    main()