import os
import vcffile 
import csv

DEFAULT_DATA_DIR = '../data/'
DEFAULT_OUTPUT_FILE_NAME = DEFAULT_DATA_DIR + 'diffcounts.csv'
DEFAULT_VCFS_DIR = DEFAULT_DATA_DIR + 'vcfdata/'
MAXSNPID ='zz'    #snpIDs begin with an 'rs' so they will always be less than this 
MINSNPID = 'aa'
FIELD_PERSONID = 'personId'

class DifferenceCounts():
    '''
    DifferenceCounts creates a table that is a comparison of people. It contains one row per person
    and one column per person and each cell is the count of snps that those two people have
    the same allele (A,C,G or T) for.  
    '''
    
    def __init__(self, inputDirectory = DEFAULT_VCFS_DIR, outputFileName = DEFAULT_OUTPUT_FILE_NAME):
        self.inputDirectory = inputDirectory
        self.filename = outputFileName
    
    def create_file(self):
        '''
        Loops through the snp files and creates a table where each row is a person
        and each column is a person. The cells contain the number of differences found
        between them.
        
        Future work - change the number so that it is a measure of similarity instead
        of a measure of difference.  
        '''
        
        headerFields = [FIELD_PERSONID]
        
        srcFileNames = os.listdir(self.inputDirectory)
        for srcFileName in srcFileNames:
            srcFile = vcffile.VcfFile(srcFileName)
            personId = srcFile.get_person_id()
            headerFields.append(personId)
        
        with open(self.filename, 'w') as destFile:
            writer = csv.DictWriter(destFile, fieldnames=headerFields, lineterminator='\n')
            writer.writeheader()
            countOfSrcFiles = 0
            for srcFileName in srcFileNames:
                print srcFileName
                srcFile = vcffile.VcfFile(self.inputDirectory + srcFileName)
                personId = srcFile.get_person_id()
                rowOut = {FIELD_PERSONID:personId}
                snpsAndAlleles = srcFile.get_all_snps_and_alleles()
                snpsAndAlleles = sorted(snpsAndAlleles)
                for compareFileName in srcFileNames:
                    compareFile = vcffile.VcfFile(self.inputDirectory + compareFileName)
                    comparePerson = compareFile.get_person_id()
                    if (personId == comparePerson):
                        countDiffs = 0
                    else:
                        print '   ' + compareFileName
                        compareSnpsAndAlleles = compareFile.get_all_snps_and_alleles()
                        compareSnpsAndAlleles = sorted(compareSnpsAndAlleles)
                        countDiffs = self.count_diffs(snpsAndAlleles, compareSnpsAndAlleles)
                    rowOut[comparePerson] = countDiffs
                writer.writerow(rowOut)
                countOfSrcFiles += 1
        print "Wrote " + str(countOfSrcFiles) + " to " + self.filename
                    
    
    def count_diffs(self, snpsAndAlleles, compareSnpsAndAlleles):
        '''
        Returns the count of differences between these two people.  
        '''
        index = 0
        compareIndex = 0
        diffCount = 0
        snpAndAllele = snpsAndAlleles[index]
        compareSnpAndAllele = compareSnpsAndAlleles[compareIndex]
        snp = snpAndAllele[0]
        compareSnp = compareSnpAndAllele[0]
        while ((snp < MAXSNPID) or (compareSnp < MAXSNPID)):
            if (snp == compareSnp):
                if snpAndAllele[1] != compareSnpAndAllele[1]:
                    diffCount += 1
                index += 1
                compareIndex += 1
            elif (snp < compareSnp):
                diffCount += 1
                index += 1
            else:  #snp > compareSnp
                diffCount += 1
                compareIndex += 1
            if (index < len(snpsAndAlleles)):
                snpAndAllele = snpsAndAlleles[index]
                snp = snpAndAllele[0]
            else:
                snp = MAXSNPID
            if (compareIndex < len(compareSnpsAndAlleles)):
                compareSnpAndAllele = compareSnpsAndAlleles[compareIndex]
                compareSnp = compareSnpAndAllele[0]
            else:
                compareSnp = MAXSNPID
        return diffCount

    
if __name__ == '__main__':
    destObj = DifferenceCounts()
    destObj.create_file()
    
        
    
    