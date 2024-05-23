import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics.pairwise import rbf_kernel, polynomial_kernel
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from .basecluster import BaseCluster

AFFINITY_METRICS = ['rbf', 'nearest_neighbors', 'poly']

class mvSpectralCluster(BaseCluster):
  r'''
  A class for multiview spectral clustering using the
    basic co-training framework [#1Clu]. This 
    implementation can handle two or more views.
  
  Parametrs
  ----------
  n_clusters : int, default: 1
              The number of clusters to form.
  max_iter : int, default: 1
             The maximum number of iterations for the clustering algorithm.
  
  info_view : int, default: None
              The most informative view. Final clustering will be performed 
              on the designated view alone. If it’s None the algorithm will 
              concatenate across all views and cluster on the result.
  
  affinity : string, default: 'poly'
            {‘rbf’,‘nearest_neighbors’ or ‘Poly’} The affinity metric used to 
            construct the affinity matrix.
  
  gamma : float, default: None
          Kernel coefficient for rbf and polynomial kernels
  
  n_neighbors : int default:10
                The number of neighbors to use for the nearest 
                neighbors kernel (only for ‘nearest_neighbors’ affinity metrix).
  
  n_init: int, default: 1
    The number of times the algorithm will be run with different centroid seeds
  
  random_state: int, default: None 
    The seed used by the random number generator for reproducibility
  
  
  References
  ----------
  [#1Clu] Abhishek Kumar and Hal Daume. "A co-training approach for
        multi-view spectral clustering." In Proceedings of the 28th
        International Conference on Machine Learning, page 393–400.
        Omnipress, 2011.
  '''
  def __init__(self, n_clusters=2, max_iter=5, info_view=None,
               affinity='poly', gamma=None, n_neighbors=10,
               n_init=1, random_state=None,device="cpu"):
    super().__init__(n_clusters=n_clusters, max_iter=max_iter, n_init=n_init, 
                     random_state=random_state)

    self.info_view = info_view
    self.affinity = affinity
    self.gamma = gamma
    self.n_neighbors = n_neighbors
    self.device = device if torch.cuda.is_available() else 'cpu'
    self.labels_ = None
    self.embedding_ = None

  def _affinity_mat(self, X):
    r'''
    Computes the affinity matrix based on the given kernel type.
    Parametrs
    ----------
    X : torch.Tensor
        The data in a single view.
    
    Returns
    -------
    sims: torch.Tensor
        The affinity matrix for data in a single view.
    '''
    gamma = self.gamma
    # If gamma is None, then compute default gamma value for this view
    if self.gamma is None:
      distances = torch.cdist(X, X)
      gamma = 1 / (2 * torch.median(distances) ** 2)
    
    # Compute the affinity matrix
    if self.affinity == 'rbf':
      print(gamma)
      X = X.to(self.device)
      sims = torch.tensor(rbf_kernel(X.cpu().numpy(), gamma=gamma.item()), 
                          device=self.device)
    elif self.affinity == 'nearest_neighbors':
      neighbor = NearestNeighbors(n_neighbors=self.n_neighbors)
      neighbor.fit(X.cpu().numpy())
      sims = torch.tensor(neighbor.kneighbors_graph(X.cpu().numpy()).toarray(),
                          device=self.device)
    elif self.affinity == 'poly':
      sims = torch.tensor(polynomial_kernel(X.cpu().numpy(), 
                                            gamma=gamma.item()), 
                                            device=self.device)
    else:
      raise ValueError('Invalid Kernel type')
    return sims

  def _compute_eigs(self, X):
    r'''Computes the top several eigenvectors of the
        normalized graph laplacian of a given similarity matrix.
    Parametrs
    ----------
    X : torch.Tensor
        The similarity matrix for data in a single view.
    
    Returns
    -------
    la_eigs: torch.Tensor
            The top n_cluster eigenvectors of the normalized graph
            laplacian.
    '''
    # Compute the normalized laplacian
    d_mat = torch.diag(torch.sum(X, axis=1))
    d_alt = torch.sqrt(torch.linalg.inv(d_mat))
    laplacian = d_alt @ X @ d_alt
    
    # Make the resulting matrix symmetric
    laplacian = (laplacian + laplacian.T) / 2.0

    # Obtain the top n_cluster eigenvectors of the laplacian
    eigenvalues, eigenvectors = torch.linalg.eigh(laplacian)
    idx = torch.argsort(eigenvalues, descending=True)[:self.n_clusters]
    la_eigs = eigenvectors[:, idx]
    return la_eigs

  def check_views(self, Xs):
    r''' Checks the number of views in data. Raises an error if the number
        of views is less than 2 or negative.
    Parameters
    ----------
    Xs: List of torch.Tensors
        The len of list must be equal to the number of views.
    '''
    if len(Xs) < 2:
      raise ValueError('Xs must have at least 2 views')

    self._n_views = len(Xs)
    if not isinstance(self.n_clusters, int) or self.n_clusters <= 0:
      raise ValueError('n_clusters must be a positive integer')
    return Xs

  def fit(self, Xs, y=None):
    r''' Performs clustering on the multi-view data.
    
    Parameters
    ----------
    Xs: List of torch.Tensors
        The len of list must be equal to the number of views.
    
    Returns
    -------
        self : returns an instance of self.
    '''

    self.check_views(Xs)

    #Compute similarity matrix
    sims = [self._affinity_mat(X) for X in Xs]

    # Initialize matrices of eigenvectors
    U_mats = [self._compute_eigs(sim) for sim in sims]

    #Iteratively compute new graph similarities, laplacians,and eigenvectors
    for iter in range(self.max_iter):
      eig_sums = [u_mat @ u_mat.T for u_mat in U_mats]
      U_sum = torch.sum(torch.stack(eig_sums), axis=0)
      new_sims = []

      for view in range(self._n_views):
        mat1 = sims[view] @ (U_sum - eig_sums[view])
        mat1 = (mat1 + mat1.T) / 2.0
        new_sims.append(mat1)
      U_mats = [self._compute_eigs(sim) for sim in new_sims]

    #Row Normalization
    for view in range(self._n_views):
      U_norm = torch.norm(U_mats[view], p=2, dim=1, keepdim=True)
      U_norm[U_norm == 0] = 1
      U_mats[view] /= U_norm

    #Performin K-means clustering
    kmeans = KMeans(n_clusters=self.n_clusters, n_init=self.n_init, 
                    random_state=self.random_state)

    #Use a single view if infor_view is not None
    if self.info_view is not None:
      self.embedding_ = U_mats[self.info_view].cpu().numpy()
      self.labels_ = kmeans.fit_predict(self.embedding_)

    #Concatenation across views if info_view is None
    else:
      self.embedding_ = torch.cat(U_mats, dim=1).cpu().numpy()
      self.labels_ = kmeans.fit_predict(self.embedding_)

    return self
