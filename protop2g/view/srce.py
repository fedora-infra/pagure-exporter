import sys
from asciimatics.widgets import Frame, Layout, Divider, Text, Button, Label
from asciimatics.exceptions import NextScene
from protop2g.work.srce import rqstrepo
from protop2g.view import colrschm


class PagureNSView(Frame):
    def __init__(self, scrn, dataobjc):
        super(PagureNSView, self).__init__(scrn,
                                          scrn.height * 2 // 3,
                                          scrn.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="protop2g :: Source Namespace",
                                          on_load=self.formwipe,
                                          reduce_cpu=True)
        self.set_theme(colrschm)
        self.scrn = scrn
        self.dataobjc = dataobjc

        layoutAA = Layout([100], fill_frame=True)
        self.add_layout(layoutAA)
        desctext = "protop2g is a prototype project assets importer that moves repositories from Pagure to GitLab. In order to use the tool, you need to have API keys of both Pagure and GitLab with elevated access levels."
        descobjc = Label(desctext, height=3)
        layoutAA.add_widget(descobjc)

        layoutBB = Layout([100])
        self.add_layout(layoutBB)
        self.textpaguname = Text("Source namespace", "paguname")
        self.textpagucode = Text("Pagure API key", "pagucode")
        dvdrlvbb = Divider()
        layoutBB.add_widget(self.textpaguname)
        layoutBB.add_widget(self.textpagucode)
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
        butnwipe = Button("Wipe", self.formwipe)
        butnexit = Button("Exit", self.formexit)
        layoutDD.add_widget(butnnext, 0)
        layoutDD.add_widget(butnwipe, 2)
        layoutDD.add_widget(butnexit, 4)

        self.fix()

    def formwipe(self):
        self.textpaguname.value = ""
        self.textpagucode.value = ""
        self.progtext.text = "STATUS - All fields are cleared."

    def formnext(self):
        if self.textpaguname.value.strip() == "":
            self.progtext.text = "STATUS - No source namespace specified."
        else:
            self.save()
            self.progtext.text = "STATUS - Please wait."
            rtrn, stat = rqstrepo(self.textpaguname.value.strip(), self.dataobjc)
            if rtrn:
                raise NextScene("protop2g :: Project Information")
            else:
                self.progtext.text = "STATUS - Code %d - The requested repository could not be accessed." % stat

    @staticmethod
    def formexit():
        sys.exit()
