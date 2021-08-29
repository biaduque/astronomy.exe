import PySimpleGUI as sg
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib import pyplot
from estrela_nv1 import estrela
from eclipse_nv1 import Eclipse
from verify import Validar,calSemiEixo,calculaLat

#desenvolvido por BEATRIZ DUQUE ESTRADA

fechou = False
esc = 0

fa = [] #vetor area manchas
fi = [] #vetor intensidade manchas
lg = [] #vetor longitude manchas
lt = [] #vetor tatitude manchas

class LayoutStar :
    def __init__(self):
        sg.theme('Dark Teal 10')
        global fechou


        #layout
        LayoutStar=[
            [sg.Image(r'./dependences/logo.png',tooltip = 'logotipo.png' )],
            [sg.Text('Raio da Estrela (em relação ao raio do sol)  '),sg.Input(size=(10,0),key='raio')],
            [sg.Text('Coeficiente de Escurecimento de limbo 1    '),sg.Input(size=(10,0),key='coeficienteHum')],
            [sg.Text('Coeficiente de Escurecimento de limbo 2    '),sg.Input(size=(10,0),key='coeficienteDois')],
            [sg.Text('MATRIZ : 856', justification='center')],
            [sg.Button('Enviar Dados')]
        ]
        #janela 
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutStar)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Enviar Dados'):
                break
        self.janela.close()

    #LAYOUT DO ERRO
    def LayoutError(self):
        sg.theme('Dark Teal 10') 
        [sg.popup_error('Erro!')] #Printa um botao de erro vermelho
        #self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutError)
        self.janela.close()
        
    #ESCOLHER SE HA MANCHAS OU NAO 
    def LayoutEsc(self):
        global fechou
        global esc
        sg.theme('Dark Teal 10') 
        LayoutEsc =[
            [sg.Text('Deseja adicionar manchas em sua estrela?')],
            [sg.Button('Sim'), sg.Button('Nao')]
        ]
        #janela 
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutEsc)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Sim'):
                esc = 1
                break
            if (self.event == 'Nao'):
                esc = 2
                break
        self.janela.close()

    #ESCOLHER SE HA LUAS OU NAO 
    def LayoutEscMoon(self):
        global fechou
        global esc
        sg.theme('Dark Teal 10') 
        LayoutEscMoon =[
            [sg.Text('Deseja adicionar LUAS em seu planeta?')],
            [sg.Button('Sim'), sg.Button('Nao')]
        ]
        #janela 
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutEscMoon)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Sim'):
                esc = 1
                break
            if (self.event == 'Nao'):
                esc = 2
                break
        self.janela.close()

    def LayoutLatitudesugerida(self):
        sg.theme('Dark Teal 10')
        sg.Popup('Latitude sugerida para a mancha:',calculaLat(self.semiEixoRaioStar,self.anguloInclinacao))
        
    #PARAMETROS DA MANCHA
    def LayoutMancha(self):
        global fechou
        sg.theme('Dark Teal 10') 
        LayoutMancha =[
            [sg.Image(r'./dependences/manchas estelares.png',tooltip = 'estrela manchada.png' )],
            [sg.Text('Raio da Mancha       '),sg.Input(size=(15,0),key='raioMancha')],
            [sg.Text('Intensidade da Mancha'),sg.Input(size=(15,0),key='intensidadeMancha')],
            [sg.Text('Latitude da Mancha   '),sg.Input(size=(15,0),key='latitudeMancha')],
            [sg.Text('Longitude da Mancha  '),sg.Input(size=(15,0),key='longitudeMancha')],
            [sg.Button('Enviar Dados')]
        ]
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutMancha)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Enviar Dados'):
                break
        self.janela.close()



    def LayoutMoon(self):
        global fechou
        sg.theme('Dark Teal 10') 
        LayoutMancha =[
            [sg.Image(r'./dependences/luas.png',tooltip = 'luas.png' )],
            [sg.Text('Raio da Lua (em função ao Raio da Terra) '),sg.Input(size=(15,0),key='rMoon')],
            [sg.Text('Massa da Lua (em função à massa da Terra)'),sg.Input(size=(15,0),key='massMoon')],
            [sg.Text('Massa do planeta (em Raios de Júpiter)   '),sg.Input(size=(15,0),key='massPlaneta')],
            [sg.Text('Período da órbita da Lua (em dias)       '),sg.Input(size=(15,0),key='perLua')],
            [sg.Button('Enviar Dados')]
        ]
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutMancha)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Enviar Dados'):
                break
        self.janela.close()

    def iniciarMoon(self):
        self.rMoon=float(self.values['rMoon'])
        erro = Validar(self.rMoon)
        if erro == True: 
            return True
        self.massMoon=float(self.values['massMoon'])
        erro = Validar(self.massMoon)
        if erro == True: 
            return True
        self.massPlaneta=float(self.values['massPlaneta'])
        erro = Validar(self.massPlaneta)
        if erro == True: 
            return True
        self.perLua=float(self.values['perLua'])
        erro = Validar(self.perLua)
        if erro == True: 
            return True

        self.rMoon = self.rMoon *6371 #multiplicando pelo R da terra em Km
        self.massMoon = self.massMoon * (5.972*(10**24))
        self.massPlaneta = self.massPlaneta * (1.898 *(10**27)) #passar para gramas por conta da constante G
        G = (6.674184*(10**(-11)))
        distancia=((((self.perLua*24.*3600./2./np.pi)**2)*G*(self.massPlaneta+self.massMoon))**(1./3))/self.raioStar
        distancia = distancia/100
        moon = self.eclipse.criarLua(self.rMoon,self.massMoon,self.raioPlanetaPixel,self.raioStar,self.tempoHoras,self.anguloInclinacao,self.periodo,distancia)
        self.estrela = self.estrela_.getEstrela()
        erro = False

    def LayoutQuantidade(self):
        global fechou
        sg.theme('Dark Teal 10') 
        LayoutQuantidade =[
            [sg.Text('Quantidade desejada:'),sg.Input(size=(15,0),key='count')],
            [sg.Button('Enviar Dados')]
        ]
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutQuantidade)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Enviar Dados'):
                break
        self.janela.close()

    def LayoutQuantidadeMoon(self):
        global fechou
        sg.theme('Dark Teal 10') 
        LayoutQuantidadeMoon =[
            [sg.Text('Quantidade de LUAS desejada:'),sg.Input(size=(15,0),key='countMoon')],
            [sg.Button('Enviar Dados')]
        ]
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutQuantidadeMoon)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Enviar Dados'):
                break
        self.janela.close()    

    def LayoutIntervaloTempo(self):
        global fechou
        sg.theme('Dark Teal 10') 
        LayoutIntervaloTempo =[
            [sg.Text('Digite o Intervalo de tempo gráfico (sugestão : 1)'),sg.Input(size=(15,0),key='intervaloTempo')],
            [sg.Button('Enviar Dados')]
        ]
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutIntervaloTempo)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Enviar Dados'):
                break
        self.janela.close()    

    def coletaIntervaloTempo(self):
        intervaloTempo = float(self.values['intervaloTempo'])
        intervaloTempo = Validar(intervaloTempo)
        return False,intervaloTempo

    def LayoutAvisoSemiEixo(self):
        global fechou
        LayoutAvisoSemiEixo=[
            [sg.Image(r'./dependences/lei de kepler.png',tooltip = 'aviso.png' )],
            [sg.Button('Enviar Dados')]
        ]
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutAvisoSemiEixo)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Enviar Dados'):
                break
        self.janela.close()

    def LayoutPlaneta(self):
        global fechou
        LayoutPlaneta=[
            [sg.Image(r'./dependences/transito.png',tooltip = 'transito.png' )],
            [sg.Text('Ângulo de Inclinação (graus)'),sg.Input(size=(15,0),key='anguloInclinacao')],
            [sg.Text('Raio do Planeta em Relacao ao raio de Júpiter'),sg.Input(size=(15,0),key='raioPlanetaRstar')],
            [sg.Text('Excentricidade'),sg.Input(size=(15,0),key='ecc')],
            [sg.Text('Anomalia'),sg.Input(size=(15,0),key='anom')],
            [sg.Button('Enviar Dados')]
        ]
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutPlaneta)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Enviar Dados'):
                break
        self.janela.close()
    

    def LayoutUA(self):
        global fechou
        LayoutUA = [
            [sg.Text('Semi Eixo Orbital (Em unidades Astronomicas UA)'),sg.Input(size=(15,0),key='semiEixoRaioStar')],
            [sg.Button('Enviar Dados')]
        ]
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutUA)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Enviar Dados'):
                break
        self.janela.close()


    def UA(self):
        self.semiEixoRaioStar = float(self.values['semiEixoRaioStar'])
        erro = Validar(self.semiEixoRaioStar)
        if erro == True:
            return True

        self.semiEixoRaioStar = ((1.469*(10**8))*self.semiEixoRaioStar)/self.raioStar
        return False


    def CriarPlaneta(self):

        def LayoutErroInclinacao(self):
            global fechou
            sg.theme('Dark Teal 10')
            LayoutErroInclinacao =[
                [sg.Text('O Planeta não orbita a Estrela. Por favor, mude o ângulo de inclinação.')],
                [sg.Text('Ângulo de Inclinação:'),sg.Input(size=(15,0),key='anguloInclinacao2')],
                [sg.Button('Enviar Dados')]
            ]
            self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutErroInclinacao)
            while True:
                #extrair dados da tela 
                self.event, self.values = self.janela.Read()
                if (self.event == sg.WIN_CLOSED):
                    fechou = True
                    break
                if (self.event == 'Enviar Dados'):
                    break
            self.janela.close()
        
        dtor = np.pi/180. 

        self.anguloInclinacao = float(self.values['anguloInclinacao'])
        erro=Validar(self.anguloInclinacao)
        if erro == True: 
            return True
        raioPlanetaRstar = float(self.values['raioPlanetaRstar'])
        erro=Validar(raioPlanetaRstar)
        if erro == True: 
            return True

        self.ecc = float(self.values['ecc'])
        erro=Validar(self.ecc)
        if erro == True: 
            return True

        self.anom = float(self.values['anom'])
        erro=Validar(self.anom)
        if erro == True: 
            return True

        self.raioPlanetaRstar = (raioPlanetaRstar*69911)/self.raioStar #multiplicando pelo raio de jupiter em km 
        while self.semiEixoRaioStar*np.cos(self.anguloInclinacao*dtor) >= 1: 
            LayoutErroInclinacao(self)
            if(fechou == True):
                return 5
            self.anguloInclinacao = float(self.values['anguloInclinacao2'])
        return False
    
    def CriarEclipse(self,intervaloTempo):
        self.eclipse= Eclipse(self.Nx,self.Ny,self.raio,self.estrela) 
        self.eclipse.setIntervaloTempo(intervaloTempo)
        self.eclipse.geraTempoHoras()
        self.raioPlanetaPixel = (self.raioPlanetaRstar)*(self.raio)
        self.tempoHoras = self.eclipse.getTempoHoras()
        '''
        #Plotagem da curva de luz 
        #pyplot.plot(tempoHoras,curvaLuz)
        #pyplot.axis([-tempoTransito/2,tempoTransito/2,min(curvaLuz)-0.001,1.001])                       
        #pyplot.show()
        '''
        return False

    def geraEclipse(self,lua):
        self.eclipse.criarEclipse(self.semiEixoRaioStar, self.raioPlanetaRstar,self.periodo,self.anguloInclinacao,lua,self.ecc,self.anom)
        self.tempoTransito=self.eclipse.getTempoTransito()
        self.curvaLuz=self.eclipse.getCurvaLuz()
        return False

    def LayoutSemiEixoEsc(self):
        global fechou
        global esc
        sg.theme('Dark Teal 10')
        LayoutSemiEixoEsc = [
            [sg.Text('Período do trânsito (dias)'),sg.Input(size=(15,0),key='periodo')],
            [sg.Text('Deseja calcular o semi eixo orbital através da 3a Lei de Kepler?')],
            [sg.Button('Sim'), sg.Button('Nao')]
        ]
        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutSemiEixoEsc)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Sim'):
                esc = 1
                break
            if (self.event == 'Nao'):
                esc = 2
                break
        self.janela.close()

    def LayoutSemiEixo(self):
        global fechou
        sg.theme('Dark Teal 10')
        LayoutSemiEixo = [
            [sg.Text('Digite a massa da estrela em unidades de MassSun:'),sg.Input(size=(15,0),key='mass')],
            [sg.Button('Enviar Dados')]
        ]

        self.janela = sg.Window("Cálculo da curva de luz de uma host star").layout(LayoutSemiEixo)
        while True:
            #extrair dados da tela 
            self.event, self.values = self.janela.Read()
            if (self.event == sg.WIN_CLOSED):
                fechou = True
                break
            if (self.event == 'Enviar Dados'):
                break
        self.janela.close()

    def LayoutResultados(self):
        global fechou
        sg.theme('Dark Teal 10')
        fa = []
        for i in range(len(self.fa)):
            aux = '{:.2f}'.format(self.fa[i])
            fa.append(aux)
        tempoTransito = float(self.tempoTransito)
        sg.Popup("Areas das manchas respectivamente : {fa} \nTempo de trânsito em Horas: {tempoTransito:.2f}".format(fa = fa, tempoTransito = tempoTransito))
        #sg.Popup("Areas das manchas respectivamente :",self.fa,"\nTempo de trânsito em Horas: ",self.tempoTransito)
    
    def LayoutAguarde(self):
        global fechou
        sg.theme('Dark Teal 10')
        sg.Popup("Aguarde um momento, a animação do Trânsito está sendo gerada!")
        
    def IniciarCalSemiEixo(self):
        self.mass=float(self.values['mass'])
        erro= Validar(self.mass)
        if erro == True: 
            return True

        semieixoorbital = calSemiEixo(self.periodo,self.mass) #retorna o semieixo orbital
        self.semiEixoRaioStar = ((semieixoorbital/1000)/self.raioStar)
        #transforma em km para fazer em relação ao raio da estrela
        return False

    def iniciarEstrela (self):
        self.raio=373
        intensidadeMax=240
        tamanhoMatriz=856
        self.raioStar=float(self.values['raio'])
        erro = Validar(self.raioStar)
        if erro == True: 
            return True
        self.raioStar=self.raioStar*696340 
        self.coeficienteHum=float(self.values['coeficienteHum'])
        erro = Validar(self.coeficienteHum)
        if erro == True: 
            return True
        self.coeficienteDois=float(self.values['coeficienteDois'])
        erro = Validar(self.coeficienteDois)
        if erro == True: 
            return True


        self.estrela_ = estrela(self.raio,intensidadeMax,self.coeficienteHum,self.coeficienteDois,tamanhoMatriz)
        self.Nx= self.estrela_.getNx() #Nx  e Ny necessarios para a plotagem do eclipse
        self.Ny= self.estrela_.getNy()
        self.estrela = self.estrela_.getEstrela()
        return False

    def criaVetores(self,count): #qtd de manchas
        global fa, fi, lg, lt
        self.fa = [0.]*count #vetor area manchas
        self.fi = [0.]*count #vetor intensidade manchas
        self.lg = [0.]*count #vetor longitude manchas
        self.lt = [0.]*count #vetor latitude manchas
        self.fa = self.fa + fa
        fa = self.fa
        self.fi = self.fi + fi
        fi = self.fi
        self.lg = self.lg + lg
        lg = self.lg
        self.lt = self.lt + lt
        lt = self.lt
    

    def iniciarMancha(self,x):
        self.raioMancha=float(self.values['raioMancha'])
        erro = Validar(self.raioMancha)
        if erro == True: 
            return True

        raioreal= self.raioMancha*self.raioStar
        area = np.pi *(raioreal**2)
        self.fa[x] = area

        self.intensidadeMancha=float(self.values['intensidadeMancha'])
        erro = Validar(self.intensidadeMancha)
        if erro == True: 
            return True
        self.fi[x] = self.intensidadeMancha

        self.latitudeMancha=float(self.values['latitudeMancha'])
        lat = self.latitudeMancha
        self.lt[x] = self.latitudeMancha
        
        self.longitudeMancha=float(self.values['longitudeMancha'])
        longt = self.longitudeMancha
        self.lg[x] = self.longitudeMancha
      
        self.estrela=self.estrela_.manchas(self.raioMancha,self.intensidadeMancha,lat,longt)
        self.estrela = self.estrela_.getEstrela()
        self.eclipse.setEstrela(self.estrela)
        return False

    def quantidade(self):
        self.count=int(self.values['count'])
        return self.count

    def quantidadeMoon(self):
        self.countMoon=int(self.values['countMoon'])
        return self.countMoon

    def escolhaSemiEixo(self):
        self.periodo = float(self.values['periodo'])
        erro=Validar(self.periodo)
        if erro == True: 
            return True


#funcoes para rodar o programa
#inicio, onde sao passados os parametros iniciais da estrela
def inicio():
    error = True
    while error==True:
        try:
            tela=LayoutStar()
            if fechou==True:
                return 0
            error = tela.iniciarEstrela()
            if error==True:
                tela.LayoutError()
        except Exception as erro :
            print(f'\033[0;31mO tipo de problema encontrado foi{erro.__class__}\n\n\033[m')
            tela.LayoutError()
    return tela

#calculo do semieixo
def semieixo(tela):
    error = True
    while error==True:
        try: 
            tela.LayoutSemiEixoEsc()#sim ou nao
            if fechou == True:
                return 0
            error = tela.escolhaSemiEixo()
            if error==True:
                tela.LayoutError()
            elif esc == 1:
                tela.LayoutAvisoSemiEixo()
                if fechou == True:
                    return 0
                tela.LayoutSemiEixo()
                if fechou == True:
                    return 0
                error = tela.IniciarCalSemiEixo() #iniciando calculo do semieixo que o retornara para a classe
            elif esc ==2:
                tela.LayoutUA() #digita semieixo em UA
                if fechou == True:
                    return 0
                error = tela.UA() #conversao das UA
            else:
                tela.LayoutError()
        except Exception:
            tela.LayoutError()
    return tela

#parametros das manchas
def manchas(tela,decisao):
    error = True
    while error == True: 
        try:
            tela.LayoutEsc()
            if fechou == True:
                return 0,0
            if esc == 1:
                decisao=True
                x=0
                tela.LayoutQuantidade()
                if fechou == True:
                    return 0,0
                count = tela.quantidade() #retorna a quantidade de manchas 
                tela.criaVetores(count)
                if fechou == True:
                    return 0,0
                tela.LayoutLatitudesugerida()
                if fechou == True:
                    return 0,0
                while x<count:
                    tela.LayoutMancha()
                    if fechou == True:
                        return 0,0
                    error = tela.iniciarMancha(x) #passa o indice
                    if error == True:
                        tela.LayoutError()
                        break #para a contagem de manchas
                    x+=1
            elif esc==2:
                decisao=False
                error=False
                tela.criaVetores(1)#cria vetores simbolicos
                if fechou == True:
                    return 0,0
            
        except Exception :
            tela.LayoutError()
    return tela,decisao

def decLuas(tela,decisao):
    error = True
    while error == True: 
        try:
            tela.LayoutEscMoon()
            if fechou == True:
                return 0,0
            if esc == 1:
                decisao=True
            elif esc==2:
                decisao=False
                error=False
                if fechou == True:
                    return 0,0
            error = False
        except Exception :
            tela.LayoutError()
    return tela,decisao

def criaLuas(tela):
    x=0
    tela.LayoutQuantidadeMoon()
    if fechou == True:
        return 0,0
    count = tela.quantidadeMoon() #retorna a quantidade de manchas
    if count <= 0:
        return tela, False
    if fechou == True:
        return 0,0
    while x<count:
        tela.LayoutMoon()
        if fechou == True:
            return 0,0
        error = tela.iniciarMoon() #passa o indice
        if error == True:
            tela.LayoutError()
            break #para a contagem de Luas
        x+=1
    return tela, True

#parametros do eclipse e do planeta
def criaeclipse(tela):
    error = True 
    while error == True:
        try:
            tela.LayoutPlaneta() #passa parametros dos planetas
            if fechou == True:
                return 0
            error = tela.CriarPlaneta()
            if error == 5:
                return 0
            if error==True:
                tela.LayoutError()
            
        except Exception:
            tela.LayoutError()
    return tela

def criaIntervalo(tela):
    error = True 
    while error == True:
        try:
            tela.LayoutIntervaloTempo()
            if fechou == True:
                return 0
            error, intervaloTempo = tela.coletaIntervaloTempo()
            if error==True:
                tela.LayoutError()
        except Exception:
            tela.LayoutError()
            return 0,1
    return tela,intervaloTempo

#main
def main():
    tela = inicio()
    if(tela == 0):
        return 0
    #se nao houverem erros, continuara 
    #semi eixo
    tela = semieixo(tela)
    if(tela == 0):
        return 0

    #fase do eclipse
    decisaoMoon=True
    tela,decisaoMoon = decLuas(tela,decisaoMoon)
    if(tela == 0):
        return 0
    if(decisaoMoon == True):
        lua = True
    else:
        lua = False
    tela = criaeclipse(tela)
    if(tela == 0):
        return 0
    tela, intervaloTempo = criaIntervalo(tela)
    if(tela == 0):
        return 0
    tela.CriarEclipse(intervaloTempo)#instancia o eclipse
    if (lua ==True): #coleta dados da lua
        tela,lua = criaLuas(tela)
        if(tela == 0):
            return 0
    decisao=True
    #Fase das manchas
    while True:
        tela.LayoutAguarde()
        tela.geraEclipse(lua) #calculo da curva de luz
        tela,decisao = manchas(tela,decisao)
        if(tela == 0):
            return 0
        tela.LayoutResultados()
        if decisao == False:
            break


#codigo
main()
