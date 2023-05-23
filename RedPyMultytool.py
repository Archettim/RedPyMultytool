from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Container, Horizontal
from textual.widgets import Button, Footer, Header, Static, Switch, Input
from cryptography.fernet import Fernet
from cipher import Ramsom
from ArpPoisoning import ArpPoison

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
        if button_id=="rmw":
            self.add_class("rams")
            self.remove_class("shell")
        elif button_id=="sh":
            self.add_class("shell")
            self.remove_class("rams")

class ReverseSH(Static):
    def compose(self) -> ComposeResult:
        yield Container(
        Button("prova",id="start", variant="success"),
        Input(placeholder="Prova"),
        Input(placeholder="Prova"),
        Button("prova2",id="stop", variant="success"),
        id="reverseSH")

class Ramsomware(Static):
    def compose(self) -> ComposeResult:
        yield Container(
        Button("prova",id="start", variant="success"),
        Input(placeholder="Prova"),
        Input(placeholder="Prova"),
        Button("prova2",id="stop", variant="success"),
        id="ramsom")

    def on_button_pressed(self,event:Button.Pressed) -> None:
        button_id=event.button.id
        if button_id=="start":
            self.add_class("started")
        elif button_id=="stop":
            self.remove_class("started")

class RedPyMultytool(App):
    CSS_PATH = "app.css"
    BINDINGS=[("q","quit","Exit app"),("d","toggle_dark","Toggle dark mode"),("b", "toggle_sidebar", "Sidebar"),]
    def compose(self) -> ComposeResult:
        yield Header()
        yield Sidebar(classes="-hidden")
        yield Container(
            Ramsomware(),
            ReverseSH())
        yield Footer()
        
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