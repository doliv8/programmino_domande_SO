import tkinter as tk
import json
from tkinter import messagebox
import random
import os



lista_domande_caricata = []
lista_domande_fatte = []
punti = 0
dimensione_testo = 16
diff_titoli = 2 
diff_info = 5
sett_diff = 8
nome_file = ""
margine_finestre = 40


def pulisci_finestra(finestra):
    for widget in finestra.winfo_children():
        widget.destroy()

def elenca_file_json(cartella="."):
   
    files_json = []
    
    try:
        tutti_i_file = os.listdir(cartella)
        
        for file in tutti_i_file:
            if file.lower().endswith(".json"):
                files_json.append(file)
                
    except FileNotFoundError:
        print(f"Errore: La cartella '{cartella}' non esiste.")
        return []

    return files_json


def randomizza_lista(list_inp):
    new_list = []
    lista = list_inp.copy()

    while len(lista) > 0:
        rand = random.randrange(len(lista))
        new_list.append(lista.pop(rand))

    return new_list

def mischia_domande():
    global lista_domande_caricata
    lista_domande_caricata = randomizza_lista(lista_domande_caricata)



def inizializza_dati():
    global nome_file
    global lista_domande_caricata

    try:
        # <--- CORREZIONE: Aggiunto encoding='utf-8' per leggere gli accenti correttamente, onomatopea della libellula
        with open(nome_file, 'r', encoding='utf-8') as file:
            lista_domande_caricata = json.load(file)
            print(f"Caricato file {nome_file}")
    except FileNotFoundError:
        messagebox.showerror(f"Errore", "File {nome_file} non trovato!")
        root.destroy()
    except json.JSONDecodeError:
        messagebox.showerror(
            f"Errore", "Il file {nome_file} non è formattato correttamente.")
        root.destroy()

    #randomizza le domande
    mischia_domande()

def genera_schermata_scelta_file(finestra):
    global nome_file

    var_temp = tk.StringVar(value=None)

    lbl = tk.Label(finestra, text="Quale file vuoi usare?",font=("Arial", dimensione_testo+diff_titoli,"bold"))
    lbl.pack(pady=10)

    for file in elenca_file_json():

        radio = tk.Radiobutton(
            finestra,
            text=file,              # Il testo che leggi a video
            value=file,             # Il valore che la variabile assumerà se clicchi qui
            variable=var_temp, # Collega tutti alla stessa variabile!
            font=("Arial", dimensione_testo),
            anchor="w"               # Allinea il testo a sinistra (West)
        )   
        radio.pack(fill='x', padx=20, pady=2)

    def set_nome_file():
        global nome_file
        nome_file = var_temp.get()
        inizializza_dati()

        if lista_domande_caricata:
            carica_nuova_domanda()



    btn = tk.Button(finestra, text="CONFERMA SCELTA", bg="green", fg="white", command=set_nome_file)
    btn.pack(pady=20)



def genera_schermata(finestra, domanda, opzioni, soluzioni, funzione_salta):
    global punti
    global dimensione_testo


    # pulisci schiavo
    for widget in finestra.winfo_children():
        widget.destroy()





    # <--- Aumentato wraplength per finestre più larghe, ci sta gem
    lbl_domanda = tk.Label(finestra, text=domanda, font=(
        "Arial", dimensione_testo+diff_titoli, "bold"), justify="center")
    lbl_domanda.pack(pady=20,expand=True, fill='both')

    # 3. OPZIONI
    lista_checkbuttons = []

    frame_opzioni = tk.Frame(finestra)
    frame_opzioni.pack(pady=10)

    temp_opzioni = randomizza_lista(opzioni)
    for opzione in temp_opzioni:
        var = tk.BooleanVar()
        # Aggiunto wraplength anche alle opzioni per evitare che escano dallo schermo, super mario karta
        chk = tk.Checkbutton(frame_opzioni, text=opzione, variable=var, font=(
            "Arial", dimensione_testo), selectcolor="white", wraplength=500, justify="left")
        chk.pack(anchor="w", pady=2)
        lista_checkbuttons.append((chk, var, opzione))

    # LOGICA VALIDA
    def valida_risposte():
        global punti
        count_giuste = 0
        errore_commesso = False 
        
        for chk_widget, var_value, testo_opzione in lista_checkbuttons:
            
            # calcolo punti
            is_selezionata = var_value.get()
            is_corretta = testo_opzione in soluzioni
            
            if is_selezionata and not is_corretta:
                errore_commesso = True
            
            if is_selezionata and is_corretta:
                count_giuste += 1
            
            # -------------------------

            chk_widget.config(bg="#f0f0f0", fg="black") # Reset
            
            if is_corretta:
                chk_widget.config(bg="lightgreen", selectcolor="lightgreen")

            elif is_selezionata and not is_corretta:
                chk_widget.config(bg="#ffcccc")

        
        if not errore_commesso and len(soluzioni) > 0:
            tot_punti = (1 / len(soluzioni)) * count_giuste
            punti += tot_punti
      
    

    # tastini oja
    frame_tasti = tk.Frame(finestra)
    frame_tasti.pack(side="bottom", pady=20)

    btn_indietro = tk.Button(frame_tasti, text="INDIETRO", bg="red", fg ="white", font= ("Arial",dimensione_testo,"bold"), command = carica_domanda_precedente)
    btn_indietro.pack(side = "left", padx = 20)
    btn_valida = tk.Button(frame_tasti, text="VALIDA", bg="green", fg="white", font=("Arial", dimensione_testo, "bold"),
                           command=valida_risposte)
    btn_valida.pack(side="right", padx=20)

    btn_salta = tk.Button(frame_tasti, text="SALTA / PROSSIMA", bg="orange", fg="white", font=("Arial", dimensione_testo, "bold"),
                          command=funzione_salta)
    btn_salta.pack(side="left", expand = True)
    



    #info
    frame_info = tk.Frame(finestra)
    frame_info.pack(pady=10)
    label_N_domande = tk.Label(frame_info, text = f"domanda: {len(lista_domande_fatte)}/{len(lista_domande_caricata)+len(lista_domande_fatte)}",font=("Arial", dimensione_testo-diff_info))
    label_N_domande.pack(side= "left", padx=20)

    label_punti = tk.Label(frame_info, text = f"punti: {punti:.2f}/{len(lista_domande_caricata)+len(lista_domande_fatte)}",font=("Arial", dimensione_testo-diff_info))
    label_punti.pack(side="right",padx = 20)

    
    def inc_dim_text():
        global dimensione_testo
        dimensione_testo+=2
        genera_schermata(finestra,domanda,opzioni,soluzioni,funzione_salta)
        return
    def dec_dim_text():
        global dimensione_testo
        dimensione_testo-=2
        genera_schermata(finestra,domanda,opzioni,soluzioni,funzione_salta)
        return

    inc_button = tk.Button(frame_info, text="+", bg="gray", fg ="black", font= ("Arial",dimensione_testo-sett_diff,"bold"), command = inc_dim_text)
    inc_button.pack(side="right", pady=2)
    dec_button =tk.Button(frame_info, text="-", bg="gray", fg ="black", font= ("Arial",dimensione_testo-sett_diff,"bold"), command = dec_dim_text)
    dec_button.pack(side="left", pady=2)


    def aggiorna_wraplength(event):
        # Imposta il wraplength alla larghezza della finestra meno un margine (es. 40px)
        lbl_domanda.config(wraplength=finestra.winfo_width() - margine_finestre)
        label_N_domande.config(wraplength=finestra.winfo_width() - margine_finestre)
        label_punti.config(wraplength=finestra.winfo_width() - margine_finestre)
    finestra.bind('<Configure>', aggiorna_wraplength)
        




def carica_domanda_precedente():
    lista_domande_caricata.append(lista_domande_fatte.pop(-1))
    lista_domande_caricata.append(lista_domande_fatte.pop(-1))

    
    carica_nuova_domanda()


def carica_nuova_domanda():
    """Pesca una domanda dalla lista caricata e aggiorna la grafica"""
    
    if not lista_domande_caricata:
        messagebox.showinfo(
            "Finito!", "Hai risposto a tutte le domande disponibili.")
        root.destroy()
        return

    
    
    lista_domande_fatte.append(lista_domande_caricata.pop())
    dati = lista_domande_fatte[-1]
    # Chiama la funzione grafica
    genera_schermata(
        root,
        dati["domanda"],
        dati["opzioni"],
        dati["soluzioni"],
        carica_nuova_domanda
    )


# --- main senza main ---
root = tk.Tk()
root.title("Quiz SO")
root.geometry("1000x800")


genera_schermata_scelta_file(root)

print(len(lista_domande_caricata))


root.mainloop()
