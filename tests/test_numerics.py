
import numpy as np
import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.numerics import lu_decomposition, determinant_from_lu, inverse_from_lu

def test_random_matrix(n):
    print(f"Testing random matrix size {n}x{n}...")
    A = np.random.rand(n, n)
    
    # 1. Decomposition Check: PA = LU
    P, L, U, swaps = lu_decomposition(A)
    PA = P @ A
    LU = L @ U
    diff = np.max(np.abs(PA - LU)) # Wait, P A = L U is wrong. 
    # My docstring said "Performs PA=LU". 
    # Usually scipy.linalg.lu returns P, L, U such that A = P L U or similar depending on def.
    # In my code:
    # U starts as A.
    # We pivot U and apply same swaps to P and L.
    # U is processed.
    # Let's re-read the code logic carefully.
    
    # My code:
    # U = A.copy()
    # P = I
    # When swapping row k and pivot:
    #   U[[k, pivot]] = U[[pivot, k]]
    #   P[[k, pivot]] = P[[pivot, k]]
    #   L swaps too.
    #
    # Finally L U = (Permuted A).
    # Since P tracks the permutations applied to A...
    # If P starts as I and we apply swaps to P...
    # Then P @ A_original would be the permuted matrix IF we applied swaps to A. 
    # But I applied swaps to U (which is a copy of A).
    # So P is the permutation matrix such that P @ A_orig = L @ U ???
    # Let's check:
    # P[[k, p]] = P[[p, k]] swaps rows of P.
    # If P starts as I, then P @ A is swapping rows of A.
    # Correct.
    
    PA = P @ A
    
    if np.allclose(PA, LU):
        print("  [Pass] PA = LU")
    else:
        print(f"  [FAIL] PA = LU. Max diff: {np.max(np.abs(PA - LU))}")
        
    # 2. Determinant Check
    det_calc = determinant_from_lu(U, swaps)
    det_ref = np.linalg.det(A)
    
    if np.isclose(det_calc, det_ref):
        print(f"  [Pass] Determinant ({det_calc:.4f} vs {det_ref:.4f})")
    else:
        print(f"  [FAIL] Determinant. Calc: {det_calc}, Ref: {det_ref}")
        
    # 3. Inverse Check
    try:
        inv_calc = inverse_from_lu(P, L, U)
        inv_ref = np.linalg.inv(A)
        if np.allclose(inv_calc, inv_ref):
            print("  [Pass] Inverse matches numpy")
        else:
            print(f"  [FAIL] Inverse. Max diff: {np.max(np.abs(inv_calc - inv_ref))}")
    except Exception as e:
        print(f"  [Error] Inverse calculation failed: {e}")

def test_singular_matrix():
    print("Testing singular matrix...")
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.float64) # Det is 0
    P, L, U, swaps = lu_decomposition(A)
    det = determinant_from_lu(U, swaps)
    
    if np.isclose(det, 0, atol=1e-8):
        print("  [Pass] Determinant is ~0")
    else:
        print(f"  [FAIL] Determinant should be 0, got {det}")

if __name__ == "__main__":
    np.random.seed(42)
    test_random_matrix(5)
    test_random_matrix(10)
    test_random_matrix(50)
    test_singular_matrix()
