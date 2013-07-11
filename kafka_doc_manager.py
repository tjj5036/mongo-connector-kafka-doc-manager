# Copyright 2012 10gen, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file will be used with PyPi in order to package and distribute the final
# product.

""" Kafka doc manager
"""

try:
    from kafka.client import KafkaClient
    from kafka.producer import SimpleProducer
except ImportError:
    raise SystemError    

class DocManager(object):
    """ Connects to a kafka instance, generates producers for a given
    database and collection
    """

    def __init__(self, url, auto_commit=True, unique_key='_id'):
        """Connect to kafka instance
        """
        url_info = url.split(":")
        if len(url_info) < 2:
            raise SystemError

        self.server = KafkaClient(url_info[0], int(url_info[1]))
        self.producer_dict = {}
        self.auto_commit = auto_commit

    def generate_producer(self, doc):
        """ Generates a producer for a given database and collection
        """
        database, coll = doc['ns'].split('.', 1)
        topic = (('%s-%s') % (database, coll))
        if topic not in self.producer_dict:
            try:
                self.producer_dict[topic] = SimpleProducer(
                    self.server,
                    str(topic),
                    async=True,
                    req_acks=SimpleProducer.ACK_AFTER_LOCAL_WRITE)
            except:
                self.producer_dict[topic] = None
        return self.producer_dict[topic]

    def stop(self):
        """ Stops the instance
        """
        self.auto_commit = False
        self.server.close()

    def upsert(self, doc):
        """ Sends the document to kafka
        """
        producer = self.generate_producer(doc)
        if producer:
            producer.send_messages(str(doc))
        else:
            raise SystemError

    def remove(self, doc):
        """ Not revelant in this context
        """
        pass

    def search(self, start_ts, end_ts):
        """ Not revelant in this context
        """
        pass

    def commit(self):
        """ Not revelant in this context
        """
        pass

    def run_auto_commit(self):
        """ Not revelant in this context
        """
        pass

    def get_last_doc(self):
        """ This is probably possible but unsure of implementation.
            Hestitant to implement this since it might be system
            specific.
        """
        pass
