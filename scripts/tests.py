import unittest
import risksnps
import os
import vcffile
import risksnptable

TESTDATADIR = '../data/'
SOURCEFILENAMEDEFAULT = TESTDATADIR + 'oddsRatio.csv';
SAMPLEFILENAME = TESTDATADIR + 'A0024_hg19.gatk.flt.vcf'

class TestVcfFile(unittest.TestCase):
    '''
    Tests for the VcfFile class.
    '''

    def setUp(self):
        unittest.TestCase.setUp(self)
        print self.__class__.__name__ 


    def test_person_id(self):
        '''VcfFile.get_person_id should pull the person id from the file name'''
        self.assertTrue(os.path.exists(SAMPLEFILENAME))
        inputfile = vcffile.VcfFile(SAMPLEFILENAME)
        personid = inputfile.get_person_id()
        self.assertEqual("A0024", personid)

    def test_get_first_snp_line(self):
        '''VcfFile.get_first_snp_line should return the first snp in the file'''
        self.assertTrue(os.path.exists(SAMPLEFILENAME))
        inputfile = vcffile.VcfFile(SAMPLEFILENAME)
        firstSnpLine = inputfile.get_first_snp_line()
        firstSnp = inputfile.get_a_snp_id(firstSnpLine)
        self.assertEqual('rs12028261', firstSnp)

    def test_get_an_allele(self):
        '''VcfFile.get_an_allele should return the snps allele'''
        self.assertTrue(os.path.exists(SAMPLEFILENAME))
        inputfile = vcffile.VcfFile(SAMPLEFILENAME)
        firstSnpLine = inputfile.get_first_snp_line()
        firstSnpAllele = inputfile.get_an_allele(firstSnpLine)
        self.assertEqual('A', firstSnpAllele)
        
    def test_get_an_allele_number(self):
        '''get_an_allele_number should convert from a character allele to a number'''
        inputfile = vcffile.VcfFile()
        alleleNumber = inputfile.get_an_allele_number('A', 'G')
        self.assertEqual('1', alleleNumber)
        alleleNumber = inputfile.get_an_allele_number('G', 'G')
        self.assertEqual('4', alleleNumber)

    def test_get_these_snps(self):
        '''
        VcfFile.get_these_snps should return a list of allele numbers.
        Note that they will usually be 4s because 4 represents the risk
        allele and in this dataset, if a person has an allele that is different
        from the reference genome, and it is for one of the risk snps,
        it is usually, but not always the risk allele. 
        '''
        riskSnps = risksnps.RiskSnps()
        riskSnps.set_snps(['rs102275', 'rs3764147', 'rs7927997', 'rs415890', 'rs4077515', 'rs3810936', 'rs2476601', 'rs3792109'])
        riskSnps.set_alleles(['C','G','T','C','T','C','G','A'])
        inputfile = vcffile.VcfFile(SAMPLEFILENAME)
        alleleNumbers = inputfile.get_these_snps(riskSnps)
        self.assertEqual(riskSnps.len(), len(alleleNumbers))
        self.assertEqual('4', alleleNumbers[0])
        self.assertEqual('4', alleleNumbers[1])


class TestRiskSnps(unittest.TestCase):
    '''
    Tests for the RiskSnps class.
    '''
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        print self.__class__.__name__ 

    def test_read_from_file(self):
        '''
        RiskSnps.read_from_file should fill in the snps with the expected risk snps.

        Here we use a known risk snps file and compare what is read in to what is expected.
        '''
        riskSnpsExpected = risksnps.RiskSnps()
        riskSnpsExpected.set_snps(['rs1998598','rs2549794','rs2797685'])
        riskSnpsExpected.set_alleles(['G','C', 'A'])
        riskSnpAllelesActual = risksnps.RiskSnps()
        riskSnpAllelesActual.read_from_file(SOURCEFILENAMEDEFAULT)
        self.assertEqual(71, riskSnpAllelesActual.len())
        self.assertEqual(riskSnpsExpected.get_snp(0), riskSnpAllelesActual.get_snp(0))
        self.assertEqual(riskSnpsExpected.get_allele(0), riskSnpAllelesActual.get_allele(0))
        self.assertEqual(riskSnpsExpected.get_snp(1), riskSnpAllelesActual.get_snp(1))
        self.assertEqual(riskSnpsExpected.get_allele(1), riskSnpAllelesActual.get_allele(1))
        self.assertEqual(riskSnpsExpected.get_snp(2), riskSnpAllelesActual.get_snp(2))
        self.assertEqual(riskSnpsExpected.get_allele(2), riskSnpAllelesActual.get_allele(2))

    def test_vcffile_get_these_snps(self):
        riskSnps = risksnps.RiskSnps()
        riskSnps.set_snps(['rs102275', 'rs3764147', 'rs7927997', 'rs415890', 'rs4077515', 'rs3810936', 'rs2476601', 'rs3792109'])
        riskSnps.set_alleles(['C','G','T','C','T','C','G','A'])
        snpDataFile = vcffile.VcfFile(SAMPLEFILENAME)
        alleles = snpDataFile.get_these_snps(riskSnps)
        self.assertEqual(riskSnps.len(), len(alleles))
        self.assertEqual('4', alleles[0])
        self.assertEqual('4', alleles[1])
        
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
    