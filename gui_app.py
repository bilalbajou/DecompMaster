
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from src.numerics import lu_decomposition, determinant_from_lu, inverse_from_lu
from src.utils import parse_input, format_matrix

class LUApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Décomposition LU - Maître")
        self.root.geometry("900x700")
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Helvetica", 11))
        style.configure("TLabel", font=("Helvetica", 11))
        
        # Main Frame
        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- Top Section: Input ---
        input_label = ttk.Label(main_frame, text="Matrice d'entrée (Espaces/Virgules ou Liste Python):", font=("Helvetica", 12, "bold"))
        input_label.pack(anchor="w", pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(main_frame, height=8, width=80, font=("Consolas", 11))
        self.input_text.pack(fill=tk.X, expand=False, pady=(0, 10))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.calc_btn = ttk.Button(btn_frame, text="Calculer Décomposition", command=self.calculate)
        self.calc_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(btn_frame, text="Effacer", command=self.clear_input)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.example_btn = ttk.Button(btn_frame, text="Charger Exemple", command=self.load_example)
        self.example_btn.pack(side=tk.LEFT)
        
        # --- Bottom Section: Results ---
        # Using Notebook for organized tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tabs
        self.tab_overview = self.create_tab("Aperçu")
        self.tab_matrices = self.create_tab("Matrices (L, U, P)")
        self.tab_inverse = self.create_tab("Matrice Inverse")
        
    def create_tab(self, title):
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text=title)
        
        text_area = scrolledtext.ScrolledText(frame, font=("Consolas", 11), state='disabled')
        text_area.pack(fill=tk.BOTH, expand=True)
        return text_area
        
    def write_tab(self, tab, content):
        tab.config(state='normal')
        tab.delete(1.0, tk.END)
        tab.insert(tk.END, content)
        tab.config(state='disabled')
        
    def clear_input(self):
        self.input_text.delete(1.0, tk.END)
        self.write_tab(self.tab_overview, "")
        self.write_tab(self.tab_matrices, "")
        self.write_tab(self.tab_inverse, "")
        
    def load_example(self):
        example = "3 2 1\n2 3 2\n1 2 3"
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(tk.END, example)
        
    def calculate(self):
        raw_input = self.input_text.get(1.0, tk.END)
        if not raw_input.strip():
            messagebox.showwarning("Entrée Vide", "Veuillez entrer une matrice d'abord.")
            return
            
        try:
            A = parse_input(raw_input)
            
            if A.ndim != 2 or A.shape[0] != A.shape[1]:
                raise ValueError(f"La matrice doit être carrée. Forme reçue: {A.shape}")
            
            n = A.shape[0]
            
            # Perform calculations
            P, L, U, swaps = lu_decomposition(A)
            det = determinant_from_lu(U, swaps)
            is_invertible = not np.isclose(det, 0.0)
            
            # 1. Overview Tab
            overview_text = f"Analysis Results\n{'='*20}\n"
            overview_text += f"Dimension: {n}x{n}\n"
            overview_text += f"Determinant: {det:.6g}\n"
            overview_text += f"Invertible: {'YES' if is_invertible else 'NO'}\n"
            
            if is_invertible:
                try:
                    inv_A = inverse_from_lu(P, L, U)
                    check = np.trace(A @ inv_A)
                    overview_text += f"Trace Check (A*A_inv): {check:.6f} (Target: {float(n)})\n"
                except Exception as e:
                    overview_text += f"Inverse Error: {e}\n"
            
            self.write_tab(self.tab_overview, overview_text)
            
            # 2. Matrices Tab
            matrices_text = "Originale 'A':\n" + format_matrix(A) + "\n\n"
            matrices_text += "Permutation 'P':\n" + format_matrix(P) + "\n\n"
            matrices_text += "Inférieure (Lower) 'L':\n" + format_matrix(L) + "\n\n"
            matrices_text += "Supérieure (Upper) 'U':\n" + format_matrix(U) + "\n"
            self.write_tab(self.tab_matrices, matrices_text)
            
            # 3. Inverse Tab
            if is_invertible:
                inv_text = "Matrice Inverse 'A^-1':\n" + format_matrix(inv_A)
                self.write_tab(self.tab_inverse, inv_text)
            else:
                self.write_tab(self.tab_inverse, "La matrice est singulière (non inversible).")
                
            # Switch to Overview tab
            self.notebook.select(0)
            
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = LUApp(root)
    root.mainloop()
