import os
import csv

DEFAULT_DATA_DIR = '../data/'
DEFAULT_INPUT_FILE_NAME = DEFAULT_DATA_DIR + 'dietmortcor.csv'
DEFAULT_OUTPUT_FILE_NAME = DEFAULT_DATA_DIR + 'dietmortflat.csv'


class CorrelationMatrix():
    '''
    CorrelationMatrix is a table of correlations.  The first column is the name
    of the things being compared and each column is something it's being compared to. 
    
    An example correlation matrix is the correlations of the China Study dietary elements
    to causes of mortality.  Each row is a dietary element, such as meat or rice. Each column
    is a cause of mortality, such as heart disease. Each cell contains a correlation, the 
    correlation of meat to heart disease, for example.  
    
    Here we support the flattening of the matrix, to a tall table where there are three columns
    field1Name, field2Name and correlation value.  This format is useful for some visualizations 
    such as heatmap.
    
    @todo: allow column name args (for now we're using colA and colB and cor as our column names)
    '''
    
    def __init__(self, inputFileName=DEFAULT_INPUT_FILE_NAME, outputFileName=DEFAULT_OUTPUT_FILE_NAME):
        self._input_file_name = inputFileName
        self._output_file_name = outputFileName
        
    def flatten(self):
        '''
        Loop through all the cells creating a 'tall' file with 3 columns from a 'wide' file.
        '''
        
        if (os.path.exists(self._output_file_name)):
            os.remove(self._output_file_name)
        
        #open input file
        with open(self._input_file_name, 'r') as inputFile:
            with open(self._output_file_name, 'w') as outputFile:
                lineOut = "A,B,value\n"
                outputFile.write(lineOut)
                
                #get fields from header line
                lineIn = inputFile.readline()
                lineIn = lineIn[:-1]    #remove carriage return
                print lineIn
                colBNames = lineIn.split(',')
                #remove first one field
                colBNames = colBNames[1:]
                    
                for lineIn in inputFile:
                    lineIn = lineIn[:-1]  #remove carriage return
                    print lineIn
                    lineOut = ''
                    corValues = lineIn.split(',')
                    colAName = corValues[0]
                    corValues = corValues[1:]
                    
                    colBIndex = 0
                    for value in corValues:
                        lineOut = colAName + ',' + colBNames[colBIndex] + ',' + value + '\n'
                        colBIndex += 1
                        outputFile.write(lineOut)
                print '.'
            
        
if __name__ == '__main__':
    destObj = CorrelationMatrix()
    destObj.flatten()
