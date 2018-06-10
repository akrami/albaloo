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

wrapper = '''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>SSL Results</title>
    <meta name="description" content="Albaloo SSL Check Result">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <style>
            body {
                background-color: #EEEEEE;
                font-family: helvetica, arial, sans-serif;
                font-size: 13px;
                font-weight: normal;
                text-rendering: optimizeLegibility;
            }
            h1.table-title {
                color: #353535;
                font-size: 3.5em;
                font-weight: bolder;
                font-style: normal;
                font-family: Georgia, serif;
                text-shadow: 2px 2px 1px rgba(0, 0, 0, 0.3);
            }
            /*** Table Styles **/
            .table-fill {
                background: white;
                border-radius:3px;
                border-collapse: collapse;
                margin: auto;
                padding:5px;
                width: 100%;
                box-shadow: 0 5px 0 #C1C3D1;
                animation: float 5s infinite;
                border: 1px rgba(0, 0, 0, 0.7);
            }
            
            th {
                color: #D5DDE5;;
                background: #1b1e24;
                border-bottom: 4px solid #9ea7af;
                border-right: 1px solid #343a45;
                font-size: 23px;
                font-weight: 500;
                padding: 24px;
                text-align: left;
                text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
                vertical-align: middle;
                font-family: calibri, verdana, sans-serif;
            }
            th:first-child {
                border-left: 1px solid #1b1e24;
            }
            
            th:last-child {
                border-right: 1px solid #1b1e24;
            }
            
            tr {
                border-top: 1px solid #C1C3D1;
                border-bottom: 1px solid #C1C3D1;
                color:#666B85;
                font-size:13px;
                font-weight:normal;
                text-shadow: 0 1px 1px rgba(256, 256, 256, 0.1);
            }            
            tr:first-child {
                border-top:none;
            }
            tr:last-child {
                border-bottom:none;
            }
            
            tr:nth-child(odd) td {
                background:#EBEBEB;
            }
            tr:last-child td:first-child {
                border-bottom-left-radius:3px;
            }
            
            tr:last-child td:last-child {
                border-bottom-right-radius:3px;
            }
            
            td {
                background:#FFFFFF;
                padding:15px;
                text-align:left;
                vertical-align:middle;
                font-weight:200;
                font-size:14px;
                text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.1);
                border-right: 1px solid #C1C3D1;
                font-family: calibri, verdana, sans-serif;
            }
            td a {
                text-decoration: none;
                color: #1b1e24;
                font-weight: bold;
            }
            td:first-child {
                border-left: 1px solid #C1C3D1;
            }
            th.text-left {
                text-align: left;
            }
            th.text-center {
                text-align: center;
            }
            th.text-right {
                text-align: right;
            }
            td.text-left {
                text-align: left;
            }
            td.text-center {
                text-align: center;
            }
            td.text-right {
                text-align: right;
            }
            p#footer {
                position: fixed;
                right: 0;
                bottom: 0;
                padding: 7px;
                font-family: sans-serif;
                color: white;
                background-color: black;
                margin: 0;
                border-top-left-radius: 5px;
            }
        </style>
</head>
<body>
    <h1 class="table-title">SSL Results</h1>
    <table class="table-fill">
        <thead>
            <tr>
                <th>Domain</th>
                <th>IP</th>
                <th>SSLLab Rank</th>
                <th>HTTP to HTTPS Redirect?</th>
                <th>HSTS?</th>
            </tr>
        </thead>
        <tbody>
'''

for result in results:
    if result.redirect:
        redirect_emoji = '👍'
    else:
        redirect_emoji = '⛔'

    if result.hsts:
        hsts_emoji = '👍'
    else:
        hsts_emoji = '⛔'
    wrapper += '<tr><td><a href="{0}.json">{0} ↗</a></td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>'.format(result.address, result.ip, 'Not Available', redirect_emoji, hsts_emoji)

wrapper += '</tbody></table><p id="footer">Generated by <a href="https://github.com/akrami/albaloo/">Albaloo</a> 🍒</p></body></html>'
with open('{0}/index.html'.format(directory), 'w', encoding='UTF-8') as g:
    g.write(wrapper)
    g.close()
