#!/bin/env python

"""

Converts the GP to GT in VCF/BCF files
Need to add hard calls in subsequent versions

"""
import pysam
import argparse
import os 

parser = argparse.ArgumentParser(description='Add GT Format to GP (Genotype probability from Imputed Data) in VCF/VCF.gz/BCF form')
parser.add_argument('--input',help='input vcf/bcf/vcf.gz',required=True)
parser.add_argument('--output',help="output vcf/bcf/vcf.gz file",required=True)
parser.add_argument('--hard-call',help="output vcf/bcf/vcf.gz file",required=True)


args = parser.parse_args()


# read the input file
myvcf = pysam.VariantFile(args.input, "r")


# Add the GT field to header
myvcf.header.formats.add("GT", "1", "String", "Genotype")
#print(myvcf.header)

# create an object of new vcf file and open in to write data.
#vcf_out = pysam.VariantFile('/home/rcf-proj/dn/ANCESTRY/LALES_TEMP/bcfs/out.vcf', 'w', header=myvcf.header)
vcf_out = pysam.VariantFile(args.output, 'w', header=myvcf.header)


with open(args.output, "a") as out:
  for variant in myvcf:
    for sample in variant.samples:
      if variant.samples[sample]['GP'] == (1.0, 0.0, 0.0):
        variant.samples[sample]['GT'] = (1,0)
      elif variant.samples[sample]['GP'] == (0.0, 1.0, 0.0):
        variant.samples[sample]['GT'] =(0,0)
      elif variant.samples[sample]['GP'] == (0.0, 0.0, 1.0):
        variant.samples[sample]['GT'] = (1,1)
    out.write(str(variant))

    
