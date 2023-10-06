# from _typeshed import Incomplete
from tkinter import *
import mysql.connector
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk  
import uuid
from datetime import datetime



class App(Tk):
    
    current_username = None  # Inizializza la variabile con None
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        

        # Crea uno stile personalizzato per la barra del titolo
        style = ttk.Style()
        style.configure("Title.TFrame", background="Blue")

        # Applica lo stile personalizzato alla barra del titolo
        self.title_frame = ttk.Frame(self, style="Title.TFrame")
        self.title_frame.pack(fill="x",ipady=3)




        # Cambia il titolo della finestra
        self.title("Magazzino Python")

        # Cambia l'icona della finestra
        self.iconbitmap('./assets/warehouse2.ico')

        # Setup Menu
        MainMenu(self)
        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        

        self.frames = {}
       

        for F in (StartPage, Utenti, Clienti, Gestionale, GestionaleClienti, GestionaleProdotti, AggiungiProdotto, EliminaProdotto, ModificaProdotto, Ordini, Notifiche, ClienteNuovoOrdine, ClienteOrdiniEffettuati, ClienteOrdiniLavorati, NuoviOrdini, OrdiniLavorati ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)


    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def show_start_page(self):
        self.show_frame(StartPage)



#############################################################################################################################################


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Creare un font personalizzato con una dimensione maggiore
        button_font = ("Trebuchet MS", 16) 

        page_one = Button(self, width=30, text="UTENTI", font=button_font, command=lambda: controller.show_frame(Utenti))
        page_one.pack(ipady=20, ipadx=10, expand=True, fill=BOTH)

        self.frame = ttk.Frame(self, style="Title.TFrame")
        self.frame.pack(fill="x",ipady=3)

        page_two = Button(self, width=30, text="CLIENTI", font=button_font, command=lambda: controller.show_frame(Clienti))
        page_two.pack(ipady=20, ipadx=10, expand=True, fill=BOTH)

        self.frame = ttk.Frame(self, style="Title.TFrame")
        self.frame.pack(fill="x",ipady=3)



#############################################################################################################################################


# Crea la classe ModificaProdotto
class ModificaProdotto(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        text_font = ("Trebuchet MS", 14) 
        button_font = ("Trebuchet MS", 13) 

        label = Label(self, font=title_font, text="MODIFICA NOME / CODICE / PREZZO")
        label.pack(padx=10, pady=(30,0))

        # Aggiungi la lista dei prodotti
        self.product_listbox = Listbox(self, font=text_font, height=15, width=30)
        self.product_listbox.pack(pady=10)

        # Campi di input per il nome, il codice e la quantità da eliminare
        nome_label = Label(self, font=text_font, text="Nome del Prodotto:")
        nome_label.pack()
        self.nome_entry = Entry(self)
        self.nome_entry.pack(ipadx=80, ipady=5)

        codice_label = Label(self, font=text_font, text="Codice del Prodotto:")
        codice_label.pack(pady=(10,0))
        self.codice_entry = Entry(self)
        self.codice_entry.pack(ipadx=80, ipady=5)

        quantita_label = Label(self, font=text_font, text="Nuovo nome:")
        quantita_label.pack(pady=(10,0))
        self.newNome_entry = Entry(self)
        self.newNome_entry.pack(ipadx=80, ipady=5)

        quantita_label = Label(self, font=text_font, text="Nuovo codice:")
        quantita_label.pack(pady=(10,0))
        self.newCodice_entry = Entry(self)
        self.newCodice_entry.pack(ipadx=80, ipady=5)

        quantita_label = Label(self, font=text_font, text="Prezzo da modificare:")
        quantita_label.pack(pady=(10,0))
        self.prezzo_entry = Entry(self)
        self.prezzo_entry.pack(ipadx=80, ipady=5)

        # Pulsante per eseguire l'eliminazione
        modifica_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Modifica", command=self.mod_product)
        modifica_button.pack(ipady=10, pady=(20,0))

        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(ipady=10, pady=10)


   
        # Chiamare la funzione per aggiornare la lista dei prodotti quando la pagina viene aperta
        self.update_product_listbox()
    

    def goBack(self):
        self.controller.show_frame(GestionaleProdotti)


 
    def update_product_listbox(self):
    # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Seleziona tutti i prodotti dalla tabella prodotti
        select_all_query = "SELECT nomeProdotto, codiceProdotto, prezzoProdotto FROM prodotti"
        cursor.execute(select_all_query)
        products = cursor.fetchall()

        # Svuota la Listbox
        self.product_listbox.delete(0, END)

        # Aggiungi i prodotti alla Listbox
        for product in products:
            nome_prodotto = product[0]
            codice_prodotto = product[1]
            prezzo_prodotto = product[2]
            self.product_listbox.insert(END, f"Nome: {nome_prodotto}")
            self.product_listbox.insert(END, f"Codice: {codice_prodotto}")
            self.product_listbox.insert(END, f"Prezzo: {prezzo_prodotto}€")
            self.product_listbox.insert(END, f"")

        # Chiudi la connessione al database
        db.close()
    

    def mod_product(self):
    # Recupera i dati inseriti dall'utente
        nome_prodotto = self.nome_entry.get()
        codice_prodotto = self.codice_entry.get()
        newNome_prodotto = self.newNome_entry.get()
        newCodice_prodotto = self.newCodice_entry.get()
        prezzo_da_modificare = self.prezzo_entry.get()
    
        # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )
    
        cursor = db.cursor()
    
        # Cerca il prodotto nel database
        select_query = "SELECT * FROM prodotti WHERE nomeProdotto = %s AND codiceProdotto = %s"
        cursor.execute(select_query, (nome_prodotto, codice_prodotto))
        existing_product = cursor.fetchone()
    
        if existing_product:
            # Costruisci la query di aggiornamento dinamicamente
            update_query = "UPDATE prodotti SET"
    
            update_values = []  # Una lista per memorizzare i valori da passare nella tupla di execute
    
            if newNome_prodotto != "":
                update_query += " nomeProdotto = %s,"
                update_values.append(newNome_prodotto)
            if newCodice_prodotto != "":
                update_query += " codiceProdotto = %s,"
                update_values.append(newCodice_prodotto)
            if prezzo_da_modificare != "":
                update_query += " prezzoProdotto = %s,"
                update_values.append(prezzo_da_modificare)
    
            # Rimuovi l'ultima virgola dalla query di aggiornamento
            update_query = update_query.rstrip(',')
    
            # Aggiungi la clausola WHERE
            update_query += " WHERE nomeProdotto = %s AND codiceProdotto = %s"
    
            # Aggiungi i valori di nome e codice all'elenco dei valori da passare a execute
            update_values.extend([nome_prodotto, codice_prodotto])
    
            # Esegui la query di aggiornamento
            cursor.execute(update_query, tuple(update_values))

            # Ottieni la data e l'ora corrente
            data_ora_notifica = datetime.now().strftime("%d/%m/%Y %H:%M")
            id_notifica = str(uuid.uuid4())

            # Registazione Notifica se modifico NOME
            if update_query == "UPDATE prodotti SET nomeProdotto = %s WHERE nomeProdotto = %s AND codiceProdotto = %s":
               messaggio_notifica = f"{nome_prodotto} | {codice_prodotto}  -  Nome modificato in: {newNome_prodotto}"
               insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
               notification_data = (id_notifica, messaggio_notifica, data_ora_notifica)
               cursor.execute(insert_notification_query, notification_data)
            
            # Registazione Notifica se modifico CODICE
            elif update_query == "UPDATE prodotti SET codiceProdotto = %s WHERE nomeProdotto = %s AND codiceProdotto = %s":
               messaggio_notifica = f"{nome_prodotto} | {codice_prodotto}  -  Codice modificato in: {newCodice_prodotto}"
               insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
               notification_data = (id_notifica, messaggio_notifica, data_ora_notifica)
               cursor.execute(insert_notification_query, notification_data)
            
            # Registazione Notifica se modifico PREZZO
            elif update_query == "UPDATE prodotti SET prezzoProdotto = %s WHERE nomeProdotto = %s AND codiceProdotto = %s":
               messaggio_notifica = f"{nome_prodotto} | {codice_prodotto}  -  Prezzo modificato in: {prezzo_da_modificare}€"
               insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
               notification_data = (id_notifica, messaggio_notifica, data_ora_notifica)
               cursor.execute(insert_notification_query, notification_data)
            
            # Registazione Notifica se modifico NOME e CODICE
            elif update_query == "UPDATE prodotti SET nomeProdotto = %s, codiceProdotto = %s WHERE nomeProdotto = %s AND codiceProdotto = %s":
               messaggio_notifica = f"{nome_prodotto} | {codice_prodotto}  -  Nome e Codice modificato in: {newNome_prodotto} | {newCodice_prodotto}"
               insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
               notification_data = (id_notifica, messaggio_notifica, data_ora_notifica)
               cursor.execute(insert_notification_query, notification_data)   
            
            # Registazione Notifica se modifico NOME e PREZZO
            elif update_query == "UPDATE prodotti SET nomeProdotto = %s, prezzoProdotto = %s WHERE nomeProdotto = %s AND codiceProdotto = %s":
               messaggio_notifica = f"{nome_prodotto} | {codice_prodotto}  -  Nome e Prezzo modificato in: {newNome_prodotto} | {prezzo_da_modificare}€"
               insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
               notification_data = (id_notifica, messaggio_notifica, data_ora_notifica)
               cursor.execute(insert_notification_query, notification_data)   

            # Registazione Notifica se modifico CODICE e PREZZO
            elif update_query == "UPDATE prodotti SET codiceProdotto = %s, prezzoProdotto = %s WHERE nomeProdotto = %s AND codiceProdotto = %s":
               messaggio_notifica = f"{nome_prodotto} | {codice_prodotto}  -  Codice e Prezzo modificato in: {newCodice_prodotto} | {prezzo_da_modificare}€"
               insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
               notification_data = (id_notifica, messaggio_notifica, data_ora_notifica)
               cursor.execute(insert_notification_query, notification_data)      

            
            db.commit()
            db.close()
    
            # Aggiorna la lista dei prodotti nella Listbox (questa parte dovresti implementarla)
            self.update_product_listbox()

            # Aggiorna la lista dei prodotti nella pagina di eliminazione
            self.controller.frames[EliminaProdotto].update_product_listbox()

            messagebox.showinfo("Successo", f"Prodotto con nome '{nome_prodotto}' e codice '{codice_prodotto}' modificato con successo.")
        

            # Alla fine della funzione, svuota i campi di input
            self.nome_entry.delete(0, END)
            self.codice_entry.delete(0, END)
            self.newNome_entry.delete(0, END)
            self.newCodice_entry.delete(0, END)
            self.prezzo_entry.delete(0, END)

        else:
            messagebox.showerror("Errore", f"Prodotto con nome '{nome_prodotto}' e codice '{codice_prodotto}' non trovato nel database.")



#############################################################################################################################################


# Crea la classe EliminaProdotto
class EliminaProdotto(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        text_font = ("Trebuchet MS", 14) 
        button_font = ("Trebuchet MS", 13) 

        label = Label(self, font=title_font, text="ELIMINA QUANTITà")
        label.pack(padx=10, pady=(30,20))

        # Aggiungi la lista dei prodotti
        self.product_listbox = Listbox(self, font=text_font, height=15, width=30)
        self.product_listbox.pack(pady=10)

        # Campi di input per il nome, il codice e la quantità da eliminare
        nome_label = Label(self, font=text_font, text="Nome del Prodotto:")
        nome_label.pack(pady=(40,0))
        self.nome_entry = Entry(self)
        self.nome_entry.pack(ipadx=80, ipady=5)

        codice_label = Label(self, font=text_font, text="Codice del Prodotto:")
        codice_label.pack(pady=(10,0))
        self.codice_entry = Entry(self)
        self.codice_entry.pack(ipadx=80, ipady=5)

        quantita_label = Label(self, font=text_font, text="Quantità da Eliminare:")
        quantita_label.pack(pady=(10,0))
        self.quantita_entry = Entry(self)
        self.quantita_entry.pack(ipadx=80, ipady=5)

        # Pulsante per eseguire l'eliminazione
        elimina_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Elimina", command=self.delete_product)
        elimina_button.pack(ipady=10, pady=(100,0))

        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(ipady=10, pady=10)

        # Chiamare la funzione per aggiornare la lista dei prodotti quando la pagina viene aperta
        self.update_product_listbox()



    def goBack(self):
        self.controller.show_frame(GestionaleProdotti)

 
    def update_product_listbox(self):
    # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Seleziona tutti i prodotti dalla tabella prodotti
        select_all_query = "SELECT nomeProdotto, codiceProdotto, quantitàProdotto FROM prodotti"
        cursor.execute(select_all_query)
        products = cursor.fetchall()

        # Svuota la Listbox
        self.product_listbox.delete(0, END)

        # Aggiungi i prodotti alla Listbox
        for product in products:
            nome_prodotto = product[0]
            codice_prodotto = product[1]
            quantita_prodotto = product[2]
            self.product_listbox.insert(END, f"Nome: {nome_prodotto}")
            self.product_listbox.insert(END, f"Codice: {codice_prodotto}")
            self.product_listbox.insert(END, f"Qtà: {quantita_prodotto}")
            self.product_listbox.insert(END, f"")

        # Chiudi la connessione al database
        db.close()



    def delete_product(self):
        # Recupera i dati inseriti dall'utente
        nome_prodotto = self.nome_entry.get()
        codice_prodotto = self.codice_entry.get()
        quantita_da_eliminare = self.quantita_entry.get()

        # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Cerca il prodotto nel database
        select_query = "SELECT * FROM prodotti WHERE nomeProdotto = %s AND codiceProdotto = %s"
        cursor.execute(select_query, (nome_prodotto, codice_prodotto))
        existing_product = cursor.fetchone()

        if existing_product:
           # Calcola la nuova quantità dopo l'eliminazione
           quantita_attuale = existing_product[3]
           nuova_quantita = max(quantita_attuale - int(quantita_da_eliminare), 0)

           # Esegui un'operazione di aggiornamento nel database per impostare la quantità al nuovo valore
           update_query = "UPDATE prodotti SET quantitàProdotto = %s WHERE nomeProdotto = %s AND codiceProdotto = %s"
           cursor.execute(update_query, (nuova_quantita, nome_prodotto, codice_prodotto))

           # Inserisci un record nella tabella notifiche

           # Ottieni la data e l'ora corrente
           data_ora_notifica = datetime.now().strftime("%d/%m/%Y %H:%M")

           # Crea un ID notifica casuale
           id_notifica_2 = str(uuid.uuid4())

           # Crea messaggio
           messaggio_notifica_2 = f"Prodotto: '{nome_prodotto}' Qnt eliminata: '{quantita_da_eliminare}' Nuova qnt: '{nuova_quantita}'"

           insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
           notification_data_2 = (id_notifica_2, messaggio_notifica_2, data_ora_notifica)
           cursor.execute(insert_notification_query, notification_data_2)



           # Se la quantità rimanente è inferiore a 5, crea una seconda notifica
           if nuova_quantita < 5:
               
               id_notifica = str(uuid.uuid4())
               nome_prodotto = existing_product[1]  # Ottieni il nome del prodotto
               messaggio_notifica = f"Qnt '{nome_prodotto}' inferiore a 5"
               insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
               notification_data = (id_notifica, messaggio_notifica, data_ora_notifica)
               cursor.execute(insert_notification_query, notification_data)

           # Esegui il commit delle modifiche al database
           db.commit()

           # Chiudi la connessione al database
           db.close()

           # Aggiorna la lista dei prodotti nella Listbox
           self.update_product_listbox()

           # Aggiorna la lista dei prodotti nella pagina di modifica
           self.controller.frames[ModificaProdotto].update_product_listbox()

           messagebox.showinfo("Successo", f"Quantità di '{nome_prodotto}' eliminata con successo.")

           # Alla fine della funzione, svuota i campi di input
           self.nome_entry.delete(0, END)
           self.codice_entry.delete(0, END)
           self.quantita_entry.delete(0, END)
           
        else:
           messagebox.showerror("Errore", f"Prodotto con nome '{nome_prodotto}' e codice '{codice_prodotto}' non trovato nel database.")





#############################################################################################################################################

class AggiungiProdotto(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller  # Conserva il riferimento al controller

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        text_font = ("Trebuchet MS", 14) 
        button_font = ("Trebuchet MS", 13) 

        label = Label(self, font=title_font, text="CREA / AGGIUNGI")
        label.pack(padx=10, pady=(30,0))

        # Aggiungi la lista dei prodotti
        self.product_listbox = Listbox(self, font=text_font, height=15, width=30)
        self.product_listbox.pack(pady=10)

        # Campi di input per il nuovo prodotto
        nome_label = Label(self, font=text_font, text="Nome del Prodotto:")
        nome_label.pack(pady=(30,0))
        self.nome_entry = Entry(self)
        self.nome_entry.pack(ipadx=80, ipady=5)

        codice_label = Label(self, font=text_font, text="Codice del Prodotto:")
        codice_label.pack(pady=(10,0))
        self.codice_entry = Entry(self)
        self.codice_entry.pack(ipadx=80, ipady=5)

        quantita_label = Label(self, font=text_font, text="Quantità del Prodotto:")
        quantita_label.pack(pady=(10,0))
        self.quantita_entry = Entry(self)
        self.quantita_entry.pack(ipadx=80, ipady=5)

        prezzo_label = Label(self, font=text_font, text="Prezzo per Unità:")
        prezzo_label.pack(pady=(10,0))
        self.prezzo_entry = Entry(self)
        self.prezzo_entry.pack(ipadx=80, ipady=5)

       
        # Pulsante per confermare l'aggiunta del prodotto
        conferma_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Conferma", command=self.add_product)
        conferma_button.pack(ipady=10, pady=(60,0))

        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(ipady=10, pady=10)

        # Chiamare la funzione per aggiornare la lista dei prodotti quando la pagina viene aperta
        self.update_product_listbox()

        

    def goBack(self):
        self.controller.show_frame(GestionaleProdotti)


    def update_product_listbox(self):
    # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Seleziona tutti i prodotti dalla tabella prodotti
        select_all_query = "SELECT nomeProdotto, codiceProdotto, quantitàProdotto, prezzoProdotto FROM prodotti"
        cursor.execute(select_all_query)
        products = cursor.fetchall()

        # Svuota la Listbox
        self.product_listbox.delete(0, END)

        # Aggiungi i prodotti alla Listbox
        for product in products:
            nome_prodotto = product[0]
            codice_prodotto = product[1]
            quantita_prodotto = product[2]
            prezzo_prodotto = product[3]

            self.product_listbox.insert(END, f"Nome: {nome_prodotto}")
            self.product_listbox.insert(END, f"Codice: {codice_prodotto}")
            self.product_listbox.insert(END, f"Prezzo: {prezzo_prodotto}€")
            self.product_listbox.insert(END, f"Qtà: {quantita_prodotto}")
            self.product_listbox.insert(END, f"")

        # Chiudi la connessione al database
        db.close()

    

    def add_product(self):
        # Recupera i dati dal form
        nome_prodotto = self.nome_entry.get()
        codice_prodotto = self.codice_entry.get()
        quantita_prodotto = self.quantita_entry.get()
        prezzo_prodotto = self.prezzo_entry.get()

        # Creare una connessione al database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Ottieni la data e l'ora corrente
        data_ora_notifica = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Cerca se esiste già un prodotto con lo stesso nome e codice
        select_query = "SELECT * FROM prodotti WHERE nomeProdotto = %s AND codiceProdotto = %s"
        product_data = (nome_prodotto, codice_prodotto)

        cursor.execute(select_query, product_data)
        existing_product = cursor.fetchone()

        if existing_product:
            # Se il prodotto esiste già, aggiorna la quantità
            existing_id = existing_product[0]
            existing_quantita = existing_product[3]

            # Assicurati che quantita_prodotto sia un numero intero
            try:
                quantita_prodotto = int(quantita_prodotto)
            except ValueError:
                quantita_prodotto = 0
            
            new_quantita = existing_quantita + quantita_prodotto

            # Esegui una query di aggiornamento della quantità
            update_query = "UPDATE prodotti SET quantitàProdotto = %s WHERE IDprodotto = %s"
            updated_data = (new_quantita, existing_id)
            cursor.execute(update_query, updated_data)

            # Inserisci un record nella tabella notifiche

            # Crea un ID notifica casuale
            id_notifica_2 = str(uuid.uuid4())

            # Crea messaggio
            messaggio_notifica_2 = f"Prodotto: '{nome_prodotto}' Qnt aggiunta: '{quantita_prodotto}'\n Nuova qnt: '{new_quantita}'"

            insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
            notification_data_2 = (id_notifica_2, messaggio_notifica_2, data_ora_notifica)
            cursor.execute(insert_notification_query, notification_data_2)


        else:
            # Se il prodotto non esiste, crea un nuovo prodotto con un nuovo ID
            id_prodotto = str(uuid.uuid4())
            insert_query = "INSERT INTO prodotti (IDprodotto, nomeProdotto, codiceProdotto, quantitàProdotto, prezzoProdotto) VALUES (%s, %s, %s, %s, %s)"
            product_data = (id_prodotto, nome_prodotto, codice_prodotto, quantita_prodotto, prezzo_prodotto)
            cursor.execute(insert_query, product_data)

            # Inserisci un record nella tabella notifiche

            # Crea un ID notifica casuale
            id_notifica = str(uuid.uuid4())

            # Crea messaggio
            messaggio_notifica = f"Nuovo Prodotto: '{nome_prodotto}' Codice: '{codice_prodotto}'"

            insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
            notification_data = (id_notifica, messaggio_notifica, data_ora_notifica)
            cursor.execute(insert_notification_query, notification_data)

        # Esegui il commit delle modifiche al database
        db.commit()

        # Chiudere la connessione al database
        db.close()

        # Aggiorna la lista dei prodotti nella pagina di eliminazione e di modifica
        self.controller.frames[EliminaProdotto].update_product_listbox()
        self.controller.frames[ModificaProdotto].update_product_listbox()

        # Visualizza un messaggio di successo
        messagebox.showinfo("Successo", "Prodotto aggiunto/aggiornato con successo al database.")

        # Torna alla pagina "GestionaleProdotti"
        self.controller.show_frame(GestionaleProdotti)

    


#############################################################################################################################################


class GestionaleProdotti(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller  # Conserva il riferimento al controller

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        button_font = ("Trebuchet MS", 13) 

        label = Label(self, font=title_font, text="PRODOTTI")
        label.pack(padx=10, pady=50)

        # Aggiungi il pulsante "Aggiungi Prodotto" che apre la pagina "Aggiungi Prodotto"
        add_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Aggiungi Prodotto", command=lambda: controller.show_frame(AggiungiProdotto))
        add_button.pack(pady=(100,0),ipady=10)

        # Aggiungi il pulsante "Elimina Prodotti" che apre la pagina "Elimina Prodotto"
        delete_products_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Elimina Prodotti", command=lambda: controller.show_frame(EliminaProdotto))
        delete_products_button.pack(pady=50,ipady=10)

        # Aggiungi il pulsante "Elimina Prodotti" che apre la pagina "Elimina Prodotto"
        mod_products_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Modifica Prodotti", command=lambda: controller.show_frame(ModificaProdotto))
        mod_products_button.pack(ipady=10)

        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(pady=50,ipady=10)

        

    def goBack(self):
        self.controller.show_frame(Gestionale)

        


#############################################################################################################################################


class OrdiniLavorati(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller  # Conserva il riferimento al controller

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        text_font = ("Trebuchet MS", 14) 
        button_font = ("Trebuchet MS", 13) 

        label = Label(self, font=title_font, text="ORDINI LAVORATI")
        label.pack(padx=10, pady=50)

        self.order_listbox = Listbox(self, font=text_font, height=20, width=80)
        self.order_listbox.pack()


        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(pady=(100,0),ipady=10)

        # Chiamare la funzione per aggiornare la lista degli ordini quando la pagina viene aperta
        self.update_orderWork_listbox()

        

    def goBack(self):
        self.controller.show_frame(Ordini)


    def update_orderWork_listbox(self):
        # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Seleziona tutti gli ordini dalla tabella ordini, ordinati per data e ora decrescenti
        select_all_query = "SELECT IdprodottoOrdineLavorato, quantitàOrdineLavorato, codiceSpedizioneOrdineLavorato, ordineLavoratoDataOra, ordineLavoratoCompletato, ordineLavoratoUsername FROM ordinilavorati ORDER BY ordineLavoratoCompletato DESC"
        cursor.execute(select_all_query)
        orders = cursor.fetchall()

        # Svuota la Listbox
        self.order_listbox.delete(0, END)

        for order in orders:
            nome_prodotto_ordine_lavorato = order[0]
            qnt_ordine_lavorato = order[1]
            codice_spedizione_lavorato = order[2]
            data_ora_ordine_lavorato = order[3]
            data_ora_ordine_completato = order[4]
            ordine_cliente_username = order[5]
        
            
            self.order_listbox.insert(END, f"Data e Ora completamento ordine: {data_ora_ordine_completato}")
            self.order_listbox.insert(END, f"Data e Ora ricezione ordine: {data_ora_ordine_lavorato}")
            self.order_listbox.insert(END, f"Username Cliente: {ordine_cliente_username}")
            self.order_listbox.insert(END, f"Nome: {nome_prodotto_ordine_lavorato}")
            self.order_listbox.insert(END, f"Qnt: {qnt_ordine_lavorato}")
            self.order_listbox.insert(END, f"Codice Spedizione: {codice_spedizione_lavorato}")  
            self.order_listbox.insert(END, "")

        # Chiudi la connessione al database
        db.close()



#############################################################################################################################################




class NuoviOrdini(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller  # Conserva il riferimento al controller

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        text_font = ("Trebuchet MS", 14) 
        button_font = ("Trebuchet MS", 13) 

        label = Label(self, font=title_font, text="NUOVI ORDINI")
        label.pack(padx=10, pady=(50,20))

        label = Label(self, font=text_font, text="Seleziona il codice spedizione da lavorare")
        label.pack(padx=10, pady=(0,20))

        self.order_listbox = Listbox(self, font=text_font, height=20, width=80)
        self.order_listbox.pack()

        # Pulsante per spostare l'ordine a "Ordini Lavorati"
        move_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Sposta a Ordini Lavorati", command=self.move_order_to_processed)
        move_button.pack(pady=20, ipady=10)

        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(pady=(0,20), ipady=10)

        # Chiamare la funzione per aggiornare la lista degli ordini quando la pagina viene aperta
        self.update_order_listbox()

    def goBack(self):
        self.controller.show_frame(Ordini)

    def update_order_listbox(self):
        # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Seleziona tutti gli ordini dalla tabella ordini, ordinati per data e ora decrescenti
        select_all_query = "SELECT IDordini, IdprodottoOrdine, quantitàOrdine, codiceSpedizioneOrdine, ordineDataOra, usernameClienteOrdine FROM ordini ORDER BY ordineDataOra DESC"
        cursor.execute(select_all_query)
        orders = cursor.fetchall()

        # Svuota la Listbox
        self.order_listbox.delete(0, END)

        for order in orders:
            id_ordine = order[0]
            nome_prodotto_ordine = order[1]
            qnt_ordine = order[2]
            codice_spedizione = order[3]
            data_ora_ordine = order[4]
            username_cliente_ordine = order[5]
        
            self.order_listbox.insert(END, f"Codice Spedizione: {codice_spedizione}")  # Mostra il codice spedizione
            self.order_listbox.insert(END, f"Data e Ora: {data_ora_ordine}")
            self.order_listbox.insert(END, f"Username Cliente: {username_cliente_ordine}")
            self.order_listbox.insert(END, f"Nome: {nome_prodotto_ordine}")
            self.order_listbox.insert(END, f"Qnt: {qnt_ordine}")
            self.order_listbox.insert(END, "")

        # Chiudi la connessione al database
        db.close()

    def move_order_to_processed(self):
        selected_index = self.order_listbox.curselection()
      
        if selected_index:
            selected_text = self.order_listbox.get(selected_index[0])
      
            if selected_text.startswith("Codice Spedizione"):
                selected_codice_spedizione = selected_text.split(": ")[1]
      
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="MagazzinoPython",
                    database="magazzinopython"
                )
      
                cursor = db.cursor()
      
                try:
                    # Recupera i dettagli dell'ordine dalla tabella ordini basandoti sul codice spedizione
                    select_order_query = "SELECT * FROM ordini WHERE codiceSpedizioneOrdine = %s"
                    cursor.execute(select_order_query, (selected_codice_spedizione,))
                    order_data = cursor.fetchone()
      
                    if order_data:

                        # Elimina l'ordine dalla tabella ordini
                        delete_order_query = "DELETE FROM ordini WHERE codiceSpedizioneOrdine = %s"
                        cursor.execute(delete_order_query, (selected_codice_spedizione,))

                        # Ottieni la data e l'ora corrente
                        data_ora_notifica = datetime.now().strftime("%d/%m/%Y %H:%M")
      
                        # Aggiungi l'ordine alla tabella ordinilavorati
                        id_ordine_lavorato = str(uuid.uuid4())
                        insert_processed_order_query = "INSERT INTO ordinilavorati (IDordiniLavorati, IdprodottoOrdineLavorato, quantitàOrdineLavorato, codiceSpedizioneOrdineLavorato, ordineLavoratoDataOra, ordineLavoratoCompletato, ordineLavoratoUsername) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        processed_order_data = (id_ordine_lavorato, order_data[1], order_data[2], order_data[3], order_data[4], data_ora_notifica, order_data[5])
                        cursor.execute(insert_processed_order_query, processed_order_data)
      
                        db.commit()
                        self.update_order_listbox()
                        # Aggiorna la lista dei prodotti nella pagina di eliminazione
                        self.controller.frames[OrdiniLavorati].update_orderWork_listbox()
                        messagebox.showinfo("Successo", "Ordine spostato a Ordini Lavorati con successo.")
                    else:
                        messagebox.showerror("Errore", "Ordine non trovato.")
                except Exception as e:
                    messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")
                finally:
                    db.close()
            else:
                messagebox.showerror("Errore", "Seleziona un ordine da spostare.")


  

#############################################################################################################################################

class Ordini(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller  # Conserva il riferimento al controller

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        button_font = ("Trebuchet MS", 13) 

        label = Label(self, font=title_font, text="ORDINI")
        label.pack(padx=10, pady=50)

        # Pulsante per la Gestione Nuovi Ordini
        product_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Nuovi Ordini", command=lambda: controller.show_frame(NuoviOrdini))
        product_button.pack(pady=(100,0),ipady=10)

        # Pulsante per la Gestione Ordini Lavorati
        product_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Ordini Lavorati", command=lambda: controller.show_frame(OrdiniLavorati))
        product_button.pack(pady=50,ipady=10)


        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(ipady=10)

        

    def goBack(self):
        self.controller.show_frame(Gestionale)


#############################################################################################################################################

class Notifiche(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller # Conserva il riferimento al controller

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        text_font = ("Trebuchet MS", 14) 
        button_font = ("Trebuchet MS", 13) 


        label = Label(self, font=title_font, text="NOTIFICHE EVENTI")
        label.pack(padx=10, pady=50)


        # Aggiungi una Listbox per mostrare i prodotti con bassa quantità
        self.notification_listbox = Listbox(self, font=text_font, height=20, width=80)
        self.notification_listbox.pack()
        

        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(pady=(100,0),ipady=10)

        self.update_notification_listbox()

        

    def goBack(self):
        self.controller.show_frame(Gestionale)


    def update_notification_listbox(self):
        # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )
    
        cursor = db.cursor()
    
        select_all_query = "SELECT messaggioNotifica, dataOraNotifica FROM notifiche ORDER BY dataOraNotifica DESC"
        cursor.execute(select_all_query)
        notifications = cursor.fetchall()
    
        # Svuota la Listbox
        self.notification_listbox.delete(0, END)
    
        # Aggiungi i prodotti con bassa quantità alla Listbox
        for notification in notifications:
            messaggio_notifica = notification[0]
            data_ora = notification[1]
            self.notification_listbox.insert(END, data_ora)
            self.notification_listbox.insert(END, messaggio_notifica)
            self.notification_listbox.insert(END, "")
    
        # Chiudi la connessione al database
        db.close()



#############################################################################################################################################

class Gestionale(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        button_font = ("Trebuchet MS", 13) 

        label = Label(self, font=title_font, text="GESTIONALE")
        label.pack(padx=10, pady=50)

        # Pulsante per la Gestione Prodotti
        product_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Gestione Prodotti", command=lambda: controller.show_frame(GestionaleProdotti))
        product_button.pack(pady=(100,0),ipady=10)

        # Pulsante per la Gestione Ordini
        product_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Gestione Ordini", command=lambda: controller.show_frame(Ordini))
        product_button.pack(pady=50,ipady=10)

        # Pulsante per la Gestione Notifiche
        product_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Notifiche Eventi", command=lambda: controller.show_frame(Notifiche))
        product_button.pack(ipady=10)



#############################################################################################################################################


class ClienteNuovoOrdine(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller # Conserva il riferimento al controller


        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        text_font = ("Trebuchet MS", 14) 
        button_font = ("Trebuchet MS", 13) 
        
        self.username_label = Label(self, font=title_font,  text="Effettua un nuovo ordine")
        self.username_label.pack(padx=10, pady=50)


        self.product_listbox = Listbox(self, font=text_font, height=15, width=30)
        self.product_listbox.pack(pady=10)

        nome_label = Label(self, font=text_font, text="Nome del Prodotto:")
        nome_label.pack(pady=(30,0))
        self.nome_entry = Entry(self)
        self.nome_entry.pack(ipadx=80, ipady=5)

        quantita_label = Label(self, font=text_font,  text="Quantità del Prodotto:")
        quantita_label.pack(pady=(10,0))
        self.quantita_entry = Entry(self)
        self.quantita_entry.pack(ipadx=80, ipady=5)
        
        # Pulsante per confermare l'aggiunta del prodotto
        conferma_button = Button(self, width=30, font=button_font, bg="blue", fg="white", text="Conferma Ordine", command=self.new_order_wrapper)
        conferma_button.pack(ipady=10, pady=(60,0))

        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(ipady=10, pady=10)

        # Chiamare la funzione per aggiornare la lista dei prodotti quando la pagina viene aperta
        self.update_product_listbox()

        

    def goBack(self):
        self.controller.show_frame(GestionaleClienti)

    def set_username(self, username):
        self.username = username  # Memorizza l'username nella classe  
        self.username_label.config(text=f"Effettua un nuovo ordine {self.username}!") 

    def new_order_wrapper(self):
        username = self.username  # Ottieni l'username dalla classe
        self.new_order(username)


    
    def update_product_listbox(self):
    # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Seleziona tutti i prodotti dalla tabella prodotti
        select_all_query = "SELECT nomeProdotto, prezzoProdotto FROM prodotti"
        cursor.execute(select_all_query)
        products = cursor.fetchall()

        # Svuota la Listbox
        self.product_listbox.delete(0, END)

        # Aggiungi i prodotti alla Listbox
        for product in products:
            nome_prodotto = product[0]
            prezzo_prodotto = product[1]
            self.product_listbox.insert(END, f"Nome: {nome_prodotto}")
            self.product_listbox.insert(END, f"Prezzo: {prezzo_prodotto}€")
            self.product_listbox.insert(END, f"")

        # Chiudi la connessione al database
        db.close()



    def new_order(self, username):
        
        self.username = username  # Memorizza l'username nella classe  
        
        # Recupera i dati dal form
        nome_ordine = self.nome_entry.get()
        quantita_ordine = self.quantita_entry.get()

        # Creare una connessione al database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        try:
            # Cerca il prodotto nel database
            select_query = "SELECT * FROM prodotti WHERE nomeProdotto = %s"
            cursor.execute(select_query, (nome_ordine,))
            existing_product = cursor.fetchone()

            if existing_product:
                # Verifica se la quantità richiesta è disponibile
                quantita_attuale = existing_product[3]
                if int(quantita_ordine) <= quantita_attuale:
                    # Crea un ID notifica casuale
                    id_notifica = str(uuid.uuid4())

                    # Ottieni la data e l'ora corrente
                    data_ora = datetime.now().strftime("%d/%m/%Y %H:%M")

                    # Aggiungi il nuovo ordine nella tabella ordini
                    
                    codice_spedizione = str(uuid.uuid4())
                    username_cliente = self.username
                    id_ordine = str(uuid.uuid4())
                    insert_query = "INSERT INTO ordini (IDordini, IdprodottoOrdine, quantitàOrdine, codiceSpedizioneOrdine, ordineDataOra, usernameClienteOrdine) VALUES (%s, %s, %s, %s, %s, %s)"
                    ordine_data = (id_ordine, nome_ordine, quantita_ordine, codice_spedizione, data_ora, username_cliente)
                    cursor.execute(insert_query, ordine_data)

                    # Calcola la nuova quantità dopo l'eliminazione
                    nuova_quantita = quantita_attuale - int(quantita_ordine)

                    # Esegui un'operazione di aggiornamento nel database per impostare la quantità al nuovo valore
                    update_query = "UPDATE prodotti SET quantitàProdotto = %s WHERE nomeProdotto = %s"
                    cursor.execute(update_query, (nuova_quantita, nome_ordine))

                    # Inserisci un record nella tabella notifiche

                    # Crea messaggio
                    messaggio_notifica = f"Nuovo ordine! Codice spedizione: '{codice_spedizione}'"

                    insert_notification_query = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
                    notification_data = (id_notifica, messaggio_notifica, data_ora)
                    cursor.execute(insert_notification_query, notification_data)

                    # Se la quantità rimanente è inferiore a 5, crea una seconda notifica
                    if nuova_quantita < 5:
                        id_notifica_2 = str(uuid.uuid4())
                        nome_prodotto = existing_product[1]  # Ottieni il nome del prodotto
                        messaggio_notifica_2 = f"Qnt '{nome_prodotto}' inferiore a 5"
                        insert_notification_query_2 = "INSERT INTO notifiche (IDnotifiche, messaggioNotifica, dataOraNotifica) VALUES (%s, %s, %s)"
                        notification_data_2 = (id_notifica_2, messaggio_notifica_2, data_ora)
                        cursor.execute(insert_notification_query_2, notification_data_2)


                    # Esegui il commit delle modifiche al database
                    db.commit()

                    # Aggiorna la lista dei prodotti nella pagina di modifica
                    self.controller.frames[ClienteOrdiniEffettuati].update_order_listbox(username)
                    self.controller.frames[NuoviOrdini].update_order_listbox()

                    # Alla fine della funzione, svuota i campi di input
                    self.nome_entry.delete(0, END)
                    self.quantita_entry.delete(0, END)

                    # Visualizza un messaggio di successo
                    messagebox.showinfo("Successo", "Prodotto aggiunto/aggiornato con successo al database.")
                else:
                    # Se la quantità non è disponibile, mostra un messaggio di errore
                    messagebox.showerror("Errore", "Quantità non disponibile")

            else:
                # Se il prodotto non esiste, mostra un messaggio di errore
                messagebox.showerror("Errore", f"Il prodotto '{nome_ordine}' non esiste nel database.")

        except Exception as e:
            # Gestisci eventuali errori del database
            messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")

        finally:
            # Chiudere la connessione al database
            db.close()




#############################################################################################################################################


class ClienteOrdiniEffettuati(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller # Conserva il riferimento al controller

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        text_font = ("Trebuchet MS", 14) 
        button_font = ("Trebuchet MS", 13) 


        self.username_label = Label(self, font=title_font, text="Visualizza i tuoi ordini effettuati")
        self.username_label.pack(padx=10, pady=50)


        self.order_listbox = Listbox(self, font=text_font, height=20, width=80)
        self.order_listbox.pack()

 
        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(pady=(100,0),ipady=10)

        

    def set_username(self, username):
        self.username = username  # Memorizza l'username nella classe  
        self.username_label.config(text=f"Visualizza i tuoi ordini effettuati {self.username}!")
        self.update_order_listbox(username)  # Chiama la funzione con l'username


    def goBack(self):
        self.controller.show_frame(GestionaleClienti)        

    
    def update_order_listbox(self, username=None, **kwargs):

        self.username = username  # Memorizza l'username nella classe  
        
        # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Seleziona tutti i prodotti dalla tabella prodotti
        select_all_query = "SELECT IDprodottoOrdine, quantitàOrdine, codiceSpedizioneOrdine, ordineDataOra FROM ordini WHERE usernameClienteOrdine = %s ORDER BY ordineDataOra DESC"
        cursor.execute(select_all_query, (username,))

        orders = cursor.fetchall()

        # Svuota la Listbox
        self.order_listbox.delete(0, END)

        # Aggiungi i prodotti alla Listbox
        for order in orders:
            nome_prodotto_ordine = order[0]
            qnt_ordine = order[1]
            codice_spedizione = order[2]
            data_ora_ordine = order[3]
            self.order_listbox.insert(END, data_ora_ordine)
            self.order_listbox.insert(END, f"Nome: {nome_prodotto_ordine}")
            self.order_listbox.insert(END, f"Qnt: {qnt_ordine}")
            self.order_listbox.insert(END, f"Codice Spedizione:")
            self.order_listbox.insert(END, codice_spedizione)
            self.order_listbox.insert(END, f"")

        # Chiudi la connessione al database
        db.close()





#############################################################################################################################################


class ClienteOrdiniLavorati(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller  # Conserva il riferimento al controller

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        text_font = ("Trebuchet MS", 14) 
        button_font = ("Trebuchet MS", 13) 


        self.username_label = Label(self, font=title_font, text="Visualizza i tuoi ordini lavorati")
        self.username_label.pack(padx=10, pady=50)


        self.order_listbox = Listbox(self, font=text_font, height=20, width=80)
        self.order_listbox.pack()


        # Pulsante per tornare indietro
        back_button = Button(self, width=30, font=button_font, bg="grey", fg="white", text="Indietro", command=lambda: self.goBack())
        back_button.pack(pady=(100,0),ipady=10)

        

    def goBack(self):
        self.controller.show_frame(GestionaleClienti)


    def set_username(self, username):
        self.username = username  # Memorizza l'username nella classe  
        self.username_label.config(text=f"Visualizza i tuoi ordini lavorati {self.username}!")
        self.update_order_listbox(username)  


    def update_order_listbox(self, username=None, **kwargs):

        self.username = username  # Memorizza l'username nella classe  
        
        # Connessione al database MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Seleziona tutti i prodotti dalla tabella prodotti
        select_all_query = "SELECT IDprodottoOrdineLavorato, quantitàOrdineLavorato, codiceSpedizioneOrdineLavorato, ordineLavoratoDataOra, ordineLavoratoCompletato FROM ordinilavorati WHERE ordineLavoratoUsername = %s ORDER BY ordineLavoratoCompletato DESC"
        cursor.execute(select_all_query, (username,))

        orders = cursor.fetchall()

        # Svuota la Listbox
        self.order_listbox.delete(0, END)

        # Aggiungi i prodotti alla Listbox
        for order in orders:
            nome_prodotto_ordine_lavorato = order[0]
            qnt_ordine_lavorato = order[1]
            codice_spedizione_lavorato = order[2]
            data_ora_ordine_lavorato = order[3]
            data_ora_ordine_completato = order[4]

            self.order_listbox.insert(END,f"Ordine completato il: {data_ora_ordine_completato}")
            self.order_listbox.insert(END,f"Ordine effettuato il: {data_ora_ordine_lavorato}")
            self.order_listbox.insert(END, f"Nome: {nome_prodotto_ordine_lavorato}")
            self.order_listbox.insert(END, f"Qnt: {qnt_ordine_lavorato}")
            self.order_listbox.insert(END, f"Codice Spedizione:")
            self.order_listbox.insert(END, codice_spedizione_lavorato)
            self.order_listbox.insert(END, f"")

        # Chiudi la connessione al database
        db.close()      



#############################################################################################################################################


class GestionaleClienti(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)


        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        button_font = ("Trebuchet MS", 13) 


        self.username_label = Label(self,font=title_font, text="Benvenuto")
        self.username_label.pack(padx=10, pady=50)

       
        # Pulsante per la Gestione Ordini
        product_button = Button(self, width=30, font=button_font, text="Crea Nuovo Ordine", bg="blue", fg="white", command=lambda: controller.show_frame(ClienteNuovoOrdine))
        product_button.pack(pady=(100,0),ipady=10)

        # Pulsante per la Gestione Ordini
        product_button = Button(self, width=30, font=button_font, text="Visualizza Nuovi Ordini", bg="blue", fg="white", command=lambda: controller.show_frame(ClienteOrdiniEffettuati))
        product_button.pack(pady=50,ipady=10)

        # Pulsante per la Gestione Ordini
        product_button = Button(self, width=30, font=button_font, text="Visualizza Ordini Lavorati", bg="blue", fg="white", command=lambda: controller.show_frame(ClienteOrdiniLavorati))
        product_button.pack(ipady=10)


    def set_username(self, username):
        self.username = username  # Memorizza l'username nella classe  
        self.username_label.config(text=f"Benvenuto {self.username}")



#############################################################################################################################################


class Utenti(Frame):
    def __init__(self, parent, app):
        Frame.__init__(self, parent)
        self.app = app  # Conserva il riferimento all'istanza di App

        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        button_font = ("Trebuchet MS", 13) 
        text_font = ("Trebuchet MS", 14) 



        label = Label(self, text="UTENTI",font=title_font)
        label.pack(padx=10, pady=50)

        # Campi di input per username e password
        username_label = Label(self, font=text_font, text="Username:")
        username_label.pack()
        username_entry = Entry(self)
        username_entry.pack(ipadx=80, ipady=5, pady=(6,0))

        password_label = Label(self, font=text_font, text="Password:")
        password_label.pack(pady=(20,0))
        password_entry = Entry(self, show="*")  # Mostra asterischi per la password
        password_entry.pack(ipadx=80, ipady=5, pady=(6,0))

        # Pulsante di login
        login_button = Button(self, width=30, font=button_font, text="Login", bg="blue", fg="white", command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.pack(pady=(50,15),ipady=10)

        # Pulsante di registrazione
        user_register_button = Button(self, width=30, font=button_font, text="Registra", bg="blue", fg="white", command=lambda: self.register(username_entry.get(), password_entry.get()))
        user_register_button.pack(ipady=10)

        

    def login(self, username, password):
        # Connessione al database magazzinopython per l'autenticazione
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()
        cursor.execute("SELECT * FROM Utenti WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        db.close()

        if user:
            # L'utente è autenticato con successo
            messagebox.showinfo("Login", "Accesso riuscito!")
            self.app.show_frame(Gestionale)  # Reindirizza alla pagina Gestionale
        else:
            messagebox.showerror("Errore", "Credenziali non valide")





    def generate_unique_id(self):
        return str(uuid.uuid4())

    def register(self, username, password):
        # Connessione al database magazzinopython per la registrazione
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Controlla se l'username esiste già nel database
        cursor.execute("SELECT * FROM Utenti WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Errore", "Utente già esistente. Scegli un altro username.")
        else:
            # Genera un ID univoco
            unique_id = self.generate_unique_id()

            cursor.execute("INSERT INTO Utenti (idUtenti, username, password) VALUES (%s, %s, %s)", (unique_id, username, password))

            db.commit()
            db.close()

            messagebox.showinfo("Registrazione", "Utente registrato con successo!")




#############################################################################################################################################


class Clienti(Frame):
    def __init__(self, parent, app):
        Frame.__init__(self, parent)
        self.app = app  # Conserva il riferimento all'istanza di App


        # Creare un font personalizzato con una dimensione maggiore
        title_font = ("Trebuchet MS", 20) 
        button_font = ("Trebuchet MS", 13) 
        text_font = ("Trebuchet MS", 14) 

        label = Label(self, text="CLIENTI", font=title_font)
        label.pack(padx=10, pady=50)
        
        # Campi di input per username e password
        username_label = Label(self, font=text_font, text="Username:")
        username_label.pack()
        username_entry = Entry(self)
        username_entry.pack(ipadx=80, ipady=5, pady=(6,0))

        password_label = Label(self,font=text_font, text="Password:")
        password_label.pack(pady=(20,0))
        password_entry = Entry(self, show="*")  # Mostra asterischi per la password
        password_entry.pack(ipadx=80, ipady=5, pady=(6,0))

        # Pulsante di login
        login_button = Button(self, width=30, font=button_font, text="Login", bg="blue", fg="white", command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.pack(pady=(50,15),ipady=10)

        # Pulsante di registrazione
        user_register_button = Button(self, width=30, font=button_font, text="Registra", bg="blue", fg="white", command=lambda: self.register(username_entry.get(), password_entry.get()))
        user_register_button.pack(ipady=10)


    def login(self, username, password):
        
        # Connessione al database magazzinopython per l'autenticazione
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()
        cursor.execute("SELECT * FROM Clienti WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        db.close()

        if user:
            # L'utente è autenticato con successo
            messagebox.showinfo("Login", "Accesso riuscito!")
            App.current_username = username  # Salva l'username

            self.app.show_frame(GestionaleClienti)  # Reindirizza alla pagina GestionaleClienti
            self.app.frames[ClienteOrdiniEffettuati].set_username(username) #passa il dato username a ClientiOrdiniEffettuati  
            self.app.frames[ClienteOrdiniLavorati].set_username(username) #passa il dato username a ClientiOrdiniEffettuati  
            self.app.frames[GestionaleClienti].set_username(username) #passa il dato username a GestionaleClienti
            self.app.frames[ClienteNuovoOrdine].set_username(username) #passa il dato username a ClienteNuovoOrdine

        else:
            messagebox.showerror("Errore", "Credenziali non valide")



    def generate_unique_id(self):
        return str(uuid.uuid4())


    def register(self, username, password):
        # Connessione al database magazzinopython per la registrazione
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MagazzinoPython",
            database="magazzinopython"
        )

        cursor = db.cursor()

        # Controlla se l'username esiste già nel database
        cursor.execute("SELECT * FROM Clienti WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Errore", "Cliente già esistente. Scegli un altro username.")
        else:
            # Genera un ID univoco
            unique_id = self.generate_unique_id()

            cursor.execute("INSERT INTO Clienti (idClienti, username, password) VALUES (%s, %s, %s)", (unique_id, username, password))

            db.commit()
            db.close()

            messagebox.showinfo("Registrazione", "Cliente registrato con successo!")

#############################################################################################################################################


class MainMenu:
    def __init__(self, master):
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Home", command=master.show_start_page)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)

app = App()
app.mainloop()
