# gui/interfaz.py
import os
import customtkinter as ctk
from gui.utilidades import CacheImagenes
from gui.componentes import TarjetaAlga
from gui.identificador import IdentificadorAsistido
from gui.ventanas import VentanaDetalle, VentanaNuevaEspecie


class AplicacionExpertaAlgas(ctk.CTk):
    """Ventana principal de la aplicación."""

    def __init__(self, base_conocimiento):
        super().__init__()

        self.gestor = base_conocimiento
        self.base_algas = self.gestor.obtener_todas()

        # Configuración de la ventana
        self.title("Sistema Experto - Identificación de Algas")
        self.geometry("1100x700")
        self.minsize(1000, 650)

        # Ruta raíz y assets
        self.ruta_raiz = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.ruta_assets = os.path.join(self.ruta_raiz, "assets")
        self.cache_imagenes = CacheImagenes(self.ruta_assets)

        # Crear interfaz
        self.crear_interfaz_principal()

        # Inicializar identificador
        self.identificador = IdentificadorAsistido(
            base_algas=self.base_algas,
            render_callback=self.renderizar_pregunta_asistida,
            abrir_detalle_callback=self.abrir_modal_detalle
        )
        self.renderizar_pregunta_asistida()

    def crear_interfaz_principal(self):
        """Crea la estructura de la ventana (navbar, columnas, galería)."""
        # Navbar
        self.navbar = ctk.CTkFrame(
            self,
            height=50,
            corner_radius=0,
            fg_color=("#222222", "#111111")
        )
        self.navbar.pack(fill="x", side="top")

        lbl_logo = ctk.CTkLabel(
            self.navbar,
            text="🔬 Sistema Experto de Algas",
            text_color="white",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        lbl_logo.pack(side="left", padx=20, pady=10)

        btn_add = ctk.CTkButton(
            self.navbar,
            text="+ Añadir Nueva Especie",
            fg_color="#27AE60",
            hover_color="#219653",
            font=ctk.CTkFont(weight="bold"),
            command=self.click_anadir_especie
        )
        btn_add.pack(side="right", padx=20, pady=10)

        # Cuerpo (dos columnas)
        self.cuerpo = ctk.CTkFrame(self, fg_color="transparent")
        self.cuerpo.pack(fill="both", expand=True, padx=20, pady=20)

        # Columna izquierda: identificador
        self.col_izquierda = ctk.CTkFrame(
            self.cuerpo,
            width=350,
            corner_radius=12
        )
        self.col_izquierda.pack(side="left", fill="both", padx=(0, 10))
        self.col_izquierda.pack_propagate(False)

        ctk.CTkLabel(
            self.col_izquierda,
            text="Identificador Asistido",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15, padx=15, anchor="w")

        self.box_pregunta = ctk.CTkFrame(
            self.col_izquierda,
            fg_color=("#F5F5F5", "#202020"),
            corner_radius=10
        )
        self.box_pregunta.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Columna derecha: galería
        self.col_derecha = ctk.CTkFrame(self.cuerpo, corner_radius=12)
        self.col_derecha.pack(
            side="right", fill="both", expand=True, padx=(10, 0)
        )

        ctk.CTkLabel(
            self.col_derecha,
            text="Galería Interactiva",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=15, padx=20, anchor="w")

        self.grid_galeria = ctk.CTkScrollableFrame(
            self.col_derecha,
            fg_color="transparent"
        )
        self.grid_galeria.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Render inicial de la galería
        self.actualizar_galeria_tarjetas()

    # ============================
    # IDENTIFICADOR ASISTIDO
    # ============================

    def renderizar_pregunta_asistida(self):
        """Refresca la UI de la pregunta actual."""
        # Limpiar contenedor
        for w in self.box_pregunta.winfo_children():
            w.destroy()

        # Obtener texto de la pregunta
        texto = self.identificador.obtener_pregunta()

        # Mostrar pregunta
        lbl_q = ctk.CTkLabel(
            self.box_pregunta,
            text=texto,
            font=ctk.CTkFont(size=15),
            wraplength=280,
            justify="center"
        )
        lbl_q.pack(pady=40, padx=20, expand=True)

        # Botones
        btn_frame = ctk.CTkFrame(self.box_pregunta, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom", pady=20, padx=20)

        ctk.CTkButton(
            btn_frame,
            text="Sí",
            width=110,
            fg_color="#2980B9",
            hover_color="#2471A3",
            font=ctk.CTkFont(weight="bold"),
            command=self.identificador.respuesta_si
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="No",
            width=110,
            fg_color="#C0392B",
            hover_color="#922B21",
            font=ctk.CTkFont(weight="bold"),
            command=self.identificador.respuesta_no
        ).pack(side="right", padx=5)

    # ============================
    # GALERÍA
    # ============================

    def actualizar_galeria_tarjetas(self):
        """Construye la galería de tarjetas a partir de los datos actuales."""
        for w in self.grid_galeria.winfo_children():
            w.destroy()

        self.grid_galeria.grid_columnconfigure(
            (0, 1, 2), weight=1, pad=10
        )

        fila = 0
        columna = 0
        for nombre, datos in self.base_algas.items():
            img = self.cache_imagenes.obtener(
                datos.get("imagen", "default.png"),
                (180, 120)
            )
            tarjeta = TarjetaAlga(
                self.grid_galeria,
                nombre=nombre,
                clase=datos["clase"],
                familia=datos["familia"],
                imagen_ctk=img,
                al_hacer_clic=self.abrir_modal_detalle
            )
            tarjeta.grid(
                row=fila, column=columna, padx=10, pady=10,
                sticky="nsew"
            )

            columna += 1
            if columna > 2:
                columna = 0
                fila += 1

    # ============================
    # MODALES
    # ============================

    def abrir_modal_detalle(self, nombre_especie):
        """Abre el modal de detalle de una especie."""
        datos = self.base_algas.get(nombre_especie)
        if datos:
            VentanaDetalle.abrir(
                self,
                nombre_especie,
                datos,
                self.ruta_assets
            )

    def click_anadir_especie(self):
        """Abre el modal para añadir una nueva especie."""
        VentanaNuevaEspecie.abrir(
            self,
            self.gestor,
            self.recargar_galeria_en_caliente
        )

    def recargar_galeria_en_caliente(self):
        """Recarga los datos del gestor y actualiza la galería y el identificador."""
        self.base_algas = self.gestor.obtener_todas()
        self.actualizar_galeria_tarjetas()
        self.identificador.base_algas = self.base_algas
        self.identificador.resetear()
        self.renderizar_pregunta_asistida()
