# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

# This code is so you can run the samples without installing the package,
# and should be before any import touching nikola, in any file under tests/
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest

from os.path import dirname, join

#from pelican import readers
from nikola.utils import LOGGER
import logbook

RESOURCES_PATH = join(dirname(__file__), 'test-resources')


class TestMicrodata(unittest.TestCase):

    #### `TestCase` protocol ##################################################

    @staticmethod
    def setUpClass():
        LOGGER.notice('--- TESTS FOR microdata')
        LOGGER.level = logbook.WARNING

    @staticmethod
    def tearDownClass():
        sys.stdout.write('\n')
        LOGGER.level = logbook.NOTICE
        LOGGER.notice('--- END OF TESTS FOR microdata')

    def setUp(self):
        super(TestMicrodata, self).setUp()

        #import microdata
        #microdata.register()

    def assert_rst_equal(self, rstfile, expected):
        filename = join(RESOURCES_PATH, rstfile)
        #content, _ = readers.read_file(filename)
        self.assertEqual(content.strip().replace('\n', ''), expected.strip())

    def test_itemprop(self):
        expected = (
            '<p>'
            '<span itemprop="name">Test</span>'
            '</p>'
        )
        self.assert_rst_equal('microdata_itemprop.rst', expected)

    def test_itemprop_url(self):
        expected = '<p><a href="http://somewhere/" itemprop="url">Test</a></p>'
        self.assert_rst_equal('microdata_itemprop_url.rst', expected)

    def test_itemscope(self):
        expected = (
            '<div itemscope itemtype="http://data-vocabulary.org/Person">'
            'My name is <span itemprop="name">John Doe</span>'
            '</div>'
        )
        self.assert_rst_equal('microdata_itemscope.rst', expected)

    def test_itemscope_tag(self):
        expected = (
            '<p itemscope itemtype="http://data-vocabulary.org/Person">'
            'My name is <span itemprop="name">John Doe</span>'
            '</p>'
        )
        self.assert_rst_equal('microdata_itemscope_tag.rst', expected)

    def test_nested_scope(self):
        expected = (
            '<div itemscope itemtype="http://data-vocabulary.org/Person">'
            '<p>'
            'My name is <span itemprop="name">John Doe</span>'
            '</p>'
            '<p itemprop="address" itemscope itemtype="http://data-vocabulary.org/Address">'
            'My name is <span itemprop="name">John Doe</span>'
            '</p>'
            '</div>'
        )
        self.assert_rst_equal('microdata_itemscope_nested.rst', expected)

    def test_nested_scope_compact(self):
        expected = (
            '<p itemscope itemtype="http://data-vocabulary.org/Person">'
            'My name is <span itemprop="name">John Doe</span>'
            '<span itemprop="address" itemscope itemtype="http://data-vocabulary.org/Address">'
            'My name is <span itemprop="name">John Doe</span>'
            '</span>'
            '</p>'
        )
        self.assert_rst_equal('microdata_itemscope_nested_compact.rst', expected)

if __name__ == "__main__":
    unittest.main()
