from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivymd.icon_definitions import md_icons
import requests

import babel.numbers
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

Window.size = (412, 915)

#Variaveis Globais
url = 'http://br7nno.pythonanywhere.com'
resposta_get = requests.request('GET', url + '/valores/1')
valores = resposta_get.json()
    
body = {}
header_valores = {'Content-Type': 'application/json'}


class FirstWindow(Screen):
    Valor_atual = ObjectProperty()
    Ultimo_ganho = ObjectProperty()   
    Ultimo_gasto = ObjectProperty()
    Valor_progress_bar = ObjectProperty()
    
    def __init__(self, **kw):
        super(FirstWindow, self).__init__(**kw)
        self.Valor_progress_bar = valores['valor_atual']
        self.Valor_atual = babel.numbers.format_currency((valores['valor_atual']), "BRL", locale='pt')
        self.Ultimo_ganho = babel.numbers.format_currency((valores['ultimo_ganho']), "BRL", locale='pt')
        self.Ultimo_gasto = babel.numbers.format_currency((valores['ultimo_gasto']), "BRL", locale='pt')
        

    def update(self, soma, ultimo_ganho, v2, v3, v4, v5):    #Da aba de ganhar
        print(soma)
        self.Valor_progress_bar = soma
        self.Valor_atual = babel.numbers.format_currency(soma, "BRL", locale='pt')
        self.Ultimo_ganho = babel.numbers.format_currency(ultimo_ganho, "BRL", locale='pt')
        self.data_put_win(soma, ultimo_ganho, v2, v3, v4, v5)

    def downdate(self, sub, ultimo_gasto, v2, v3, v4, v5):          #Da aba de perder
        self.Valor_atual = babel.numbers.format_currency(sub, "BRL", locale='pt')
        self.Ultimo_gasto = babel.numbers.format_currency(ultimo_gasto, "BRL", locale='pt')
        self.data_put_lost(sub, ultimo_gasto, v2, v3, v4, v5)

    def data_put_win(self, soma, ultimo_ganho, v2, v3, v4, v5): #Da aba de ganhar
        
        body['valor_atual'] = (soma)
        body['ultimo_ganho'] = (ultimo_ganho)
        body['ultimo_gasto'] = valores['ultimo_gasto']
        body['ganho_02'] = v2
        body['ganho_03'] = v3
        body['ganho_04'] = v4
        body['ganho_05'] = v5
        body['gasto_02'] = (valores['gasto_02'])
        body['gasto_03'] = (valores['gasto_03'])
        body['gasto_04'] = (valores['gasto_04'])
        body['gasto_05'] = (valores['gasto_05'])

        self.send_put(body)

    def data_put_lost(self, sub, ultimo_gasto, v2, v3, v4, v5):      #Da aba de perder
        body['valor_atual'] = (sub)
        body['ultimo_ganho'] = valores['ultimo_ganho']
        body['ultimo_gasto'] = (ultimo_gasto)
        body['ganho_02'] = (valores['ganho_02'])
        body['ganho_03'] = (valores['ganho_03'])
        body['ganho_04'] = (valores['ganho_04'])
        body['ganho_05'] = (valores['ganho_05'])
        body['gasto_02'] = v2
        body['gasto_03'] = v3
        body['gasto_04'] = v4
        body['gasto_05'] = v5

        self.send_put(body)

    def send_put(self, body):                          #Mandar para o banco de dados
        endpoint_put = url + '/valores/1'
        send_api = requests.request('PUT', endpoint_put, json=body, headers=header_valores)
        print(send_api.status_code)

        
        
#alteraçoes 
class SecondWindow(Screen):

    Ganho_01 = ObjectProperty()
    Ganho_02 = ObjectProperty()
    Ganho_03 = ObjectProperty()
    Ganho_04 = ObjectProperty()
    Ganho_05 = ObjectProperty()


    def __init__(self, **kw):
        super(SecondWindow, self).__init__(**kw)
        self.Ganho_01 = (valores['ultimo_ganho'])
        self.Ganho_02 = (valores['ganho_02'])
        self.Ganho_03 = (valores['ganho_03'])
        self.Ganho_04 = (valores['ganho_04'])
        self.Ganho_05 = (valores['ganho_05'])


    def win(self, ganho):
        self.dialog = MDDialog(title = 'Ops, algo deu errado!',
                        text = 'Por favor, apenas numeros!',  
                        buttons=[MDRectangleFlatButton(text='Ok, entendi!',
                        text_color = (0, 1, 0.4, 1),
                        on_release = self.close_dialog,
                        )])

        try:
            self.ids.ganho.text = ''
            resposta_get = requests.request('GET', url + '/valores/1')
            valores = resposta_get.json()
            soma = '%.2f' % (float(valores['valor_atual']) + float(ganho))

            v1 = ganho
            v2 = (valores['ultimo_ganho'])
            v3 = (valores['ganho_02'])
            v4 = (valores['ganho_03'])
            v5 = (valores['ganho_04'])

            self.parent.ids.FW.update(soma, v1, v2, v3, v4, v5)
        
        except:
            self.dialog.open()
        
    
    def close_dialog(self, obj):
        self.dialog.dismiss()

class ThirdWindow(Screen):

    Gasto_01 = ObjectProperty()
    Gasto_02 = ObjectProperty()
    Gasto_03 = ObjectProperty()
    Gasto_04 = ObjectProperty()
    Gasto_05 = ObjectProperty()   

    def __init__(self, **kw):
        super(ThirdWindow, self).__init__(**kw)
        self.Gasto_01 = (valores['ultimo_gasto'])
        self.Gasto_02 = (valores['gasto_02'])
        self.Gasto_03 = (valores['gasto_03'])
        self.Gasto_04 = (valores['gasto_04'])
        self.Gasto_05 = (valores['gasto_05'])

    def lost(self, perca):
        self.dialog = MDDialog(title = 'Ops, algo deu errado!',
                        text = 'Por favor, apenas numeros!',  
                        buttons=[MDRectangleFlatButton(text='Ok, entendi!',
                        text_color = (0, 1, 0.4, 1),
                        on_release = self.close_dialog,
                        )])
        try:
            self.ids.perca.text = ''
            resposta_get = requests.request('GET', url + '/valores/1')
            valores = resposta_get.json()
            sub = '%.2f' % (float(valores['valor_atual']) - float(perca))
            
            v1 = perca
            v2 = (valores['ultimo_gasto'])
            v3 = (valores['gasto_02'])
            v4 = (valores['gasto_03'])
            v5 = (valores['gasto_04'])
            
            self.parent.ids.FW.downdate(sub, v1, v2, v3, v4, v5 )
            
        except:
            self.dialog.open()
        
    
    def close_dialog(self, obj):
        self.dialog.dismiss()

class WindowManager(ScreenManager):
    pass

class MyApp(MDApp):
    def build(self):
        
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Orange"
        #self.theme_cls.material_style = "M3"
        return Builder.load_file('bfinance.kv')


MyApp().run()
