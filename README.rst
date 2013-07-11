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
    
Notes
-----

Previously this was included as part of the mongo-connector package.
The purpose of the separation is to encourage users to install plugins
for mongo-connector with pip as opposed to passing in source files.
However, it is still possible to do that with this module (see usage).
