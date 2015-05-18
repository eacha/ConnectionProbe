#!usr/bin/python
import argparse
import sys
from Input.CSVInput import CSVInput
from Output.CSVOutput import CSVOutput
from Output.JsonOutput import JsonOutput
from ProbeModules.SSLCertificate import SSLCertificate

parser = argparse.ArgumentParser(description='Process Zmap output')
parser.add_argument('-o', '--output', help='output file', default=sys.stdout)
parser.add_argument('-m', '--module', help='set output module. default=csv', default='csv')
parser.add_argument('-i', '--input', help='input file', default=sys.stdin)
parser.add_argument('--sslCertificate', help='obtain ssl certificate for each ip', action="store_true")
args = parser.parse_args()

# Setting output module
if args.module == 'tsv':
    output = CSVOutput(delimiter=CSVOutput.TSV_DELIMITER, output_file=args.output)
elif args.module == 'json':
    output = JsonOutput(output_file=args.output)
else:
    output = CSVOutput(delimiter=CSVOutput.CSV_DELIMITER, output_file=args.output)

# Setting input module
input = CSVInput(input_file=args.input)

# TODO Implementar threads
if args.sslCertificate:
    ssl_cert = SSLCertificate(input_module=input, output_module=output)
    ssl_cert.start()
    ssl_cert.join()
print 'end'
