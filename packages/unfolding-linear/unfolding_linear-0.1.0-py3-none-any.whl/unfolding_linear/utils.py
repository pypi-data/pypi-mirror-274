# Copyright (c) 2023-2024 Salah Berra and contributors
# Distributed under the the GNU General Public License (See accompanying file LICENSE or copy
# at https://www.gnu.org/licenses/)

# This script contains the functions that will be used in the various modules of the dee_unfolding package.
import numpy as np
import math
import torch
from typing import Tuple

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # GPU, if not CPU
print(f"Code run on : {device}")

def generate_A_H_sol(n: int = 300, m: int = 600, seed: int = 12, bs: int = 10, device: torch.device = device) -> Tuple[np.ndarray, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Generate matrices A, H, and W, as well as the solution and y.

    Args:
        - n (int, optional): Number of rows. Defaults to 300.
        - m (int, optional): Number of columns. Defaults to 600.
        - seed (int, optional): Seed for random number generation. Defaults to 12.
        - bs (int, optional): Batch size. Defaults to 10.
        - device (torch.device, optional): Device to run the computations on. Defaults to the global 'device'.

    Returns:
        - Tuple[np.ndarray, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]: 
            - Matrix A (square matrix) of shape (n, n)
            - Matrix H (random matrix) of shape (n, m)
            - Matrix W with diagonal eigenvalues of A of shape (n, n)
            - Solution tensor of shape (bs, n)
            - Tensor y resulting from solution@H of shape (bs, m)
    """
    np.random.seed(seed=seed)
    H = np.random.normal(0, 1.0 / math.sqrt(n), (n, m))
    A = np.dot(H, H.T)
    eig = np.linalg.eig(A)[0]  # Eigenvalues
    
    W = torch.Tensor(np.diag(eig)).to(device)  # Define the appropriate 'device'
    H = torch.from_numpy(H).float().to(device)  # Define the appropriate 'device'
    
    print("Condition number, min. and max. eigenvalues of A:")
    print(np.max(eig) / np.min(eig), np.max(eig), np.min(eig))
    
    solution = torch.normal(torch.zeros(bs, n), 1.0).to(device).detach()
    y = solution @ H.detach()
    
    return A, H, W, solution, y

def decompose_matrix(A: np.ndarray) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Decompose a given matrix into its diagonal, lower triangular, upper triangular components and their inverses.

    Args:
        - A (np.ndarray): Input square matrix to decompose.

    Returns:
        - Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]: 
            - A (torch.Tensor): Original matrix converted to a torch tensor.
            - D (torch.Tensor): Diagonal matrix of A.
            - L (torch.Tensor): Lower triangular matrix of A.
            - U (torch.Tensor): Upper triangular matrix of A.
            - Dinv (torch.Tensor): Inverse of the diagonal matrix D.
            - Minv (torch.Tensor): Inverse of the matrix (D + L).
    """
    # Decomposed matrix calculations
    D = np.diag(np.diag(A))  # Diagonal matrix
    L = np.tril(A, -1)       # Lower triangular matrix
    U = np.triu(A, 1)        # Upper triangular matrix
    Dinv = np.linalg.inv(D)  # Inverse of the diagonal matrix
    invM = np.linalg.inv(D + L)  # Inverse of the matrix (D + L)

    # Convert to Torch tensors and move to device
    A = torch.Tensor(A).to(device)
    D = torch.Tensor(D).to(device)
    L = torch.Tensor(L).to(device)
    U = torch.Tensor(U).to(device)
    Dinv = torch.Tensor(Dinv).to(device)
    Minv = torch.Tensor(invM).to(device)
    
    return A, D, L, U, Dinv, Minv