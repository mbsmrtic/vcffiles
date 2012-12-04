import unittest
import risksnptable
import os

TESTDATADIR = '../data/'        
SAMPLEFILENAME = TESTDATADIR + 'A0024_hg19.gatk.flt.vcf'

class TestRiskSnpTable(unittest.TestCase):
    '''
    The RiskSnpTable class should create a risk snp table file containing
    one row per person and one column per risk snp.
    '''

    def setUp(self):
        unittest.TestCase.setUp(self)
        print self.__class__.__name__ 

    def test_get_one_person(self):
        '''
        RiskSnpTable.get_one_person_row should return a comma separated line that
        begins with the snpId, then has that person's risk snp alleles.
        '''
        table = risksnptable.RiskSnpTable()
        #these are some snps that I know are in the sample file 
        table.riskSnps.set_snps(['rs7553640', 'rsnotinfile', 'rs2072928', 'rsalsonotthere', 'rs28640257'])
        table.riskSnps.set_alleles(['C', 'T', 'G', 'C', 'G'])
        personline = table.get_one_person_from_file(SAMPLEFILENAME)
        print "personline: " + personline + "\n"
        splitLine = personline[:-1].split(',')   #we remove the last character, the newline
        self.assertEqual(6, len(splitLine))
        self.assertEqual("A0024", splitLine[0])#person id
        self.assertEqual('4', splitLine[1])    #rs7553640 risk allele C
        self.assertEqual('0', splitLine[2]) #rsnotinfile
        self.assertEqual('4', splitLine[3])    #rs2072928 risk allele G
        self.assertEqual('0', splitLine[4]) #rsalsonotthere
        self.assertEqual('4', splitLine[5])    #rs28640257 risk allele G

    def test_get_file_header(self):
        '''
        RiskSnpTable.get_file_header should return a comma separated line that
        has one entry for each risk snp.
        '''
        table = risksnptable.RiskSnpTable()
        headerLine = table.get_file_header()
        print "headerLine: " + headerLine
        self.assertTrue(headerLine.find("PersonId, rs1998598, rs2549794") == 0)

def main():
    unittest.main()

if __name__ =='__main__':
    main()
    
