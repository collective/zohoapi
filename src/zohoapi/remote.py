
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

from zohoapi.i18n import WRITER_LANGUAGES
from zohoapi.i18n import SHEET_LANGUAGES
from zohoapi.i18n import SHOW_LANGUAGES




# Register the streaming http handlers with urllib2
register_openers()


class Response(object):
    """ Response objects
    """

    def __init__(self, txt=None, json=None):
        self._response = response
        for line in response.split('\n'):
            if line.strip():
                key, value = line.split('=', 1)
                if value == 'TRUE':
                    value = True
                elif value == 'FALSE':
                    value = False
                setattr(self, key.lower(), value)

    def __str__(self):
        return self._response




def remote(apikey, mode, filename, documentid, saveurl,
           content=None, url=None, skey=None, format=None,
           output='url', lang='en'):
    """ Zoho Remote API
    """

    apiurl = ''
    data = {'apikey': apikey, 'id': documentid, 'saveurl': saveurl}

    # mode must be valid
    assert mode in REMOTE_API_MODES
    data['mode'] = mode

    # filename type must be supported
    filetype = filename.split('.')[-1]
    assert filetype in (WRITER_TYPES + SHEET_TYPES + SHOW_TYPES)
    data['filename'] = filename
    if filetype in WRITER_TYPES:
        apiurl = REMOTE_API_WRITER_URL
    elif filetype in SHEET_TYPES:
        apiurl = REMOTE_API_SHEET_URL
    elif filetype in SHOW_TYPES:
        apiurl = REMOTE_API_SHOW_URL

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
    assert output in REMOTE_API_OUTPUTS
    data['output'] = output

    # language must be supported by the api
    if filetype in WRITER_TYPES:
        assert lang in WRITER_LANGUAGES
    elif filetype in SHEET_TYPES:
        assert lang in SHEET_LANGUAGES
    elif filetype in SHOW_TYPES:
        assert lang in SHOW_LANGUAGES
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
    if response.RESULT is True:
        return response.URL
    else:
        raise Exception(response)
