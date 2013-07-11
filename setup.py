from setuptools import setup
import sys

setup(name='mongo-connector-kafka-doc-manager',
      version='1.0.0',
      maintainer='10gen',
      description='Kafka plugin for mongo-connector',
      platforms=['any'],
      author='10gen labs',
      author_email='tyler.jones@10gen.com',
      url='https://github.com/10gen-labs/',
      py_modules=['kafka_doc_manager'],
      install_requires=[''],
      license='OSI Approved :: Apache Software License',
      keywords='mongo-connector',
      entry_points={
          'mongo_connector_plugins': 
            ['kafka_doc_manager = kafka_doc_manager:DocManager']},
      )
