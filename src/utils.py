
import numpy as np
import ast
import re

def parse_input(input_str):
    """
    Parses a string input into a numpy array.
    Supports:
    - Python list syntax: [[1, 2], [3, 4]]
    - Space/Tab/Comma separated values with newlines for rows.
    """
    input_str = input_str.strip()
    
    # Try parsing as python list first
    try:
        # Check if it looks like a list
        if input_str.startswith('[') and input_str.endswith(']'):
            # AST literal eval for safe parsing
            data = ast.literal_eval(input_str)
            return np.array(data, dtype=np.float64)
    except Exception:
        pass
    
    # Fallback: Text block parsing
    # Split by newlines for rows
    lines = input_str.strip().splitlines()
    rows = []
    
    for line in lines:
        if not line.strip(): 
            continue
        # Replace commas with spaces, then split
        parts = line.replace(',', ' ').split()
        row = [float(p) for p in parts]
        rows.append(row)
        
    return np.array(rows, dtype=np.float64)

def format_matrix(matrix, precision=4):
    """
    Returns a formatted string representation of the matrix.
    """
    # Use numpy's built-in array2string for stability and options
    return np.array2string(
        matrix, 
        precision=precision, 
        suppress_small=True, 
        separator=', ',
        floatmode='fixed'
    )
