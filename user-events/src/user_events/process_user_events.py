__author__ = 'tom'

import sys
import userevent_pb2 as ue
import uuid
import protobuf_json
import random
import os

pageExamples = [ 'home', 'mySettings', 'mainMenu', 'charts']
sectionExamples = { 'home': [ 'nowPlaying', 'welcome' ],
                    'mySettings': [ 'likesAndDislikes', 'payment' ],
                    'mainMenu': ['savedStations', 'favourites' ],
                    'charts': ['artistStations', 'featuredStations'] }
componentExamples = { 'home': [ 'stationInfo', 'welcome' ],
                      'mySettings': [ 'topPanel', '' ], # blank is possible
                      'mainMenu': ['listStations', 'customize' ],
                      'charts': ['playerBar', 'chartPanel'] }
elementExamples = { 'home': [ 'continueButton', 'searchBox' ],
                      'mySettings': [ 'likeButton', 'cancelSubscriptionButton' ], # blank is possible
                      'mainMenu': ['deleteStationButton', 'saveStationButton' ],
                      'charts': ['stationEntry', 'exitButton'] }
actionExamples = [ 'click' ]

platformExamples = [ 'web', 'iphone', 'ipad' ]
initiatorExamples = [ 'userClient', 'appClient' ]

stationCodeExamples = [ 'a', 'g', 's', 'z' ]

arbitraryKeys = [ 'searchPhrase', 'lyricId', 'newName' ]
arbitraryValues = [ 'michael jackson', 'shiina ringo', 'man in the mirror', 'tadashii machi', 'toms playlist', 'old playlist' ]

timestampCounter = 1385475691000L

def randomListEntry(thisList):
    return thisList[random.randint(0, len(thisList) - 1)]

def randomDictEntry(thisDict, key):
    return randomListEntry(thisDict[key])

def randomlyInclude(randomThresh, fun, *args):
    if random.random() < randomThresh:
        fun (*args)

def appendUserEvent(userEventsBatch):

    userEvent = userEventsBatch.userEvent.add()

    # main keys

    global timestampCounter
    timestampCounter = timestampCounter + random.randint(0, 1000)
    userEvent.timestamp = timestampCounter
    userEvent.uuid = str(uuid.uuid4())
    userEvent.platform = randomListEntry(platformExamples)
    userEvent.userId = 1000000 + random.randint(0, 1000000)

    randomPage = randomListEntry(pageExamples)
    userEvent.page = randomPage
    userEvent.section = randomDictEntry(sectionExamples, randomPage)
    userEvent.component = randomDictEntry(componentExamples, randomPage)
    userEvent.element = randomDictEntry(elementExamples, randomPage)
    userEvent.action = randomListEntry(actionExamples)

    userEvent.initiator = randomListEntry(initiatorExamples)

    # another uuid will do as an example
    userEvent.sessionId = str(uuid.uuid4())

    # event data

    eventData = userEvent.eventData

    # must include some event data otherwise it won't validate
    eventData.playlistId.append(random.randint(1, 100000))

    # can be a list of values
    randomlyInclude(0.3, eventData.stationId.append, "{0}{1}".format(randomListEntry(stationCodeExamples), random.randint(1, 100000)))
    randomlyInclude(0.3, eventData.stationId.append, "{0}{1}".format(randomListEntry(stationCodeExamples), random.randint(1, 100000)))
    randomlyInclude(0.3, eventData.stationId.append, "{0}{1}".format(randomListEntry(stationCodeExamples), random.randint(1, 100000)))

    randomlyInclude(0.3, eventData.trackId.append, random.randint(1, 100000))
    randomlyInclude(0.3, eventData.trackVersionId.append, random.randint(1, 100000))
    randomlyInclude(0.3, eventData.albumId.append, random.randint(1, 100000))

    if random.random() < 0.3:
        arbitraryData1 = eventData.otherEventData.add()
        arbitraryData1.key = randomListEntry(arbitraryKeys)
        arbitraryData1.value = randomListEntry(arbitraryValues)

    if random.random() < 0.3:
        arbitraryData1 = eventData.otherEventData.add()
        arbitraryData1.key = randomListEntry(arbitraryKeys)
        arbitraryData1.value = randomListEntry(arbitraryValues)

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
        print "event id: {0}, event name: {1} event data extra fields: {2}".format(userEvent.uuid,
                                                                                   "{0}.{1}.{2}.{3}.{4}".format(userEvent.page, userEvent.section, userEvent.component, userEvent.element, userEvent.action),
                                                                                   [e.key for e in userEvent.eventData.otherEventData])

def jsonifyAllUserEvents(protobufFilename, outputFilename):

    userEventsBatch = ue.BBMUserEventBatch()
    try:
        f = open(protobufFilename, "rb")
        userEventsBatch.ParseFromString(f.read())
        f.close()
    except IOError:
        print protobufFilename + ": Could not open file.  Exiting"
        sys.exit(1)

    try:
        f = open(outputFilename, "w")
        json_obj = protobuf_json.pb2json(userEventsBatch)
        f.write(str(json_obj))
        f.close()
    except IOError:
        print outputFilename + ": Could not open file.  Exiting"
        sys.exit(1)

def exportUserEvents(targetDirectory, maxItemsPerBatch, numberOfBatches):
    """
    Creates randomized events in batches of maxItemsPerBatch,
    numberOfBatches total and writes as individual binary files in targetDirectory
    """

    try:
        os.mkdir(targetDirectory)
    except:
        pass

    try:
        for batchCount in range(0, numberOfBatches):
            userEventsBatch = ue.BBMUserEventBatch()

            for j in range(0, random.randint(1, maxItemsPerBatch)):
                appendUserEvent(userEventsBatch)

            filename = "{0}/event_batch_{1}.pbin".format(targetDirectory, batchCount)
            f = open(filename, "wb")
            f.write(userEventsBatch.SerializeToString())
            f.close()

        print "Wrote {0} user events".format(batchCount + 1)

    except IOError:
        print filename + ": Could not save file. Aborting"

def main():

    if len(sys.argv) < 3:
        print "Usage:", sys.argv[0]
        print "add [num of events to add] filename"
        print "list filename"
        print "json protobuf_filename output_filename"
        print "export directory_name max_items_per_batch number_of_batches"
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

    elif command == 'json':

        jsonifyAllUserEvents(sys.argv[2], sys.argv[3])

    elif command == 'export':

        # 2: output directory
        # 3: max items per batch (will randomize up to this number)
        # 4: total batches

        exportUserEvents(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))

    else:
        print "Unregistered command. Exiting"
        sys.exit(1)

# main function

main()
