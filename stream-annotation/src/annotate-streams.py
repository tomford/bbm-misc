__author__ = 'tom'

import sys
import re
import gzip
import os

filename = sys.argv[1]

# Load in lines and assign to category

streamInfoRegexp = re.compile('.+STREAMID.+STREAMUNIQUE=([^|]+)')
radioReportRegexp = re.compile('.+STREAMID.+UUID.+STREAMUNIQUE=([^|]+)')
streamEndRegexp = re.compile('.+StreamEnd:STREAMUNIQUE=([^|]+)')

streamInfoStreamStart = {}
radioReportStreamStart = {}
streamEnd = {}

with gzip.open(filename) as f:
    for newLine in f:

#        print newLine

        # radioreport stream start
        radioReportStreamStartMatch = radioReportRegexp.match(newLine)
        if radioReportStreamStartMatch:
            radioReportStreamStart[radioReportStreamStartMatch.group(1)] = newLine
            continue

        # streamInfo stream start

        streamInfoStreamStartMatch = streamInfoRegexp.match(newLine)
        if streamInfoStreamStartMatch:
            streamInfoStreamStart[streamInfoStreamStartMatch.group(1)] = newLine
            continue
	
        # stream end
        streamEndMatch = streamEndRegexp.match(newLine)
        if streamEndMatch:
            streamEnd[streamEndMatch.group(1)] = newLine
	       

print "streamInfo {0}".format(len(streamInfoStreamStart))
print "radioReport {0}".format(len(radioReportStreamStart))
print "streamEnd {0}".format(len(streamEnd))

print "nonRadioReportStreamInfo: streamInfo - radioReport {0}".format(len(streamInfoStreamStart)-len(radioReportStreamStart))
print "radioReport + nonRadioReportStreamInfo: {0}".format(len(streamInfoStreamStart)+len(radioReportStreamStart))

# Run through file again, find the streamUnique and output an annotated line

streamUniqueRegexp = re.compile('(Sep[^S]+)(.+STREAMUNIQUE=([^|]+).+)')

# Output file]

path, filenameOnly = os.path.split(filename)
outputFilename = filenameOnly[:-3] + "-annotated.gz"

with gzip.open(filename) as f:
    with gzip.open(outputFilename, 'w') as fwrite:
        for newLine in f:
            uniqueMatch = streamUniqueRegexp.match(newLine)

            if not uniqueMatch:
                continue

            isStreamEndMatch = streamEndRegexp.match(newLine)
        
            timestamp = uniqueMatch.group(1)
            restOfLine = uniqueMatch.group(2)
            lineStreamUnique = uniqueMatch.group(3)

            annotation=""

            if lineStreamUnique in radioReportStreamStart:
            
                if isStreamEndMatch:
                    annotation="RadioReport:" # keep existing StreamEnd:
                else:
                    annotation="RadioReport:StreamStart:"

            elif lineStreamUnique in streamInfoStreamStart:
                
                if isStreamEndMatch:
                    annotation="" # this is a native StreamEnd call, so not adding any annotation
                else:
                    annotation="StreamInfo:"

            annotatedLine = "{0}{1}{2}\n".format(timestamp, annotation, restOfLine)
            #print annotatedLine
            fwrite.write(annotatedLine)
