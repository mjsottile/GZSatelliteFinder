#
# cherrypy-based web service for testing trail finder.
#
import urllib2, json, urllib
import cherrypy
import csv
import os.path
import FeatureExtractor as features
import config as cfg
import LinePlotter as lines

def genform():
    return """
<form action="processImage" method="post">
    <p>SDSS DR10 ObjID</p>
    <input type="text" name="objid" value=""
        size="15" maxlength="40"/>
    <p><input type="submit" value="Submit"/></p>
</form>"""

class Root(object):
    def __init__(self):
        self.image_cache = "/home/matt/gzhelper/images/"
        self.sdss_file = "/home/matt/gzhelper/sdss_ids_URLs.csv"
        self.sdss_db = None
        self.latest_image = None
        self.config = cfg.read_gztf_config("trailfinder.cfg")

    def do_line_search(self, fname, objid):
        retval = features.line_signature_wrapper(fname,self.config)
        
        # set latest lineout image to the "no lineouts" default, which
        # will get overwritten if something is there.
        self.latest_lineout_image = "/home/matt/gzhelper/images/nothing.jpg"

        if (retval == None):
            return (False,-1)

        (rd,rh,rl) = retval

        ### NO LINES.
        if (rd.size == 0):
            return (False,-1)

        objs = features.compute_sig_objects(rd,rh,rl)

        fname = "/home/matt/gzhelper/images/lineouts_"+str(objid)+".jpg"
        self.latest_lineout_image = fname
        lines.show_lineout(fname, objs, 4, 4, self.config)

        for o in objs:
            (bool,which) = features.is_it_a_trail(o, self.config)
            if bool:
                return (True, which)
        
        return (False, -1)

    def refresh_sdss_db(self):
        if self.sdss_db==None:
            print "Refreshing SDSS DB"
            self.sdss_db = {}
            with open(self.sdss_file, 'rb') as csvfile:
                entries = csv.reader(csvfile)
                for entry in entries:
                    self.sdss_db[entry[1]] = entry[2]
        else:
            print "Using cached SDSS DB"

    def get_gz_image(self, objid):
        fname = self.image_cache+str(objid)+".jpg"
        if not os.path.exists(fname):
            image = urllib.URLopener()
            image.retrieve(self.sdss_db[str(objid)], fname)
    
        self.latest_image = fname

    def query_simbad(self,ra,dec):
        baseurl = "http://simbad.u-strasbg.fr/simbad/sim-script"
        data = {}
        script = "format object \"%OTYPE(S)\"\n"
        script = script + "query coo "+str(ra)+" "+str(dec)
        data['script'] = script
        fullurl = baseurl + "?" + urllib.urlencode(data)
        response = urllib2.urlopen(fullurl)
        keep_next = False
        val = ""
        for line in response:
            if (len(line.rstrip('\r\n')) < 1):
                continue
            if keep_next == True:
                val = val + line.rstrip('\r\n')
                break
            if line.startswith('::data::'):
                keep_next = True
        return val


    def query_sdss(self,objid):
        baseurl = "http://skyserver.sdss3.org/public/en/tools/search/x_sql.aspx"
        data = {}
        data['format'] = 'json'
        data['cmd'] = 'select * from photoobj where objid = '+str(objid)
        fullurl = baseurl + '?' + urllib.urlencode(data)
        response = urllib2.urlopen(fullurl)
        out = json.load(response)
        
        if len(out[0]['Rows']) < 1:
            return None

        result = out[0]['Rows'][0]
        return result

    @cherrypy.expose
    def index(self):
        return '<HTML>'+genform()+'</HTML>'

    @cherrypy.expose
    def showLatestLineoutImage(self):
        cherrypy.response.headers['Content-Type'] = 'application/jpeg'
        f = open(self.latest_lineout_image, 'r')
        data = f.read()
        f.close()
        return data

    @cherrypy.expose
    def showLatestLineImage(self):
        cherrypy.response.headers['Content-Type'] = 'application/jpeg'
        f = open(self.latest_lines_image, 'r')
        data = f.read()
        f.close()
        return data

    @cherrypy.expose
    def showLatestImage(self):
        cherrypy.response.headers['Content-Type'] = 'application/jpeg'
        f = open(self.latest_image, 'r')
        data = f.read()
        f.close()
        return data

    @cherrypy.expose
    def processImage(self, objid=None):
        if objid==None:
            return "<HTML><BODY>No ID provided.</BODY></HTML>"

        if len(objid)<1:
            return "<HTML><BODY>No ID provided.</BODY></HTML>"

        # remove leading and trailing whitespace
        objid = objid.strip()

        self.refresh_sdss_db()
        if not(objid in self.sdss_db):
            return "<HTML><BODY>ID not in the GZ image set.</BODY></HTML>"

        # get the image
        self.get_gz_image(objid)

        # issue an SQL query to the SDSS database for more info
        sdss_result = self.query_sdss(objid)
        
        obj_ra = sdss_result['ra']
        obj_dec = sdss_result['dec']

        mystring = 'RA='+str(obj_ra)+'<BR>DEC='+str(obj_dec)

        if (sdss_result['insideMask'] & 0x04 == 4):
            mystring += '<P>This object resides within a TRAIL mask.  You probably are seeing a satellite that passed through the imaging field.'
        elif (sdss_result['insideMask'] > 0):
            mystring += '<P>This image is masked in the SDSS database, indicating the presence of artifacts or other features that render the image useless for analysis.'
        else:
            mystring += '<P>No definitive trail mask is present from SDSS.'

        debug_string = '<P>SDSS InsideMask Column = '+str(sdss_result['insideMask'])

        # test if there is a line present that could be a trail.
        (is_line, which) = self.do_line_search(self.latest_image, objid)

        if is_line:
            mystring += "<P>Hough filter detects a trail in the "
            if which == 1:
                mystring += "green channel"
            elif which == 2:
                mystring += "blue channel"
            elif which == 3:
                mystring += "red channel"
            
            outfile = "/home/matt/gzhelper/images/lines_"+str(objid)+".jpg"
            self.latest_lines_image = outfile
            lines.lineplot_wrapper(self.latest_image, outfile, self.config)

            debug_string += '<P>Image w/ Hough results highlighted below.<P><IMG SRC="/showLatestLineImage"><P>'
        else:
            mystring += "<P>No trail detected via Hough method."
            outfile = "/home/matt/gzhelper/images/lines_"+str(objid)+".jpg"
            self.latest_lines_image = outfile
            lines.lineplot_wrapper(self.latest_image, outfile, self.config)
            debug_string += '<P>Image w/ Hough results highlighted below.<P><IMG SRC="/showLatestLineImage"><P>'

        debug_string += '<P>RGB lineouts for up to 16 lines.<P><IMG SRC="/showLatestLineoutImage"><P>'

        simbad_type = self.query_simbad(obj_ra, obj_dec)

        mystring += '<P>'+self.decode_simbad_type(simbad_type)

        return '<HTML><IMG SRC="/showLatestImage"><P>'+mystring+'<P><HR><P><I>Debugging info:</I><P>'+debug_string+'</HTML>'

    def decode_simbad_type(self, ty):
        if ty=="PN":
            return "SIMBAD indicates that this object is a <A HREF=\"http://en.wikipedia.org/wiki/Planetary_nebula\">Planetary Nebula</A>"
        elif ty=="HH":
            return "SIMBAD indicates that this object is a <A HREF=\"http://en.wikipedia.org/wiki/Herbig-haro_object\">Herbig-Haro object</A>"
        elif ty=="Star":
            return "SIMBAD indicates that this object is a star."
        elif ty=="RadioG":
            return "SIMBAD indicates that this object is a radio galaxy."
        elif ty=="Galaxy":
            return "SIMBAD indicates that this object is a galaxy."
        elif ty=="GinGroup":
            return "SIMBAD indicates that this object is a galaxy in a group of galaxies."
        elif ty=="GinCl":
            return "SIMBAD indicates that this is a galaxy in a cluster of galaxies."
        elif len(ty) > 1:
            return "SIMBAD returns a type that is not interpreted by this code yet.  ("+ty+")"
        else:
            return "SIMBAD didn't return anything useful for this object."

##
## start the service
##
if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(Root())

# test objects:
#  1237660558135787607
#  1237646586638827702
#  1237657608571125897
#  1237656539664089169  <- should hit for a trail via image analysis
