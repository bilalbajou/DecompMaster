
import numpy as np

def lu_decomposition(A):
    """
    Performs LU decomposition with partial pivoting (PA = LU).
    
    Args:
        A (numpy.ndarray): Square matrix of shape (n, n).
        
    Returns:
        P (numpy.ndarray): Permutation matrix.
        L (numpy.ndarray): Lower triangular matrix with unit diagonal.
        U (numpy.ndarray): Upper triangular matrix.
        swaps (int): Number of row swaps performed (for determinant sign).
    """
    n = A.shape[0]
    U = A.astype(np.float64).copy()
    L = np.eye(n, dtype=np.float64)
    P = np.eye(n, dtype=np.float64)
    swaps = 0
    
    for k in range(n):
        # Partial Pivoting
        pivot = k + np.argmax(np.abs(U[k:, k]))
        if pivot != k:
            # Swap rows in U
            U[[k, pivot]] = U[[pivot, k]]
            # Swap rows in P
            P[[k, pivot]] = P[[pivot, k]]
            # Swap rows in L (only the part that has been computed so far)
            if k > 0:
                L[[k, pivot], :k] = L[[pivot, k], :k]
            swaps += 1
            
        # Check for singular matrix (pivot is effectively zero)
        if np.isclose(U[k, k], 0.0):
             # Depending on requirements, we might raise error or continue.
             # Singular/Warning might be handled by determinant check later.
             pass

        # Elimination
        for i in range(k + 1, n):
            factor = U[i, k] / U[k, k]
            L[i, k] = factor
            U[i, k:] -= factor * U[k, k:]
            
    return P, L, U, swaps

def forward_substitution(L, b):
    """
    Solves the system Ly = b for y.
    L is lower triangular with unit diagonal.
    """
    n = L.shape[0]
    y = np.zeros_like(b, dtype=np.float64)
    
    for i in range(n):
        # L[i, i] is 1, so no division needed.
        # y[i] = b[i] - sum(L[i, j] * y[j] for j < i)
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
        
    return y

def backward_substitution(U, y):
    """
    Solves the system Ux = y for x.
    U is upper triangular.
    """
    n = U.shape[0]
    x = np.zeros_like(y, dtype=np.float64)
    
    for i in range(n - 1, -1, -1):
        if np.isclose(U[i, i], 0.0):
            raise ValueError("La matrice est singulière, impossible d'effectuer la substitution arrière.")
        
        # x[i] = (y[i] - sum(U[i, j] * x[j] for j > i)) / U[i, i]
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
        
    return x

def determinant_from_lu(U, swaps):
    """
    Computes determinant using diagonal of U and swap count.
    det(A) = det(P) * det(L) * det(U)
           = (-1)^swaps * 1 * prod(diag(U))
    """
    det_u = np.prod(np.diag(U))
    return det_u * ((-1) ** swaps)

def inverse_from_lu(P, L, U):
    """
    Computes inverse of A using PA=LU factorization.
    AX = I => PA X = PI => LU X = PI
    Solve for each column.
    """
    n = L.shape[0]
    inv_A = np.zeros((n, n), dtype=np.float64)
    
    # Right side is Identity permuted by P -> P @ I = P
    # But wait, PA = LU. So A = P.T L U.
    # Inverse A^-1 = (LU)^-1 (P.T)^-1 = U^-1 L^-1 P
    # OR solve A x_i = e_i
    # PA x_i = P e_i
    # LU x_i = P[:, i] (i-th column of P)
    
    # We solve for each column of the identity matrix
    identity = np.eye(n)
    
    # We can vectorize this or loop over columns. 
    # Looping is clearer for "solving n linear systems".
    for i in range(n):
        e_i = identity[:, i]
        b = P @ e_i # Apply permutation to RHS
        
        # Forward: L y = b
        y = forward_substitution(L, b)
        
        # Backward: U x = y
        x = backward_substitution(U, y)
        
        inv_A[:, i] = x
        
    return inv_A
