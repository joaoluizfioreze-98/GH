import tkinter as tk
from tkinter import ttk, messagebox
import math

root=tk.Tk()
root.title("Protótipo Renovação GH")
root.geometry("700x650")

conc=tk.StringVar(value='12')

# Interface simples de teste
frm=tk.Frame(root)
frm.pack(fill='both', expand=True, padx=10, pady=10)

tk.Label(frm,text='Concentração').pack()
ttk.Combobox(frm, values=['4','12'], textvariable=conc).pack()

tk.Label(frm,text='Última dose').pack()
last=tk.Entry(frm); last.pack()
last_unit=tk.StringVar(value='UI')
ttk.Combobox(frm, values=['UI','mL'], textvariable=last_unit).pack()
last_days=tk.Entry(frm); last_days.insert(0,'7'); last_days.pack()

tk.Label(frm,text='Dose atual').pack()
current=tk.Entry(frm); current.pack()
current_unit=tk.StringVar(value='UI')
ttk.Combobox(frm, values=['UI','mL'], textvariable=current_unit).pack()
current_days=tk.Entry(frm); current_days.insert(0,'7'); current_days.pack()

classe=tk.StringVar(value='Crianca E23')
ttk.Combobox(frm, values=['Crianca E23','Adulto E23','Crianca Q96','Adulto Q96'], textvariable=classe).pack()

peso=tk.Entry(frm)
peso.pack()
peso.insert(0,'0')

saida=tk.Text(frm,height=15)
saida.pack(fill='both',expand=True)

def calc():
    try:
        c=float(conc.get())
        lv=float(last.get().replace(',','.'))
        cv=float(current.get().replace(',','.'))
        ld=float(last_days.get().replace(',','.'))
        cd=float(current_days.get().replace(',','.'))

        last_ui=lv if last_unit.get()=='UI' else lv*c
        curr_ui=cv if current_unit.get()=='UI' else cv*c

        saida.delete('1.0','end')

        if abs(last_ui*ld-curr_ui*cd)<0.0001:
            saida.insert('end','Tudo certo, dose atual confere com a última deferida!
Agora lembre-se de observar os itens obrigatórios na receita.')
            return

        alerta=''
        dose_dia=(curr_ui*cd)/7

        if classe.get()=='Crianca E23':
            limite=0.1*float(peso.get().replace(',','.'))
            if dose_dia>limite:
                alerta+='Dose acima do limite Criança E23.
'
        elif classe.get()=='Adulto E23':
            if dose_dia>1:
                alerta+='Dose acima do limite Adulto E23.
'
        else:
            limite=0.15*float(peso.get().replace(',','.'))
            if dose_dia>limite:
                alerta+='Dose acima do limite Q96. A dose 0,2 UI/kg/dia somente casos especiais conforme PCDT.
'

        ml_aplic=curr_ui/c
        frascos=math.ceil(ml_aplic*(cd/7)*30)

        saida.insert('end',f'Frascos para 30 dias: {frascos}
')
        if c==4 and frascos>93:
            alerta+='Ultrapassa 93 frascos.
'
        if c==12 and frascos>31:
            alerta+='Ultrapassa 31 frascos.
'

        saida.insert('end', alerta if alerta else 'Dose dentro dos limites.')
    except Exception as e:
        messagebox.showerror('Erro', str(e))

btn=tk.Button(frm,text='Calcular',command=calc)
btn.pack()

root.mainloop()
