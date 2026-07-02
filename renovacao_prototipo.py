import tkinter as tk
from tkinter import ttk, messagebox
import math

class App:
    def __init__(self, root):
        self.root = root
        root.title('Renovação - GH')
        root.geometry('800x750')

        fonte=('Segoe UI',14)

        self.conc = tk.StringVar(value='12')
        self.classe = tk.StringVar(value='Crianca E23')

        ttk.Label(root, text='Concentração', font=fonte).pack()
        ttk.Radiobutton(root,text='4 UI/mL',variable=self.conc,value='4',command=self.update_conv).pack()
        ttk.Radiobutton(root,text='12 UI/mL',variable=self.conc,value='12',command=self.update_conv).pack()

        ttk.Label(root,text='Última dose', font=fonte).pack()
        self.last_val=tk.Entry(root,font=fonte); self.last_val.pack()
        self.last_unit=tk.StringVar(value='UI')
        ttk.Combobox(root,textvariable=self.last_unit,values=['UI','mL']).pack()
        self.last_days=tk.Entry(root,font=fonte); self.last_days.pack(); self.last_days.insert(0,'7')

        ttk.Label(root,text='Dose atual', font=fonte).pack()
        self.curr_val=tk.Entry(root,font=fonte); self.curr_val.pack()
        self.curr_val.bind('<KeyRelease>', lambda e:self.update_conv())
        self.curr_unit=tk.StringVar(value='UI')
        cb=ttk.Combobox(root,textvariable=self.curr_unit,values=['UI','mL'])
        cb.pack(); cb.bind('<<ComboboxSelected>>', lambda e:self.update_conv())
        self.curr_days=tk.Entry(root,font=fonte); self.curr_days.pack(); self.curr_days.insert(0,'7')

        self.conv_lbl=ttk.Label(root,text='Equivalente: -', font=fonte)
        self.conv_lbl.pack()

        ttk.Label(root,text='Classificação', font=fonte).pack()
        ttk.Combobox(root,textvariable=self.classe,values=['Crianca E23','Adulto E23','Crianca Q96','Adulto Q96']).pack()

        ttk.Label(root,text='Peso (kg) - quando aplicável', font=fonte).pack()
        self.peso=tk.Entry(root,font=fonte); self.peso.pack()

        ttk.Button(root,text='Calcular',command=self.calc).pack(pady=10)

        self.out=tk.Text(root,height=18,font=('Segoe UI',12))
        self.out.pack(fill='both',expand=True)
        self.out.tag_config('alerta', foreground='red')

    def update_conv(self):
        try:
            v=float(self.curr_val.get().replace(',','.'))
            c=float(self.conc.get())
            if self.curr_unit.get()=='UI':
                self.conv_lbl.config(text=f'Equivalente: {v/c:.3f} mL')
            else:
                self.conv_lbl.config(text=f'Equivalente: {v*c:.3f} UI')
        except:
            self.conv_lbl.config(text='Equivalente: -')

    def calc(self):
        try:
            c=float(self.conc.get())
            lv=float(self.last_val.get().replace(',','.'))
            cv=float(self.curr_val.get().replace(',','.'))
            ld=float(self.last_days.get().replace(',','.'))
            cd=float(self.curr_days.get().replace(',','.'))

            last_ui = lv if self.last_unit.get()=='UI' else lv*c
            curr_ui = cv if self.curr_unit.get()=='UI' else cv*c

            last_week = last_ui*ld
            curr_week = curr_ui*cd

            self.out.delete('1.0',tk.END)

            if abs(last_week-curr_week) < 0.0001:
                self.out.insert(tk.END,'✅ Tudo certo, dose atual confere com a última deferida!
Agora lembre-se de observar os itens obrigatórios na receita.')
                return

            alerta=''
            cls=self.classe.get()
            if cls=='Crianca E23':
                peso=float(self.peso.get().replace(',','.'))
                max_day=0.1*peso
                dose_day=curr_week/7
                if dose_day>max_day:
                    alerta+='
ATENÇÃO: Dose acima do limite Criança CID E23 (0,1 UI/kg/dia).
'
            elif cls=='Adulto E23':
                dose_day=curr_week/7
                if dose_day>1:
                    alerta+='
ATENÇÃO: Dose acima do limite Adulto CID E23 (1 UI/dia).
'
            else:
                peso=float(self.peso.get().replace(',','.'))
                max_day=0.15*peso
                dose_day=curr_week/7
                if dose_day>max_day:
                    alerta+='
ATENÇÃO: Dose acima do limite CID Q96 (0,15 UI/kg/dia).
'

            ml_aplic = curr_ui/c if c else 0
            ml_30 = ml_aplic * (cd/7) * 30
            frascos = math.ceil(ml_30)

            self.out.insert(tk.END,f'Dose semanal atual: {curr_week:.2f} UI
')
            self.out.insert(tk.END,f'Frascos para 30 dias: {frascos}
')

            if c==4 and frascos>93:
                alerta+='
ATENÇÃO: Ultrapassa o limite de 93 frascos para 4 UI/mL.
'
            if c==12 and frascos>31:
                alerta+='
ATENÇÃO: Ultrapassa o limite de 31 frascos para 12 UI/mL.
'

            if alerta:
                self.out.insert(tk.END, alerta, 'alerta')
            else:
                self.out.insert(tk.END, '
✅ Dose dentro dos limites cadastrados.')

        except Exception as e:
            messagebox.showerror('Erro', str(e))

root=tk.Tk()
App(root)
root.mainloop()
