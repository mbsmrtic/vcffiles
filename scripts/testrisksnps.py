import unittest
import risksnps
import os
import vcffile

TESTDATADIR = '../data/'
SOURCEFILENAMEDEFAULT = TESTDATADIR + 'oddsRatio.csv';
SAMPLEFILENAME = TESTDATADIR + 'A0024_hg19.gatk.flt.vcf'

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
    
def main():
    unittest.main()

if __name__ =='__main__':
    main()
    
