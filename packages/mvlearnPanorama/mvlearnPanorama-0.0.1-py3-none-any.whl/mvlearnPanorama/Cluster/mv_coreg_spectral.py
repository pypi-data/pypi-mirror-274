import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics.pairwise import rbf_kernel, polynomial_kernel
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from .mv_spectral import mvSpectralCluster

class mvCoregSpectral(mvSpectralCluster):
  r'''An implementation of co-regularized multi-view spectral clustering 
    based on an unsupervied version of the co-training framework.
    This uses the pairwise co-regularization scheme [#4Clu]. 
    This algorithm can handle 2 or more views of data.
    Parametrs
  ----------
  n_clusters : int, default: 1
              The number of clusters to form.
  max_iter : int, default: 1
             The maximum number of iterations for the clustering algorithm.
  
  v_lambda : float, default: 2
             The regularization parameter

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
[#4Clu] Abhishek Kumar, Piyush Rai, and Hal Daume.  Co-regularized
        multi-view spectral clustering. In Proceedings of the 24th
        International Conference on Neural Information Processing Systems,
        page 1413–1421. Curran Associates Inc., 2011.
  '''
  def __init__(self, n_clusters=2, max_iter=5, v_lambda=2,
              info_view=None, affinity='poly', gamma=None, 
              n_neighbors=10, n_init=1, random_state=None,device="cpu"):

    super().__init__(n_clusters=n_clusters, max_iter=max_iter, 
                     info_view=info_view, affinity=affinity, gamma=gamma, 
                     n_neighbors=n_neighbors, n_init=n_init, 
                     random_state=random_state,device=device)

    self.v_lambda = v_lambda
    self.objective_ = None

  def _init_umat(self, X):
    r'''Computes the top (n-clusters) number of eigenvectors of the
        normalized graph laplacian of a given similarity matrix.
        
    Parameters
    ----------
    X : torch.Tensor
        The similarity matrix for data in a single view.
        
    Returns
    -------
    u_mat: torch.Tensor
        The top n_cluster eigenvectors of the normalized graph laplacian.
    laplacian: torch.Tensor
        The normalized graph laplacian for the similarity matrix.
    obj_val: torch.Tensor
        The updated value for the objective of the clustering for given view.
    '''

    #Compute normalized laplacian
    X = torch.tensor(X, device=self.device)
    d_mat = torch.diag(torch.sum(X, dim=1))
    d_alt = torch.sqrt(torch.linalg.inv(d_mat))
    laplacian = d_alt @ X @ d_alt

    laplacian = (laplacian + laplacian.T) / 2.0

    #Get top n-clusters eigenvectors of the laplacian
    u_mat, d_mat, _ = torch.svd(laplacian)
    u_mat = u_mat[:, :self.n_clusters]
    d_mat = d_mat[:self.n_clusters]
    obj_val = torch.sum(d_mat)

    return u_mat, laplacian, obj_val

  def fit(self, Xs):
    r''' Performs clustering on the multi-view data.
    
    Parameters
    ----------
    Xs: List of torch.Tensors
        The len of list must be equal to the number of views.

    Returns
    -------
        self : returns an instance of self.
    '''
    #Check number of views
    self.check_views(Xs)
    
    #Compute similarity matrix
    sims = [self._affinity_mat(X) for X in Xs]
    check_u_mats = list()

    #Intialize the matrics for eigen vectors
    U_mats = []
    L_mats = []
    obj_vals = torch.zeros((self._n_views, self.max_iter), device=self.device)
    for ind in range(len(sims)):
      u_mat, l_mat, o_val = self._init_umat(sims[ind])
      U_mats.append(u_mat)
      L_mats.append(l_mat)
      obj_vals[ind, 0] = o_val

    check_u_mats.append(U_mats[0])

    n_items = Xs[0].shape[0]

    # Computing all U's iteratively
    for it in range(1, self.max_iter):

      #Alternating maximization by cycling through all pairs of views and updating all except view 1
      for v1 in range(1, self._n_views):

        # Computing the regularization term for view v1
        l_comp = torch.zeros((n_items, n_items), device=self.device)
        for v2 in range(self._n_views):
          if v1 != v2:
            l_comp = l_comp + U_mats[v2] @ U_mats[v2].T
        l_comp = (l_comp + l_comp.T) / 2
        
        # Adding the symmetrized graph laplacian for view v1
        l_mat = L_mats[v1] + self.v_lambda * l_comp
        U_mats[v1], d_mat, _ = torch.svd(l_mat)
        U_mats[v1] = U_mats[v1][:, :self.n_clusters]
        d_mat = d_mat[:self.n_clusters]
        obj_vals[v1, it] = torch.sum(d_mat)

      # Update U and the objective function value for view 1
      l_comp = torch.zeros((n_items, n_items), device=self.device)
      for vi in range(self._n_views):
        if vi != 0:
          l_comp = l_comp + U_mats[vi] @ U_mats[vi].T
      l_comp = (l_comp + l_comp.T) / 2
      l_mat = L_mats[0] + self.v_lambda * l_comp
      U_mats[0], d_mat, _ = torch.svd(l_mat)
      U_mats[0] = U_mats[0][:, :self.n_clusters]
      d_mat = d_mat[:self.n_clusters]
      obj_vals[0, it] = torch.sum(d_mat)
      check_u_mats.append(U_mats[0])
    self.objective_ = obj_vals.cpu().numpy()

    # Create final spectral embedding to cluster
    V_mat = torch.hstack(U_mats)
    norm_v = torch.sqrt(torch.diag(V_mat @ V_mat.T))
    norm_v[norm_v == 0] = 1
    self.embedding_ = torch.linalg.inv(torch.diag(norm_v)) @ V_mat

    self.embedding_ = self.embedding_.cpu().numpy()

    #Performing k-means clustering on embedding
    kmeans = KMeans(n_clusters=self.n_clusters, n_init=self.n_init,
                    random_state=self.random_state)
    self.labels_ = kmeans.fit_predict(self.embedding_)
    return self
