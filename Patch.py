#!usr/bin/python
import argparse
import logging
import logging.config
import sys
from Input.CSVInput import CSVInput
from Output.CSVOutput import CSVOutput
from Output.JsonOutput import JsonOutput
from ProbeModules.SSLCertificate import SSLCertificate
from util import get_logging_config

logging.config.fileConfig(get_logging_config())
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Process Zmap output')
parser.add_argument('-o', '--output', help='output file', default=sys.stdout)
parser.add_argument('-om', '--outputModule', help='set output module. default=csv', default='csv')
parser.add_argument('-i', '--input', help='input file', default=sys.stdin)
parser.add_argument('-t', '--threads', help='number of threads of module execution', default=1, type=int)
parser.add_argument('--sslCertificate', help='obtain ssl certificate for each ip', action="store_true")
args = parser.parse_args()

# Setting output module
if args.outputModule == 'tsv':
    output = CSVOutput(delimiter=CSVOutput.TSV_DELIMITER, output_file=args.output)
elif args.outputModule == 'json':
    output = JsonOutput(output_file=args.output)
else:
    output = CSVOutput(delimiter=CSVOutput.CSV_DELIMITER, output_file=args.output)

# Setting input module
input = CSVInput(input_file=args.input)

logger.info('Start scanning')

threads = list()
if args.sslCertificate:
    for x in range(0, args.threads):
        ssl_cert = SSLCertificate(input_module=input, output_module=output)
        ssl_cert.start()
        threads.append(ssl_cert)

# Wait for the threads
for thread in threads:
    thread.join()

logger.info('End scanning')

input.close()
output.close()
