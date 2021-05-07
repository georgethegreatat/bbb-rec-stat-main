import datetime
import urllib.request
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring
import json
import os
import csv
import pandas as pd
import threading
import socket
from pretty_html_table import build_table

# Environment variables
ui_logo_link = "https://www.webhostingzone.org/wp-content/uploads/2020/06/new-logo-small.png"
fb_link = "https://www.facebook.com/WebHostingZone/"
twitter_link = "https://twitter.com/WebHostingZone"
hname = socket.gethostname()

# Delete the old *.txt files before start
def cleanoldtxt():
    directory = "/var/www/stat/stat"

    files_in_directory = os.listdir(directory)

    filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

# Grobal variables define
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

def muser(userm):
    global muserm
    muserm = userm
    return userm

def memail(ememail):
    global emailmod
    emailmod = ememail
    return emailmod

# Time convertation function
def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

# General data function; parsing userlist from events.xml and creating json with it; converting to csv and html;
def nine(y):
    global meeting_end
    if os.path.isfile("/var/bigbluebutton/recording/raw/" + y + "/events.xml"):
        if os.path.isfile("/var/www/stat/stat/" + y + ".htm"):
            print("File already in the folder. ID: ", y)
        else:
            archived_files_id_list = os.listdir("/var/bigbluebutton/recording/raw")
            for archived_files_id in archived_files_id_list:

                root = ET.parse("/var/bigbluebutton/recording/raw/" + y + '/events.xml').getroot()

                visit_log = {}
                joins, leaves = [], []

                # registering events of interest
                for event in root.findall("./event[@module='PARTICIPANT']"):
                    time = int(event.find('timestampUTC').text) // 1000
                    if event.get('eventname') == 'ParticipantJoinEvent':
                        joins.append({'time': time,
                                      'name': event.find('name').text,
                                      'id': event.find('userId').text})
                    if event.get('eventname') == 'ParticipantLeftEvent':
                        leaves.append({'time': time,
                                       'id': event.find('userId').text})
                    if event.get('eventname') == 'EndAndKickAllEvent':
                        meeting_end = time

                # compiling records by user
                for jn in joins:
                    username, lgn = jn['name'], jn['time']
                    lgt = meeting_end

                    # finding who's left before meeting end
                    for i, lv in enumerate(leaves):
                        if jn['id'] == lv['id']:
                            lgt = lv['time']
                            leaves.pop(i)
                            break

                    duration = round((lgt - lgn) / 60)
                    user_standing = "%d:%02d" % (divmod(duration, 60))

                    if visit_log.get(username):
                        visit_log[username]['TimeLogout'] = convert_timestamp(lgt)
                        visit_log[username]['Standing'] = user_standing
                    #                    visit_log[username]['number_of_visits'] += 1
                    else:
                        visit_log[username] = dict(
                            Name=username,
                            TimeLogin=convert_timestamp(lgn),
                            TimeLogout=convert_timestamp(lgt),
                            Standing=user_standing
                        )

                # saving the log as a JSON to file
                with open('/var/www/stat/stat/' + y + '.json', 'w') as f:
                    json.dump([visit_log[u] for u in sorted(visit_log)], f, ensure_ascii=True, sort_keys=True, indent=4,
                              default=str)

            def jsontocsv():
                jsoncsv = pd.read_json(r'/var/www/stat/stat/' + y + '.json')
                jsoncsv.to_csv(r'/var/www/stat/stat/' + y + '.csv', index=None)

            def csvtohtml():
                print(y)
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

                filepcsvt = open("/var/www/stat/stat/" + y + ".csv")
                numlinee = len(filepcsvt.readlines())
                trany = numlinee - 1
                tran = str(trany)

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
                                    <link rel="shortcut icon" href="''' + ui_logo_link + '''">
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
                                                                                    <a href="https://www.webhostingzone.org/" title="ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â»ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã‚ÂÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã‚ÂÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â¡ÃƒÆ’Ã‚Â">WebHostingZone</a>
                                                                                </li>

                                                                                <li>
                                                                                    <a href="https://www.webhostingzone.org/members/clientarea.php" title="ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‚Âº ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¢ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒâ€¹Ã…â€œÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬ÂÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã‚ÂÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‹Å“ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‹Å“">Client Area</a>
                                                                                </li>

                                                                                <li>
                                                                                    <a href="https://github.com/georgethegreatat/bbb-rec-stat-main/" title="Notes">Release Notes</a>
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
                                                                <p><b>Participants:</b> ''' + tran + ''' | <b>Moderator:</b> ''' + muserm + '''</p>
                                                                <p><b>Moderator Email:</b> ''' + emailmod + '''</p>
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
                                                                <p>ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â© 2020 <a href="https://www.webhostingzone.org/" title="WebHostingZone">WebHostingZone</a>, all rights reserved. Version --> v1.1 <a href="https://github.com/georgethegreatat" title="GitHub</a></p>

                                                            </div><!-- /End Copyright Block Container -->
                                                        </div><!-- /End Copyright Block -->


                                                        <!-- Copyright Block -->
                                                        <div class="col-md-6 copyright-block">
                                                            <!-- Copyright Block Container -->
                                                            <div class="copyright-block-container">

                                                                <!-- Social Icons Block -->
                                                                <div class="social-icons-block social-icons-block-sm social-icons-block-style-1 text-right">
                                                                    <ul>
                                                                        <li><a href="''' + fb_link + '''" title="Facebook"><i class="fa fa-facebook"></i></a></li>
                                                                        <li><a href="''' + twitter_link + '''" title="Twitter"><i class="fa fa-twitter"></i></a></li>
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

    else:
        print("There is no file.")



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
        <link rel="shortcut icon" href="''' + ui_logo_link + '''">
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
                                                        <a href="https://www.webhostingzone.org/" title="ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â»ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã‚ÂÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã‚ÂÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â¡ÃƒÆ’Ã‚Â">WebHostingZone</a>
                                                    </li>

                                                    <li>
                                                        <a href="https://www.webhostingzone.org/members/clientarea.php" title="ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‚Âº ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¢ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒâ€¹Ã…â€œÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬ÂÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â°ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã‚ÂÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‹Å“ÃƒÆ’Ã‚ÂÃƒâ€šÃ‚Â ÃƒÆ’Ã¢â‚¬ËœÃƒÂ¢Ã¢â€šÂ¬Ã‹Å“">Client Area</a>
                                                    </li>

                                                    <li>
                                                        <a href="https://github.com/georgethegreatat/bbb-rec-stat-main/" title="Notes">Release Notes</a>
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
                                    <h4>Why doesn't it count users correctly?</h4>

                                    <!-- Description -->
                                    <p>BigBlueButton is tracking all users log-in/out moves. Correct count feature will be adding soon.</p>

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
                                    <p>WebHostingZone © 2021 <a href="https://www.webhostingzone.org/" title="WebHostingZone">WebHostingZone</a>, all rights reserved. Version --> v1.1 <a href="https://github.com/georgethegreatat" title="GitHub</a></p>

                                </div><!-- /End Copyright Block Container -->
                            </div><!-- /End Copyright Block -->


                            <!-- Copyright Block -->
                            <div class="col-md-6 copyright-block">
                                <!-- Copyright Block Container -->
                                <div class="copyright-block-container">

                                    <!-- Social Icons Block -->
                                    <div class="social-icons-block social-icons-block-sm social-icons-block-style-1 text-right">
                                        <ul>
                                            <li><a href="''' + fb_link + '''" title="Facebook"><i class="fa fa-facebook"></i></a></li>
                                            <li><a href="''' + twitter_link + '''" title="Twitter"><i class="fa fa-twitter"></i></a></li>
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
    bbfile = open('/var/www/stat/stat/recordings_statistics.html', 'w')
    art0 = '''<center><table class="dataframe" style="width: 973px; height: 73px;" border="0">
<thead>
<tr style="text-align: right; height: 24px;">
<th style="background-color: #ffffff; font-family: 'Century Gothic'; font-size: medium; color: #305496; text-align: center; border-bottom: 2px solid #305496; padding: 0px 20px 0px 0px; height: 24px; width: 157px;">Meeting Name</th>
<th style="background-color: #ffffff; font-family: 'Century Gothic'; font-size: medium; color: #305496; text-align: center; border-bottom: 2px solid #305496; padding: 0px 20px 0px 0px; height: 24px; width: 182px;">Start</th>
<th style="background-color: #ffffff; font-family: 'Century Gothic'; font-size: medium; color: #305496; text-align: center; border-bottom: 2px solid #305496; padding: 0px 20px 0px 0px; height: 24px; width: 183px;">End</th>
<th style="background-color: #ffffff; font-family: 'Century Gothic'; font-size: medium; color: #305496; text-align: center; border-bottom: 2px solid #305496; padding: 0px 20px 0px 0px; height: 24px; width: 117px;">Participants</th>
<th style="background-color: #ffffff; font-family: 'Century Gothic'; font-size: medium; color: #305496; text-align: center; border-bottom: 2px solid #305496; padding: 0px 20px 0px 0px; height: 24px; width: 100px;">Users List</th>
<th style="background-color: #ffffff; font-family: 'Century Gothic'; font-size: medium; color: #305496; text-align: center; border-bottom: 2px solid #305496; padding: 0px 20px 0px 0px; height: 24px; width: 100px;">MP4</th>
</tr>
</thead>
</table>
</center>
    '''
    bbfile.write(art0)
    bbfile.close()

    internal_meeting_id_list = os.listdir("/var/bigbluebutton/recording/raw")

    for internal_meeting_id in internal_meeting_id_list:
        path = "/var/bigbluebutton/recording/raw/" + internal_meeting_id + "/events.xml"

        tree = ET.parse(path)
        root = tree.getroot()

        for meeting in root.findall('meeting'):
            idc = meeting.get('id')
            namemeeting = meeting.get('name')
        for metadata in root.findall('metadata'):
            moderator_address = metadata.get('canvas-recording-ready-user')
            if moderator_address is None:
                moderator_email = 'Unknown'
            else:
                moderator_email = moderator_address
            server = metadata.get('bbb-origin')
            if server is None:
                server_fin = "Unknown"
            else:
                server_fin = server
        for event in root.findall("./event[@module='PRESENTATION']"):
            if event.get('eventname') == 'CreatePresentationPodEvent':
                Time1 = datetime.datetime.fromtimestamp(int(event.find('timestampUTC').text) / 1000).strftime('%Y-%m-%d | %H:%M:%S')
        for event in root.findall("./event[@module='PARTICIPANT']"):
            if event.get('eventname') == 'EndAndKickAllEvent':
                Time2 = datetime.datetime.fromtimestamp(int(event.find('timestampUTC').text) / 1000).strftime('%Y-%m-%d | %H:%M:%S')
        for event in root.findall("./event[@module='PARTICIPANT']"):
            if event.get('eventname') == 'ParticipantJoinEvent':
                defvalue = event.find('role').text
                if defvalue == 'MODERATOR':
                    slov = event.find('name').text
                    break


        ten(wrt=namemeeting)
        sttm(mtts=Time1)
        ettm(mtte=Time2)
        muser(userm=slov)
        memail(ememail=moderator_email)
        nine(y=idc)

        filepcsv = open("/var/www/stat/stat/" + idc + ".csv")
        numline = len(filepcsv.readlines())
        pumpy = numline - 1
        pump = str(pumpy)

        bbbfile = open('/var/www/stat/stat/recordings_statistics.html', 'a')
        art1 =('''<center>
                <table>
                <tbody>
                <tr style="height: 31px;">
                <td style="background-color: #d9e1f2; font-family: 'Century Gothic'; font-size: medium; text-align: center; padding: 0px 20px 0px 0px; height: 31px; width: 157px;">''' + ten(wrt=namemeeting) + '''</td>
                <td style="background-color: #d9e1f2; font-family: 'Century Gothic'; font-size: medium; text-align: center; padding: 0px 20px 0px 0px; height: 31px; width: 182px;">''' + sttm(mtts=Time1) + '''</td>
                <td style="background-color: #d9e1f2; font-family: 'Century Gothic'; font-size: medium; text-align: center; padding: 0px 20px 0px 0px; height: 31px; width: 183px;">''' + ettm(mtte=Time2) + '''</td>
                <td style="background-color: #d9e1f2; font-family: 'Century Gothic'; font-size: medium; text-align: center; padding: 0px 20px 0px 0px; height: 31px; width: 117px;">''' + pump + '''</td>
                <td style="background-color: #d9e1f2; font-family: 'Century Gothic'; font-size: medium; text-align: center; padding: 0px 20px 0px 0px; height: 31px; width: 100px;"><a title="Details" href="https://''' + hname + '''/stat/''' + idc + '''.html" target="_blank">Link</a></td>
                <td style="background-color: #d9e1f2; font-family: 'Century Gothic'; font-size: medium; text-align: center; padding: 0px 20px 0px 0px; height: 31px; width: 100px;"><a href="https://''' + hname + '''/record/''' + idc + '''.mp4" title="Download mp4">Download</td>
                </tr>
                </tbody>
                </table>
                </center>
                '''
                )
        if numline <= 2:
            bbbfile.close()
        else:
            bbbfile.write(str(art1))
            bbbfile.close()

cleanoldtxt()

genglobindexpage()

globalinfo()

getresultoperation()
