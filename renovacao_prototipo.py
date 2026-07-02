import tkinter as tk
from tkinter import ttk, messagebox
import math

class App:
    def __init__(self, root):
        self.root = root
        root.title('GH Renovacao V3')
        root.geometry('1000x800')

        fonte = ('Segoe UI', 14)

        tk.Label(root, text='Sistema GH - Renovacao V3', font=('Segoe UI',18,'bold')).pack(pady=10)

        topo = tk.Frame(root)
        topo.pack(fill='x', padx=10)

        tk.Label(topo, text='Concentracao', font=fonte).grid(row=0,column=0)
        self.conc = ttk.Combobox(topo, values=['4','12'], width=10)
        self.conc.set('12')
        self.conc.grid(row=0,column=1)

        tk.Label(topo, text='Classificacao', font=fonte).grid(row=0,column=2)
        self.classe = ttk.Combobox(topo, values=['Crianca CID E23','Adulto CID E23','Crianca CID Q96','Adulto CID Q96'], width=25)
        self.classe.set('Crianca CID E23')
        self.classe.grid(row=0,column=3)
        self.classe.bind('<<ComboboxSelected>>', lambda e:self.atualizar_peso())

        lf = ttk.LabelFrame(root, text='Ultima dose deferida')
        lf.pack(fill='x', padx=10, pady=5)
        self.lv = tk.Entry(lf, font=fonte, width=10)
        self.lv.grid(row=0,column=0)
        self.lu = ttk.Combobox(lf, values=['UI','mL'], width=8)
        self.lu.set('UI')
        self.lu.grid(row=0,column=1)
        tk.Label(lf,text='Dias por semana',font=fonte).grid(row=0,column=2)
        self.ld = ttk.Combobox(lf, values=[1,2,3,4,5,6,7], width=5)
        self.ld.set('7')
        self.ld.grid(row=0,column=3)

        cf = ttk.LabelFrame(root, text='Dose atual')
        cf.pack(fill='x', padx=10, pady=5)
        self.cv = tk.Entry(cf, font=fonte, width=10)
        self.cv.grid(row=0,column=0)
        self.cu = ttk.Combobox(cf, values=['UI','mL'], width=8)
        self.cu.set('UI')
        self.cu.grid(row=0,column=1)
        tk.Label(cf,text='Dias por semana',font=fonte).grid(row=0,column=2)
        self.cd = ttk.Combobox(cf, values=[1,2,3,4,5,6,7], width=5)
        self.cd.set('7')
        self.cd.grid(row=0,column=3)

        self.eq = tk.Label(cf, text='Equivalente: -', font=fonte)
        self.eq.grid(row=1,column=0,columnspan=4,sticky='w')

        self.cv.bind('<KeyRelease>', lambda e:self.atualizar_equiv())

        self.peso_frame = tk.Frame(root)
        self.peso_frame.pack(fill='x', padx=10)
        tk.Label(self.peso_frame,text='Peso (kg)',font=fonte).pack(side='left')
        self.peso = tk.Entry(self.peso_frame,font=fonte,width=10)
        self.peso.pack(side='left')

        tk.Button(root,text='CALCULAR',font=('Segoe UI',16,'bold'),command=self.calcular).pack(pady=10)

        self.out = tk.Text(root,height=20,font=('Consolas',12))
        self.out.pack(fill='both',expand=True,padx=10,pady=10)
        self.out.tag_config('red', foreground='red')
        self.out.tag_config('green', foreground='green')

        self.atualizar_peso()

    def atualizar_peso(self):
        if self.classe.get() == 'Adulto CID E23':
            self.peso_frame.pack_forget()
        else:
            self.peso_frame.pack(fill='x', padx=10)

    def atualizar_equiv(self):
        try:
            v=float(self.cv.get().replace(',','.'))
            c=float(self.conc.get())
            if self.cu.get()=='UI':
                self.eq.config(text='Equivalente: %.3f mL' % (v/c))
            else:
                self.eq.config(text='Equivalente: %.3f UI' % (v*c))
        except:
            pass

    def conv(self,v,u,c):
        if u=='UI':
            return v, v/c
        return v*c, v

    def calcular(self):
        self.out.delete('1.0','end')
        try:
            conc=float(self.conc.get())
            lv=float(self.lv.get().replace(',','.'))
            cv=float(self.cv.get().replace(',','.'))
            ld=float(self.ld.get())
            cd=float(self.cd.get())

            if self.classe.get() != 'Adulto CID E23':
                if self.peso.get().strip() == '':
                    messagebox.showerror('Atencao','E necessario informar o peso.')
                    return
                peso=float(self.peso.get().replace(',','.'))
                if peso <= 0:
                    messagebox.showerror('Atencao','Informe um peso valido.')
                    return
            else:
                peso=None

            lui,lml=self.conv(lv,self.lu.get(),conc)
            cui,cml=self.conv(cv,self.cu.get(),conc)

            dose_dia=(cui*cd)/7
            alertas=[]

            if self.classe.get()=='Crianca CID E23':
                dose_max=0.1*peso
                if dose_dia>dose_max: alertas.append('Dose acima de 0,1 UI/kg/dia')
            elif self.classe.get()=='Adulto CID E23':
                dose_max=1
                if dose_dia>1: alertas.append('Dose acima de 1 UI/dia')
            else:
                dose_max=0.15*peso
                if dose_dia>dose_max:
                    alertas.append('Dose acima de 0,15 UI/kg/dia')
                    alertas.append('Dose 0,2 UI/kg/dia somente em casos especiais conforme PCDT')

            iguais = abs((lui*ld)-(cui*cd)) < 0.0001
            frascos = math.ceil(cml*(cd/7)*30)

            if conc==4 and frascos>93: alertas.append('Ultrapassa 93 frascos')
            if conc==12 and frascos>31: alertas.append('Ultrapassa 31 frascos')

            if iguais and not alertas:
                self.out.insert('end','Tudo certo, dose atual confere com a ultima deferida.

')
            elif iguais:
                self.out.insert('end','A dose atual confere com a ultima deferida.

')

            resumo = (
                'RENOVACAO GH

'
                + 'Classificacao: ' + self.classe.get() + '
'
                + 'Dose anterior: %.2f UI (%.3f mL)
' % (lui,lml)
                + 'Dose atual: %.2f UI (%.3f mL)
' % (cui,cml)
                + 'Frequencia: %d dias por semana
' % int(cd)
                + 'Dose maxima: %.2f UI/dia
' % dose_max
                + 'Dose prescrita: %.2f UI/dia
' % dose_dia
                + 'Frascos para 30 dias: %d

' % frascos
            )
            self.out.insert('end', resumo)

            if alertas:
                self.out.insert('end','REVISAR PRESCRICAO
','red')
                for a in alertas:
                    self.out.insert('end','- '+a+'
','red')
            else:
                self.out.insert('end','APTO PARA DISPENSACAO','green')

        except Exception as e:
            messagebox.showerror('Erro', str(e))

root=tk.Tk()
App(root)
root.mainloop()
