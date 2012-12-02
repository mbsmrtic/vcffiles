from talltable import TallTable
from talltable import DEFAULT_DATA_DIR
from talltable import DEFAULT_VCFS_DIR
from os import remove
from os import listdir
from os.path import exists
from vcffile import VcfFile

DEFAULT_OUTPUT_FILE_NAME = DEFAULT_DATA_DIR + 'tallsomeppl.csv'

class TallSomePeople(TallTable):
    '''
    TallSomePeople is a tall table that does not contain all the people.  
    '''
    
    def __init__(self, inputDirectoryName = DEFAULT_VCFS_DIR, outputFileName=DEFAULT_OUTPUT_FILE_NAME):
        TallTable.__init__(self, inputDirectoryName, outputFileName)

    def add_some(self, personIds):
        '''
        Loops through the files that contain the data for the people identified in personIds.
        Creates a file similar to add_all except that not all the people are added.  
        '''
        if exists(self.filename): 
            remove(self.filename)
        
        #open the destination file and write the header line
        with open(self.filename, 'w') as destFile:
            print "created " + self.filename + "\n"
            headerLine = "personid, snpid, allele"
            destFile.write(headerLine + "\n")

            #loop through the files in the directory and add a column for each
            srcFileNames = []
            inputFile = VcfFile()
            for personId in personIds:
                srcFileName = inputFile.get_persons_file_name(personId)
                srcFileNames.append(srcFileName)
            
            fileCount = 0
            for srcFileName in srcFileNames:
                self.write_one_person_to_file(self.inputDir + srcFileName, destFile)
                fileCount += 1
    
if __name__ == '__main__':
    destObj = TallSomePeople()
    destObj.add_some(['A1037', 'A1053'])
    
