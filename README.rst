mongo-connector-kafka-doc-manager
==================================

Kafka Doc Manager for the mongo-connector tool

Usage
-----

Install via::

    python setup.py install

Start the mongo connector with::

    mongo-connector -df kafka_doc_manager    

Alternatively, if you download this module, you can 
start the connector with::

    mongo-connector -d <path_to>/kafka_doc_manager.py

Requirements
------------

This doc manager makes use of the kafka-python package 
which can be found here::

    https://github.com/mumrah/kafka-python

Attempting to run use this without it will result in an error.

Notes
-----

When specifying namesapces, the assumption is that the namespace
will match a topic.
That means that if a namespace of "foo.bar" is specified, the corresponding
topic will be "foo-bar" (note the hyphen!).

Tests
-----
Testing can be run via::

     python -m unittest discover test

Please note that in order to run the tests successfully, you need to checkout
the Kafka source.
This can be done with::

    git submodule init
    git submodule update
    cd kafka-src
    ./sbt update
    ./sbt package
    
