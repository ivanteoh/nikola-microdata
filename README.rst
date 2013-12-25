Microdata plugin for Nikola
============================

`Microdata`_ semantic markups support for `Nikola`_ static blog generator. 
The original code is at `pelican-microdata`_. It is created to support `recipe 
microdata`_ (`recipe schema`_)in mind. It should support other microdata type. More info, 
please refer to 

Directives
~~~~~~~~~~

Microdata plugin provides two directives:

- ``itemscope``, a block directive allowing to declare an itemscope block:

    .. code-block:: ReST

        .. itemscope:: <Schema type>
            :tag: element type (default: div)
            :itemprop: optionnal itemprop attribute
            :compact: optionnal

            Nested content

- ``itemprop``, an inline directive/role allowing to annotate some text with an itemprop attribute.

    .. code-block:: ReST

        :itemprop:`Displayed text <itemprop name>`
        :itemprop:`Displayed text <itemprop name:http://some.url/>` #depreciated, use | instead
        :itemprop:`Displayed text <itemprop name|itemprop info>` 
        :itemprop:`Displayed text <itemprop name|itemprop info|itemprop tag>` #itemprop tag is optional, default is span or specific tag, depending on the itemprop name, defined in schema.org

Specific itemprop name that currently support:

- url

Example
~~~~~~~

This reStructuredText document:

.. code-block:: ReST

    .. itemscope: Person
        :tag: p

        My name is :itemprop:`Bob Smith <name>`
        but people call me :itemprop:`Smithy <nickanme>`.
        Here is my home page:
        :itemprop:`www.exemple.com <url:http://www.example.com>`
        I live in Albuquerque, NM and work as an :itemprop:`engineer <title>`
        at :itemprop:`ACME Corp <affiliation>`.


will result in:

.. code-block:: html

    <p itemscope itemtype="http://data-vocabulary.org/Person">
        My name is <span itemprop="name">Bob Smith</span>
        but people call me <span itemprop="nickname">Smithy</span>.
        Here is my home page:
        <a href="http://www.example.com" itemprop="url">www.example.com</a>
        I live in Albuquerque, NM and work as an <span itemprop="title">engineer</span>
        at <span itemprop="affiliation">ACME Corp</span>.
    </p>

Test
~~~~
To run unit test
$ cd tests
$ python -m unittest tests.ItemPropTestCase

.. _Microdata: http://schema.org/
.. _Nikola: http://getnikola.com/
.. _pelican-microdata: https://github.com/noirbizarre/pelican-microdata
.. _recipe microdata: https://support.google.com/webmasters/answer/173379?hl=en
.. _recipe schema: http://www.schema.org/Recipe
