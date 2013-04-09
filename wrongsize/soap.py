# coding: utf-8

import sys
import logging
logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

from datetime import datetime
from suds.client import Client

from settings import *


def make_request(name, *args):
    client = get_client(name)
    return client.service.Execute(*args)

def get_url(endpoint, prefix=None):
    return '%s%s' % (prefix or SOAP_URL_PREFIX, endpoint)

def get_client(name, prefix=None):
    url = '%s?wsdl' % get_url(name, prefix=prefix)
    # Disable caching
    client = Client(url, faults=False, cache=None)
    return client


class SoapBase(object):
    def __init__(self):
        self.cookie = None
        self.prefix = None

    def set_cookie(self, cookie):
        self.cookie = cookie

    def __getattr__(self, name):
        def func(*args, **kws):
            client = get_client(name, self.prefix)
            silent = kws.pop('silent', False)
            if not silent:
                pass

            headers = kws.pop('headers', {})
            if 'Cookie' not in headers and self.cookie:
                headers.update({'Cookie': self.cookie})
            client.options.headers.update(headers)

            if not silent:
                print name
                print datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S')
                print client.wsdl.url

            rslt = None
            try:
                rslt = client.service.Execute(*args, **kws)
                assert rslt[0] in (200, 201, 202, 204)
            except AssertionError:
                print 'Error: %s' % rslt[0]
                return rslt
            except:
                print >> sys.stderr, u'Error'
            finally:
                if not silent:
                    print 'Request\n', '-' * 80
                    print client.last_sent()

            if not silent:
                print 'Response\n', '-' * 80
                print client.last_received()
                print '\n'
                # print rslt

            return rslt
        return func


class Soap(SoapBase):
    pass


if __name__ == '__main__':
    ws = Soap()
    ws.dosth()

