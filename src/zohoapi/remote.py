
import urllib
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise Exception('simplejson is missing.')


# remote api settings 
WRITER_URL = 'http://writer.zoho.com/remotedoc.im'
WRITER_STATUS_URL = 'http://writer.zoho.com/remotedocStatus.im'
WRITER_TYPES = ['doc', 'docx', 'html', 'pdf', 'sxw', 'odt', 'rtf', 'txt']
WRITER_LANGUAGES = ['en', 'da', 'de', 'es', 'hu', 'it', 'ja', 'nl', 'pl',
        'pt', 'pt_BR', 'pt_EU', 'ru', 'sv', 'tr', 'zh', 'zh_CN']

SHEET_URL = 'http://sheet.zoho.com/remotedoc.im'
SHEET_STATUS_URL = 'http://sheet.zoho.com/remotedocStatus.im'
SHEET_TYPES = ['xls', 'xlsx', 'ods', 'sxc', 'csv', 'tsv', 'pdf']
SHEET_LANGUAGES = ['en', 'da', 'de', 'es', 'it', 'ja', 'nl', 'pl', 'pt',
        'ru', 'sv', 'tr', 'zh', 'bg', 'ca', 'cz', 'eo', 'no', 'ro']

SHOW_URL = 'http://show.zoho.com/remotedoc.im'
SHOW_STATUS_URL = 'http://show.zoho.com/remotedocStatus.im'
SHOW_TYPES = ['ppt', 'pps', 'odp', 'sxi']
SHOW_LANGUAGES = ['en', 'da', 'de', 'es', 'it', 'ja', 'nl', 'pt_BR',
        'pt_EU','sv', 'tr', 'zh']

MODES = ['view', 'normaledit', 'collabview', 'collabedit']
OUTPUTS = ['view', 'viewurl', 'url', 'editor']


# Register the streaming http handlers with urllib2
register_openers()


class RemoteResponse(object):
    """ Response object
    """

    def __init__(self, response):
        self._response = response
        for key in response.keys():
            setattr(self, key, response[key])

    def __str__(self):
        return self._response


class Remote(object):
    """
    """

    def __init__(self, apikey, saveurl, skey=None):
        self.apikey = apikey
        self.saveurl = saveurl
        self.skey = skey

    def _raw_remote(self, mode, filename, documentid, content,
                    format, output, lang, username=None):
        """ url parameter is skipped since (for now) we only do
            form requests on remote api.
        """

        # validate
        assert mode in MODES
        assert output in OUTPUTS
        assert format in (WRITER_TYPES + SHEET_TYPES + SHOW_TYPES)
        if format in WRITER_TYPES:
            assert lang in WRITER_LANGUAGES
        elif format in SHEET_TYPES:
            assert lang in SHEET_LANGUAGES
        elif format in SHOW_TYPES:
            assert lang in SHOW_LANGUAGES

        # data to send
        DATA = {
                'apikey': self.apikey,
                'saveurl': self.saveurl,
                'id': documentid,
                'content': content,
                'mode': mode,
                'filename': filename,
                'format': format,
                'output': output,
                'lang': lang,
               }

        # calculate url which to request
        URL = ''
        if format in WRITER_TYPES:
            URL = WRITER_URL
        elif format in SHEET_TYPES:
            URL = SHEET_URL
        elif format in SHOW_TYPES:
            URL = SHOW_URL

        # skey tell us wheather we want to use http or https
        if self.skey is not None:
            URL = URL.replace('http://', 'https://')
            DATA['skey'] = self.skey

        if username is not None:
            DATA['username'] = username

        # request data
        datagen, headers = multipart_encode(DATA)
        request = urllib2.Request(URL, datagen, headers)
        try:
            return urllib2.urlopen(request).read()
        except urllib2.HTTPError, error:
            return error.read()

    def _raw_status(self, doctype, documentid):
        DATA = {
                'apikey': self.apikey,
                'doc': documentid,
               }

        URL = None
        doctype = doctype.lower()
        if doctype == 'writer':
            URL = WRITER_STATUS_URL
        elif doctype == 'sheet':
            URL = SHEET_STATUS_URL
        elif doctype == 'show':
            URL = SHOW_STATUS_URL

        URL += "?" + (urllib.urlencode(DATA))
        try:
            return urllib2.urlopen(urllib2.Request(URL, None)).read()
        except urllib2.HTTPError, e:
            return e.read()

    def _parse_response(self, response):
        _response = dict()
        for line in response.split('\n'):
            if line.strip():
                key, value = line.split('=', 1)
                key = key.lower().strip()
                value = value.strip()
                if value == 'TRUE':
                    value = True
                elif value == 'FALSE':
                    value = False
                elif value == 'NULL':
                    value = None
                _response[key] = value
        return RemoteResponse(_response)

    def _parse_status_response(self, response):
        try:
            return RemoteResponse(json.loads(response)['result'])
        except:
            return self._parse_response(response)

    def remote(self, *arg, **kw):
        return self._parse_response(self._raw_remote(*arg, **kw))

    def status(self, *arg, **kw):
        return self._parse_status_response(self._raw_status(*arg, **kw))

    def doctype(self, format):
        doctype = None
        if format in WRITER_TYPES:
            doctype = 'writer'
        elif format in SHEET_TYPES:
            doctype = 'sheet'
        elif format in SHOW_TYPES:
            doctype = 'show'
        assert doctype is not None
        return doctype

    def collab_edit(self, documentid, filename, content, format, lang):
        """ helper methos to call remote api for collab editing of documents
        """
        return self.remote(
            mode='collabedit',
            output='url',
            documentid=documentid,
            filename=filename,
            content=content,
            format=format,
            lang=lang,
            )
