
import unittest
import doctest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        doctest.DocFileSuite('remote.rst'),
        ])
    return suite
