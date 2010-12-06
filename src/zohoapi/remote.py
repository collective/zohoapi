
import urllib
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from zohoapi import config

try:
    import json
except:
    import simplejson as json

# Register the streaming http handlers with urllib2
register_openers()


class Response(object):
    """ Response objects
    """

    def __init__(self, response):
        self._raw_response = response
        self._response = dict()

        try:
            self._response = json.loads(response)['result']
        except:
            for line in response.split('\n'):
                if line.strip():
                    key, value = line.split('=', 1)
                    key = key.lower()
                    if value == 'TRUE':
                        value = True
                    elif value == 'FALSE':
                        value = False
                    self._response[key] = value

    def getattr(self, key):
        return self._response.get(key, None)

    def __str__(self):
        return self._raw_response


def remote(apikey, mode, filename, documentid, saveurl,
           content=None, url=None, skey=None, format=None,
           output='url', lang='en'):
    """ Zoho Remote API
    """

    apiurl = ''
    data = {'apikey': apikey, 'id': documentid, 'saveurl': saveurl}

    # mode must be valid
    assert mode in config.REMOTE_API_MODES
    data['mode'] = mode

    # filename type must be supported
    filetype = filename.split('.')[-1]
    assert filetype in (config.WRITER_TYPES + \
                        config.SHEET_TYPES + \
                        config.SHOW_TYPES)
    data['filename'] = filename
    if filetype in config.WRITER_TYPES:
        apiurl = config.REMOTE_API_WRITER_URL
    elif filetype in config.SHEET_TYPES:
        apiurl = config.REMOTE_API_SHEET_URL
    elif filetype in config.SHOW_TYPES:
        apiurl = config.REMOTE_API_SHOW_URL

    # user must provide content _or_ url
    assert (content and url) or (not content or not url)
    if content:
        data['content'] = content
    if url:
        data['url'] = url

    # skey tell us wheather we want to use http or https
    if skey is not None:
        apiurl = apiurl.replace('http://', 'https://')
        data['skey'] = skey

    # default to filename format
    if format is None:
        format = filetype
    data['format'] = format

    # output shoul be valid type
    assert output in config.REMOTE_API_OUTPUTS
    data['output'] = output

    # language must be supported by the api
    if filetype in config.WRITER_TYPES:
        assert lang in config.WRITER_LANGUAGES
    elif filetype in config.SHEET_TYPES:
        assert lang in config.SHEET_LANGUAGES
    elif filetype in config.SHOW_TYPES:
        assert lang in config.SHOW_LANGUAGES
    data['lang'] = lang

    # talk with zoho servers
    if content:
        datagen, headers = multipart_encode(data)
        request = urllib2.Request(apiurl, datagen, headers)
        try:
            response = Response(urllib2.urlopen(request).read())
        except urllib2.HTTPError, error:
            response = Response(error.read())
    elif url:
        raise

    # handle response
    return response


def remote_status(apikey, documentid, documenttype):
    """ Status of document
    """

    documenttype = documenttype.lower()
    if documenttype == 'writer':
        url = config.REMOTE_API_WRITER_STATUS_URL
    elif documenttype == 'sheet':
        url = config.REMOTE_API_SHEET_STATUS_URL
    elif documenttype == 'show':
        url = config.REMOTE_API_SHOW_STATUS_URL

    params = dict(
        doc=documentid,
        apikey=apikey,
        )
    url += "?" + (urllib.urlencode(params))
    response = Response(urllib2.urlopen(urllib2.Request(url, None)).read())

    return response
