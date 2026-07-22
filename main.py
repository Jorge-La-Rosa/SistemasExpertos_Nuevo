# main.py
from data.gestor_datos import GestorDatos
from gui.interfaz import AplicacionExpertaAlgas


def main():
    gestor_db = GestorDatos()
    app = AplicacionExpertaAlgas(base_conocimiento=gestor_db)
    app.mainloop()


if __name__ == "__main__":
    main()
