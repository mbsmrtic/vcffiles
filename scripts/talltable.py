import os
import vcffile
import risksnps
import snpcounts
import csv

DEFAULT_DATA_DIR = '../data/'
DEFAULT_OUTPUT_FILE_NAME = DEFAULT_DATA_DIR + 'talltable.csv'
DEFAULT_VCFS_DIR = DEFAULT_DATA_DIR + 'vcfdata/'
DEFAULT_SNPS_FILE = DEFAULT_DATA_DIR + 'snpcounts.csv'
FIELD_PERSONID = 'personid'
FIELD_SNPID = 'snpid'
FIELD_ALLELE = 'allele'
FIELD_INDEX = 'index'
FIELD_ODDSRATIO = 'oddsratio'

class TallTable():
    '''
    TallTable is a table we'll create from the vcf files. It contains one
    column of personids, one column of risksnpids and one column of allele values.

    The data for each person is stored in a vcf file, so we loop through the vcf 
    directory adding a person at a time.
    
    '''
    
    def __init__(self, inputDirectoryName = DEFAULT_VCFS_DIR, outputFileName=DEFAULT_OUTPUT_FILE_NAME):
        self.filename = outputFileName
        self.inputDir = inputDirectoryName
        self._recordCount = 0

        
    def add_all(self):
        '''
        Loops through all the files in inputDir directory, adding a column of personIds,
        a column of snpIds and a column of alleles
        '''
                    
        #open the destination file and write the header line
        with open(self.filename, 'w') as destFile:
            colNames = self.get_column_names()
            writer = csv.DictWriter(destFile, fieldnames=colNames, lineterminator='\n')
            print "created " + self.filename + "\n"
            writer.writeheader()
            
            #loop through the files in the directory and add a column for each
            srcFileNames = os.listdir(self.inputDir)
            fileCount = 0
            for srcFileName in srcFileNames:
                self.write_one_person_to_file(self.inputDir + srcFileName, writer)
                fileCount += 1
            
            
            if (fileCount == 1):
                print ("You ran this on one snp file, for the entire dataset go to " +
                        "https://genomeinterpretation.org/content/crohns-disease-2012 \n")
            else:
                print "Read " + str(fileCount) + " files from " + self.inputDir
                
    def get_column_names(self):
        colnames=[FIELD_PERSONID, FIELD_SNPID, FIELD_ALLELE]
        return colnames
        
    def write_one_person_to_file(self, srcFileName, writer):
        '''
        Gets the alleles for the snps from srcFile and writes them to the output file
        '''

        srcData = vcffile.VcfFile(srcFileName)
        personId = srcData.get_person_id()
        snpsAndAlleles = srcData.get_all_snps_and_alleles()
        recordCount = 0
        rowOut = {FIELD_PERSONID:personId, FIELD_SNPID:0, FIELD_ALLELE:0}
        for snpAndAllele in snpsAndAlleles:
            if (snpAndAllele[1] != '0'):
                rowOut[FIELD_SNPID] = snpAndAllele[0]
                rowOut[FIELD_ALLELE] = snpAndAllele[1]
                writer.writerow(rowOut)
                #lineOut = personId + ',' + snpAndAllele[0] + ',' + snpAndAllele[1] + '\n'
                #destFile.write(lineOut)
            recordCount += 1
        print srcFileName + ' wrote ' + str(recordCount) + ' records to ' + self.filename

class SomeSnpsTallTable(TallTable):
    '''
    SomeSnpsTallTable is the same format as TallTable, but only includes some of the snps.
    '''
    
    def __init__(self, snpsFileName = DEFAULT_SNPS_FILE,inputDirectoryName = DEFAULT_VCFS_DIR, outputFileName=DEFAULT_OUTPUT_FILE_NAME):
        TallTable.__init__(self, inputDirectoryName, outputFileName)
        self.snpsFileName = snpsFileName

    def get_column_names(self):
        colnames=[FIELD_INDEX, FIELD_PERSONID, FIELD_SNPID, FIELD_ALLELE]
        return colnames
        
    def write_one_person_to_file(self, srcFileName, writer):
        #get the snps
        snpsToUse = self.get_snps_to_use()
        srcData = vcffile.VcfFile(srcFileName)
        personId = srcData.get_person_id()
        alleles = srcData.get_these_snps(snpsToUse)
        rowOut = {FIELD_INDEX:0, FIELD_PERSONID:personId, FIELD_SNPID:0, FIELD_ALLELE:0}
        index = 0
        snpsFoundThisPerson = 0
        for allele in alleles:
            if (allele != '0'):
                rowOut[FIELD_INDEX] = self._recordCount
                rowOut[FIELD_SNPID] = snpsToUse[index]
                rowOut[FIELD_ALLELE] = allele
                writer.writerow(rowOut)
                self._recordCount += 1
                snpsFoundThisPerson += 1
            index += 1
        print srcFileName + '  ' + str(snpsFoundThisPerson) + ' snps found'
     
    def get_snps_to_use(self):   
        snpCounts = snpcounts.SnpCounts()
        return snpCounts.read_snps()
                    
        
class RiskSnpTallTable(TallTable):
    '''
    RiskSnpTallTable is the same format as TallTable, but instead of including all the snps
    from all the vcf files, we include only the snps that in riskSnps.  This will result
    in a table with fewer rows.  

    A risk snp is a Single Nucleotide Polymorphism (snp) that has an allele
    with a significant association with the disease.


    '''

    def __init__(self, inputDirectoryName = DEFAULT_VCFS_DIR, outputFileName=DEFAULT_OUTPUT_FILE_NAME):
        TallTable.__init__(self, inputDirectoryName, outputFileName)
        self.riskSnps = risksnps.RiskSnps()

    def get_column_names(self):
        colnames=[FIELD_INDEX, FIELD_PERSONID, FIELD_SNPID, FIELD_ALLELE, FIELD_ODDSRATIO]
        return colnames

    def write_one_person_to_file(self, srcFileName, writer):
        '''
        Gets the alleles for the risk snps from srcFile and writes them to the output file
        '''

        if (self.riskSnps.len() == 0):
            self.riskSnps.read_from_file()
        
        srcData = vcffile.VcfFile(srcFileName)
        personId = srcData.get_person_id()
        riskAlleles = srcData.get_these_risksnps(self.riskSnps)
        rowOut = {FIELD_INDEX:0, FIELD_PERSONID:personId, FIELD_SNPID:0, FIELD_ALLELE:0, FIELD_ODDSRATIO:0}
        index = 0
        riskSnpsThisPerson = 0
        for allele in riskAlleles:
            if (allele != '0'):
                rowOut[FIELD_INDEX] = index
                rowOut[FIELD_SNPID] = self.riskSnps.snps[index]
                rowOut[FIELD_ALLELE] = allele
                rowOut[FIELD_ODDSRATIO] = self.riskSnps.oddsratio[index]
                writer.writerow(rowOut)
                self._recordCount += 1
                riskSnpsThisPerson += 1
            index += 1
        print srcFileName + '  ' + str(riskSnpsThisPerson) + ' risk snps'

if __name__ == '__main__':
    #destObj = TallTable()
    #destObj.add_all()
    destObj = RiskSnpTallTable(outputFileName='../data/risksnptalltable.csv')
    destObj.add_all()
    #destObj = SomeSnpsTallTable(outputFileName='../data/somesnpstall.csv')
    #destObj.add_all()
    
    
        
        
        
