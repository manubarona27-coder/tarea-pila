import sys

# Verificación de seguridad para asegurar que tkinter esté disponible
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    print("ERROR: La librería 'tkinter' no está instalada en tu entorno de Python.")
    print("Si estás en Linux (Ubuntu/Debian), ejecuta en tu terminal: sudo apt install python3-tk")
    sys.exit(1)

class PilaGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Pila (Stack) LIFO")
        self.root.geometry("450x650")
        self.root.config(bg="#f0f0f0")

        # Configuración de colores
        self.bg_color = "#f0f0f0"
        self.color_pila = "#e0e0e0" 
        self.color_elemento = "#4CAF50" 
        self.color_texto_elemento = "white"

        # La pila lógica (lista de Python)
        self.pila_datos = []
        self.max_elementos_visuales = 10
        self.elementos_visuales = []

        self.crear_interfaz()

    def crear_interfaz(self):
        # --- Título ---
        titulo = tk.Label(self.root, text="Estructura de Datos: PILA (LIFO)", font=("Arial", 16, "bold"), bg=self.bg_color)
        titulo.pack(pady=15)

        subtitulo = tk.Label(self.root, text="Último en Entrar, Primero en Salir", font=("Arial", 10, "italic"), bg=self.bg_color)
        subtitulo.pack()

        # --- Área de Controles ---
        marco_controles = tk.Frame(self.root, bg=self.bg_color)
        marco_controles.pack(pady=15)

        tk.Label(marco_controles, text="Dato:", font=("Arial", 12), bg=self.bg_color).grid(row=0, column=0, padx=5)
        
        self.entrada_dato = tk.Entry(marco_controles, font=("Arial", 12), width=12)
        self.entrada_dato.grid(row=0, column=1, padx=5)
        self.entrada_dato.focus() # Pone el cursor listo para escribir
        self.entrada_dato.bind('<Return>', lambda event: self.push_elemento()) # Enter para apilar

        btn_push = tk.Button(marco_controles, text="PUSH (Apilar)", command=self.push_elemento, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), relief="raised")
        btn_push.grid(row=0, column=2, padx=8)

        marco_botones_inferior = tk.Frame(self.root, bg=self.bg_color)
        marco_botones_inferior.pack(pady=5)

        btn_pop = tk.Button(marco_botones_inferior, text="POP (Desapilar)", command=self.pop_elemento, bg="#f44336", fg="white", font=("Arial", 10, "bold"), relief="raised")
        btn_pop.pack(side=tk.LEFT, padx=10)

        btn_peek = tk.Button(marco_botones_inferior, text="PEEK (Ver Cima)", command=self.peek_elemento, bg="#FF9800", fg="white", font=("Arial", 10, "bold"), relief="raised")
        btn_peek.pack(side=tk.LEFT, padx=10)

        # --- Área Gráfica (Canvas) ---
        self.canvas_width = 300
        self.canvas_height = 420
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg=self.color_pila, highlightthickness=2, highlightbackground="#9e9e9e")
        self.canvas.pack(pady=20)

        # Dibujar contenedor de la pila
        self.canvas.create_rectangle(50, 40, 250, self.canvas_height - 20, fill=self.color_pila, outline="")
        self.canvas.create_line(50, 40, 50, self.canvas_height - 20, width=3, fill="#616161") # Pared izq
        self.canvas.create_line(250, 40, 250, self.canvas_height - 20, width=3, fill="#616161") # Pared der
        self.canvas.create_line(50, self.canvas_height - 20, 250, self.canvas_height - 20, width=3, fill="#616161") # Piso

        # Etiqueta de Cima
        self.etiqueta_cima = self.canvas.create_text(150, 20, text="", font=("Arial", 11, "bold"), fill="#333333")

        self.actualizar_vista()

    def actualizar_vista(self):
        for element in self.elementos_visuales:
            self.canvas.delete(element)
        self.elementos_visuales = []
        self.canvas.itemconfig(self.etiqueta_cima, text="")

        ancho_bloque = 196
        alto_bloque = 32
        x_inicio = 52
        y_piso = self.canvas_height - 20 - alto_bloque 

        num_elementos = len(self.pila_datos)
        elementos_a_dibujar = min(num_elementos, self.max_elementos_visuales)

        for i in range(elementos_a_dibujar):
            y_pos = y_piso - (i * alto_bloque)
            dato_texto = str(self.pila_datos[i])
            
            # Dibujar rectángulo del elemento
            rect = self.canvas.create_rectangle(x_inicio, y_pos, x_inicio + ancho_bloque, y_pos + alto_bloque, fill=self.color_elemento, outline="#2E7D32", width=2)
            self.elementos_visuales.append(rect)
            
            # Dibujar texto centrado en el bloque
            text = self.canvas.create_text(x_inicio + (ancho_bloque/2), y_pos + (alto_bloque/2), text=dato_texto, fill=self.color_texto_elemento, font=("Arial", 10, "bold"))
            self.elementos_visuales.append(text)

        if num_elementos > 0:
            self.canvas.itemconfig(self.etiqueta_cima, text=f"▲ CIMA (Dato: {str(self.pila_datos[-1])})", fill="#1b5e20")

    def push_elemento(self):
        dato = self.entrada_dato.get().strip()
        if not dato:
            messagebox.showwarning("Entrada Vacía", "Por favor, escribe un valor para apilar.")
            return

        self.pila_datos.append(dato)
        self.entrada_dato.delete(0, tk.END)
        self.actualizar_vista()

    def pop_elemento(self):
        if not self.pila_datos:
            messagebox.showerror("Error", "La pila está vacía. No se puede hacer POP (Underflow).")
            return

        dato_eliminado = self.pila_datos.pop()
        self.actualizar_vista()
        messagebox.showinfo("POP Exitoso", f"Se retiró de la cima: '{dato_eliminado}'")

    def peek_elemento(self):
        if not self.pila_datos:
            messagebox.showinfo("PEEK", "La pila está vacía.")
            return

        dato_cima = self.pila_datos[-1]
        messagebox.showinfo("PEEK (Cima Actual)", f"El elemento en la cima es: '{dato_cima}'\n(La pila no se modificó)")


if __name__ == "__main__":
    root = tk.Tk()
    app = PilaGrafica(root)
    # Forzar que la ventana aparezca al frente en algunos sistemas operativos
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    root.mainloop()