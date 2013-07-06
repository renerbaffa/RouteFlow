from couchbase import Couchbase

import pymongo as mongo
import bson

import rflib.ipc.IPC as IPC
from rflib.defs import *

FROM_FIELD = "from"
TO_FIELD = "to"
TYPE_FIELD = "type"
READ_FIELD = "read"
CONTENT_FIELD = "content"

def put_in_envelope(from_, to, msg):
    envelope = {}

    envelope[FROM_FIELD] = from_
    envelope[TO_FIELD] = to
    envelope[READ_FIELD] = False
    envelope[TYPE_FIELD] = msg.get_type()

    envelope[CONTENT_FIELD] = {}
    for (k, v) in msg.to_dict().items():
        envelope[CONTENT_FIELD][k] = v

    return envelope

def take_from_envelope(envelope, factory):
    msg = factory.build_for_type(envelope[TYPE_FIELD]);
    msg.from_dict(envelope[CONTENT_FIELD]);
    return msg;
            
class CouchIPCMessageService(IPC.IPCMessageService):
    def __init__(self, host, bucket, id_, thread_constructor, sleep_function):
        """Construct an IPCMessageService

        Args:
            bucket: Bucket name of CouchBase.
            host: list of hosts in the CouchBase cluster.
            thread_constructor: function that takes 'target' and 'args'
                parameters for the function to run and arguments to pass, and
                return an object that has start() and join() functions.
            sleep_function: function that takes a float and delays processing
                for the specified period.
        """
        self._host = host
        self._bucket = bucket
        self._connection = Couchbase.connect(
                bucket=self._bucket,
                host=self._host
            )
        self._id = id_
        self._threading = thread_constructor
        self._sleep = sleep_function
        self._connection.set("key", COUCH_INITIAL_VALUE)
    
    #mudar...
    def listen(self, channel_id, factory, processor, block=True):
        worker = self._threading(target=self._listen_worker,
                                 args=(channel_id, factory, processor))
        worker.start()
        if block:
            worker.join()
    
    def send(self, channel_id, to, msg):
        key = self._connection.incr("key")
        envelope = put_in_envelope(self.get_id(), to, msg)
        key = "{0}-{1}-{2}".format(
            envelope[CONTENT_FIELD]['dp_id'],
            envelope[CONTENT_FIELD]['ct_id'],
            envelope[CONTENT_FIELD]['dp_port'])
        self._connection.set( key, put_in_envelope(self.get_id(), to, msg) )
        return True

    # Denis alterou
    #mudar...
    def _listen_worker(self, channel_id, factory, processor):
    #   collection = self._connection
    #   cursor = collection.query("all", "default_all" {TO_FIELD: self.get_id(), READ_FIELD: False}, sort=[("_id", mongo.ASCENDING)])
        connection = mongo.Connection(MONGO_ADDRESS)
        self._create_channel(connection, channel_id)
        collection = connection[MONGO_DB_NAME][channel_id]
        cursor = collection.find({TO_FIELD: self.get_id(), READ_FIELD: False}, sort=[("_id", mongo.ASCENDING)])
        while True:
            for envelope in cursor:
                msg = take_from_envelope(envelope, factory)
                print "\n\n\n\n\n\n\n\n\n\n"
                print msg
                print "\n\n\n\n\n\n\n\n\n\n"
                processor.process(envelope[FROM_FIELD], envelope[TO_FIELD], channel_id, msg);
                collection.update({"_id": envelope["_id"]}, {"$set": {READ_FIELD: True}})
            self._sleep(0.05)
            cursor = collection.find({TO_FIELD: self.get_id(), READ_FIELD: False}, sort=[("_id", mongo.ASCENDING)])
            
    #mudar...
    def _create_channel(self, connection, name):
        db = connection[MONGO_DB_NAME]
        try:
            collection = mongo.collection.Collection(db, name, None, True, capped=True, size=CC_SIZE)
            collection.ensure_index([("_id", mongo.ASCENDING)])
            collection.ensure_index([(TO_FIELD, mongo.ASCENDING)])
        # TODO: improve this catch. It should be more specific, but pymongo
        # behavior doesn't match its documentation, so we are being dirty.
        except:
            pass

class CouchIPCMessage(dict, IPC.IPCMessage):
    def __init__(self, type_, **kwargs):
        dict.__init__(self)
        self.from_dict(kwargs)
        self._type = type_
        
    def get_type(self):
        return self._type

    def from_dict(self, data):
        for (k, v) in data.items():
            self[k] = v
        
    def from_bson(self, data):
        self.from_dict(data)

    def to_bson(self):
        return self
        
    def str(self):
        string = ""
        for (k, v) in self.items():
            string += str(k) + ": " + str(v) + "\n"
        return string
        
    def __str__(self):
        return IPC.IPCMessage.__str__(self)
