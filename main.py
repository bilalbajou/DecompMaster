
import sys
import numpy as np
from src.numerics import lu_decomposition, determinant_from_lu, inverse_from_lu
from src.utils import parse_input, format_matrix

def get_input_from_user():
    print("\n--- Entrée de la Matrice ---")
    print("Option 1: Coller un bloc de texte (espaces/virgules ou liste Python).")
    print("Option 2: Entrée ligne par ligne (Manuel).")
    choice = input("Sélectionnez une option (1/2): ").strip()
    
    if choice == '1':
        print("Entrez les données de la matrice ci-dessous. Appuyez sur Entrée deux fois pour terminer:")
        lines = []
        while True:
            try:
                line = input()
                if not line.strip():
                    break
                lines.append(line)
            except EOFError:
                break
        return "\n".join(lines)
    
    elif choice == '2':
        try:
            n = int(input("Entrez la taille de la matrice (n): "))
            rows = []
            print(f"Entrez {n} lignes (nombres séparés par des espaces):")
            for i in range(n):
                line = input(f"Ligne {i+1}: ")
                rows.append(line)
            return "\n".join(rows)
        except ValueError:
            print("Nombre invalide.")
            return None
    else:
        print("Choix invalide.")
        return None

def process_matrix(A):
    print("\n" + "="*40)
    print("RÉSULTATS DE L'ANALYSE")
    print("="*40)
    
    n = A.shape[0]
    print(f"\nMatrice Originale ({n}x{n}):")
    print(format_matrix(A))
    
    # LU Decomposition
    try:
        P, L, U, swaps = lu_decomposition(A)
        det = determinant_from_lu(U, swaps)
        
        print("\n--- Décomposition LU (PA = LU) ---")
        print("Matrice de Permutation P:")
        print(format_matrix(P))
        print("\nMatrice Triangulaire Inférieure L:")
        print(format_matrix(L))
        print("\nMatrice Triangulaire Supérieure U:")
        print(format_matrix(U))
        
        print("\n--- Propriétés ---")
        print(f"Déterminant: {det:.6g}")
        
        is_invertible = not np.isclose(det, 0.0)
        print(f"Inversible: {'OUI' if is_invertible else 'NON'}")
        
        if is_invertible:
            print("\n--- Matrice Inverse ---")
            inv_A = inverse_from_lu(P, L, U)
            print(format_matrix(inv_A))
            
            # Simple check
            identity_check = A @ inv_A
            tuck = np.trace(identity_check)
            print(f"\nVérification (Trace A * A_inv): {tuck:.6f} / {float(n)}")

    except Exception as e:
        print(f"\nErreur pendant le calcul: {e}")

def main():
    print("Bienvenue dans l'Outil de Décomposition LU Python")
    
    while True:
        raw_input = get_input_from_user()
        if not raw_input:
            print("Aucune entrée fournie.")
            retry = input("Réessayer? (o/n): ").lower()
            if retry != 'o':
                break
            continue
            
        try:
            matrix = parse_input(raw_input)
            if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
                print(f"Erreur: La matrice doit être carrée. Forme reçue: {matrix.shape}")
                continue
                
            process_matrix(matrix)
            
        except Exception as e:
            print(f"Erreur d'analyse de l'entrée: {e}")
            
        retry = input("\nAnalyser une autre matrice? (o/n): ").lower()
        if retry != 'o':
            break

if __name__ == "__main__":
    main()
