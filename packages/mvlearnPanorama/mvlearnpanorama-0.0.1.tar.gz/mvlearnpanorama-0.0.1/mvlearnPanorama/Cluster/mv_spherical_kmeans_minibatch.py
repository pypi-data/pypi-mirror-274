import torch
from joblib import Parallel, delayed
import numpy as np
import torch.nn.functional as F
from .mv_kmeans_minibatch import mvKMeansMinibatch

class mvSphericalKMeansMinibatch(mvKMeansMinibatch):
  r'''
  An optimized implementation of multi-view spherical K-Means.
  This implementation closely follows the implementation of mvSphericalKMeans 
  with the minibatch provision. The minibatch implementation helps in optimizing 
  the memory usage in computing resources.
  
  Parameters
  ----------
  n_clusters: int, default: 2
              The number of clusters to form
  
  max_iter: int, default: 5
            The maximum number of iterations for the clustering algorithm.
  
  patience: int, default: 3
            The number of iterations to wait for convergence before stopping early.
  
  tol: float, default: 0.0001
       The tolerance for convergence, determining when to stop the algorithm.

  init: str, default: k-means++
        {Random or k-means++} The method for initialization of cluster centers for k-means 
        based clustering algorithm
  
  batch_size: int default: 4
              Mini batch-size
    
  n_jobs: int, default: -1
          The number of jobs to run in parallel. n_init will start parallelly with n_jobs
          workers.
  
  n_init: int, default: 1
          The number of times the algorithm will be run with different centroid seeds
  
  random_state: int, default: None 
                The seed used by the random number generator for reproducibility
  '''
  def __init__(self, n_clusters=2, max_iter=5, 
               patience=3, tol=0.0001, init='random', 
               batch_size=4, n_jobs=-1, n_init=1, random_state=None):
    super().__init__(n_clusters=n_clusters,max_iter=max_iter, 
                    patience=patience,tol=tol,init=init, batch_size=batch_size,
                    n_jobs=n_jobs,n_init=n_init,random_state=random_state)

  def _compute_dist(self, X, Y):
    r''' Compute the Cosine distance between X and Y
    
    Parameters
    ---------
    X: torch.Tensor
      shape (n_sample,n_features)
    
    Y: torch.Tensor
       shape (n_sample,n_features)
    Returns
    -------
    dist: torch.Tensor
          Cosine distance computed between X and Y.
    '''
    cosine_dist = 1 - torch.mm(X, Y.T)
    return cosine_dist

  def fit(self, Xs, y=None):
    r''' Performs clustering algorithm on multi-view data
    Parameters
    ----------
    Xs : list of torch.Tensor
         - Xs length: n_views
         - Xs[i] shape: (n_samples, n_features_i)
    '''
    self.check_views(Xs)
    super().fit(Xs)
    for view in range(len(self.centroids)):
      self.centroids[view] = F.normalize(self.centroids[view], dim=1)
