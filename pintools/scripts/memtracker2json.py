#!/usr/bin/python -tt

help = """This script converts a trace of memory allocations and accesses generated
by memtracker and optionally processed by memtracker-process-raw.py, which augments 
the memory-access records with the names and types of corresponding variables when
possible, to json format. 

The trace format can be found at:

        https://github.com/craiig/memdb

The most recent example is:

{"event": "function-begin", "name": "main"}
{"event": "allocation", "alloc-size": "80", "alloc-base": "0xcb3010", "type": "malloc", "alloc-tag": "1"}
{"event": "memory-access", "function": "main", "region-base": "0xcb3010", "pc": "0x40231b", "region-size": "80", "address": "0xcb3010", "type": "write", "region-tag": "1"}
{"event": "function-end", "name": "main"}

This scrpt adds other fields to the records, such as the thread id, source file location, variable name and type. 

Raw trace records generated by memtracker are of the following format:

1) Allocation records:

Delimiter  Thread ID  Address FuncName Size Number SourceLoc VarName VarType
============================================================================
alloc:      0    0x00007fd2c62a2b71 __wt_calloc 3776 1 /cs/systems/home/fedorova/Work/WiredTiger/wt-dev/build_posix/../src/conn/conn_api.c:1216 conn WT_CONNECTION

2) Memory-access records:

Type   Thread ID    Address  Size  FuncName  SourceLoc VarName VarType
=======================================================================
write:     0  0x00007fff0f495ac0 8 __libc_memalign

The last two fields are optional as this information may not always be 
available. 

3) Function delimiter records:

Delimiter      ThreadId  FuncName
===========================================
function-begin    0      pthread_mutex_lock
function-end      0      pthread_mutex_unlock

"""

from os import system
import os.path
import re
import sys
from sys import stdin
import argparse


def parseAlloc(line):

    threadID = "<unknown>";
    addr = "<unknown>";
    funcName = "<unknown>";
    size = "<unknown>";
    numItems = "<unknown>";
    sourceLoc = "<unknown>";
    varName = "<unknown>";
    varType = "<unknown>";

    words = line.split(" ");
            
    for i in range(0, len(words)):
        if(i == 0):
            continue;
        if(i == 1):
            threadID = words[i];
        if(i == 2):
            addr = words[i];
        if(i == 3):
            funcName = words[i];
        if(i == 4):
            size = words[i];
        if(i == 5):
            numItems = words[i];
        if(i == 6):
            sourceLoc = words[i];
        if(i == 7):
            varName = words[i];
        if(i == 8):
            varType = words[i];

    # Now print the JSON record
    print("{\"event\": \"allocation\", " 
          "\"thread-id\": \"" + threadID + "\", "
          "\"alloc-base\": \"" + addr + "\", "
          "\"type\": \"" + funcName + "\", "
          "\"alloc-size\": \"" + size + "\", "
          "\"num-items\": \"" + numItems + "\", "
          "\"source-location\": \"" + sourceLoc + "\", "
          "\"var-name\": \"" + varName + "\", "
          "\"var-type\": \"" + varType + "\"}");


def parseMemoryAccess(line):

    accessType = "<unknown>";
    threadID = "<unknown>";
    addr = "<unknown>";
    size = "<unknown>";
    funcName = "<unknown>";
    varName = "<unknown>";
    varType = "<unknown>";
    allocLoc = "<unknown>";

    words = line.split(" ");
            
    for i in range(0, len(words)):
        if(i == 0):
            accessType = words[i].strip(':');
        if(i == 1):
            threadID = words[i];
        if(i == 2):
            addr = words[i];
        if(i == 3):
            size = words[i];
        if(i == 4):
            funcName = words[i];
        if(i == 5):
            varName = words[i];
        if(i == 6):
            varType = words[i];    
        if(i == 7):
            allocLoc = words[i];


    # Now print the JSON record
    print("{\"event\": \"memory-access\", " 
          "\"type\": \"" + accessType + "\", "
          "\"thread-id\": \"" + threadID + "\", "
          "\"address\": \"" + addr + "\", "
          "\"size\": \"" + size + "\", "
          "\"function\": \"" + funcName + "\", "
          "\"alloc-location\": \"" + allocLoc + "\", "
          "\"var-name\": \"" + varName + "\", "
          "\"var-type\": \"" + varType + "\"}");


def parseFunction(line):

    eventType = "";
    threadID = "<unknown>";
    funcName = "<unknown>";
    
    words = line.split(" ");
            
    for i in range(0, len(words)):
        if(i == 0):
            eventType = words[i].strip(':');
        if(i == 1):
            threadID = words[i];
        if(i == 2):
            funcName = words[i];

    # Now print the JSON record
    print("{\"event\": \"" + eventType + "\", " 
          "\"thread-id\": \"" + threadID + "\", "
          "\"name\": \"" + funcName + "\"}");
    

#
# First just parse and convert as-is. Later, we might want to match 
# memory-access records with corresponding allocation records and convert
# memory-access data with the information that the allocation gives us.
#
def parse(fdTrace, keepdots):


    for line in fdTrace:
        
        if(not keepdots):
            if ".plt" in line:
                continue;

            if ".text" in line:
                continue

        line = line.rstrip();

        if line.startswith("alloc:"):
            parseAlloc(line);
        if line.startswith("read") or line.startswith("write"):
            parseMemoryAccess(line);
        if line.startswith("function-begin") or line.startswith("function-end"):
            parseFunction(line);



###
def main():

    parser = argparse.ArgumentParser(description='Convert memtracker trace to JSON.')
    parser.add_argument('--infile', 
                        help='Name of the trace file generated by the memtracker pintool.')
    parser.add_argument('--keepdots', action='store_true', 
                        help='Do not skip records from .text and .plt when generating trace');


    args = parser.parse_args()
    

    if args.infile is None:
        parse(sys.stdin, args.keepdots);
    else:
        if not os.path.exists(args.infile):
            print 'File ' + args.infile + ' does not exist.';
            sys.exit(1);

        fdTrace = open(args.infile, "r");
        parse(fdTrace, args.keepdots);

if __name__ == '__main__':
    main()
