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
from test_rst_compiler import ReSTExtensionTestCase


class ItemPropTestCase(ReSTExtensionTestCase):

    @staticmethod
    def setUpClass():
        LOGGER.notice('--- TESTS FOR ItemProp')
        LOGGER.level = logbook.WARNING

    @staticmethod
    def tearDownClass():
        sys.stdout.write('\n')
        LOGGER.level = logbook.NOTICE
        LOGGER.notice('--- END OF TESTS FOR ItemProp')

    sample = ':itemprop:`Test <name>`'

    def test_itemprop(self):
        # the result should be
        # <p><span itemprop="name">Test</span></p>
        self.basic_test()
        self.assertHTMLContains("span", attributes={"itemprop": "name"},
                                text="Test")
        self.assertHTMLContains("p")


class ItemPropUrlTestCase(ReSTExtensionTestCase):

    @staticmethod
    def setUpClass():
        LOGGER.notice('--- TESTS FOR ItemPropUrl')
        LOGGER.level = logbook.WARNING

    @staticmethod
    def tearDownClass():
        sys.stdout.write('\n')
        LOGGER.level = logbook.NOTICE
        LOGGER.notice('--- END OF TESTS FOR ItemPropUrl')

    sample = ':itemprop:`Test <url:http://somewhere/>`'

    def test_itemprop_url(self):
        # the result should be 
        # <p><a href="http://somewhere/" itemprop="url">Test</a></p>
        self.basic_test()
        self.assertHTMLContains("a", attributes={"itemprop": "url", "href": "http://somewhere/"},
                                text="Test")
        self.assertHTMLContains("p")


class ItemScopeTestCase(ReSTExtensionTestCase):

    @staticmethod
    def setUpClass():
        LOGGER.notice('--- TESTS FOR ItemScope')
        LOGGER.level = logbook.WARNING

    @staticmethod
    def tearDownClass():
        sys.stdout.write('\n')
        LOGGER.level = logbook.NOTICE
        LOGGER.notice('--- END OF TESTS FOR ItemScope')

    sample = """.. itemscope:: Person

        My name is :itemprop:`John Doe <name>`
    """

    def test_itemscope(self):
        # the result should be 
        # <div itemscope itemtype="http://data-vocabulary.org/Person">
        # My name is <span itemprop="name">John Doe</span>
        # </div>
        self.basic_test()
        self.assertHTMLContains("div", attributes={"itemscope": "", "itemtype": "http://data-vocabulary.org/Person"},
                                text="My name is ")
        self.assertHTMLContains("span", attributes={"itemprop": "name"},
                                text="John Doe")


class ItemScopeTagTestCase(ReSTExtensionTestCase):

    @staticmethod
    def setUpClass():
        LOGGER.notice('--- TESTS FOR ItemScopeTag')
        LOGGER.level = logbook.WARNING

    @staticmethod
    def tearDownClass():
        sys.stdout.write('\n')
        LOGGER.level = logbook.NOTICE
        LOGGER.notice('--- END OF TESTS FOR ItemScopeTag')

    sample = """.. itemscope:: Person  
        :tag: p

        My name is :itemprop:`John Doe <name>`
    """

    def test_itemscope_tag(self):
        # the result should be 
        # <p itemscope itemtype="http://data-vocabulary.org/Person">
        # My name is <span itemprop="name">John Doe</span>
        # </p>
        self.basic_test()
        self.assertHTMLContains("p", attributes={"itemscope": "", "itemtype": "http://data-vocabulary.org/Person"},
                                text="My name is ")
        self.assertHTMLContains("span", attributes={"itemprop": "name"},
                                text="John Doe")


class ItemScopeNestedTestCase(ReSTExtensionTestCase):

    @staticmethod
    def setUpClass():
        LOGGER.notice('--- TESTS FOR ItemScopeNested')
        LOGGER.level = logbook.WARNING

    @staticmethod
    def tearDownClass():
        sys.stdout.write('\n')
        LOGGER.level = logbook.NOTICE
        LOGGER.notice('--- END OF TESTS FOR ItemScopeNested')

    sample = """.. itemscope:: Person

        My name is :itemprop:`John Doe <name>`

        .. itemscope:: Address
            :tag: p
            :itemprop: address

            My name is :itemprop:`John Doe <name>`
    """

    def test_nested_scope(self):
        # the result should be 
        # <div itemscope itemtype="http://data-vocabulary.org/Person">
        # <p>My name is <span itemprop="name">John Doe</span></p>
        # <p itemprop="address" itemscope itemtype="http://data-vocabulary.org/Address">
        # My name is <span itemprop="name">John Doe</span>
        # </p></div>
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
        self.basic_test()
        self.assertHTMLContains("div", attributes={"itemscope": "", 
                                "itemtype": "http://data-vocabulary.org/Person"},
                                text="")
        self.assertHTMLEqual(expected.strip())


class ItemScopeNestedCompactTestCase(ReSTExtensionTestCase):

    @staticmethod
    def setUpClass():
        LOGGER.notice('--- TESTS FOR ItemScopeNestedCompact')
        LOGGER.level = logbook.WARNING

    @staticmethod
    def tearDownClass():
        sys.stdout.write('\n')
        LOGGER.level = logbook.NOTICE
        LOGGER.notice('--- END OF TESTS FOR ItemScopeNestedCompact')

    sample = """.. itemscope:: Person
        :tag: p
        :compact:

        My name is :itemprop:`John Doe <name>`

        .. itemscope:: Address
            :tag: span
            :itemprop: address

            My name is :itemprop:`John Doe <name>`
    """

    def test_nested_scope_compact(self):
        # the result should be 
        # <p itemscope itemtype="http://data-vocabulary.org/Person">
        # My name is <span itemprop="name">John Doe</span>
        # <span itemprop="address" itemscope itemtype="http://data-vocabulary.org/Address">
        # My name is <span itemprop="name">John Doe</span>
        # </span></p>
        expected = (
            '<p itemscope itemtype="http://data-vocabulary.org/Person">'
            'My name is <span itemprop="name">John Doe</span>'
            '<span itemprop="address" itemscope itemtype="http://data-vocabulary.org/Address">'
            'My name is <span itemprop="name">John Doe</span>'
            '</span>'
            '</p>'
        )
        self.basic_test()
        self.assertHTMLContains("p", attributes={"itemscope": "", 
                                "itemtype": "http://data-vocabulary.org/Person"},
                                text="My name is ")
        self.assertHTMLEqual(expected.strip())


if __name__ == "__main__":
    unittest.main()
