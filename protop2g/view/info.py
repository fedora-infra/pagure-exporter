import sys
from asciimatics.widgets import Frame, Layout, Divider, Text, Button, Label
from asciimatics.exceptions import NextScene
from protop2g.view import colrschm
from time import strftime, localtime
from protop2g.base.data import revertdb


class ProjInfoView(Frame):
    def __init__(self, scrn, dataobjc):
        super(ProjInfoView, self).__init__(scrn,
                                           scrn.height * 2 // 3,
                                           scrn.width * 2 // 3,
                                           hover_focus=True,
                                           can_scroll=False,
                                           title="protop2g :: Project Information",
                                           on_load=self.putvalue,
                                           reduce_cpu=True)
        self.set_theme(colrschm)
        self.scrn = scrn
        self.dataobjc = dataobjc

        layoutAA = Layout([100], fill_frame=True)
        self.add_layout(layoutAA)
        desctext = "Is this the project the assets of which you wish to import from Pagure to GitLab?"
        self.descobjc = Label(desctext, height=3)
        layoutAA.add_widget(self.descobjc)

        layoutBB = Layout([100])
        self.add_layout(layoutBB)
        self.textreponame = Text("Name", "reponame", readonly=True)
        self.textrepolink = Text("URL", "repolink", readonly=True)
        self.textdescript = Text("Description", "descript", readonly=True)
        self.textlastmode = Text("Last modified", "lastmode", readonly=True)
        self.textmakedate = Text("Created on", "makedate", readonly=True)
        self.textmaintain = Text("Maintainer", "maintain", readonly=True)
        self.texttagslist = Text("Tags", "tagslist", readonly=True)
        dvdrlvbb = Divider()
        layoutBB.add_widget(self.textreponame)
        layoutBB.add_widget(self.textrepolink)
        layoutBB.add_widget(self.textdescript)
        layoutBB.add_widget(self.textlastmode)
        layoutBB.add_widget(self.textmakedate)
        layoutBB.add_widget(self.textmaintain)
        layoutBB.add_widget(self.texttagslist)
        layoutBB.add_widget(dvdrlvbb)

        layoutCC = Layout([100])
        self.add_layout(layoutCC)
        self.progtext = Label("STATUS - Ready", height=1)
        dvdrlcc = Divider()
        layoutCC.add_widget(self.progtext)
        layoutCC.add_widget(dvdrlcc)

        layoutDD = Layout([1, 1, 1, 1, 1])
        self.add_layout(layoutDD)
        butnnext = Button("Next", self.formnext)
        butnback = Button("Back", self.formback)
        butnexit = Button("Exit", self.formexit)
        layoutDD.add_widget(butnnext, 0)
        layoutDD.add_widget(butnback, 2)
        layoutDD.add_widget(butnexit, 4)

        self.putvalue()
        self.fix()

    def putvalue(self):
        self.textreponame.value = "%s (ID %s)" % (self.dataobjc.repodata["reponame"], self.dataobjc.repodata["iden"])
        self.textrepolink.value = "%s" % self.dataobjc.repodata["repolink"]
        self.textdescript.value = "%s" % self.dataobjc.repodata["descript"]
        self.textlastmode.value = "%s" % strftime("%c", localtime(int(self.dataobjc.repodata["lastmode"])))
        self.textmakedate.value = "%s" % strftime("%c", localtime(int(self.dataobjc.repodata["makedate"])))
        self.textmaintain.value = "%s (FAS %s)" % (self.dataobjc.repodata["main"]["fullname"], self.dataobjc.repodata["main"]["username"])
        self.texttagslist.value = "%s" % str(self.dataobjc.repodata["tags"])

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
