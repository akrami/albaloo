import os
import datetime
import website
import optparse

parser = optparse.OptionParser()
parser.add_option('-o', '--output', dest='output_directory',
                  default='results/{0}'.format(datetime.datetime.now().strftime('%Y-%m-%d')),
                  help='Results Location\n(default is \'results/[current date]\')')
parser.add_option('-w', '--website', dest='host', help='Host to Check')
parser.add_option('-i', '--input', dest='input_file', help='List of Hosts (ignored if -w is set)')
parser.add_option('-v', '--verbose', dest='verbose', default=False, action='store_true', help='Verbose Mode')
options, remainder = parser.parse_args()
directory = options.output_directory
if not os.path.exists(directory):
    if verbose:
        print("[Main] New Directory: {0}".format(directory))
    os.makedirs(directory)
verbose = options.verbose
if options.host:
    result = website.Website(options.host)
    ip = result.check_ip(verbose)
    if verbose:
        print('[{0}] IP: {1}'.format(result.address, ip))
    redirect = result.check_redirect(verbose)
    if verbose:
        print('[{0}] HTTPS REDIRECT: {1}'.format(result.address, redirect))
    hsts = result.check_hsts(verbose)
    if verbose:
        print('[{0}] HSTS: {1}'.format(result.address, hsts))
    if verbose:
        print('[{0}] SSLLAB: Start'.format(result.address))
    ssllab_result = result.check_ssllab(verbose)
    if verbose:
        print('[{0}] SSLLAB: Finished'.format(result.address))
    with open('{0}/{1}.json'.format(directory, result.address), 'w') as f:
        f.write(ssllab_result)
elif options.input_file:
    file = open(options.input_file, 'r')
    for line in file:
        line = line.strip()
        temp = website.Website(line)
        ip = temp.check_ip(verbose)
        if verbose:
            print('[{0}] IP: {1}'.format(line, ip))
        redirect = temp.check_redirect(verbose)
        if verbose:
            print('[{0}] HTTPS REDIRECT: {1}'.format(line, redirect))
        hsts = temp.check_hsts(verbose)
        if verbose:
            print('[{0}] HSTS: {1}'.format(line, hsts))
        if verbose:
            print("[{0}] SSLLAB: Start ".format(line))
        result = temp.check_ssllab(verbose)
        if verbose:
            print("[{0}] SSLLAB: Finished ".format(line))
        with open(directory + "/" + line + '.json', 'w') as f:
            f.write(result)
else:
    print('Please select at least one of -w or -i options (-h for Help)')
