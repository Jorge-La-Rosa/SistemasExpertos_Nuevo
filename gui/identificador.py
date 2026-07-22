# gui/identificador.py
from tkinter import messagebox


class IdentificadorAsistido:
    """
    Maneja el estado y la lógica del cuestionario de identificación.
    """

    def __init__(self, base_algas, render_callback, abrir_detalle_callback):
        """
        base_algas: diccionario con todas las especies.
        render_callback: función que refresca la UI de preguntas.
        abrir_detalle_callback: función para abrir el modal de detalle.
        """
        self.base_algas = base_algas
        self.render_callback = render_callback
        self.abrir_detalle_callback = abrir_detalle_callback

        self.resetear()

    def resetear(self):
        """Reinicia el estado del cuestionario."""
        self.paso_actual = 1          # 1: Clase, 2: Familia, 3: Especie
        self.filtro_clase = None
        self.filtro_familia = None
        self.opciones_disponibles = []
        self.indice_opcion_actual = 0

    def obtener_pregunta(self):
        """
        Devuelve el texto de la pregunta actual y actualiza las opciones.
        """
        if self.paso_actual == 1:
            self.opciones_disponibles = [
                "Chlorophyta (Verde)",
                "Rhodophyta (Roja)",
                "Phaeophyceae (Parda)"
            ]
            opcion = self.opciones_disponibles[self.indice_opcion_actual]
            return f"¿El alga pertenece al grupo o es de color {opcion}?"

        elif self.paso_actual == 2:
            if not self.opciones_disponibles:
                # Extraer familias únicas de la clase seleccionada
                familias = set(
                    datos["familia"]
                    for datos in self.base_algas.values()
                    if datos["clase"] == self.filtro_clase
                )
                self.opciones_disponibles = list(familias)
                self.indice_opcion_actual = 0
            opcion = self.opciones_disponibles[self.indice_opcion_actual]
            return f"¿Su estructura y morfología coincide con la familia {opcion}?"

        elif self.paso_actual == 3:
            if not self.opciones_disponibles:
                # Filtrar especies por clase y familia
                self.opciones_disponibles = [
                    esp
                    for esp, datos in self.base_algas.items()
                    if datos["clase"] == self.filtro_clase
                    and datos["familia"] == self.filtro_familia
                ]
                self.indice_opcion_actual = 0

            especie = self.opciones_disponibles[self.indice_opcion_actual]
            clave = self.base_algas[especie]["caracteristicas"].get(
                "clave_id", "Sin clave"
            )
            return f"¿Cumple con esta clave dicotómica?\n\n\"{clave}\""

        return ""

    def respuesta_si(self):
        """Maneja la respuesta afirmativa."""
        if self.paso_actual == 1:
            clase = self.opciones_disponibles[self.indice_opcion_actual]
            self.filtro_clase = clase.split(" ")[0]  # 'Chlorophyta', etc.
            self.paso_actual = 2
            self.opciones_disponibles = []
            self.indice_opcion_actual = 0
            self.render_callback()

        elif self.paso_actual == 2:
            self.filtro_familia = self.opciones_disponibles[
                self.indice_opcion_actual
            ]
            self.paso_actual = 3
            self.opciones_disponibles = []
            self.indice_opcion_actual = 0
            self.render_callback()

        elif self.paso_actual == 3:
            especie = self.opciones_disponibles[self.indice_opcion_actual]
            self.abrir_detalle_callback(especie)
            self.resetear()
            self.render_callback()

    def respuesta_no(self):
        """Maneja la respuesta negativa."""
        self.indice_opcion_actual += 1
        if self.indice_opcion_actual >= len(self.opciones_disponibles):
            messagebox.showinfo(
                "Sin Coincidencias",
                "No se encontraron registros que coincidan con las "
                "características descritas."
            )
            self.resetear()
        self.render_callback()
