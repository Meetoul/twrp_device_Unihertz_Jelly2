import sys
import re
import os
import glob

# BEGIN CLASS SEPolicyLog
class SEPolicyLog:
  def __init__(self):
    self.__searchLine = ": avc: denied \{"
    self.__searchSource = "scontext=u:r:([^:]+):s0"
    self.__searchTarget = "tcontext=u:(?:object_)?r:([^:]+):s0"
    self.__searchClass = "tclass=([^ ]+) "
    self.__searchOperation = "\{([^\}]+)\}"
    self.__rules = {}
  
  def parseLine(self,line):
    if re.search(self.__searchLine,line) == None:
      return
    partSource = self.__parsePart(self.__searchSource,line)
    partTarget = self.__parsePart(self.__searchTarget,line)
    partClass = self.__parsePart(self.__searchClass,line)
    partOperation = self.__parsePart(self.__searchOperation,line)
    if partOperation == None:
      print("Error operation: "+line)
      return
    else:
      partsOperation = partOperation.strip().split()
    for operation in partsOperation:
      self.__addRule(partSource,partTarget,partClass,operation,line)
    
  def __parsePart(self,searchPart,line):
    matchPart = re.search(searchPart,line)
    if matchPart == None:
      return None
    return matchPart.group(1)

  def __addRule(self,partSource,partTarget,partClass,partOperation,line):
    if partSource == None:
      print("Error source: "+line)
      return
    if partTarget == None:
      print("Error tource: "+line)
      return
    if partClass == None:
      print("Error class: "+line)
      return
    if partSource in self.__rules:
      if partTarget in self.__rules[partSource]:
        if partClass in self.__rules[partSource][partTarget]:
          if not partOperation in self.__rules[partSource][partTarget][partClass]:
            self.__rules[partSource][partTarget][partClass].add(partOperation)
        else:
          self.__rules[partSource][partTarget][partClass] = {partOperation}
      else:
        self.__rules[partSource][partTarget] = {partClass:{partOperation}}
    else:
      self.__rules[partSource] = {partTarget:{partClass:{partOperation}}}
    
  def outputFiles(self,path):
    for partSource in self.__rules:
      file = open(path+partSource+".te","wt")
      for partTarget in self.__rules[partSource]:
        for partClass in self.__rules[partSource][partTarget]:
          file.write(f"allow {partSource} {partTarget}:{partClass} "+"{")
          first = True
          for partOperation in self.__rules[partSource][partTarget][partClass]:
            if not first:
              file.write(" ")
            file.write(f"{partOperation}")
            first = False
          file.write("};"+'\n')
      file.close()
    
# END CLASS SEPolicyLog

# BEGIN CLASS SELogfileParser
class SELogfileParser:
  def __init__(self,policyLog):
    self.__policyLog = policyLog

  def parseFile(self,name):                                                   
    file = open(name,"rt")
    for line in file:
       self.__policyLog.parseLine(line)
    file.close();
# END CLASS SELogfileParser

def main():
  if len(sys.argv) != 2:
    print("Wrong parameter count")
    return
  sepolicylog = SEPolicyLog()
  selogfileparser = SELogfileParser(sepolicylog)
  selogfileparser.parseFile(sys.argv[1])
  sepolicylog.outputFiles("./logfile/")

if __name__ == '__main__':
    main()
