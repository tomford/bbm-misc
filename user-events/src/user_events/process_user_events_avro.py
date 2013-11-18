import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

schema = avro.schema.parse(open("etc/userevent.avsc").read())

schemaExample = {
    "timestamp" : 123,
    "uuid": "hello",
    "apikey": "key",
    "eventName": "api.event",
    "eventType": "api.type",
    "eventData": { "userId": 123,
                   "otherEventData": {
                       "akey": "avalue"
                   }},
    "eventContext": { "containerName": "aname" }
}
writer = DataFileWriter(open("users.avro", "w"), DatumWriter(), schema)
writer.append(schemaExample)
writer.close()

reader = DataFileReader(open("users.avro", "r"), DatumReader())
for user in reader:
    print user
reader.close()
