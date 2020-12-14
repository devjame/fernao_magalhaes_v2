from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.carousel import Carousel
from kivy.core.window import Window
from kivy.factory import Factory
from ler_cenas import Cenas

Window.size = (320, 670)
dados_da_cena = Cenas("cenas.json")


class Contextos(MDBoxLayout):
    contexto = ObjectProperty
    dilema = ObjectProperty

    def __init__(self, **kwargs):
        super(Contextos, self).__init__(**kwargs)

    def atribuir_conteudo(self, cena):
        if self.contexto is None:
            self.contexto = dados_da_cena.get_contexto(cena)
        if self.dilema is None:
            self.dilema = dados_da_cena.get_dilema(cena)


class Opcao(MDBoxLayout):
    def __init__(self, **kwargs):
        super(Opcao, self).__init__(**kwargs)


class TelaQuiz(MDBoxLayout):

    def __init__(self, **kwargs):
        super(TelaQuiz, self).__init__(**kwargs)
        self.chkbox_ref = {}
        self.chkbox_status = False
        self.cena = ""
        self.criar_layout()

    def container(self):
        cont = MDBoxLayout()
        return cont

    def chkbox(self):
        chk_box = MDCheckbox(group='opçao', color=[0.1, 1, 0, 4], size_hint=(None, None), size=("40dp", "40dp"),
                             pos_hint= {"y": .3})
        return chk_box

    def lbl_texto(self, texto):
        lbl = MDLabel(text=texto, font_size="16dp", valign="middle", size_hint_x=.9)
        return lbl

    def criar_contexto(self, cena="cena1"):
        lbl_texto = dados_da_cena.get_contexto(cena)
        contexto = self.lbl_texto(lbl_texto)
        contexto.size_hint_y = None
        contexto.height = "120dp"
        return contexto

    def criar_dilema(self, cena="cena1"):
        lbl_texto = dados_da_cena.get_dilema(cena)
        dilema = self.lbl_texto(lbl_texto)
        dilema.halign = 'center'
        dilema.size_hint_y = None
        dilema.height = "84dp"
        return dilema

    def criar_layout(self, cena="cena1"):
        self.clear_widgets()
        self.cena = cena
        opcoes = dados_da_cena.get_opcao(cena)

        dilema = self.criar_dilema(cena)
        contexto = self.criar_contexto(cena)

        self.add_widget(contexto)
        self.add_widget(dilema)

        for opcao in opcoes:

            chk_box = self.chkbox()
            chk_box.bind(active=self.on_checkbox_active)

            lbl_text = self.lbl_texto(opcao)

            box = self.container()
            box.size_hint_y = None
            box.height = "84dp"
            box.add_widget(chk_box)
            box.add_widget(lbl_text)

            self.add_widget(box)
            self.chkbox_ref[chk_box] = opcao

    def on_checkbox_active(self, checkbox, value):
        opcoes = dados_da_cena.get_opcao(self.cena)
        if value:
            self.chkbox_status = True
            if self.chkbox_ref[checkbox] == opcoes[0]:
                print(opcoes[0])
            else:
                popup = MDDialog(
                    text="Fim Prematuro!",
                    size_hint_x=.8,
                    buttons=[
                        MDFlatButton(
                            text="OK"
                        )
                    ],
                )
                popup.open()
                popup.buttons[0].bind(on_release=popup.dismiss)


class TelaRecrutamento(MDBoxLayout):
    pass


class ViagemRoot(MDBoxLayout):
    def __init__(self, **kwargs):
        super(ViagemRoot, self).__init__(**kwargs)
        self.carousel = Carousel()
        self.cenas = dados_da_cena.get_cenas()
        self.popup = None
        for cena in self.cenas:
            self.viagem_quiz = TelaQuiz()
            self.viagem_quiz.criar_layout(cena)
            btn_box = self.container()
            btn_box.size_hint_y = "40dp"
            if cena == 'cena1':
                btn_box.orientation = 'vertical'
                btn_next = MDFlatButton(text="Seguinte", size_hint_x='24dp', pos_hint={"x": .5})
                btn_next.bind(on_release=self.load_next_quiz)
                btn_box.add_widget(btn_next)
            else:
                btn_next = MDFlatButton(text="Seguinte", size_hint_x='24dp')
                btn_next.bind(on_release=self.load_next_quiz)
                btn_prev = MDFlatButton(text="Anterior", size_hint_x='24dp')
                btn_prev.bind(on_release=self.load_prev_quiz)
                btn_box.add_widget(btn_prev)
                btn_box.add_widget(btn_next)
            self.viagem_quiz.add_widget(btn_box)
            self.carousel.add_widget(self.viagem_quiz)
        self.add_widget(self.carousel)

    def container(self):
        cont = MDBoxLayout()
        return cont

    def load_next_quiz(self, *args):
        if self.viagem_quiz.chkbox_status is not True:
            self.popup = MDDialog(
                text="Please select an option.",
                size_hint_x=.8,
                buttons=[
                    MDFlatButton(
                        text="OK"
                    )
                ],
            )
            self.popup.buttons[0].bind(on_release=self.popup.dismiss)
            self.popup.open()
            print(self.carousel.slides)
            return self.carousel.index

        return self.carousel.load_next()

    def load_prev_quiz(self, *args):
        if self.viagem_quiz.chkbox_status is not True:
            self.popup = MDDialog(
                text="Please select an option.",
                size_hint_x=.8,
                buttons=[
                    MDFlatButton(
                        text="OK"
                    )
                ],
            )
            self.popup.buttons[0].bind(on_release=self.popup.dismiss)
            self.popup.open()
            return self.carousel.index

        return self.carousel.load_previous()


class ViagemApp(MDApp):
    pass


ViagemApp().run()