__author__ = 'tom'

import sys
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import uuid

def createUserEvent():

    # main keys

    userEvent = {
        "timestamp" : 1000,
        "uuid" : str(uuid.uuid4()),
        "apikey": "key",
        "eventName": "artist_search",
        "eventType": "ap.user",
    }

    # context
    # contains standardized (optional keys) and list of arbitrary key/values

    userEvent["eventContext"] = {
        "containerName": "now_playing",
        "trackIdPlaying": 12345,
        "otherEventContext": {
            "panel_number": "6",
            "veil_lifted": "true"
        }
    }

    # event data

    userEvent["eventData"] = {
        "userId": 1234,
        "stationId": "a123",
        "trackId": 4321,
        "otherEventData": {
            "search_phrase": "christmas",
            "search_results": "0"
        }
    }

    return userEvent

def listAllUserEvents(filename):

    try:

        reader = DataFileReader(open(filename, "r"), DatumReader())
        for event in reader:

            # Query uuids of events
            print "event id: {0}, event data extra fields: {1}".format(event["uuid"], event["eventData"]["otherEventData"])

        reader.close()
    except IOError:
        print filename + ": Could not open file.  Exiting"
        sys.exit(1)

def main():

    if len(sys.argv) < 3:
        print "Usage:", sys.argv[0]
        print "add [num of events to add] filename"
        print "list filename"
        exit(1)

    command = sys.argv[1]

    if command == 'add':

        noEvents = sys.argv[2]
        filename = sys.argv[3]

        # load existing events

        existingEvents = {}

        try:
            reader = DataFileReader(open(filename, "rb"), DatumReader())
            existingEvents = reader
            reader.close()
        except IOError:
            print filename + ": Could not open file.  Creating a new one."

        # Write back out to disk

        try:

            schema = avro.schema.parse(open("etc/userevent.avsc").read())

            f = open(filename, "w")
            writer = DataFileWriter(f, DatumWriter(), schema)

            # Append new user events

            for i in range(0, int(noEvents)):
                newEvent = createUserEvent()
                print newEvent
                writer.append(newEvent)

            writer.close()

            print "Wrote {0} user events".format(noEvents)
        except IOError:
            print filename + ": Could not save file."

    elif command == 'list':

        listAllUserEvents(sys.argv[2])

    else:
        print "Unregistered command. Exiting"
        sys.exit(1)

# main function

main()
