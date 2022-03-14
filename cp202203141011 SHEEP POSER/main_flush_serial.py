import sys, select

readable, writeable, errors = select.select([sys.stdin],[],[],0.001)

readchars = len(readable)

if readchars < 1:
    print ('Nothing to read')
else:
    while readchars > 0:
        c = sys.stdin.read()
        readable, writeable, errors = select.select([sys.stdin],[],[],0.001)
        readchars = len(readable)
