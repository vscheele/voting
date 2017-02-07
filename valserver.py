from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import time
from os import curdir, sep



class WebserverHandler(BaseHTTPRequestHandler):
    lastRefresh = 0.0
    cachedvalues = []
    def do_GET(self):
        try:
            if self.path.endswith("/v123"):
                self.send_response(200)
                self.send_header('Content-Type','text/html')
                self.end_headers()

                output=""
                output+="<html><title>FG-434 Vote</title>" \
                        "<head>" \
                        "<link rel=\"stylesheet\" href=\"styles.css\">"\
                        "<script src=\"jquery-3.1.1.min.js\"></script> " \
                        "<script src=\"valscript.js\"></script> " \
                        "<body onload=\"javascript:initform()\"><div class=\"header\"> FG-434 Vote:</div>"
                output += "<div id=\"formdiv\"><form method='POST' id='idform' enctype='multipart/form-data' action='/voted'><h2>" \
                          "</h2>" \
                          "<div class=\"hideme\"> Antwort -1 <input type=\"radio\" name=\"radiovote\" value=\"-1\" checked=\"checked\"/></div>" \
                          "<div class=\"opt\"> Antwort 1 <input type=\"radio\" name=\"radiovote\" value=\"0\" /></div>"\
                          "<div class=\"opt\"> Antwort 2 <input type=\"radio\" name=\"radiovote\" value=\"1\" /></div>"\
                          "<div class=\"opt\"> Antwort 3 <input type=\"radio\" name=\"radiovote\" value=\"2\" /></div>"\
                          "<div class=\"submitdiv\"><input class=\"submitbutton\" type='submit' value='OK!'></div>"\
                          "</form></div>" \
                          "<div id='resultcontent'></div>"
                output+="</body></html>"
                self.wfile.write(output)
                print output
                return
            else:
                #Check the file extension required and
                #set the right mime type

                sendReply = False
                if self.path.endswith(".html"):
                    mimetype='text/html'
                    sendReply = True
                if self.path.endswith(".txt"):
                    mimetype='text/html'
                    sendReply = True
                if self.path.endswith(".jpg"):
                    mimetype='image/jpg'
                    sendReply = True
                if self.path.endswith(".png"):
                    mimetype='image/png'
                    sendReply = True
                if self.path.endswith(".gif"):
                    mimetype='image/gif'
                    sendReply = True
                if self.path.endswith(".js"):
                    mimetype='application/javascript'
                    sendReply = True
                if self.path.endswith(".css"):
                    mimetype='text/css'
                    sendReply = True

                if sendReply == True:
                    #Open the static file requested and send it
                    #f = open(curdir + sep + self.path)
                    f = open(curdir + sep + self.path, 'rb')
                    self.send_response(200)
                    self.send_header('Content-type',mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                return
        except IOError:
            self.send_error(404,"File not Found %s" % self.path)

    def do_POST(self):
        if self.path.endswith("/votedajax"):
                self.send_response(200)
                self.end_headers()
                postvars={}
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    postvars = cgi.parse_multipart(self.rfile, pdict)
                elif ctype == 'application/x-www-form-urlencoded':
                    length = int(self.headers.getheader('content-length'))
                    postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                choice= int(postvars['radiovote'][0])
                if choice !=-1:
                    raiseCounter(choice)
                print choice, " has been voted"
                self.wfile.write(self.readandformatresults())
                return
        elif self.path.endswith("/refresh"):  #only refresh, no vote
                self.send_response(200)
                self.end_headers()
                self.wfile.write(self.readandformatresults())
                return

    def readandformatresults(self):
        t000 = time.time()
        result = ""
        # result="<table cellspacing=\"0\" cellpadding=\"0\" summary=\"Sweden was the top importing country by far in 1998.\">      <caption align=\"top\">Top banana importers 1998 (value of banana imports in millions of US dollars per million people)<br /><br /></caption>      <tr>        <th scope=\"col\"><span class=\"auraltext\">Country</span> </th>        <th scope=\"col\"><span class=\"auraltext\">Millions of US dollars per million people</span> </th>      </tr>      <tr>        <td class=\"first\">Sweden</td>        <td class=\"value first\"><img src=\"bar.png\" alt=\"\" width=\"200\" height=\"16\" />17.12</td>      </tr>      <tr>        <td>United&nbsp;Kingdom</td>        <td class=\"value\"><img src=\"bar.png\" alt=\"\" width=\"104\" height=\"16\" />8.88</td>      </tr>      <tr>        <td>Germany</td>        <td class=\"value\"><img src=\"bar.png\" alt=\"\" width=\"98\" height=\"16\" />8.36</td>      </tr>      <tr>        <td>Italy</td>        <td class=\"value\"><img src=\"bar.png\" alt=\"\" width=\"70\" height=\"16\" />5.96</td>      </tr>      <tr>        <td>United States </td>        <td class=\"value\"><img src=\"bar.png\" alt=\"\" width=\"56\" height=\"16\" />4.78</td>      </tr>      <tr>        <td>Canada</td>        <td class=\"value\"><img src=\"bar.png\" alt=\"\" width=\"54\" height=\"16\" />4.62</td>      </tr>      <tr>        <td>Japan</td>        <td class=\"value\"><img src=\"bar.png\" alt=\"\" width=\"50\" height=\"16\" />4.30</td>      </tr>      <tr>        <td>France</td>        <td class=\"value\"><img src=\"bar.png\" alt=\"\" width=\"39\" height=\"16\" />3.33</td>      </tr>      <tr>        <td>Russia</td>        <td class=\"value last\"><img src=\"bar.png\" alt=\"\" width=\"12\" height=\"16\" />1.04</td>      </tr>    </table>"
        result += "<table cellspacing=\"0\" cellpadding=\"0\" summary=\"Results.\">"
        t0 = time.time()
        if (t0 - WebserverHandler.lastRefresh > 1):
            f = open('results123.txt', 'r')
            entries = f.read().split(";")
            f.close()
            WebserverHandler.cachedvalues = entries
            WebserverHandler.lastRefresh = t0
            print "non-cache",entries
        else:
            entries = WebserverHandler.cachedvalues
            print "cache",entries
        for i in range(0, len(entries)):
            result += "<tr><td class=\"first\">Antwort " + str(i) + "</td>\r\n"
            result += "        <td class=\"value first\"><img src=\"bar.png\" alt=\"\" width=\"" + str(
                10 * int(entries[i])) + "\" height=\"16\" />" + entries[i] + "</td>\r\n"
            result += "</tr>\r\n"
        result += "</table>"
        t1 = time.time()
        print time, t1 - t000
        return result

def raiseCounter(index):

    f = open('results123.txt', 'r')
    oldres=f.read().split(";")
    f.close()
    oldres[index]=int(oldres[index])+1
    f = open('results123.txt', 'w')
    resultstring=""
    for i in oldres:
        resultstring+=str(i)+";"
    f.write(resultstring[:-1])
    f.close()


def main():
    try:
        port=8080
        server=HTTPServer(('',port),WebserverHandler)
        print "Valentin's Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping Valentin's web server"
        server.socket.close()

if  __name__ =='__main__':
    main()

