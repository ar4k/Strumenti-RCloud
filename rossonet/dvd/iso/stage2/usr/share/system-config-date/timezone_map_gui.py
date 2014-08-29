# -*- coding: utf-8 -*-
#
# timezone_map_gui.py: gui timezone map widget.
#
# Copyright 2001 - 2006 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# library public license.
#
# You should have received a copy of the GNU Library Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#Originally written by Matt Wilson <msw@redhat.com>
#Additions by:
#Brent Fox <bfox@redhat.com>
#Nils Philippsen <nphilipp@redhat.com>
#Chris Lumens <clumens@redhat.com>

import gobject
import pango
import gtk
try:
    import gnomecanvas
except ImportError:
    import gnome.canvas as gnomecanvas
import string
import re
import math
import zonetab
import random
import sys

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("system-config-date")

class Enum:
    def __init__ (self, *args):
        i = 0
        for arg in args:
            self.__dict__[arg] = i
            i += 1

class TimezoneMap (gtk.VBox):
    #force order of destruction for a few items.
    def __del__ (self):
        del self.arrow
        del self.shaded_map
        del self.markers
        del self.current

    def setActionLabelToMap (self):
        if self.tzActionLabel:
            self.tzActionLabel.set_text (_("Please click into the map to choose a region:"))

    def setActionLabelToCity (self):
        if self.tzActionLabel:
            self.tzActionLabel.set_text (_("Please select the nearest city in your timezone:"))


    def setActionLabelToMap (self):
        if self.tzActionLabel:
            self.tzActionLabel.set_text (_("Please click into the map to choose a region:"))

    def setActionLabelToCity (self):
        if self.tzActionLabel:
            self.tzActionLabel.set_text (_("Please select the nearest city in your timezone:"))

    def map_canvas_init (self, map, viewportWidth):        
        self.canvas = gnomecanvas.Canvas ()
        root = self.canvas.root ()
        pixbuf = gtk.gdk.pixbuf_new_from_file (map)

        self.mapWidth = pixbuf.get_width ()
        self.mapHeight = pixbuf.get_height ()
        self.mapShown = (0.0, 0.0, self.mapWidth, self.mapHeight)
        self.viewportWidth = viewportWidth
        self.viewportHeight = int (float (self.viewportWidth) / float (self.mapWidth) * float (self.mapHeight))

        root.add (gnomecanvas.CanvasPixbuf, x=0, y=0, pixbuf=pixbuf, anchor=gtk.ANCHOR_NW)
        x1, y1, x2, y2 = root.get_bounds ()
        self.canvas.set_scroll_region (x1, y1, x2, y2)
        self.canvas.set_size_request (self.viewportWidth, self.viewportHeight)

        hbox = gtk.HBox (False, 0)
        hbox.pack_start (self.canvas, True, False)
        self.pack_start (hbox, False, False)

        root.connect ("event", self.mapEvent)
        self.canvas.connect ("event", self.canvasEvent)

        # shaded/desaturated map when highlighting a region
        shaded_pixbuf = pixbuf.copy ()
        pixbuf.saturate_and_pixelate (shaded_pixbuf, 0.3, False)
        self.shaded_map = root.add (gnomecanvas.CanvasPixbuf,
                                    x = 0, y = 0, pixbuf = shaded_pixbuf, anchor = gtk.ANCHOR_NW)
        self.shaded_map.hide ()
       
        # set up the region pixmaps
        for r in self.regions_list:
            rpixbuf = gtk.gdk.Pixbuf (gtk.gdk.COLORSPACE_RGB, has_alpha = False, bits_per_sample = pixbuf.get_bits_per_sample (), width = r['w'], height = r['h'])
            pixbuf.copy_area (r['x'], r['y'], r['w'], r['h'], rpixbuf, 0, 0)
            r['pixbuf'] = root.add (gnomecanvas.CanvasPixbuf, x = r['x'], y = r['y'], pixbuf = rpixbuf, anchor = gtk.ANCHOR_NW)
            r['pixbuf'].hide ()
            r['frame'] = root.add (gnomecanvas.CanvasRect, x1 = r['x'], y1 = r['y'], x2 = r['x'] + r['w'] - 1, y2 = r['y'] + r['h'] - 1, outline_color = 'yellow')
            r['frame'].hide ()

    def status_bar_init (self):
        self.status = gtk.Statusbar ()
        self.status.set_has_resize_grip (False)
        self.statusContext = self.status.get_context_id ("")
        self.pack_start (self.status, False, False)

    def timezone_list_init (self, default):
        root = self.canvas.root ()
        self.treeStore = gtk.TreeStore (gobject.TYPE_STRING,
                                        gobject.TYPE_STRING,
                                        gobject.TYPE_PYOBJECT,
                                        gobject.TYPE_STRING)
        self.treeStoreRoots = {}
        
        for entry in self.zonetab.getEntries ():
            if entry.tz[0:4] != 'Etc/':
                try:
                    tz_root_str, tz_node_str = _(entry.tz).rsplit ('/', 1)
                except ValueError:
                    sys.stderr.write ("Couldn't split timezone name fields:\nUntranslated TZ: %s\nTranslated TZ:%s\n" % (entry.tz, _(entry.tz)))
                    raise
                tzsortprefix = "0/"
            else:
                tz_root_str = _('Non-geographic timezones')
                tz_node_str = entry.tz.split("/", 1)[1]
                tzsortprefix = "1/"
            tz_root_str_split = tz_root_str.split ('/')
            for depth in xrange (len (tz_root_str_split)):
                root_joined_str = '/'.join (tz_root_str_split[:depth])
                root_joined_str_1 = '/'.join (tz_root_str_split[:depth+1])
                if depth == 0:
                    riter = None
                else:
                    riter = self.treeStoreRoots[root_joined_str]
                if not self.treeStoreRoots.has_key (root_joined_str_1):
                    iter = self.treeStore.append (riter)
                    self.treeStore.set_value (iter, self.columns.TZ, tz_root_str_split [depth])
                    self.treeStore.set_value (iter, self.columns.COMMENTS, None)
                    self.treeStore.set_value (iter, self.columns.ENTRY, None)
                    self.treeStore.set_value (iter, self.columns.TZSORT, tzsortprefix + tz_root_str_split [depth])
                    self.treeStoreRoots[root_joined_str_1] = iter
                
            iter = self.treeStore.append (self.treeStoreRoots[tz_root_str])
            self.treeStore.set_value (iter, self.columns.TZ, tz_node_str)
            if entry.comments:
                self.treeStore.set_value (iter, self.columns.COMMENTS,
                                         _(entry.comments))
            else:
                self.treeStore.set_value (iter, self.columns.COMMENTS, "")
            self.treeStore.set_value (iter, self.columns.ENTRY, entry)
            self.treeStore.set_value (iter, self.columns.TZSORT, (tzsortprefix + tz_node_str).replace ('+', '+1').replace ('-', '-0'))
            
            if entry.long and entry.lat:
                x, y = self.map2canvas (entry.lat, entry.long)
                marker = root.add (gnomecanvas.CanvasText, x=x, y=y,
                                text=u'\u00B7', fill_color='yellow',
                                anchor=gtk.ANCHOR_CENTER,
                                weight=pango.WEIGHT_BOLD)
                self.markers[entry.tz] = marker

            if entry.tz == default:
                self.currentEntry = entry
            if entry.tz == "America/New_York":
                #In case the /etc/sysconfig/clock is messed up, use New York as default
                self.fallbackEntry = entry

        self.treeStore.set_sort_column_id (self.columns.TZSORT, gtk.SORT_ASCENDING)

        self.treeView = gtk.TreeView (self.treeStore)
        selection = self.treeView.get_selection ()
        selection.connect ("changed", self.selectionChanged)
        self.treeView.set_property ("headers-visible", False)
        col = gtk.TreeViewColumn (None, gtk.CellRendererText (), text=0)
        self.treeView.append_column (col)
        col = gtk.TreeViewColumn (None, gtk.CellRendererText (), text=1)
        self.treeView.append_column (col)

        sw = gtk.ScrolledWindow ()
        sw.add (self.treeView)
        sw.set_shadow_type (gtk.SHADOW_IN)
        self.pack_start (sw, True, True)

    def arrow_init (self):
        root = self.canvas.root ()
        self.arrow = root.add (gnomecanvas.CanvasLine,
                               fill_color='limegreen',
                               width_pixels=2,
                               first_arrowhead=False,
                               last_arrowhead=True,
                               arrow_shape_a=4.0,
                               arrow_shape_b=8.0,
                               arrow_shape_c=4.0,
                               points=(0.0, 0.0, 0.0, 0.0))
        self.arrow.hide ()

    def __init__(self, zonetab, default="America/New_York",
            map='../pixmaps/map1440.png', regions='./regions', viewportWidth = 480, tzActionLabel = None):
        gtk.VBox.__init__(self, False, 5)
        self.columns = Enum ("TZ", "COMMENTS", "ENTRY", "TZSORT")
        self.currentEntry = None
        self.fallbackEntry = None

        # read in region file
        self.read_regions (regions)
        self.region = None
        self.highlight_region = None

        # set up class member objects
        self.zonetab = zonetab
        self.markers = {}
        self.highlightedEntry = None
        self.tzActionLabel = tzActionLabel

        # set up the map canvas
        self.map_canvas_init (map, viewportWidth)

        # marker for currently selected city
        root = self.canvas.root ()
        self.current = root.add (gnomecanvas.CanvasText, text='x',
                                fill_color='red', anchor=gtk.ANCHOR_CENTER,
                                weight=pango.WEIGHT_BOLD)

        # set up the arrows
        self.arrow_init ()

        # set up status bar
        self.status_bar_init ()

        # set up list of timezones
        self.timezone_list_init (default)

        self.setActionLabelToMap ()

        self.setCurrent (self.currentEntry)
        self.zoom ()
        (self.lastx, self.lasty) = (0,0)

    def read_regions (self, regions):
        regions_list = []
        regions_re = re.compile ('^\s*(?P<x>[0-9]+)\s+(?P<y>[0-9]+)\s+(?P<w>[0-9]+)\s+(?P<h>[0-9]+)\s+(?P<cx>(?:-1)|(?:[0-9]+))\s+(?P<cy>(?:-1)|(?:[0-9]+))\s+(?P<name>.*\S)\s*')
        fd = open (regions, "r")
        if not fd:
            class OpenFileError (Exception):
                pass
            raise OpenFileError, "Couldn't open regions file '%s'" % regions
        linenr = 0
        for line in fd.readlines ():
            linenr += 1
            m = regions_re.match (line)
            if not m:
                class SyntaxError (Exception):
                    pass
                raise SyntaxError, "Syntax error in line %d of regions file '%s'" % (linenr, regions)
            newregion = {'name': m.group ('name')}
            for what in ['x', 'y', 'w', 'h', 'cx', 'cy']:
                newregion[what] = int (m.group (what))
            if newregion['cx'] == -1:
                newregion['cx'] = newregion['x'] + newregion['w'] / 2
            if newregion['cy'] == -1:
                newregion['cy'] = newregion['y'] + newregion['h'] / 2
            regions_list.append (newregion)
        fd.close ()
        self.regions_list = regions_list

    def find_region (self, xmap, ymap):
        found = None
        distance = None
        for region in self.regions_list:
            x = region['x']
            y = region['y']
            w = region['w']
            h = region['h']
            cx = region['cx']
            cy = region['cy']
            newdistance = math.sqrt ((xmap - cx) ** 2 + (ymap - cy) ** 2)
            if x <= xmap < x+w and y <= ymap < y+h and (not distance or distance > newdistance):
                found = region
                distance = newdistance
        return found

    def get_shown_region (self):
        if self.region:
            r = self.region
            return r['x'], r['y'], r['x'] + r['w'] - 1, r['y'] + r['h'] - 1
        else:
            return 0, 0, self.mapWidth - 1, self.mapHeight - 1

    def get_shown_region_long_lat (self):
        xmin, ymin, xmax, ymax = self.get_shown_region ()
        longmin, latmax = self.canvas2map (xmin, ymin)
        longmax, latmin = self.canvas2map (xmax, ymax)
        #print u"%s -> %s°, %s -> %s°, %s -> %s°, %s -> %s°" % (xmin, longmin, ymin, latmin, xmax, longmax, ymax, latmax)
        return longmin, latmin, longmax, latmax

    def getCurrent (self):
        return self.currentEntry

    def selectionChanged (self, widget, *args):
        (model, iter) = widget.get_selected ()
        if iter is None:
            return
        entry = self.treeStore.get_value (iter, self.columns.ENTRY)
        if entry:
            self.setCurrent (entry, skipList=1)

    def overviewMoveEvent (self, event):
        x, y = self.canvas.root ().w2i (event.x, event.y)
        hr = self.highlight_region
        if not hr or (abs(self.lastx - x) > 5) or (abs(self.lasty - y) > 5):
            (self.lastx, self.lasty) = (x,y)
            if self.highlight (x, y):
                self.shaded_map.show ()

    def overviewPressEvent (self):
        self.region = self.highlight_region
        self.zoom ()
        self.setActionLabelToCity ()

    def zoomMoveEvent (self, event):
        x1, y1 = self.canvas.root ().w2i (event.x, event.y)
        long, lat = self.canvas2map (x1, y1)
        r = self.region
        #print event.x, event.y, "->", x1, y1
        #print r['x'], r['y'], r['w'], r['h'], r['x'] + r['w'] - 1, r['y'] + r['h'] - 1
        longmin, latmin, longmax, latmax = self.get_shown_region_long_lat ()
        #print long, lat
        #print longmin, latmin, longmax, latmax
        last = self.highlightedEntry
        self.highlightedEntry = self.zonetab.findNearest (long, lat, longmin, latmin, longmax, latmax)
        if self.highlightedEntry:
            if last != self.highlightedEntry:
                self.status.pop (self.statusContext)
                status = _(self.highlightedEntry.tz)
                if self.highlightedEntry.comments:
                    status = "%s - %s" % (status,
                                        _(self.highlightedEntry.comments))
                self.status.push (self.statusContext, status)

            x2, y2 = self.map2canvas (self.highlightedEntry.lat,
                                    self.highlightedEntry.long)
            self.arrow.set (points=(x1, y1, x2, y2))
            self.arrow.show ()
        else:
            self.status.pop (self.statusContext)
            self.arrow.hide ()
            self.status.push (self.statusContext, '')

    def zoomPressEvent (self, event):
        if event.type == gtk.gdk.BUTTON_PRESS and event.button != 1:
            return
        if self.highlightedEntry:
            self.setCurrent (self.highlightedEntry)
        self.region = None
        self.zoom ()
        self.setActionLabelToMap ()

    def mapEvent (self, widget, event=None):
        if not self.region:
            # overview mode
            if event.type == gtk.gdk.MOTION_NOTIFY or event == gtk.gdk.ENTER_NOTIFY:
                self.overviewMoveEvent (event)
            elif event.type == gtk.gdk.BUTTON_PRESS:
                self.overviewPressEvent ()
        else:
            # zoom mode
            if event.type == gtk.gdk.MOTION_NOTIFY or event == gtk.gdk.ENTER_NOTIFY:
                self.zoomMoveEvent (event)
            elif event.type == gtk.gdk.BUTTON_PRESS or (event.type == gtk.gdk.KEY_PRESS and event.keyval == gtk.keysyms.Escape):
                self.zoomPressEvent (event)

    def canvasEvent (self, widget, event):
        if event.type == gtk.gdk.LEAVE_NOTIFY:
            self.arrow.hide ()
            if not self.region:
                self.shaded_map.hide ()
                if self.highlight_region:
                    self.highlight_region['frame'].hide ()
        elif event.type == gtk.gdk.MOTION_NOTIFY or event == gtk.gdk.ENTER_NOTIFY:
            if self.region:
                self.arrow.show ()
            else:
                self.arrow.hide ()
                if event.type == gtk.gdk.ENTER_NOTIFY:
                    self.highlight_region = None

    def zoom (self):
        if self.region:
            self.shaded_map.show ()
            self.region['frame'].hide ()
            width, height = self.region['w'], self.region['h']
            x, y = self.region['x'], self.region['y']
            #print "x,y,width,height:", x, y, width, height
            # add border
            b = 0.05
            x1 = x - width * b
            y1 = y - height * b
            x2 = x + width * (b + 1)
            y2 = y + height * (b + 1)
            #print "0: x1, y1, x2, y2:", x1, y1, x2, y2
            # clamp to shown region, keep aspect ratio
            if x1 < 0:
                x2 -= x1
                x1 = 0
                #print "1: x1, y1, x2, y2:", x1, y1, x2, y2
            if y1 < 0:
                y2 -= y1
                y1 = 0
                #print "2: x1, y1, x2, y2:", x1, y1, x2, y2
            if x2 > self.mapWidth:
                w = x2 - x1
                h = y2 - y1
                oldx2 = x2
                x2 = self.mapWidth
                x1 -= (oldx2 - x2)
                #y2 -= (oldx2 - x2) * (self.mapHeight / self.mapWidth)
                #print "3: x1, y1, x2, y2:", x1, y1, x2, y2
            if y2 > self.mapHeight:
                w = x2 - x1
                h = y2 - y1
                oldy2 = y2
                y2 = self.mapHeight
                y1 -= (oldy2 - y2)
                #x2 -= (oldy2 - y2) * (self.mapWidth / self.mapHeight)
                #print "4: x1, y1, x2, y2:", x1, y1, x2, y2
            x, y = x1, y1
            width, height = x2 - x1, y2 - y1
            #print "x,y,width,height:", x, y, width, height
        else:
            if self.highlight_region:
                self.highlight_region['frame'].show ()
            width, height = self.mapWidth, self.mapHeight
            x, y = 0, 0
        self.canvas.set_pixels_per_unit (float (self.viewportWidth) / float (width))
        self.canvas.set_scroll_region (float (x), float (y), float (x+width-1), float (y+height-1))
        self.zoomFactor = float (self.mapWidth) / float (width)

    def highlight (self, x, y):
        shr = self.highlight_region
        hr = self.find_region (x, y)
        if hr and hr != shr:
            if shr and shr['pixbuf']:
                shr['pixbuf'].hide ()
                shr['frame'].hide ()
            self.shaded_map.show ()
            hr['pixbuf'].show ()
            hr['frame'].show ()
            self.highlight_region = hr
            return True
        return False

    def find_tz_iter_for_iter (self, iter):
        entry_iter = None
        child = self.treeStore.iter_children (iter)
        while child:
            entry_iter = self.find_tz_iter_for_iter (child)
            if entry_iter:
                break
            child = self.treeStore.iter_next (child)
        if not entry_iter:
            entry = self.treeStore.get_value (iter, self.columns.ENTRY)
            if entry == self.currentEntry:
                entry_iter = iter
        return entry_iter

    def find_tz_iter (self):
        iter = self.treeStore.get_iter_first ()
        while iter:
            found_iter = self.find_tz_iter_for_iter (iter)
            if found_iter:
                return found_iter
            iter = self.treeStore.iter_next (iter)
        return None

    def updateTimezoneList (self):
        iter = self.find_tz_iter ()
        if iter:
            selection = self.treeView.get_selection ()
            selection.unselect_all ()
            path = self.treeStore.get_path (iter)
            col = self.treeView.get_column (0)
            self.treeView.expand_to_path (path)
            self.treeView.scroll_to_cell (path, col)
            self.treeView.set_cursor (path)

    def setCurrent (self, entry, skipList=0):
        # Draw marker for old currentEntry.
        if self.currentEntry and self.markers.has_key (self.currentEntry.tz):
            self.markers[self.currentEntry.tz].show ()

        if not entry:
            # If the value in /etc/sysconfig/clock is invalid, default to New York
            self.currentEntry = self.fallbackEntry
        else:
            self.currentEntry = entry

        # Hide new currentEntry, draw big red X over it instead.
        if self.currentEntry.long and self.currentEntry.lat:
            self.markers[self.currentEntry.tz].hide ()
            x, y = self.map2canvas (self.currentEntry.lat, self.currentEntry.long)
            self.current.set (x=x, y=y)
            self.current.show ()
        else:
            self.current.hide ()

        if skipList:
            return

        self.updateTimezoneList ()

    def map2canvas (self, lat, long):
        x2 = self.mapWidth
        y2 = self.mapHeight
        x = x2 / 2.0 + (x2 / 2.0) * long / 180.0
        y = y2 / 2.0 - (y2 / 2.0) * lat / 90.0
        return (x, y)

    def canvas2map (self, x, y):
        x2 = self.mapWidth
        y2 = self.mapHeight
        long = (x - x2 / 2.0) / (x2 / 2.0) * 180.0
        lat = (y2 / 2.0 - y) / (y2 / 2.0) * 90.0
        #print x, y, "->", long, lat
        return (long, lat)

if __name__ == "__main__":
    zonetab = zonetab.ZoneTab ()
    win = gtk.Window ()
    if gtk.__dict__.has_key ("main_quit"):
        win.connect ('destroy', gtk.main_quit)
    else:
        win.connect ('destroy', gtk.mainquit)
    map = TimezoneMap (zonetab)
    vbox = gtk.VBox ()
    vbox.pack_start (map)
    button = gtk.Button ("Quit")
    if gtk.__dict__.has_key ("main_quit"):
        button.connect ("pressed", gtk.main_quit)
    else:
        button.connect ("pressed", gtk.mainquit)
    vbox.pack_start (button, False, False)
    win.add (vbox)
    win.show_all ()
    if gtk.__dict__.has_key ("main"):
        gtk.main ()
    else:
        gtk.mainloop ()
    
