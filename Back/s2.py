import datetime
import urllib.request
import re
import lxml
from lxml import etree
import lxml.etree
import xml.etree.ElementTree
import time
from xmljson import parker
from xml.etree.ElementTree import fromstring
import json
import os
import csv
import pandas as pd
import threading
import socket
import hashlib
from pretty_html_table import build_table

hname = socket.gethostname()

shared = open('/home/.bbb-key').read()
shared_secret = shared.strip('\n')
base_string = "getRecordings"

checksumma = str(base_string) + str(shared_secret)
chackhashed = hashlib.sha1(checksumma.encode())
checksum = chackhashed.hexdigest()
checksum = chackhashed.hexdigest()


def cleanoldtxt():
    directory = "/var/www/stat/stat"

    files_in_directory = os.listdir(directory)

    filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

    filtered_filesn = [file for file in files_in_directory if file.endswith(".htm")]
    for file in filtered_filesn:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

    filtered_filesn = [file for file in files_in_directory if file.endswith(".html")]
    for file in filtered_filesn:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

    filtered_filesn = [file for file in files_in_directory if file.endswith(".json")]
    for file in filtered_filesn:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)


def ten(wrt):
    global cun
    cun = wrt
    return wrt

def sttm(mtts):
    global tmsrt
    tmsrt = mtts
    return mtts


def ettm(mtte):
    global kmsrt
    kmsrt = mtte
    return mtte

def attm(mtta):
    global kmtta
    kmtta = mtta
    return mtta

def nine(y):
    try:
        tree = xml.etree.ElementTree.parse('/var/bigbluebutton/recording/raw/' + y + '/events.xml')
        root = tree.getroot()

        log = {}
        joins = []
        leaves = []

        for event in root.findall("./event[@module='PARTICIPANT']"):
            time = event.find('timestampUTC').text
            srm1 = int(time)
            srm = srm1 / 1000
            time_new = datetime.datetime.fromtimestamp(srm).strftime('%H:%M:%S')
            time_duration1 = datetime.datetime.fromtimestamp(srm)
            time_duration2 = time_duration1.timestamp()
            time_duration = time_duration2
            if event.get('eventname') == 'ParticipantJoinEvent':
                joins.append({'name': event.find('name').text,
                              'time': time_new,
                              'time2': time_duration,
                              'id': event.find('userId').text})
            if event.get('eventname') == 'ParticipantLeftEvent':
                leaves.append({
                    'time': time_new,
                    'time2': time_duration,
                    'id': event.find('userId').text
                })
            if event.get('eventname') == 'EndAndKickAllEvent':
                meeting_end = time_new
                meeting_endp = time_duration

        for jn in joins:
            username = jn['name']
            lgn = jn['time']
            lgt = meeting_end
            lgnd = jn['time2']
            lgtd = meeting_endp
            oper = lgtd - lgnd
            func_oper = datetime.datetime.utcfromtimestamp(oper).strftime('%H:%M:%S')
            for j, lv in enumerate(leaves):
                if jn['id'] == lv['id']:
                    lgt = lv['time']
                    leaves.pop(j)
                    break
            log[lgn] = dict(TimeLogin=lgn,
                            Name=username,
                            TimeLogout=lgt,
                            Standing=func_oper)

        with open('/var/www/stat/stat/' + y + '.json', 'w') as f:
            json.dump([log[t] for t in sorted(log)], f, ensure_ascii=True, sort_keys=True, indent=4, default=str)

        def jsontocsv():
            jsoncsv = pd.read_json(r'/var/www/stat/stat/' + y + '.json')
            jsoncsv.to_csv(r'/var/www/stat/stat/' + y + '.csv', index=None)

        def csvtohtml():
            a = pd.read_csv('/var/www/stat/stat/' + y + '.csv')
            a.sort_values(["Name"], axis=0, ascending=True, inplace=True)
            b = build_table(a, 'blue_light')
            finalfile = open('/var/www/stat/stat/' + y + '.htm', 'w')
            finalfile.write(b)
            finalfile.close()

        def mp4check():
            try:
                link = '<a href="https://' + hname + '/record/' + y + '.mp4" title="Download mp4">Download .mp4</a>'
                filecheck = open('/var/www/bigbluebutton-default/record/' + y + '.mp4')
                filecheck.close()
                return link
            except IOError:
                no_button = '<a href="/" title="Download mp4">NO FILE FOUND</a>'
                return no_button

        def crthtml():
            filehtml = open('/var/www/stat/stat/' + y + '.html', 'w')
            alltext = '''<!DOCTYPE html>
                            <!--[if IE 9 ]>    <html lang="ru" class="no-js ie9"> <![endif]-->
                            <!--[if (gt IE 9)|!(IE)]><!--> <html lang="ru" class="no-js">
                            <!--<![endif]--><!-- head
                                ============================================================================ --><head>


                                    <!-- Basic Info
                                    ======================================================================== -->
                                    <title>BigBlueButton Meetings Statistic</title>
                                    <meta charset="utf-8">

                                    <!-- Mobile Configurations
                                    ======================================================================== -->
                                    <meta name="apple-mobile-web-app-capable" content="yes">
                                    <meta name="apple-mobile-web-app-status-bar-style" content="black">
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">

                                    <!-- fav and icons for Mobile
                                    ======================================================================== -->
                                    <link rel="shortcut icon" href="https://www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
                                    <link rel="apple-touch-icon" sizes="57x57" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
                                    <link rel="apple-touch-icon" sizes="60x60" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
                                    <link rel="apple-touch-icon" sizes="72x72" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
                                    <link rel="apple-touch-icon" sizes="76x76" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
                                    <link rel="apple-touch-icon" sizes="114x114" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
                                    <link rel="apple-touch-icon" sizes="120x120" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
                                    <link rel="apple-touch-icon" sizes="144x144" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
                                    <link rel="apple-touch-icon" sizes="152x152" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
                                    <link rel="apple-touch-icon" sizes="180x180" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">

                                    <!-- Google Fonts
                                    ======================================================================== -->
                                    <!-- <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600|Roboto:100,100i,300,300i,400,400i,500,700&amp;subset=cyrillic" rel="stylesheet"> -->

                                    <!--  CSS Files
                                    ======================================================================== -->
                                    <link rel="stylesheet" href="js/vendor/bootstrap/css/bootstrap.min.css">
                                    <link rel="stylesheet" href="fonts/font-awesome/css/font-awesome.min.css">
                                    <link rel="stylesheet" href="css/social-icons.css">
                                    <link rel="stylesheet" href="js/plugins/swiper/css/swiper.min.css">
                                    <link rel="stylesheet" href="js/plugins/mediaelement/css/mediaelementplayer.min.css">
                                    <link rel="stylesheet" href="js/plugins/fancybox/jquery.fancybox.min.css">
                                    <link rel="stylesheet" href="js/plugins/wow/css/animate.min.css">
                                    <link rel="stylesheet" href="css/style.css">
                                    <link id="changeable-colors" rel="stylesheet" href="css/css/blue.css">
                                    <link rel="stylesheet" href="css/responsive.css">

                                    <!--  Head JS Libs
                                    ======================================================================== -->
                                    <script type="text/javascript" async="" src="https://www.google-analytics.com/analytics.js"></script><script async="" src="https://mc.yandex.ru/metrika/tag.js"></script><script src="js/vendor/modernizr-custom.js"></script>


                                </head><!-- /End head -->




                                <!-- body
                                ============================================================================ -->
                                <body class="nbs-10" data-spy="scroll" data-target=".header-menu-container" data-offset="61">




                                    <!-- UP Button
                                    ======================================================================== -->
                                    <div id="up-button"><a href="#" title="To Top"><i class="fa fa-angle-up"></i></a></div>




                                    <!-- Main Wrapper
                                    ======================================================================== -->
                                    <div id="main-wrapper">

                                    <!-- Header 1
                                        ==================================================================== -->
                                        <!-- /End Header 1 --><!-- Content 1
                                        ==================================================================== -->
                                        <!-- /End Content 1 --><!-- FAQ 3
                                        ==================================================================== -->
                                        <!-- /End FAQ 3 --><!-- Social 1
                                        ==================================================================== -->
                                        <!-- /End Social 1 --><!-- Header 1
                                        ==================================================================== -->
                                        <header id="header-section-1" class="header-section header-style-1">
                                            <!-- Header Section Container -->
                                            <div class="header-section-container">


                                                <!-- Header Menu -->
                                                <div class="header-menu">
                                                    <!-- Header Menu Container -->
                                                    <div class="header-menu" style="height: 80px;"><div class="header-menu-container header-menu-stuck">


                                                        <!-- Navbar -->
                                                        <nav class="navbar">
                                                            <!-- container -->
                                                            <div class="container">
                                                                <!-- row -->
                                                                <div class="row">
                                                                    <!-- col-md-12 -->
                                                                    <div class="col-md-12">


                                                                        <!-- Navbar Header -->
                                                                        <div class="navbar-header">

                                                                            <!-- Logo -->
                                                                            <a href="/stat" class="navbar-brand" title="LPB">
                                                                                <img src="https://www.webhostingzone.org/wp-content/uploads/2020/06/logo.png" alt="LPB Logo">
                                                                            </a><!-- /End Logo -->

                                                                            <!-- Toggle Menu Button -->
                                                                            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
                                                                                Menu <span><i class="lines"></i></span>
                                                                            </button><!-- /End Toggle Menu Button -->

                                                                        </div><!-- /End Navbar Header -->


                                                                        <!-- Navbar Collapse ( Menu ) -->
                                                                        <div class="collapse navbar-collapse">
                                                                            <ul class="nav navbar-nav navbar-right">

                                                                                <li>
                                                                                    <a href="https://www.webhostingzone.org/" title="Р“Р»Р°РІРЅР°СЏ">WebHostingZone</a>
                                                                                </li>

                                                                                <li>
                                                                                    <a href="https://www.webhostingzone.org/members/clientarea.php" title="Рћ РєРѕРјРїР°РЅРёРё">Client Area</a>
                                                                                </li>

                                                                                <li>
                                                                                    <a href="https://www.webhostingzone.org/" title="РЈСЃР»СѓРіРё">Release Notes</a>
                                                                                </li>

                                                                            </ul>
                                                                        </div><!-- /End Navbar Collapse ( Menu ) -->


                                                                    </div><!-- /End col-md-12 -->
                                                                </div><!-- /End row -->
                                                            </div><!-- /End container -->
                                                        </nav><!-- /End Navbar -->


                                                    </div></div><!-- /End Header Menu Container -->
                                                </div><!-- /End Header Menu -->


                                            </div><!-- /End Header Section Container -->
                                        </header><!-- /End Header 1 --><!-- Content 1
                                        ==================================================================== -->
                                        <div id="content-section-1" class="content-section white-section">
                                            <!-- Section Container -->
                                            <div class="section-container">


                                                <!-- container -->
                                                <div class="container">
                                                    <!-- row -->
                                                    <div class="row">


                                                        <!-- Title Block -->
                                                        <div class="col-lg-10 col-lg-offset-1 col-md-12 title-block content-block-container">
                                                            <!-- Title Block Container -->
                                                            <div class="title-block-container text-center">

                                                                <!-- Title -->
                                                                <h2>BigBlueButton Meetings Statistic</h2>

                                                                <!-- Description -->
                                                                <p>BigBlueButton Server: ''' + hname + '''</p>
                                                                <p><b>Conference Name:</b> ''' + cun + '''</p>
                                                                <p><b>Start:</b> ''' + tmsrt + ''' | <b>End:</b> ''' + kmsrt + '''</p>
                                                                <p><b>Participants:</b> ''' + kmtta + '''</p>
                                                                
                                                                <!-- Line Separator -->
                                                                <div class="line-separator"></div>

                                                                <h4>Download Content:</h4>



                                                            </div><!-- /End Title Block Container -->
                                                        </div><!-- /End Title Block -->



                                                        <!-- Content Block -->
                                                        <div class="col-md-4 content-block">
                                                            <!-- Content Block Container -->
                                                            <div class="content-block-container" style="height: 200px;">

                                                                <!-- Icon -->
                                                                <i class="fa fa-diamond circle-icon-block circle-icon-block-lg"></i>

                                                                <!-- Title -->
                                                                <h4>''' + mp4check() + '''</h4>

                                                                <!-- Description -->
                                                                <p>Download your record of this meeting in .mp4 format.</p>

                                                            </div><!-- /End Content Block Container -->
                                                        </div><!-- /End Content Block -->


                                                        <!-- Content Block -->
                                                        <div class="col-md-4 content-block">
                                                            <!-- Content Block Container -->
                                                            <div class="content-block-container" style="height: 200px;">

                                                                <!-- Icon -->
                                                                <i class="fa fa-code circle-icon-block circle-icon-block-lg"></i>

                                                                <!-- Title -->
                                                                <h4><a href="https://''' + hname + '/stat/' + y + '''.htm" title="Download HTML">Download .hml</a></h4>

                                                                <!-- Description -->
                                                                <p>Download HTML file with your User List for input to your sites easy and fast.</p>

                                                            </div><!-- /End Content Block Container -->
                                                        </div><!-- /End Content Block -->


                                                        <!-- Content Block -->
                                                        <div class="col-md-4 content-block">
                                                            <!-- Content Block Container -->
                                                            <div class="content-block-container" style="height: 200px;">

                                                                <!-- Icon -->
                                                                <i class="fa fa-bar-chart circle-icon-block circle-icon-block-lg"></i>

                                                                <!-- Title -->
                                                                <h4><a href="https://''' + hname + '/stat/' + y + '''.csv" title="Analysis">Download .csv</a></h4>

                                                                <!-- Description -->
                                                                <p>Download user list of this meeting in CSV file for attach into your CRM, LMS etc system for Analytics.</p>

                                                            </div><!-- /End Content Block Container -->
                                                        </div><!-- /End Content Block -->														

                                                        <center><h4>User List:</h4></center>
                                                        <center><div class="line-separator"></div></center>

                                                        <iframe src="https://''' + hname + '/stat/' + y + '''.htm" width="1200" height="700" frameborder=0 id="frame"></iframe>


                                                    </div><!-- /End row -->
                                                </div><!-- /End container -->


                                            </div><!-- /End Section Container -->
                                        </div><!-- /End Content 1 --><!-- FAQ 3
                                        ==================================================================== -->
                                        <div id="faq-section-3" class="faq-section white-section">
                                            <!-- Section Container -->
                                            <div class="section-container">


                                                <!-- container -->
                                                <div class="container">
                                                    <!-- row -->
                                                    <div class="row">


                                                        <!-- Title Block -->
                                                        <div class="col-lg-10 col-lg-offset-1 col-md-12 title-block">
                                                            <!-- Title Block Container -->
                                                            <div class="title-block-container text-center">

                                                                <!-- Title -->
                                                                <h2>WATCH YOU RECORD ONLINE</h2>

                                                                <!-- Description -->
                                                                <p>Here you can watch your conference record after record compile process.</p>

                                                                <!-- Line Separator -->
                                                                <div class="line-separator"></div>

                                                                <!-- Video frame -->
                                                                <center><iframe width="800" height="550" src="https://''' + hname + '/playback/presentation/2.0/playback.html?meetingId=' + y + '''" allowfullscreen="allowfullscreen"></iframe></center>

                                                                <div class="line-separator"></div>

                                                                <h4>QUICK F.A.Q.</h2>

                                                            </div><!-- /End Title Block Container -->
                                                        </div><!-- /End Title Block -->


                                                        <!-- FAQ Block -->
                                                        <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                                            <!-- FAQ Block Container -->
                                                            <div class="faq-block-container" style="height: 158px;">

                                                                <!-- Title -->
                                                                <h4>Why users duplicating in list?</h4>

                                                                <!-- Description -->
                                                                <p>BigBlueButton freeSWITCH service is allowing duplicating users. In the next updates BBB dev team should update it.</p>

                                                            </div><!-- /End FAQ Block Container -->
                                                        </div><!-- /End FAQ Block -->


                                                        <!-- FAQ Block -->
                                                        <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                                            <!-- FAQ Block Container -->
                                                            <div class="faq-block-container" style="height: 158px;">

                                                                <!-- Title -->
                                                                <h4>Why some data is not available?</h4>

                                                                <!-- Description -->
                                                                <p>BidBlueButton scripts keep cleaning conference data what is the oldest then 20 days after ending.</p>

                                                            </div><!-- /End FAQ Block Container -->
                                                        </div><!-- /End FAQ Block -->


                                                        <!-- FAQ Block -->
                                                        <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                                            <!-- FAQ Block Container -->
                                                            <div class="faq-block-container" style="height: 158px;">

                                                                <!-- Title -->
                                                                <h4>There is no *.mp4 download button.</h4>

                                                                <!-- Description -->
                                                                <p>For download conference record in .mp4 format converting script should be installed on your server.</p>

                                                            </div><!-- /End FAQ Block Container -->
                                                        </div><!-- /End FAQ Block -->


                                                        <!-- FAQ Block -->
                                                        <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                                            <!-- FAQ Block Container -->
                                                            <div class="faq-block-container" style="height: 158px;">

                                                                <!-- Title -->
                                                                <h4>I need special format data.</h4>

                                                                <!-- Description -->
                                                                <p>If you need data in some special format (pdf, html etc) please contact us: support@webhostingzone.org</p>

                                                            </div><!-- /End FAQ Block Container -->
                                                        </div><!-- /End FAQ Block -->


                                                        <!-- FAQ Block -->
                                                        <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                                            <!-- FAQ Block Container -->
                                                            <div class="faq-block-container" style="height: 158px;">

                                                                <!-- Title -->
                                                                <h4>How do i change data in reports?</h4>

                                                                <!-- Description -->
                                                                <p>There is no way to change data in reports (conference name, date etc). You're able to do it manually after download the file.</p>

                                                            </div><!-- /End FAQ Block Container -->
                                                        </div><!-- /End FAQ Block -->


                                                        <!-- FAQ Block -->
                                                        <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                                            <!-- FAQ Block Container -->
                                                            <div class="faq-block-container" style="height: 158px;">

                                                                <!-- Title -->
                                                                <h4>How do i contact with you?</h4>

                                                                <!-- Description -->
                                                                <p>Email: support@webhostingzone.org  Phone: +1 (404) 382 9079 webhostingzone.org</p>                               

                                                            </div><!-- /End FAQ Block Container -->
                                                        </div><!-- /End FAQ Block -->


                                                    </div><!-- /End row -->
                                                </div><!-- /End container -->


                                            </div><!-- /End Section Container -->
                                        </div><!-- /End FAQ 3 --><!-- Timeline 1
                                        ==================================================================== -->
                            </div><!-- /End Timeline 1 --><!-- Copyright 2
                                        ==================================================================== -->
                                        <footer id="copyright-section-2" class="copyright-section white-section">
                                            <!-- Section Container -->
                                            <div class="section-container">


                                                <!-- container -->
                                                <div class="container">
                                                    <!-- row -->
                                                    <div class="row">


                                                        <!-- Copyright Block -->
                                                        <div class="col-md-6 copyright-block">
                                                            <!-- Copyright Block Container -->
                                                            <div class="copyright-block-container">

                                                                <!-- Title -->
                                                                <p>В© 2020 <a href="https://www.webhostingzone.org/" title="WebHostingZone">WebHostingZone</a>, all rights reserved. <a href="https://github.com/georgethegreatat" title="GitHub</a></p>

                                                            </div><!-- /End Copyright Block Container -->
                                                        </div><!-- /End Copyright Block -->


                                                        <!-- Copyright Block -->
                                                        <div class="col-md-6 copyright-block">
                                                            <!-- Copyright Block Container -->
                                                            <div class="copyright-block-container">

                                                                <!-- Social Icons Block -->
                                                                <div class="social-icons-block social-icons-block-sm social-icons-block-style-1 text-right">
                                                                    <ul>
                                                                        <li><a href="https://www.facebook.com/WebHostingZone/" title="Facebook"><i class="fa fa-facebook"></i></a></li>
                                                                        <li><a href="https://twitter.com/WebHostingZone" title="Twitter"><i class="fa fa-twitter"></i></a></li>
                                                                    </ul>
                                                                </div><!-- /End Social Icons Block -->

                                                            </div><!-- /End Copyright Block Container -->
                                                        </div><!-- /End Copyright Block -->


                                                    </div><!-- /End row -->
                                                </div><!-- /End container -->


                                            </div><!-- /End Section Container -->

                                        </footer><!-- /End Copyright 2 --></div><!-- /End Main Wrapper -->




                                    <!-- Java Script Files		
                                    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
                                    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>		
                                    ======================================================================== -->
                                    <script type="text/javascript" src="js/jquery.min.js"></script>
                                    <script type="text/javascript" src="js/jquery-ui.min.js"></script>
                                    <script type="text/javascript" src="js/vendor/bootstrap/js/bootstrap.min.js"></script>
                                    <script type="text/javascript" src="js/plugins/mobile/mobile.min.js"></script>
                                    <script type="text/javascript" src="js/scripts.js"></script>

                            <style>		
                            #style-switcher {
                                z-index: 9999;
                                position: fixed;
                                top: 100px;
                                width: 212px;
                                height: auto;
                                /*min-height: 200px;*/
                                border: 1px solid #f1f1f1;
                                border-top-right-radius: 5px;
                                border-bottom-right-radius: 5px;
                                text-align: left;
                                background: white;
                                -webkit-transition: all 0.5s;
                                -moz-transition: all 0.5s;
                                transition: all 0.5s;
                            }

                            .close-style-switcher {
                                left: -212px;
                            }

                            .open-style-switcher {
                                left: -1px;
                            }

                            #style-switcher .segment {
                                width: 100%;
                                padding: 15px 10px 15px 0;
                                padding: 15px 25px;

                            }

                            #style-switcher a.panel-button {
                                position: absolute;
                                top: 30px;
                                right: -50px;
                                width: 50px;
                                height: 50px;
                                border: 1px solid #f1f1f1;
                                border-top-right-radius: 5px;
                                border-bottom-right-radius: 5px;
                                text-align: center;
                                font-size: 23px;
                                line-height: 47px;
                                background: white;
                                cursor: pointer;
                            }

                            #style-switcher h3 {
                                margin: 0;
                            }

                            #style-switcher .segment a.switcher {
                                display: inline-block;
                                width: 25px;
                                height: 25px;
                                margin-top: 5px;
                                margin-right: 3px;
                                border: 1px solid #efefef;
                                cursor: pointer;
                            }

                            .red-bg {
                                background: #EF4035;
                            }

                            .orange-bg {
                                background: #F26F21;
                            }

                            .yellow-bg {
                                background: #FFC153;
                            }

                            .green-bg {
                                background: #5CB85C;
                            }

                            .turquoise-bg {
                                background: #41C4AB;
                            }

                            .aqua-bg {
                                background: #38E6D8;
                            }

                            .blue-bg {
                                background: #0A8FD5;
                            }

                            .purple-bg {
                                background: #AC5AFF;
                            }

                            .pink-bg {
                                background: #F62459;
                            }

                            .tan-bg {
                                background: #C2B49A;
                            }

                            @media(max-width:480px) {
                                #style-switcher {
                                    top: 30px;
                                }
                            }		
                                </style>		

                                <script>
                                // Style Switcher Open/Close
                            $('#style-switcher .panel-button').click(function() {
                                //$('#style-switcher').toggleClass('close-style-switcher', 'open-style-switcher', 1000);
                                $('#style-switcher').toggleClass('open-style-switcher', 'close-style-switcher', 1000);
                                return false;
                            });

                            // Color Skins
                            $('.switcher').click(function() {
                                var title = jQuery(this).attr('title');
                                jQuery('#changeable-colors').attr('href', 'css/css/' + title + '.css');
                                return false;
                            });

                                </script>


                            <iframe name="ym-native-frame" title="ym-native-frame" frameborder="0" aria-hidden="true" style="opacity: 0 !important; width: 0px !important; height: 0px !important; position: absolute !important; left: 100% !important; bottom: 100% !important; border: 0px !important;"></iframe><ym-measure class="ym-viewport" style="display: block; top: 0px; right: 0px; bottom: 0px; left: 0px; height: 100vh; width: 100vw; position: fixed; transform: translate(0px, -100%); transform-origin: 0px 0px;"></ym-measure><ym-measure class="ym-zoom" style="bottom: 100%; position: fixed; width: 100vw;"></ym-measure></body></html>'''
            filehtml.write(alltext)
            filehtml.close()

        tr2 = threading.Thread(target=crthtml)
        tr3 = threading.Thread(target=jsontocsv)
        tr4 = threading.Thread(target=csvtohtml)
        tr3.start()
        tr3.join()
        tr4.start()
        tr2.start()
        tr4.join()
        tr2.join()


    except FileNotFoundError:
        nomeetingfile = open('/var/www/stat/stat/' + y + '.html', 'w')
        errtext = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>BigBlueButton Meeting Statistic</title>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>
<body class="d-flex flex-column h-100">
    <!-- Begin page content -->
    <main role="main" class="flex-shrink-0">
        <div class="container">
            <p></p>
            <a href="/stat"><img src="https://www.webhostingzone.org/wp-content/uploads/2020/06/logo.png" alt=""/></a>

            <h1 class="mt-5">BigBlueButton Records Statistic</h1>

            <p class="lead">Quick overview of all meeting records on BigBlueButton</p>

            <p>BigBlueButton Server: bbb.fondazionemetes.it</p>
            <p>All detail information about recorded conference (user list , duration , pre-watch etc) you can find by follow the link from "Meeting Info".</p>
            <p>Also, you are able to download conference user info (inc. login/logout time, durations, names, etc in '.csv' format).</p>
            <p>All data refreshing every 60 min.</span></p>
                        <p>Oops... Seems like meeting's data has been gone. Probably meeting is too old.</p>
        </div>
    </main>

    <footer class="footer mt-auto py-3">
        <div class="container">
            <small>BigBlueButton Recordings Infopage: v1<span id="text-version"></span> <br></small>
            <small>Р’В© 2020 WebHostingZone <span id="text-version"></span> <br></small>
         <span class="text-muted">
                Copyright &copy;
                <a href="https://www.webhostingzone.org/">WebHostingZone</a>
            </span>
        </div>
    </footer>
</body>
</html>'''
        nomeetingfile.write(errtext)
        nomeetingfile.close()
        print('Meeting with ID: ' + y + ' not found')


def genglobindexpage():
    htmlindex = open('/var/www/stat/stat/index.html', 'w')
    genpage = '''<!DOCTYPE html>
<!--[if IE 9 ]>    <html lang="ru" class="no-js ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html lang="ru" class="no-js">
<!--<![endif]--><!-- head
    ============================================================================ --><head>


        <!-- Basic Info
        ======================================================================== -->
        <title>BigBlueButton Meetings Statistic</title>
        <meta charset="utf-8">

        <!-- Mobile Configurations
        ======================================================================== -->
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">

        <!-- fav and icons for Mobile
        ======================================================================== -->
        <link rel="shortcut icon" href="https://www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
        <link rel="apple-touch-icon" sizes="57x57" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
        <link rel="apple-touch-icon" sizes="60x60" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
        <link rel="apple-touch-icon" sizes="72x72" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
        <link rel="apple-touch-icon" sizes="76x76" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
        <link rel="apple-touch-icon" sizes="114x114" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
        <link rel="apple-touch-icon" sizes="120x120" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
        <link rel="apple-touch-icon" sizes="144x144" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
        <link rel="apple-touch-icon" sizes="152x152" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">
        <link rel="apple-touch-icon" sizes="180x180" href="//www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png">

        <!-- Google Fonts
        ======================================================================== -->
        <!-- <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600|Roboto:100,100i,300,300i,400,400i,500,700&amp;subset=cyrillic" rel="stylesheet"> -->

        <!--  CSS Files
        ======================================================================== -->
        <link rel="stylesheet" href="js/vendor/bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet" href="fonts/font-awesome/css/font-awesome.min.css">
        <link rel="stylesheet" href="css/social-icons.css">
        <link rel="stylesheet" href="js/plugins/swiper/css/swiper.min.css">
        <link rel="stylesheet" href="js/plugins/mediaelement/css/mediaelementplayer.min.css">
        <link rel="stylesheet" href="js/plugins/fancybox/jquery.fancybox.min.css">
        <link rel="stylesheet" href="js/plugins/wow/css/animate.min.css">
        <link rel="stylesheet" href="css/style.css">
		<link id="changeable-colors" rel="stylesheet" href="css/css/blue.css">
        <link rel="stylesheet" href="css/responsive.css">

        <!--  Head JS Libs
        ======================================================================== -->
        <script type="text/javascript" async="" src="https://www.google-analytics.com/analytics.js"></script><script async="" src="https://mc.yandex.ru/metrika/tag.js"></script><script src="js/vendor/modernizr-custom.js"></script>


    </head><!-- /End head -->




    <!-- body
    ============================================================================ -->
    <body class="nbs-10" data-spy="scroll" data-target=".header-menu-container" data-offset="61">




        <!-- UP Button
        ======================================================================== -->
        <div id="up-button"><a href="#" title="To Top"><i class="fa fa-angle-up"></i></a></div>




        <!-- Main Wrapper
        ======================================================================== -->
        <div id="main-wrapper">

        <!-- Header 1
            ==================================================================== -->
            <!-- /End Header 1 --><!-- Content 1
            ==================================================================== -->
            <!-- /End Content 1 --><!-- FAQ 3
            ==================================================================== -->
            <!-- /End FAQ 3 --><!-- Social 1
            ==================================================================== -->
            <!-- /End Social 1 --><!-- Header 1
            ==================================================================== -->
            <header id="header-section-1" class="header-section header-style-1">
                <!-- Header Section Container -->
                <div class="header-section-container">


                    <!-- Header Menu -->
                    <div class="header-menu">
                        <!-- Header Menu Container -->
                        <div class="header-menu" style="height: 80px;"><div class="header-menu-container header-menu-stuck">


                            <!-- Navbar -->
                            <nav class="navbar">
                                <!-- container -->
                                <div class="container">
                                    <!-- row -->
                                    <div class="row">
                                        <!-- col-md-12 -->
                                        <div class="col-md-12">


                                            <!-- Navbar Header -->
                                            <div class="navbar-header">

                                                <!-- Logo -->
                                                <a href="/stat" class="navbar-brand" title="LPB">
                                                    <img src="https://www.webhostingzone.org/wp-content/uploads/2020/06/logo.png" alt="LPB Logo">
                                                </a><!-- /End Logo -->

                                                <!-- Toggle Menu Button -->
                                                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
                                                    Menu <span><i class="lines"></i></span>
                                                </button><!-- /End Toggle Menu Button -->

                                            </div><!-- /End Navbar Header -->


                                            <!-- Navbar Collapse ( Menu ) -->
                                            <div class="collapse navbar-collapse">
                                                <ul class="nav navbar-nav navbar-right">

                                                    <li>
                                                        <a href="https://www.webhostingzone.org/" title="Р“Р»Р°РІРЅР°СЏ">WebHostingZone</a>
                                                    </li>

                                                    <li>
                                                        <a href="https://www.webhostingzone.org/members/clientarea.php" title="Рћ РєРѕРјРїР°РЅРёРё">Client Area</a>
                                                    </li>

                                                    <li>
                                                        <a href="https://www.webhostingzone.org/" title="РЈСЃР»СѓРіРё">Release Notes</a>
                                                    </li>

                                                </ul>
                                            </div><!-- /End Navbar Collapse ( Menu ) -->


                                        </div><!-- /End col-md-12 -->
                                    </div><!-- /End row -->
                                </div><!-- /End container -->
                            </nav><!-- /End Navbar -->


                        </div></div><!-- /End Header Menu Container -->
                    </div><!-- /End Header Menu -->


                </div><!-- /End Header Section Container -->
            </header><!-- /End Header 1 --><!-- Content 1
            ==================================================================== -->
            <div id="content-section-1" class="content-section white-section">
                <!-- Section Container -->
                <div class="section-container">


                    <!-- container -->
                    <div class="container">
                        <!-- row -->
                        <div class="row">


                            <!-- Title Block -->
                            <div class="col-lg-10 col-lg-offset-1 col-md-12 title-block content-block-container">
                                <!-- Title Block Container -->
                                <div class="title-block-container text-center">

                                    <!-- Title -->
                                    <h2>BigBlueButton Meetings Statistic</h2>

                                    <!-- Description -->
                                    <p>BigBlueButton Server: ''' + hname + '''</p>
									<p>Here you can find all information about your meetings what have been recorded.</p>

                                    <!-- Line Separator -->
                                    <div class="line-separator"></div>

									<h4>Past Meetings:</h4>

                                    <i class="fa fa-bar-chart circle-icon-block circle-icon-block-lg"></i>

                                </div><!-- /End Title Block Container -->
                            </div><!-- /End Title Block -->																		

							<iframe src="https://''' + hname + '/stat/' + '''recordings_statistics.html" width="1200" height="700" frameborder=0 id="frame"></iframe>

                        </div><!-- /End row -->
                    </div><!-- /End container -->

                </div><!-- /End Section Container -->
            </div><!-- /End Content 1 --><!-- FAQ 3
            ==================================================================== -->
            <div id="faq-section-3" class="faq-section white-section">
                <!-- Section Container -->
                <div class="section-container">

					 <center><h4>QUICK F.A.Q.</h2></center>
					 <center><div class="line-separator"></div></center>

                    <!-- container -->
                    <div class="container">
                        <!-- row -->
                        <div class="row">


                            <!-- FAQ Block -->
                            <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                <!-- FAQ Block Container -->
                                <div class="faq-block-container" style="height: 158px;">

                                    <!-- Title -->
                                    <h4>Why not clickable links?</h4>

                                    <!-- Description -->
                                    <p>This project is in Development stage. This feature will be added soon.</p>

                                </div><!-- /End FAQ Block Container -->
                            </div><!-- /End FAQ Block -->

                            <!-- FAQ Block -->
                            <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                <!-- FAQ Block Container -->
                                <div class="faq-block-container" style="height: 158px;">

                                    <!-- Title -->
                                    <h4>Why some data is not available?</h4>

                                    <!-- Description -->
                                    <p>BidBlueButton scripts keep cleaning conference data what is the oldest then 20 days after ending.</p>

                                </div><!-- /End FAQ Block Container -->
                            </div><!-- /End FAQ Block -->


                            <!-- FAQ Block -->
                            <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                <!-- FAQ Block Container -->
                                <div class="faq-block-container" style="height: 158px;">

                                    <!-- Title -->
                                    <h4>There is no *.mp4 download button.</h4>

                                    <!-- Description -->
                                    <p>For download conference record in .mp4 format converting script should be installed on your server.</p>

                                </div><!-- /End FAQ Block Container -->
                            </div><!-- /End FAQ Block -->


                            <!-- FAQ Block -->
                            <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                <!-- FAQ Block Container -->
                                <div class="faq-block-container" style="height: 158px;">

                                    <!-- Title -->
                                    <h4>I need special format data.</h4>

                                    <!-- Description -->
                                    <p>If you need data in some special format (pdf, html etc) please contact us: support@webhostingzone.org</p>

                                </div><!-- /End FAQ Block Container -->
                            </div><!-- /End FAQ Block -->


                            <!-- FAQ Block -->
                            <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                <!-- FAQ Block Container -->
                                <div class="faq-block-container" style="height: 158px;">

                                    <!-- Title -->
                                    <h4>How do i change data in reports?</h4>

                                    <!-- Description -->
                                    <p>There is no way to change data in reports (conference name, date etc). You're able to do it manually after download the file.</p>

                                </div><!-- /End FAQ Block Container -->
                            </div><!-- /End FAQ Block -->


                            <!-- FAQ Block -->
                            <div class="col-lg-4 col-md-6 faq-block faq-block-style-1">
                                <!-- FAQ Block Container -->
                                <div class="faq-block-container" style="height: 158px;">

                                    <!-- Title -->
                                    <h4>How do i contact with you?</h4>

                                    <!-- Description -->
                                    <p>Email: support@webhostingzone.org  Phone: +1 (404) 382 9079 webhostingzone.org</p>                               

                                </div><!-- /End FAQ Block Container -->
                            </div><!-- /End FAQ Block -->


                        </div><!-- /End row -->
                    </div><!-- /End container -->


                </div><!-- /End Section Container -->
            </div><!-- /End FAQ 3 --><!-- Timeline 1
            ==================================================================== -->
</div><!-- /End Timeline 1 --><!-- Copyright 2
            ==================================================================== -->
            <footer id="copyright-section-2" class="copyright-section white-section">
                <!-- Section Container -->
                <div class="section-container">


                    <!-- container -->
                    <div class="container">
                        <!-- row -->
                        <div class="row">


                            <!-- Copyright Block -->
                            <div class="col-md-6 copyright-block">
                                <!-- Copyright Block Container -->
                                <div class="copyright-block-container">

                                    <!-- Title -->
                                    <p>В© 2020 <a href="https://www.webhostingzone.org/" title="WebHostingZone">WebHostingZone</a>, all rights reserved. <a href="https://github.com/georgethegreatat" title="GitHub</a></p>

                                </div><!-- /End Copyright Block Container -->
                            </div><!-- /End Copyright Block -->


                            <!-- Copyright Block -->
                            <div class="col-md-6 copyright-block">
                                <!-- Copyright Block Container -->
                                <div class="copyright-block-container">

                                    <!-- Social Icons Block -->
                                    <div class="social-icons-block social-icons-block-sm social-icons-block-style-1 text-right">
                                        <ul>
                                            <li><a href="https://www.facebook.com/WebHostingZone/" title="Facebook"><i class="fa fa-facebook"></i></a></li>
                                            <li><a href="https://twitter.com/WebHostingZone" title="Twitter"><i class="fa fa-twitter"></i></a></li>
                                        </ul>
                                    </div><!-- /End Social Icons Block -->

                                </div><!-- /End Copyright Block Container -->
                            </div><!-- /End Copyright Block -->


                        </div><!-- /End row -->
                    </div><!-- /End container -->


                </div><!-- /End Section Container -->

            </footer><!-- /End Copyright 2 --></div><!-- /End Main Wrapper -->




        <!-- Java Script Files		
		<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>		
        ======================================================================== -->
        <script type="text/javascript" src="js/jquery.min.js"></script>
        <script type="text/javascript" src="js/jquery-ui.min.js"></script>
        <script type="text/javascript" src="js/vendor/bootstrap/js/bootstrap.min.js"></script>
        <script type="text/javascript" src="js/plugins/mobile/mobile.min.js"></script>
        <script type="text/javascript" src="js/scripts.js"></script>

<style>
#style-switcher {
    z-index: 9999;
    position: fixed;
    top: 100px;
    width: 212px;
    height: auto;
    /*min-height: 200px;*/
    border: 1px solid #f1f1f1;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    text-align: left;
    background: white;
    -webkit-transition: all 0.5s;
    -moz-transition: all 0.5s;
    transition: all 0.5s;
}

.close-style-switcher {
    left: -212px;
}

.open-style-switcher {
    left: -1px;
}

#style-switcher .segment {
    width: 100%;
    padding: 15px 10px 15px 0;
    padding: 15px 25px;

}

#style-switcher a.panel-button {
    position: absolute;
    top: 30px;
    right: -50px;
    width: 50px;
    height: 50px;
    border: 1px solid #f1f1f1;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    text-align: center;
    font-size: 23px;
    line-height: 47px;
    background: white;
    cursor: pointer;
}

#style-switcher h3 {
    margin: 0;
}

#style-switcher .segment a.switcher {
    display: inline-block;
    width: 25px;
    height: 25px;
    margin-top: 5px;
    margin-right: 3px;
    border: 1px solid #efefef;
    cursor: pointer;
}

.red-bg {
    background: #EF4035;
}

.orange-bg {
    background: #F26F21;
}

.yellow-bg {
    background: #FFC153;
}

.green-bg {
    background: #5CB85C;
}

.turquoise-bg {
    background: #41C4AB;
}

.aqua-bg {
    background: #38E6D8;
}

.blue-bg {
    background: #0A8FD5;
}

.purple-bg {
    background: #AC5AFF;
}

.pink-bg {
    background: #F62459;
}

.tan-bg {
    background: #C2B49A;
}

@media(max-width:480px) {
    #style-switcher {
        top: 30px;
    }
}		
    </style>		

    <script>
	// Style Switcher Open/Close
$('#style-switcher .panel-button').click(function() {
    //$('#style-switcher').toggleClass('close-style-switcher', 'open-style-switcher', 1000);
    $('#style-switcher').toggleClass('open-style-switcher', 'close-style-switcher', 1000);
    return false;
});

// Color Skins
$('.switcher').click(function() {
    var title = jQuery(this).attr('title');
    jQuery('#changeable-colors').attr('href', 'css/css/' + title + '.css');
    return false;
});

	</script>


<iframe name="ym-native-frame" title="ym-native-frame" frameborder="0" aria-hidden="true" style="opacity: 0 !important; width: 0px !important; height: 0px !important; position: absolute !important; left: 100% !important; bottom: 100% !important; border: 0px !important;"></iframe><ym-measure class="ym-viewport" style="display: block; top: 0px; right: 0px; bottom: 0px; left: 0px; height: 100vh; width: 100vw; position: fixed; transform: translate(0px, -100%); transform-origin: 0px 0px;"></ym-measure><ym-measure class="ym-zoom" style="bottom: 100%; position: fixed; width: 100vw;"></ym-measure></body></html>'''
    htmlindex.write(genpage)
    htmlindex.close()


def getresultoperation():
    now = datetime.datetime.now()
    print('Script has been running successfully at: ')
    print(now)


def globalinfo():
    url = 'https://' + hname + '/bigbluebutton/api/getRecordings?checksum=' + checksum

    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()

    parser = lxml.etree.XMLParser(recover=True)
    tree = lxml.etree.fromstring(respData, parser)

    arr = [element.text for element in
           tree.iter('recordID', 'meetingID', 'participants', 'startTime', 'endTime', 'name')]

    bbfile = open('/var/www/stat/stat/recordings_statistics.html', 'w')
    art0 = '''<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8">
  <title>font-family</title>
  <style>
   p {
    font-family: Verdana, Verdana, serif;
    font-size: 10pt;
   }
  </style>
 </head>
 <body>
 <p>'''
    bbfile.write(art0)
    bbfile.close()

    bbbfile = open('/var/www/stat/stat/recordings_statistics.html', 'a')
    for i in range(len(arr)):
        if (i % 6 == 0):
            art1 = 'Meeting Info:    {} <br>Meeting ID:  &nbsp  {} <br>Start Time:&nbsp&nbsp&nbsp {} <br>End Time: &nbsp&nbsp&nbsp&nbsp {} <br>Conference name: {} <br>Paricipants:     {}  <br><br><br>'.format(
                '<a href="https://' + hname + '/stat/' + arr[
                    i - 6] + '.html" target="_blank" title="Meeting Info">Details</a>',
                arr[i - 6],
                sttm(mtts=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(arr[i - 3]) / 1000.))),
                ettm(mtte=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(arr[i - 2]) / 1000.))),
                ten(wrt=arr[i - 4]), attm(mtta=arr[i - 1]),
                nine(y=arr[i - 6]))
            bbbfile.write(art1)
    bbbfile.close()


cleanoldtxt()

globalinfo()

genglobindexpage()

getresultoperation()
