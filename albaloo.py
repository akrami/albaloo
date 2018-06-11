import os
import datetime
from website import Website
import optparse
from termcolor import colored
from tqdm import tqdm

parser = optparse.OptionParser()
parser.add_option('-o', '--output', dest='output_directory',
                  default='results/{0}'.format(datetime.datetime.now().strftime('%Y-%m-%d')),
                  help='Results Location\n(default is \'results/[current date]\')')
parser.add_option('-w', '--website', dest='host', help='Host to Check')
parser.add_option('-i', '--input', dest='input_file', help='List of Hosts (ignored if -w is set)')
options, remainder = parser.parse_args()
directory = options.output_directory

hosts = []
results = []
if options.host:
    hosts = [options.host]
elif options.input_file:
    file = open(options.input_file, 'r')
    hosts = file.readlines()
    hosts = [x.strip() for x in hosts]
else:
    print('Please select at least one of -w or -i options (-h for help)')
    exit(1)

bar_length = len(hosts)*5 + 1
bar = tqdm(total=bar_length)

if not os.path.exists(directory):
    bar.write("[{0}] New Directory: {1}".format(colored('Main', 'green'), directory))
    os.makedirs(directory)
    bar.update(1)
else:
    bar.write("[{0}] Directory already exist".format(colored('Main', 'green')))
    bar.update(1)

for host in hosts:
    temp = Website(host)
    ip = temp.check_ip()
    bar.update(1)
    bar.write('[{0}] IP: {1}'.format(colored(host, 'green'), ip))
    redirect = temp.check_redirect()
    bar.update(1)
    bar.write('[{0}] HTTPS REDIRECT: {1}'.format(colored(host, 'green'), redirect))
    hsts = temp.check_hsts()
    bar.update(1)
    bar.write('[{0}] HSTS: {1}'.format(colored(host, 'green'), hsts))
    bar.update(1)
    bar.write("[{0}] SSLLAB: Start (may take several minutes)".format(colored(host, 'green')))
    result = temp.check_ssllab()
    bar.update(1)
    bar.write("[{0}] SSLLAB: Finished ".format(colored(host, 'green')))
    results.append(temp)
    with open("{0}/{1}.json".format(directory, host), 'w') as f:
        f.write(result)
        f.close()
