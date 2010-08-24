#!/usr/bin/env python
# OpenHTS Copyright (c) 2010 Abhishek Tiwari. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.
from PyQt4.QtCore import *
from PyQt4.QtXml import *
import csv
import bisect

CODEC = "UTF-8"

class HTSO(object):
    """
    A HTSO object holds the details of a HTS data point. The data held 
    are: subject number, day number, the mean hormone concentration,
    standard error of the mean, time value, and number of replicates.
    
    """
    def __init__(self, subject=None, day=None, mhc=None, sem=None, time=None,
                  replicates=None):
        self.subject = subject 
        self.day = day
        self.mhc = mhc
        self.sem = sem
        self.time= time
        self.replicates = replicates


class HTSContainer(object):
    
    def __init__(self):
        self.__fname = QString()
        self.__hts = []
        self.__htsDPFromId = {}
        self.__dirty = False

    def key(self, subject, day, time):
        itime=int(time)
        return u"%s_%s_%05d" % (subject, day, itime)
    
    def isDirty(self):
        return self.__dirty
    
    def setDirty(self, dirty=True):
        self.__dirty = dirty
        
    def clear(self, clearFilename=True):
        self.__hts = []
        self.__htsDPFromId = {}
        if clearFilename:
            self.__fname = QString()
        self.__dirty = False
    
    def htsDPFromId(self, id):
        """Returns the HTS data point with the given Python ID."""
        return self.__htsDPFromId[id]
    
    def htsDPAtIndex(self, index):
        """Returns the index-th HTS data point."""
        return self.__hts[index][1]
    
    def add(self, htsDP):
        """Adds the given htsDP to the list if it isn't already
        present. Returns True if added; otherwise returns False."""
        if id(htsDP) in self.__htsDPFromId:
            return False
        Key = self.key(htsDP.subject, htsDP.day, htsDP.time)
        bisect.insort_right(self.__hts, [Key, htsDP])
        self.__htsDPFromId[id(htsDP)] = htsDP
        self.__dirty = True
        return True
    
    def delete(self, htsDP):
        """Deletes the given htsDP from the series and returns True;
        returns False if the htsDP isn't in the list."""
        if id(htsDP) not in self.__htsDPFromId:
            return False
        key = self.key(htsDP.subject, htsDP.day, htsDP.time)
        i = bisect.bisect_left(self.__hts, [key, htsDP])
        del self.__hts[i]
        del self.__htsDPFromId[id(htsDP)]
        self.__dirty = True
        return True
    
    def updateHTS(self, htsDP, subject, day, mhc,
                   sem, time, replicates):
        s="subject is not None"
        d="day is not None"
        m="mhc is not None"
        e="sem is not None"
        t="time is not None"
        r="replicates is not None"
        if s and d and m and e and t and r:
            htsDP.mhc=mhc
            htsDP.sem=sem
            htsDP.replicates=replicates
            if subject != htsDP.subject or day != htsDP.day or time != htsDP.time:
                key = self.key(htsDP.subject, htsDP.day, htsDP.time)
                i = bisect.bisect_left(self.__hts, [key, htsDP])
                self.__hts[i][0] = self.key(subject, day, time)
                htsDP.subject=subject
                htsDP.day=day
                htsDP.time=time
                self.__hts.sort()
            self.__dirty = True
            
            
    def __iter__(self):
        for pair in iter(self.__hts):
            yield pair[1]
    
    def __len__(self):
        return len(self.__hts)
    
    def setFilename(self, fname):
        self.__fname = fname

    def filename(self):
        return self.__fname


    @staticmethod
    def formats():
        return "*.csv *.xls"
    
    def load(self, fname=QString()):
        if not fname.isEmpty():
            self.__fname = fname
        if self.__fname.endsWith(".csv"):
            return self.loadCSV()
        elif self.__fname.endsWith(".xls"):
            return self.loadXLS()
        return False, "Failed to load: invalid file extension"
    
    def loadCSV(self):
        error = None
        fh = None
        try:
            fh = open(self.__fname, "rb")
            readerdata = csv.reader(fh, delimiter="\t")
            headers = readerdata.next()
            for subject, day, mhc, sem, time, replicates in readerdata:   
                    self.add(HTSO(subject,day,mhc,sem,time,replicates))
        except csv.Error, e:
            print 'file %s, line %d: %s' % self.__fname, readerdata.line_num, e
        
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Saved %d htsDP records to %s" % (
                    len(self.__hts),
                    QFileInfo(self.__fname).fileName())
            
    def loadXLS(self):
        pass
    
    def exportXml(self, fname):
        error = None
        fh = None
        try:
            fh = QFile(fname)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec(CODEC)
            stream << ("<?xml version='1.0' encoding='%s'?>\n"
                       "<!DOCTYPE OpenHTS>\n"
                       "<OpenHTS VERSION='1.0'>\n" % CODEC)
            for key, htsDP in self.__hts:
                stream << ("<HTS SUBJECT='%s' DAY='%s' "
                           "TIME='%s'>\n" % (
                        htsDP.subject, htsDP.day, htsDP.time)) \
                       << "<MHC>" << Qt.escape(htsDP.mhc) \
                       << "</MHC>\n<SEM>"
                stream << Qt.escape(htsDP.sem)
                stream << "</SEM>\n</HTS>\n"
            stream << "</OpenHTS>\n"
        except (IOError, OSError), e:
            error = "Failed to export: %s" % e
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Exported %d HTSDP records to %s" % (
                    len(self.__hts),
                    QFileInfo(fname).fileName())