import sys
from asciimatics.widgets import Frame, Layout, Divider, Text, Button, Label
from asciimatics.exceptions import NextScene
from protop2g.work.srce import rqstproj
from protop2g.view import colrschm


class PagureNSView(Frame):
    def __init__(self, scrn, dataobjc):
        super(PagureNSView, self).__init__(scrn,
                                          scrn.height * 3 // 4,
                                          scrn.width * 3 // 4,
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
        desctext = "protop2g is a prototype project assets importer that moves repositories from Pagure to GitLab. In order to use the tool, you need to have API keys of both Pagure and GitLab with elevated access levels, associated to the pre-existing source namespaces and destination namespaces respectively. Please note that this tool will overwrite everything present in the destination namespace so ensure that the backups have been created beforehand."
        descobjc = Label(desctext, height=3)
        layoutAA.add_widget(descobjc)

        layoutBB = Layout([100])
        self.add_layout(layoutBB)
        dvdrlvba = Divider()
        self.textpaguname = Text("Source namespace", "paguname")
        self.textpagucode = Text("Pagure API key", "pagucode", hide_char="*")
        self.textgtlbname = Text("Destination namespace", "gtlbname")
        self.textgtlbcode = Text("GitLab API key", "gtlbcode", hide_char="*")
        dvdrlvbb = Divider()
        layoutBB.add_widget(dvdrlvba)
        layoutBB.add_widget(self.textpaguname)
        layoutBB.add_widget(self.textpagucode)
        layoutBB.add_widget(self.textgtlbname)
        layoutBB.add_widget(self.textgtlbcode)
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
        self.textgtlbname.value = ""
        self.textgtlbcode.value = ""
        self.progtext.text = "STATUS - All fields are cleared."

    def formnext(self):
        if self.textpaguname.value.strip() == "":
            self.progtext.text = "STATUS - No source namespace specified."
        elif self.textpagucode.value.strip() == "":
            self.progtext.text = "STATUS - No Pagure API key provided."
        elif self.textgtlbname.value.strip() == "":
            self.progtext.text = "STATUS - No destination namespace specified."
        elif self.textgtlbcode.value.strip() == "":
            self.progtext.text = "STATUS - No GitLab API key provided."
        else:
            self.progtext.text = "STATUS - Please wait."
            self.save()
            rtrn, stat, what, whyc = rqstproj(
                self.textpaguname.value.strip(),
                self.textpagucode.value.strip(),
                self.textgtlbname.value.strip(),
                self.textgtlbcode.value.strip(),
                self.dataobjc
            )
            if rtrn:
                raise NextScene("protop2g :: Namespace Confirmation")
            else:
                if what == "pagu":
                    self.progtext.text = "STATUS - %d %s - The requested source repository could not be accessed." % (stat, whyc)
                elif what == "gtlb":
                    self.progtext.text = "STATUS - %d %s - The requested destination repository could not be accessed." % (stat, whyc)

    @staticmethod
    def formexit():
        sys.exit()
