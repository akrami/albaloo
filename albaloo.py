import os
import datetime
import website
import optparse
from termcolor import colored

parser = optparse.OptionParser()
parser.add_option('-o', '--output', dest='output_directory',
                  default='results/{0}'.format(datetime.datetime.now().strftime('%Y-%m-%d')),
                  help='Results Location\n(default is \'results/[current date]\')')
parser.add_option('-w', '--website', dest='host', help='Host to Check')
parser.add_option('-i', '--input', dest='input_file', help='List of Hosts (ignored if -w is set)')
parser.add_option('-v', '--verbose', dest='verbose', default=False, action='store_true', help='Verbose Mode')
options, remainder = parser.parse_args()
directory = options.output_directory
verbose = options.verbose
if not os.path.exists(directory):
    if verbose:
        print("[{0}] New Directory: {1}".format(colored('Main', 'green'), directory))
    os.makedirs(directory)
if options.host:
    result = website.Website(options.host)
    ip = result.check_ip(verbose)
    if verbose:
        print('[{0}] IP: {1}'.format(colored(result.address, 'green'), ip))
    redirect = result.check_redirect(verbose)
    if verbose:
        print('[{0}] HTTPS REDIRECT: {1}'.format(colored(result.address, 'green'), redirect))
    hsts = result.check_hsts(verbose)
    if verbose:
        print('[{0}] HSTS: {1}'.format(colored(result.address, 'green'), hsts))
    if verbose:
        print('[{0}] SSLLAB: Start'.format(colored(result.address, 'green')))
    ssllab_result = result.check_ssllab(verbose)
    if verbose:
        print('[{0}] SSLLAB: Finished'.format(colored(result.address, 'green')))
    with open('{0}/{1}.json'.format(directory, result.address), 'w') as f:
        f.write(ssllab_result)
elif options.input_file:
    file = open(options.input_file, 'r')
    hosts = file.readlines()
    hosts = [x.strip() for x in hosts]
    for host in hosts:
        temp = website.Website(host)
        ip = temp.check_ip(verbose)
        if verbose:
            print('[{0}] IP: {1}'.format(colored(host, 'green'), ip))
        redirect = temp.check_redirect(verbose)
        if verbose:
            print('[{0}] HTTPS REDIRECT: {1}'.format(colored(host, 'green'), redirect))
        hsts = temp.check_hsts(verbose)
        if verbose:
            print('[{0}] HSTS: {1}'.format(colored(host, 'green'), hsts))
        if verbose:
            print("[{0}] SSLLAB: Start ".format(colored(host, 'green')))
        result = temp.check_ssllab(verbose)
        if verbose:
            print("[{0}] SSLLAB: Finished ".format(colored(host, 'green')))
        with open(directory + "/" + host + '.json', 'w') as f:
            f.write(result)
else:
    print('Please select at least one of -w or -i options (-h for Help)')
