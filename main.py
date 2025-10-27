import flet as ft
from flet.core.alignment import center

from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    txt_automobili_titolo =ft.Text(value="Aggiungi nuova automobile", size= 30, weight =ft.FontWeight.NORMAL)

    input_marca = ft.TextField( value = "",  label = "Marca" )
    input_modello = ft.TextField(value = "", label = "Modello")
    input_anno = ft.TextField(value = "", label = "Anno" )
    num_posti = 4
    txt_num_posti= ft.Text(str(num_posti), size =20, weight=ft.FontWeight.BOLD)


     # --- FUNZIONI APP ---
    def aumenta_posti(e):
        nonlocal num_posti
        num_posti += 1
        txt_num_posti.value = str(num_posti)
        page.update()

    def diminuisci_posti(e):
        nonlocal num_posti
        if num_posti > 1:  # minimo 1 posto
            num_posti -= 1
            txt_num_posti.value = str(num_posti)
            page.update()

    row_posti = ft.Row(
        controls=[
            ft.IconButton(icon ="remove", icon_color="red", on_click=diminuisci_posti),
            txt_num_posti,
            ft.IconButton(icon ="add", icon_color="green", on_click=aumenta_posti),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    def aggiungi_auto(e):
        marca = input_marca.value

        if marca.strip() == "":
            alert.show_alert(f"❌ inserire dati sul campo Marca..")
            return
        modello = input_modello.value
        if modello.strip() == "":
            alert.show_alert(f"❌ inserire dati sul campo Modello..")
            return
        anno = input_anno.value
        if anno.strip() == "":
            alert.show_alert(f"❌ inserire dati sul campo Anno..")
            return
        try:
            anno =int(anno)
            if anno < 1800 or anno > 2026:
                alert.show_alert(f" ❌ anno  ({anno}), non possibile/ plausibile :(")
                return

        except Exception  as t:
            alert.show_alert(f"❌ formato anno non valido :( \n {t}")


        autonoleggio.aggiungi_automobile(marca, modello, anno, num_posti)
        aggiorna_lista_auto()
        input_marca.value=""
        input_anno.value=""
        input_modello.value=""
        page.update()



    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)
    pulsante_conferma_automobile = ft.ElevatedButton("Aggiungi automobile", on_click=aggiungi_auto)
    # Bottoni per la gestione dell'inserimento di una nuova auto

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        # Sezione 3
        txt_automobili_titolo,
        ft.Row(spacing=2, controls=[input_marca, input_modello, input_anno, row_posti]),pulsante_conferma_automobile,



        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
