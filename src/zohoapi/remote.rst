
    >>> from zohoapi import remote

    >>> url = remote(apikey="5b3f8955bb4a3e90462d165cbe73451b",
    ...        mode="normaledit",
    ...        filename="test.doc",
    ...        documentid="12345",
    ...        saveurl="http://zohotest.garbas.si/saveurl",
    ...        content=open('test.doc', 'rb'),
    ...        skey="9fdf3da9267d2b605427c37aaab6254f")
    >>> print url
    https://writer.zoho.com/editor.im?doc=...
