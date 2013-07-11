import unittest
import sys
import socket
import os

from mongo_connector.mongo_connector import Connector
from setup_cluster import start_cluster, kill_all

try:
    from pymongo import MongoClient as Connection
except ImportError:
    from pymongo import Connection

from pymongo.errors import (OperationFailure,
                            ConnectionFailure)

from kafka import *  # noqa
from kafka.common import *  # noqa
from kafka.codec import has_gzip, has_snappy
from kafka.consumer import SimpleConsumer

from fixtures import ZookeeperFixture, KafkaFixture

class TestKafkaDocManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # noqa
        """Creates a kafka and mongo cluster instance
        """
        cls.zk = ZookeeperFixture.instance()
        cls.server = KafkaFixture.instance(0, cls.zk.host, cls.zk.port)
        cls.client = KafkaClient(cls.server.host, cls.server.port)
        cls.max_insertions = 100
        
        cls.flag = start_cluster()
        
        #Clear our config file
        config = os.environ.get('CONFIG', "config.txt")
        open(config, 'w').close
        
        if cls.flag:
            try:
                cls.mongo_conn = Connection("%s:27217" % 
                    (socket.gethostname()))
                cls.mongo_db = cls.mongo_conn['test']['test']
            except ConnectionFailure:
                print("Cannot connect locally!")
                cls.flag = False
        
        if cls.flag:
            cls.mongo_db = cls.mongo_conn['test']['test']
            cls.conn = Connector(("%s:27217" % (socket.gethostname())),
                config,
                "%s:%s" % (cls.server.host, cls.server.port),
                ['test.test'], '_id', None,
                "/home/tyler/doc_managers/kafka_doc_manager/kafka_doc_manager.py",
                None)
            cls.conn.start()

    @classmethod
    def tearDownClass(cls):  # noqa
        """ Ends the Kafka instances and kills the mongo cluster
        """
        cls.client.close()
        cls.server.close()
        cls.zk.close()
        cls.conn.join()
        kill_all()
    
    def setUp(self):
        """ Checks to see if the mongo instance could be started
        """
        if not self.flag:
            self.fail("Cannot start cluster!")
        try:
            self.mongo_db.remove()
        except OperationFailure:
            print("Could not remove documents!")    
    
    def test_message_len(self):
        """ Makes sure we get all the messages
        """
        # Populate our cluster with some data
        error_inserts = 0
        for i in range(0, self.max_insertions):
            try:
                self.mongo_db.insert({'i' : i})
            except OperationFailure:
                error_inserts += 1

        # Start a consumer
        consumer = SimpleConsumer(self.client, "my_group", "test-test")
        all_messages = []
        for message in consumer:
            all_messages.append(message)

        self.assertEquals(len(all_messages), 
            (self.max_insertions-error_inserts))
        self.assertEquals(len(all_messages), len(set(all_messages)))

if __name__ == "__main__":
    unittest.main()
