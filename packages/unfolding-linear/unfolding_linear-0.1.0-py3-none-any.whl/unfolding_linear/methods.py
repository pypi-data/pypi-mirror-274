# Copyright (c) 2022-2023 Salah Berra and contributors
# Distributed under the the GNU General Public License (See accompanying file LICENSE or copy
# at https://www.gnu.org/licenses/)

import torch
import numpy as np
from typing import List, Tuple
from .utils import device, decompose_matrix

def model_iterations(total_itr: int, n: int, bs: int, model, solution: torch.Tensor) -> Tuple[List[torch.Tensor], List[float]]:
    """
    Perform iterations using the provided model and calculate the error norm at each iteration.

    Args:
        - total_itr (int): Total number of iterations to perform.
        - n (int): Dimension of the solution.
        - bs (int): Batch size.
        - model: The model instance that provides the iterate method.
        - solution (torch.Tensor): The ground truth solution tensor.

    Returns:
        - Tuple[List[torch.Tensor], List[float]]:
            - List of tensors representing the solution estimates at each iteration.
            - List of float values representing the normalized error at each iteration.
    """
    norm_list_model = []  # Initialize the iteration list
    s_hats = []
    
    for i in range(total_itr + 1):
        s_hat, _ = model.iterate(i)
        err = (torch.norm(solution.to(device) - s_hat.to(device)) ** 2).item() / (n * bs)
        
        s_hats.append(s_hat)
        norm_list_model.append(err)
    
    return s_hats, norm_list_model

class base_model:
    """
    Base model class for matrix decomposition and initialization.

    Args:
        - n (int): Dimension of the solution.
        - A (np.ndarray): Input square matrix to decompose.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.

    Attributes:
        - n (int): Dimension of the solution.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - A (torch.Tensor): Original matrix converted to a torch tensor.
        - D (torch.Tensor): Diagonal matrix of A.
        - L (torch.Tensor): Lower triangular matrix of A.
        - U (torch.Tensor): Upper triangular matrix of A.
        - Dinv (torch.Tensor): Inverse of the diagonal matrix D.
        - Minv (torch.Tensor): Inverse of the matrix (D + L).
    """

    def __init__(self, n: int, A: np.ndarray, H: torch.Tensor, bs: int, y: torch.Tensor):
        """
        Initialize the base_model with the given parameters and decompose matrix A.

        Args:
            - n (int): Dimension of the solution.
            - A (np.ndarray): Input square matrix to decompose.
            - H (torch.Tensor): Random matrix H.
            - bs (int): Batch size.
            - y (torch.Tensor): Solution tensor.
        """
        self.n = n
        self.H = H
        self.bs = bs
        self.y = y

        self.A, self.D, self.L, self.U, self.Dinv, self.Minv = decompose_matrix(A)

class GS(base_model):
    """
    Class implementing the Gauss-Seidel algorithm for solving a linear system.

    Args:
        - n (int): Dimension of the solution.
        - A (np.ndarray): Input square matrix to decompose.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.

    Attributes:
        - n (int): Dimension of the solution.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - A (torch.Tensor): Original matrix converted to a torch tensor.
        - D (torch.Tensor): Diagonal matrix of A.
        - L (torch.Tensor): Lower triangular matrix of A.
        - U (torch.Tensor): Upper triangular matrix of A.
        - Dinv (torch.Tensor): Inverse of the diagonal matrix D.
        - Minv (torch.Tensor): Inverse of the matrix (D + L).
        - num_itr (int): The number of Gauss-Seidel iterations to perform.

    Methods:
        - iterate(num_itr: int) -> Tuple[torch.Tensor, list]:
            Performs the Gauss-Seidel iterations and returns the final solution and trajectory of solutions.
    """

    def __init__(self, n: int, A: np.ndarray, H: torch.Tensor, bs: int, y: torch.Tensor):
        """
        Initialize the Gauss-Seidel solver.

        Args:
            n (int): Dimension of the solution.
            A (np.ndarray): Input square matrix to decompose.
            H (torch.Tensor): Random matrix H.
            bs (int): Batch size.
            y (torch.Tensor): Solution tensor.
        """
        super(GS, self).__init__(n, A, H, bs, y)
        
    def iterate(self, num_itr: int) -> Tuple[torch.Tensor, list]:
        """
        Perform the Gauss-Seidel iterations and return the final solution.

        Args:
            - num_itr (int): The number of iterations to perform.

        Returns:
            - Tuple[torch.Tensor, list]: 
                - torch.Tensor: The final solution tensor of shape (bs, n).
                - list: List containing the trajectory of solutions throughout the iterations.
        """
        traj = []
        s = torch.zeros(self.bs, self.n).to(device)
        traj.append(s)

        yMF = torch.matmul(self.y, self.H.T)  # Assuming H is defined
        s = torch.matmul(yMF, self.Dinv)  # Generate batch initial solution vector

        for i in range(num_itr):
            temp = -torch.matmul(s, self.U) + yMF
            s = torch.matmul(temp, self.Minv)
            traj.append(s)

        return s, traj

class RI(base_model):
    """
    Class implementing the Richardson iteration algorithm for solving a linear system.

    Args:
        - n (int): Dimension of the solution.
        - A (np.ndarray): Input square matrix to decompose.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.

    Attributes:
        - n (int): Dimension of the solution.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - A (torch.Tensor): Original matrix converted to a torch tensor.
        - D (torch.Tensor): Diagonal matrix of A.
        - L (torch.Tensor): Lower triangular matrix of A.
        - U (torch.Tensor): Upper triangular matrix of A.
        - Dinv (torch.Tensor): Inverse of the diagonal matrix D.
        - Minv (torch.Tensor): Inverse of the matrix (D + L).

    Methods:
        iterate(num_itr: int) -> Tuple[torch.Tensor, list]:
            Performs the Richardson iterations and returns the final solution and trajectory of solutions.
    """

    def __init__(self, n: int, A: np.ndarray, H: torch.Tensor, bs: int, y: torch.Tensor):
        """
        Initialize the Richardson iteration solver.

        Args:
            - n (int): Dimension of the solution.
            - A (np.ndarray): Input square matrix to decompose.
            - H (torch.Tensor): Random matrix H.
            - bs (int): Batch size.
            - y (torch.Tensor): Solution tensor.
        """
        super(RI, self).__init__(n, A, H, bs, y)

    def iterate(self, num_itr: int) -> Tuple[torch.Tensor, list]:
        """
        Perform the Richardson iterations and return the final solution.

        Args:
            num_itr (int): The number of iterations to perform.

        Returns:
            - Tuple[torch.Tensor, list]:
                - torch.Tensor: The final solution tensor of shape (bs, n).
                - list: List containing the trajectory of solutions throughout the iterations.
        """
        traj = []
        omega = torch.tensor(0.25)
        s = torch.zeros(self.bs, self.n).to(device)
        traj.append(s)

        yMF = torch.matmul(self.y, self.H.T)  # Assuming H is defined
        s = torch.matmul(yMF, self.Dinv)  # Generate batch initial solution vector

        for i in range(num_itr):
            s = s + torch.mul(omega, (yMF - torch.matmul(s, self.A)))
            traj.append(s)

        return s, traj

class Jacobi(base_model):
    """
    Class implementing the Jacobi iteration algorithm for solving a linear system.

    Args:
        - n (int): Dimension of the solution.
        - A (np.ndarray): Input square matrix to decompose.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - omega (float, optional): Relaxation parameter for Jacobi iterations. Defaults to 0.2.

    Attributes:
        - n (int): Dimension of the solution.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - A (torch.Tensor): Original matrix converted to a torch tensor.
        - D (torch.Tensor): Diagonal matrix of A.
        - L (torch.Tensor): Lower triangular matrix of A.
        - U (torch.Tensor): Upper triangular matrix of A.
        - Dinv (torch.Tensor): Inverse of the diagonal matrix D.
        - Minv (torch.Tensor): Inverse of the matrix (D + L).
        - omega (torch.Tensor): Relaxation parameter for Jacobi iterations.

    Methods:
        iterate(num_itr: int) -> Tuple[torch.Tensor, list]:
            Performs the Jacobi iterations and returns the final solution and trajectory of solutions.
    """

    def __init__(self, n: int, A: np.ndarray, H: torch.Tensor, bs: int, y: torch.Tensor, omega: float = 0.2):
        """
        Initialize the Jacobi iteration solver.

        Args:
            - n (int): Dimension of the solution.
            - A (np.ndarray): Input square matrix to decompose.
            - H (torch.Tensor): Random matrix H.
            - bs (int): Batch size.
            - y (torch.Tensor): Solution tensor.
            - omega (float, optional): Relaxation parameter for Jacobi iterations. Defaults to 0.2.
        """
        super(Jacobi, self).__init__(n, A, H, bs, y)
        self.omega = torch.tensor(omega)

    def iterate(self, num_itr: int) -> Tuple[torch.Tensor, list]:
        """
        Perform the Jacobi iterations and return the final solution.

        Args:
            num_itr (int): The number of iterations to perform.

        Returns:
            - Tuple[torch.Tensor, list]:
                - torch.Tensor: The final solution tensor of shape (bs, n).
                - list: List containing the trajectory of solutions throughout the iterations.
        """
        traj = []
        s = torch.zeros(self.bs, self.n).to(device)
        traj.append(s)

        yMF = torch.matmul(self.y, self.H.T)  # Assuming H is defined
        s = torch.matmul(yMF, self.Dinv)  # Generate batch initial solution vector

        for i in range(num_itr):
            temp = torch.matmul(self.Dinv, (self.D - self.A))
            s = torch.matmul(s, temp) + torch.matmul(yMF, self.Dinv)
            traj.append(s)

        return s, traj

class SOR(base_model):
    """
    Class implementing the Successive Over-Relaxation (SOR) algorithm for solving a linear system.

    Args:
        - n (int): Dimension of the solution.
        - A (np.ndarray): Input square matrix to decompose.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - omega (float, optional): Relaxation parameter for SOR iterations. Defaults to 1.8.

    Attributes:
        - n (int): Dimension of the solution.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - A (torch.Tensor): Original matrix converted to a torch tensor.
        - D (torch.Tensor): Diagonal matrix of A.
        - L (torch.Tensor): Lower triangular matrix of A.
        - U (torch.Tensor): Upper triangular matrix of A.
        - Dinv (torch.Tensor): Inverse of the diagonal matrix D.
        - Minv (torch.Tensor): Inverse of the matrix (D + L).
        - omega (torch.Tensor): Relaxation parameter for SOR iterations.

    Methods:
        iterate(num_itr: int) -> Tuple[torch.Tensor, list]:
            Performs the SOR iterations and returns the final solution and trajectory of solutions.
    """

    def __init__(self, n: int, A: np.ndarray, H: torch.Tensor, bs: int, y: torch.Tensor, omega: float = 1.8):
        """
        Initialize the SOR solver.

        Args:
            - n (int): Dimension of the solution.
            - A (np.ndarray): Input square matrix to decompose.
            - H (torch.Tensor): Random matrix H.
            - bs (int): Batch size.
            - y (torch.Tensor): Solution tensor.
            - omega (float, optional): Relaxation parameter for SOR iterations. Defaults to 1.8.
        """
        super(SOR, self).__init__(n, A, H, bs, y)
        self.omega = torch.tensor(omega)

    def iterate(self, num_itr: int) -> Tuple[torch.Tensor, list]:
        """
        Perform the SOR iterations and return the final solution.

        Args:
            num_itr (int): The number of iterations to perform.

        Returns:
            - Tuple[torch.Tensor, list]:
                - torch.Tensor: The final solution tensor of shape (bs, n).
                - list: List containing the trajectory of solutions throughout the iterations.
        """
        traj = []
        n = self.y.size(1)

        inv_omega = torch.div(1, self.omega)
        invM_sor = torch.linalg.inv(self.D - torch.mul(inv_omega, self.L))

        s = torch.zeros(self.bs, n).to(device)
        traj.append(s)

        yMF = torch.matmul(self.y, self.H.T)
        s = torch.matmul(yMF, self.Dinv)

        for i in range(num_itr):
            temp = torch.mul((inv_omega - 1), self.D) + torch.mul(inv_omega, self.U)
            s = torch.matmul(s, torch.matmul(invM_sor, temp)) + torch.matmul(yMF, invM_sor)
            traj.append(s)

        return s, traj


class SOR_CHEBY(base_model):
    """
    Class implementing the SOR-Chebyshev algorithm for solving a linear system.

    Args:
        - n (int): Dimension of the solution.
        - A (np.ndarray): Input square matrix to decompose.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - omega (float, optional): Relaxation parameter for SOR iterations. Defaults to 1.8.
        - omegaa (float, optional): Acceleration parameter for SOR-Chebyshev iterations. Defaults to 0.8.
        - gamma (float, optional): Damping factor for SOR-Chebyshev iterations. Defaults to 0.8.

    Attributes:
        - n (int): Dimension of the solution.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - A (torch.Tensor): Original matrix converted to a torch tensor.
        - D (torch.Tensor): Diagonal matrix of A.
        - L (torch.Tensor): Lower triangular matrix of A.
        - U (torch.Tensor): Upper triangular matrix of A.
        - Dinv (torch.Tensor): Inverse of the diagonal matrix D.
        - Minv (torch.Tensor): Inverse of the matrix (D + L).
        - omega (torch.Tensor): Relaxation parameter for SOR iterations.
        - omegaa (torch.Tensor): Acceleration parameter for SOR-Chebyshev iterations.
        - gamma (torch.Tensor): Damping factor for SOR-Chebyshev iterations.

    Methods:
        iterate(num_itr: int) -> Tuple[torch.Tensor, list]:
            Performs the SOR-Chebyshev iterations and returns the final solution and trajectory of solutions.
    """

    def __init__(self, n: int, A: np.ndarray, H: torch.Tensor, bs: int, y: torch.Tensor, omega: float = 1.8, omegaa: float = 0.8, gamma: float = 0.8):
        """
        Initialize the SOR-Chebyshev solver.

        Args:
            - n (int): Dimension of the solution.
            - A (np.ndarray): Input square matrix to decompose.
            - H (torch.Tensor): Random matrix H.
            - bs (int): Batch size.
            - y (torch.Tensor): Solution tensor.
            - omega (float, optional): Relaxation parameter for SOR iterations. Defaults to 1.8.
            - omegaa (float, optional): Acceleration parameter for SOR-Chebyshev iterations. Defaults to 0.8.
            - gamma (float, optional): Damping factor for SOR-Chebyshev iterations. Defaults to 0.8.
        """
        super(SOR_CHEBY, self).__init__(n, A, H, bs, y)
        self.omega = torch.tensor(omega)
        self.omegaa = torch.tensor(omegaa)
        self.gamma = torch.tensor(gamma)

    def iterate(self, num_itr: int) -> Tuple[torch.Tensor, list]:
        """
        Perform the SOR-Chebyshev iterations and return the final solution.

        Args:
            num_itr (int): The number of iterations to perform.

        Returns:
            - Tuple[torch.Tensor, list]:
                - torch.Tensor: The final solution tensor of shape (bs, n).
                - list: List containing the trajectory of solutions throughout the iterations.
        """
        traj = []

        inv_omega = torch.div(1, self.omega)
        invM_sor = torch.linalg.inv(self.D - torch.mul(inv_omega, self.L))

        s = torch.zeros(self.bs, self.n).to(device)
        s_new = torch.zeros(self.bs, self.n).to(device)
        traj.append(s)

        yMF = torch.matmul(self.y, self.H.T)
        s = torch.matmul(yMF, self.Dinv)

        s_present = s
        s_old = torch.zeros(s_present.shape).to(device)

        for i in range(num_itr):
            temp = torch.mul((inv_omega - 1), self.D) + torch.mul(inv_omega, self.U)
            s = torch.matmul(s, torch.matmul(invM_sor, temp)) + torch.matmul(yMF, invM_sor)

            s_new = self.omegaa * (self.gamma * (s - s_present) + (s_present - s_old)) + s_old
            s_old = s
            s_present = s_new

            traj.append(s_new)

        return s_new, traj

class AOR(base_model):
    """
    Class implementing the Accelerated Over-Relaxation (AOR) algorithm for solving a linear system.

    Args:
        - n (int): Dimension of the solution.
        - A (np.ndarray): Input square matrix to decompose.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - omega (float, optional): Relaxation parameter for AOR iterations. Defaults to 0.3.
        - r (float, optional): Relaxation parameter r. Defaults to 0.2.

    Attributes:
        - n (int): Dimension of the solution.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - A (torch.Tensor): Original matrix converted to a torch tensor.
        - D (torch.Tensor): Diagonal matrix of A.
        - L (torch.Tensor): Lower triangular matrix of A.
        - U (torch.Tensor): Upper triangular matrix of A.
        - Dinv (torch.Tensor): Inverse of the diagonal matrix D.
        - Minv (torch.Tensor): Inverse of the matrix (D + L).
        - omega (torch.Tensor): Relaxation parameter for AOR iterations.
        - r (torch.Tensor): Relaxation parameter r.

    Methods:
        iterate(num_itr: int) -> Tuple[torch.Tensor, list]:
            Performs the AOR iterations and returns the final solution and trajectory of solutions.
    """

    def __init__(self, n: int, A: np.ndarray, H: torch.Tensor, bs: int, y: torch.Tensor, omega: float = 0.3, r: float = 0.2):
        """
        Initialize the AOR solver.

        Args:
            - n (int): Dimension of the solution.
            - A (np.ndarray): Input square matrix to decompose.
            - H (torch.Tensor): Random matrix H.
            - bs (int): Batch size.
            - y (torch.Tensor): Solution tensor.
            - omega (float, optional): Relaxation parameter for AOR iterations. Defaults to 0.3.
            - r (float, optional): Relaxation parameter r. Defaults to 0.2.
        """
        super(AOR, self).__init__(n, A, H, bs, y)
        self.omega = torch.tensor(omega)
        self.r = torch.tensor(r)

    def iterate(self, num_itr: int) -> Tuple[torch.Tensor, list]:
        """
        Perform the AOR iterations and return the final solution.

        Args:
            num_itr (int): The number of iterations to perform.

        Returns:
            - Tuple[torch.Tensor, list]:
                - torch.Tensor: The final solution tensor of shape (bs, n).
                - list: List containing the trajectory of solutions throughout the iterations.
        """
        traj = []

        M = (self.D - torch.mul(self.r, self.L))
        invM_aor = torch.linalg.inv(M)
        N = (torch.mul((1 - self.omega), self.D) + torch.mul((self.omega - self.r), self.L) + torch.mul(self.omega, self.U))

        s = torch.zeros(self.bs, self.n).to(device)
        traj.append(s)

        yMF = torch.matmul(self.y, self.H.T)
        s = torch.matmul(yMF, self.Dinv)

        for i in range(num_itr):
            s = torch.matmul(s, torch.matmul(invM_aor, N)) + torch.mul(self.omega, torch.matmul(yMF, invM_aor))
            traj.append(s)

        return s, traj


class AOR_CHEBY(base_model):
    """
    Class implementing the Accelerated Over-Relaxation (AOR) with Chebyshev acceleration algorithm for solving a linear system.

    Args:
        - n (int): Dimension of the solution.
        - A (np.ndarray): Input square matrix to decompose.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - omega (float, optional): Relaxation parameter for AOR iterations. Defaults to 0.1.
        - r (float, optional): Relaxation parameter r. Defaults to 0.1.

    Attributes:
        - n (int): Dimension of the solution.
        - H (torch.Tensor): Random matrix H.
        - bs (int): Batch size.
        - y (torch.Tensor): Solution tensor.
        - A (torch.Tensor): Original matrix converted to a torch tensor.
        - D (torch.Tensor): Diagonal matrix of A.
        - L (torch.Tensor): Lower triangular matrix of A.
        - U (torch.Tensor): Upper triangular matrix of A.
        - Dinv (torch.Tensor): Inverse of the diagonal matrix D.
        - Minv (torch.Tensor): Inverse of the matrix (D + L).
        - omega (torch.Tensor): Relaxation parameter for AOR iterations.
        - r (torch.Tensor): Relaxation parameter r.

    Methods:
        iterate(num_itr: int) -> Tuple[torch.Tensor, list]:
            Performs the AOR-Chebyshev iterations and returns the final solution and trajectory of solutions.
    """

    def __init__(self, n: int, A: np.ndarray, H: torch.Tensor, bs: int, y: torch.Tensor, omega: float = 0.1, r: float = 0.1):
        """
        Initialize the AOR-Chebyshev solver.

        Args:
            - n (int): Dimension of the solution.
            - A (np.ndarray): Input square matrix to decompose.
            - H (torch.Tensor): Random matrix H.
            - bs (int): Batch size.
            - y (torch.Tensor): Solution tensor.
            - omega (float, optional): Relaxation parameter for AOR iterations. Defaults to 0.1.
            - r (float, optional): Relaxation parameter r. Defaults to 0.1.
        """
        super(AOR_CHEBY, self).__init__(n, A, H, bs, y)
        self.omega = torch.tensor(omega)
        self.r = torch.tensor(r)

    def iterate(self, num_itr: int) -> Tuple[torch.Tensor, list]:
        """
        Perform the AOR-Chebyshev iterations and return the final solution.

        Args:
            num_itr (int): The number of iterations to perform.

        Returns:
            - Tuple[torch.Tensor, list]:
                - torch.Tensor: The final solution tensor of shape (bs, n).
                - list: List containing the trajectory of solutions throughout the iterations.
        """
        traj = []

        s = torch.zeros(self.bs, self.n).to(device)
        traj.append(s)

        yMF = torch.matmul(self.y, self.H.T)
        s = torch.matmul(yMF, self.Dinv)

        Y0 = s

        M = (self.D - torch.mul(self.r, self.L))
        invM = torch.linalg.inv(M)
        N = (torch.mul((1 - self.omega), self.D) + torch.mul((self.omega - self.r), self.L) + torch.mul(self.omega, self.U))
        temp = torch.matmul(invM, N)

        rho = torch.tensor(0.1)
        mu0 = torch.tensor(1)
        mu1 = rho
        xhat1 = torch.matmul(s, temp) + self.omega * torch.matmul(yMF, invM)
        Y1 = xhat1
        Y = Y1

        for i in range(num_itr):
            f = 2 / (rho * mu1)
            j = 1 / mu0
            c = f - j
            mu = 1 / c
            a = (2 * mu) / (rho * mu1)
            Y = torch.matmul((Y1 * a), torch.matmul(invM, N)) - (((mu / mu0)) * Y0) + (a * torch.matmul(yMF, invM))
            Y0 = Y1
            Y1 = Y
            mu0 = mu1
            mu1 = mu

            traj.append(Y)

        return Y, traj