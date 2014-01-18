# -*- coding: utf-8 -*-

# Copyright © 2013-2014 Axel Haustant, Ivan Teoh and others.

# pelican-microdata is LGPL-licensed.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import re

from docutils import nodes
from docutils.parsers.rst import directives, Directive, roles
from nikola.plugin_categories import RestExtension
from nikola.plugins.compile.rest import add_node

RE_ROLE = re.compile(r'(?P<value>.+?)?\s*\<(?P<name>.+)\>')


class Plugin(RestExtension):

    name = "rest_microdata"

    def set_site(self, site):
        self.site = site
        directives.register_directive('itemscope', ItemScopeDirective)
        directives.register_directive('itempropblock', ItemPropDirective)
        roles.register_canonical_role('itemprop', itemprop_role)

        add_node(ItemProp, visit_ItemProp, depart_ItemProp)
        add_node(ItemPropBlock, visit_ItemPropBlock, depart_ItemPropBlock)
        add_node(ItemScope, visit_ItemScope, depart_ItemScope)

        return super(Plugin, self).set_site(site)


class ItemProp(nodes.Inline, nodes.TextElement):
    pass


def itemprop_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    match = RE_ROLE.match(text)
    if not match or not match.group('name'):
        raise ValueError('%s does not match expected itemprop format: :itemprop:`value <name>`')
    value = ''
    if match.group('value'):
        value = match.group('value')
    name = match.group('name')
    info = ''
    tag = 'span'
    if ':' in name:
        # depreciated, use | for nikola
        name, info = name.split(':', 1)
    elif '|' in name:
        names = name.split('|', 2)
        name = names[0]
        if len(names) > 1:
            info = names[1]
        if len(names) > 2:
            tag = names[2]
    return [ItemProp(value, value, name=name, info=info, tag=tag)], []


class ItemPropBlock(nodes.Element):
    def __init__(self, tagname, itemprop, classes=None):
        kwargs = {
            'itemprop': itemprop,
        }
        if classes:
            kwargs['class'] = classes
        super(ItemPropBlock, self).__init__('', **kwargs)
        self.tagname = tagname


class ItemPropDirective(Directive):
    required_arguments = 1
    has_content = True
    option_spec = {
        'tag': directives.unchanged,
        'class': directives.unchanged,
    }

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        itemprop = self.arguments[0]
        tag = self.options.get('tag', 'div')
        classes = self.options.get('class', None)
        node = ItemPropBlock(tag, itemprop, classes)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class ItemScope(nodes.Element):
    def __init__(self, tagname, itemtype, itemprop=None, compact=False, classes=None):
        kwargs = {
            'itemscope': None,
            'itemtype': "http://data-vocabulary.org/%s" % itemtype,
        }
        if itemprop:
            kwargs['itemprop'] = itemprop
        if classes:
            kwargs['class'] = classes
        super(ItemScope, self).__init__('', **kwargs)
        self.tagname = tagname
        self.compact = tagname == 'p' or compact


class ItemScopeDirective(Directive):
    required_arguments = 1
    has_content = True
    option_spec = {
        'tag': directives.unchanged,
        'itemprop': directives.unchanged,
        'compact': directives.unchanged,
        'class': directives.unchanged,
    }

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        itemtype = self.arguments[0]
        tag = self.options.get('tag', 'div')
        itemprop = self.options.get('itemprop', None)
        compact = 'compact' in self.options
        classes = self.options.get('class', None)
        node = ItemScope(tag, itemtype, itemprop, compact, classes)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_ItemProp(self, node):
    if not node['tag']:
        node['tag'] = 'span'

    if node['name'] == 'url':
        node['tag'] = 'a'
        self.body.append(self.starttag(node, node['tag'], '', itemprop=node['name'], href=node['info']))
    elif node['tag'] == 'img':
        self.body.append(self.emptytag(node, node['tag'], '', itemprop=node['name'], src=node['info']))
    elif node['tag'] == 'time':
        # TODO: auto convert the time
        self.body.append(self.starttag(node, node['tag'], '', itemprop=node['name'], datetime=node['info']))
    elif node['tag'] == 'meta':
        # TODO: auto convert the time
        self.body.append(self.emptytag(node, node['tag'], '', itemprop=node['name'], content=node['info']))
    else:
        self.body.append(self.starttag(node, node['tag'], '', itemprop=node['name']))


def depart_ItemProp(self, node):
    end_tag = '</' + node['tag'] + '>'
    if node['tag'] == 'img' or node['tag'] == 'meta':
        return
    self.body.append(end_tag)


def visit_ItemPropBlock(self, node):
    self.body.append(node.starttag())


def depart_ItemPropBlock(self, node):
    self.body.append(node.endtag())


def visit_ItemScope(self, node):
    self.context.append(self.compact_simple)
    self.compact_simple = node.compact
    self.body.append(node.starttag())


def depart_ItemScope(self, node):
    self.compact_simple = self.context.pop()
    self.body.append(node.endtag())
