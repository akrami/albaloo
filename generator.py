def generate_html(output, rows):
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
    for result in rows:
        if result.redirect:
            redirect_emoji = '👍'
        else:
            redirect_emoji = '⛔'

        if result.hsts:
            hsts_emoji = '👍'
        else:
            hsts_emoji = '⛔'
        wrapper += '<tr><td><a href="{0}.json">{0} ↗</a></td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>'.format(
            result.address, result.ip, 'Not Available', redirect_emoji, hsts_emoji)
    wrapper += '</tbody></table><p id="footer">Generated by <a href="https://github.com/akrami/albaloo/">Albaloo</a> 🍒</p></body></html>'
    with open(output, 'w', encoding='UTF-8') as g:
        g.write(wrapper)
        g.close()
