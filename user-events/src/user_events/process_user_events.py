__author__ = 'tom'

import sys
import userevent_pb2 as ue
import uuid

def appendUserEvent(userEventsBatch):

    userEvent = userEventsBatch.userEvent.add()

    # main keys

    userEvent.timestamp = 1000L
    userEvent.uuid = str(uuid.uuid4())
    userEvent.platform = 'key'
    userEvent.userId = 12345
    userEvent.page = 'home'
    userEvent.section = 'nowPlaying'
    userEvent.component = 'stationInfo'
    userEvent.element = 'favouriteStationButton'
    userEvent.action = 'click'

    userEvent.initiator = 'userClient'

    # event data

    eventData = userEvent.eventData

    eventData.stationId.append('a123')
    eventData.trackId.append(4321)

    arbitraryData1 = eventData.otherEventData.add()
    arbitraryData1.key = 'search_phrase'
    arbitraryData1.value = 'christmas'

    arbitraryData1 = eventData.otherEventData.add()
    arbitraryData1.key = 'search_results'
    arbitraryData1.value = '0'

    userEvent.version = 1

    if not userEvent.IsInitialized():
        print "Error in event initialization"
        sys.exit(1)

    return userEvent

def listAllUserEvents(filename):

    userEventsBatch = ue.BBMUserEventBatch()
    try:
        f = open(filename, "rb")
        userEventsBatch.ParseFromString(f.read())
        f.close()
    except IOError:
        print filename + ": Could not open file.  Exiting"
        sys.exit(1)

    # Query uuids of events

    for userEvent in userEventsBatch.userEvent:
        print "event id: {0}, event data extra fields: {1}".format(userEvent.uuid, [e.key for e in userEvent.eventData.otherEventData])

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

        userEventsBatch = ue.BBMUserEventBatch()

        try:
            f = open(filename, "rb")
            userEventsBatch.ParseFromString(f.read())
            f.close()
        except IOError:
            print filename + ": Could not open file.  Creating a new one."

        # Append new user events

        for i in range(0, int(noEvents)):
            appendUserEvent(userEventsBatch)

        # Write back out to disk

        try:
            f = open(filename, "wb")
            f.write(userEventsBatch.SerializeToString())
            f.close()

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
