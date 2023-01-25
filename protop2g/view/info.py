import sys
from asciimatics.widgets import Frame, Layout, Divider, Text, Button, Label, CheckBox
from asciimatics.exceptions import NextScene
from protop2g.view import colrschm
from time import strftime, localtime
from protop2g.base.data import revertdb


class ProjInfoView(Frame):
    def __init__(self, scrn, dataobjc):
        super(ProjInfoView, self).__init__(scrn,
                                           scrn.height * 3 // 4,
                                           scrn.width * 3 // 4,
                                           hover_focus=True,
                                           can_scroll=False,
                                           title="protop2g :: Namespace Confirmation",
                                           on_load=self.putvalue,
                                           reduce_cpu=True)
        self.set_theme(colrschm)
        self.scrn = scrn
        self.dataobjc = dataobjc

        layoutAA = Layout([100], fill_frame=True)
        self.add_layout(layoutAA)
        desctext = "Please confirm if the following source and destination namespaces are correctly listed before continuing with selecting the assets that would be imported."
        self.descobjc = Label(desctext, height=3)
        layoutAA.add_widget(self.descobjc)

        layoutBB = Layout([1,1])
        self.add_layout(layoutBB)
        dvdrlva1 = Divider()
        lablsrce = Label("Source namespace", height=1)
        dvdrlva2 = Divider()
        self.textpaguname = Text("Name", "paguname", readonly=True)
        self.textpagulink = Text("URL", "pagulink", readonly=True)
        self.textpagudesc = Text("Description", "pagudesc", readonly=True)
        self.textpagulast = Text("Last modified", "pagulast", readonly=True)
        self.textpagumake = Text("Created on", "pagumake", readonly=True)
        self.textpagumain = Text("Maintainer", "pagumain", readonly=True)
        self.textpagutags = Text("Tags", "pagutags", readonly=True)
        layoutBB.add_widget(dvdrlva1, 0)
        layoutBB.add_widget(lablsrce, 0)
        layoutBB.add_widget(dvdrlva2, 0)
        layoutBB.add_widget(self.textpaguname, 0)
        layoutBB.add_widget(self.textpagulink, 0)
        layoutBB.add_widget(self.textpagudesc, 0)
        layoutBB.add_widget(self.textpagulast, 0)
        layoutBB.add_widget(self.textpagumake, 0)
        layoutBB.add_widget(self.textpagumain, 0)
        layoutBB.add_widget(self.textpagutags, 0)

        dvdrlvb1 = Divider()
        labldest = Label("Destination namespace", height=1)
        dvdrlvb2 = Divider()
        self.textgtlbname = Text("Name", "gtlbname", readonly=True)
        self.textgtlblink = Text("URL", "gtlblink", readonly=True)
        self.textgtlbdesc = Text("Description", "gtlbdesc", readonly=True)
        self.textgtlblast = Text("Last modified", "gtlblast", readonly=True)
        self.textgtlbmake = Text("Created on", "gtlbmake", readonly=True)
        self.textgtlbmain = Text("Maintainer", "gtlbmain", readonly=True)
        self.textgtlbtags = Text("Tags", "gtlbtags", readonly=True)
        layoutBB.add_widget(dvdrlvb1, 1)
        layoutBB.add_widget(labldest, 1)
        layoutBB.add_widget(dvdrlvb2, 1)
        layoutBB.add_widget(self.textgtlbname, 1)
        layoutBB.add_widget(self.textgtlblink, 1)
        layoutBB.add_widget(self.textgtlbdesc, 1)
        layoutBB.add_widget(self.textgtlblast, 1)
        layoutBB.add_widget(self.textgtlbmake, 1)
        layoutBB.add_widget(self.textgtlbmain, 1)
        layoutBB.add_widget(self.textgtlbtags, 1)

        layoutCC = Layout([100])
        self.add_layout(layoutCC)
        dvdrlvcc = Divider()
        self.chckrepoasst = CheckBox("Import all repository data", name="repoasst")
        self.chckopentick = CheckBox("Transfer all open issue tickets", name="opentick")
        self.chckclostick = CheckBox("Transfer all closed issue tickets", name="clostick")
        layoutCC.add_widget(dvdrlvcc)
        layoutCC.add_widget(self.chckrepoasst)
        layoutCC.add_widget(self.chckopentick)
        layoutCC.add_widget(self.chckclostick)

        layoutEE = Layout([100])
        self.add_layout(layoutEE)
        dvdrlvea = Divider()
        self.progtext = Label("STATUS - Ready", height=1)
        dvdrlvee = Divider()
        layoutEE.add_widget(dvdrlvea)
        layoutEE.add_widget(self.progtext)
        layoutEE.add_widget(dvdrlvee)

        layoutFF = Layout([1, 1, 1, 1, 1])
        self.add_layout(layoutFF)
        butnnext = Button("Next", self.formnext)
        butnback = Button("Back", self.formback)
        butnexit = Button("Exit", self.formexit)
        layoutFF.add_widget(butnnext, 0)
        layoutFF.add_widget(butnback, 2)
        layoutFF.add_widget(butnexit, 4)

        self.putvalue()
        self.fix()

    def putvalue(self):
        # Pagure - Source
        self.textpaguname.value = "%s (ID %s)" % (self.dataobjc.pagurepo["reponame"], self.dataobjc.pagurepo["iden"])
        self.textpagulink.value = "%s" % self.dataobjc.pagurepo["repolink"]
        self.textpagudesc.value = "%s" % self.dataobjc.pagurepo["descript"]
        self.textpagulast.value = "%s" % strftime("%c", localtime(int(self.dataobjc.pagurepo["lastmode"])))
        self.textpagumake.value = "%s" % strftime("%c", localtime(int(self.dataobjc.pagurepo["makedate"])))
        self.textpagumain.value = "%s (FAS %s)" % (self.dataobjc.pagurepo["main"]["fullname"], self.dataobjc.pagurepo["main"]["username"])
        self.textpagutags.value = "%s" % str(self.dataobjc.pagurepo["tags"])
        # GitLab - Destination
        self.textgtlbname.value = "%s (ID %s)" % (self.dataobjc.gtlbrepo["reponame"], self.dataobjc.gtlbrepo["iden"])
        self.textgtlblink.value = "%s" % self.dataobjc.gtlbrepo["repolink"]
        self.textgtlbdesc.value = "%s" % self.dataobjc.gtlbrepo["descript"]
        self.textgtlblast.value = "%s" % self.dataobjc.gtlbrepo["lastmode"]
        self.textgtlbmake.value = "%s" % self.dataobjc.gtlbrepo["makedate"]
        self.textgtlbmain.value = "%s (UID %s)" % (self.dataobjc.gtlbrepo["main"]["fullname"], self.dataobjc.gtlbrepo["main"]["username"])
        self.textgtlbtags.value = "%s" % str(self.dataobjc.gtlbrepo["tags"])

    def formnext(self):
        self.save()
        self.progtext.value = "STATUS - Accessing resource. Please wait."
        rtrn, stat = rqstrepo(self.textpaguname.value)
        if rtrn:
            raise NextScene("protop2g :: Project Information")
        else:
            self.progtext.value = "STATUS - Code %d - The requested repository could not be accessed." % stat

    def formback(self):
        revertdb(self.dataobjc)
        raise NextScene("protop2g :: Source Namespace")

    @staticmethod
    def formexit():
        sys.exit()
