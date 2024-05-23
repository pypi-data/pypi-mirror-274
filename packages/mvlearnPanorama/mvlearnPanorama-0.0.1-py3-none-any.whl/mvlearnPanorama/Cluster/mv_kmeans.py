import torch
from joblib import Parallel, delayed
import numpy as np
from .basecluster import BaseCluster

class mvKMeansCluster(BaseCluster):
  def __init__(self, n_clusters=2, max_iter=5, 
               patience=3, tol=0.0001,init="random",
               n_jobs=-1,n_init=1,random_state = None):
    r'''
    Multiview k-means clustering algorithm by co-Em algorithm [#2Clu]_. 
    Multi-view k-means clustering adapts the traditional k-means clustering
    algorithm to handle two views of data.

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

    init: str, default:k-means++
        {Random or k-means++} The method for initialization of cluster centers for k-means 
        based clustering algorithm
    
    n_jobs: int, default: -1
            The number of jobs to run in parallel. n_init will start parallelly with n_jobs
            workers.
    n_init: int, default: 1
            The number of times the algorithm will be run with different centroid seeds
  
    random_state: int, default: None 
                  The seed used by the random number generator for reproducibility
    
    Co-EM Algorithm
    -----------------

    Input: Unlabeled data D with 2 views

    #. Initialize :math:`\Theta_0^{(2)}`, T, :math:`t = 0`.

    #. E step for view 2: compute expectation for hidden variables given

    #. Loop until stopping criterion is true:

        a. For v = 1 ... 2:

           i. :math:`t = t + 1`

           ii. M step view v: Find model parameters :math:`\Theta_t^{(v)}`
               that maximize the likelihood for the data given the expected
               values for hidden variables of view :math:`\overline{v}` of
               iteration :math:`t` - 1

           iii. E step view :math:`v`: compute expectation for hidden
                variables given the model parameters :math:`\Theta_t^{(v)}`


    #. return combined :math:`\hat{\Theta} = \Theta_{t-1}^{(1)} \cup
       \Theta_t^{(2)}`

    The final assignment of examples to partitions is performed by assigning
    each example to the cluster with the largest averaged posterior
    probability over both views.

    References
    ----------
    [#2Clu] Steffen Bickel and Tobias Scheffer. Multi-view clustering. In
            Proceedings of the Fourth IEEE International Conference on Data
            Mining, page 19–26. IEEE Computer Society, 2004.
    '''
    super().__init__(n_clusters=n_clusters, max_iter=max_iter,
                     n_init=n_init,random_state = random_state)
    self.patience = patience
    self.tol = tol
    self.centroids = list()
    self.init = init
    self.n_jobs = n_jobs

  def _compute_distance(self, X, centroids):
    r'''Compute the Euclidian distance between X and centroids
    
    Parameters
    ---------
    X: torch.Tensor
      shape (n_sample,n_features) a tensor presenting a single view
    
    centroids: torch.Tensor
                centroids for a single-view
    Returns
    -------
    dist: torch.Tensor
          Euclidian distance computed between X and centroids
    '''
    return torch.cdist(X,centroids)

  def _init_centroids(self,Xs):
    r''' initialize the centroid based on the given initialization method.
    Paramters
    ---------
    Xs : list of torch.Tensor
         - Xs length: n_views
         - Xs[i] shape: (n_samples, n_features_i)
    Returns
    -------
    centroids : list of torch.Tensor
            - centroids length: n_views
            - centroids[i] shape: (n_clusters, n_features_i)
    '''
    if self.init == "random":
      indices = np.random.choice(Xs[0].shape[0], self.n_clusters).tolist()
      centers1 = Xs[0][indices]
      centers2 = Xs[1][indices]
      centroids = [centers1, centers2]
    elif self.init == "k-means++":
      indices = list()
      centers2 = list()
      indices.append(int(torch.randint(0,Xs[1].shape[0],(1,))))
      centers2.append(Xs[1][indices[0], :])

      # Compute the remaining n_cluster centroids
      for cent in range(self.n_clusters - 1):
        dists = self._compute_distance(torch.stack(centers2),Xs[1])
        dists = torch.min(dists, dim=0)
        max_index = torch.argmax(dists.values).item()
        indices.append(int(max_index))
        centers2.append(Xs[1][max_index])

      centers1 = Xs[0][indices]
      centers2 = torch.stack(centers2)
      centroids = [centers1, centers2]
    else:
      raise ValueError('Invalid initialization method.')
    return centroids

  def _em_step(self, X, partition, centroids):
    r'''
    This function computes one iteration of expectation-maximization.
    Parameters
    ----------
    X: torch.Tensor, shape (n_samples, n_features)
            tensor presenting a single view of the data.

    partition: torch.Tensor, shape (n_samples,)
            tensor of cluster labels indicating the cluster to which
            each data sample is assigned.

    centroids: torch.Tensor , shape (n_clusters, n_features)
            The current cluster centers.
    Returns
    -------
    new_parts: torch.Tensor, shape (n_samples,)
            The new cluster assignments for each sample in the data

    new_centers: torch.Tensor, shape (n_clusters, n_features)
            The updated cluster centers.

    o_funct: float
            The new value of the objective function.
    '''
    n_samples = X.shape[0]
    new_centers = list()
    for cl in range(self.n_clusters):
        # Recompute centroids using samples from each cluster
        mask = (partition == cl)
        if (torch.sum(mask) == 0):
          new_centers.append(centroids[cl])
        else:
          cent = torch.mean(X[mask], dim=0, dtype=float)
          new_centers.append(cent)

    new_centers = torch.stack(new_centers)

    # Compute expectation and objective function
    distances = self._compute_distance(X, new_centers)
    new_parts = torch.argmin(distances, dim=1).squeeze()
    min_dists = distances[torch.arange(n_samples), new_parts]
    o_funct = torch.sum(min_dists)

    return new_parts, new_centers, o_funct

  def _one_init (self,Xs):
    r'''Run the algorithm for one random initialization.

    Parameters
    ----------
    Xs : list of torch.Tensor
            - Xs length: n_views
            - Xs[i] shape: (n_samples, n_features_i)
    Returns
    -------
    intertia: int
              The final intertia for this run.

    centroids : list of torch.Tensor
            - centroids length: n_views
            - centroids[i] shape: (n_clusters, n_features_i)
    '''
    # Initialize centroids for clustering
    centroids = self._init_centroids(Xs)

    # Initializing partitions, objective value, and loop vars
    distances = self._compute_distance(Xs[1], centroids[1])
    parts = torch.argmin(distances, dim=1).squeeze()
    partitions = [None, parts]
    objective = [torch.tensor(float(10000000)), torch.tensor(float(10000000))]
    o_funct = [None, None]
    iter_stall = [0, 0]
    iter_num = 0
    max_iter = self.max_iter

    # While objective is still decreasing and iterations < max_iter
    while(max(iter_stall) < self.patience and iter_num < max_iter):

        for vi in range(2):
            pre_view = (iter_num + 1) % 2
            # Switch partitions and compute maximization
            partitions[vi], centroids[vi], o_funct[vi] = self._em_step(
                Xs[vi], partitions[pre_view], centroids[vi])
        iter_num += 1
        # Track the number of iterations without improvement
        for view in range(2):
          if(objective[view] - o_funct[view] > self.tol * torch.abs(objective[view])):
              objective[view] = o_funct[view]
              iter_stall[view] = 0
          else:
              iter_stall[view] += 1
    intertia = torch.sum(torch.tensor(objective,dtype=float))
    return intertia, centroids

  def _final_centroids(self, Xs, centroids):
    r'''Computes the final cluster centroids based on consensus samples across
        both views. Consensus samples are those that are assigned to the same
        partition in both views.
  
      Parameters
      ----------
      Xs : list of torch.Tensor
          - Xs length: n_views
          - Xs[i] shape: (n_samples, n_features_i)
  
      centroids : list of torch.Tensor
                - centroids length: n_views
                - centroids[i] shape: (n_clusters, n_features_i)
      '''
    # Compute consensus vectors for final clustering
    v1_consensus = list()
    v2_consensus = list()
    v1_distances = self._compute_distance(Xs[0], centroids[0])
    v1_partitions = torch.argmin(v1_distances, dim=1).squeeze()
    v2_distances = self._compute_distance(Xs[1], centroids[1])
    v2_partitions = torch.argmin(v2_distances, dim=1).squeeze()
    for clust in range(self.n_clusters):
      # Find data points in the same partition in both views
      part_indices = (v1_partitions == clust) * (v2_partitions == clust)

      # Recompute centroids based on these data points
      if (torch.sum(part_indices) != 0):
        cent1 = torch.mean(Xs[0][part_indices], dim=0)
        v1_consensus.append(cent1)
        cent2 = torch.mean(Xs[1][part_indices], dim=0)
        v2_consensus.append(cent2)

    # Check if there are no consensus vectors
    self.centroids = [None, None]
    if (len(v1_consensus) == 0):
      print('No distinct cluster centroids have been found.')
    else:
      self.centroids[0] = torch.stack(v1_consensus)
      self.centroids[1] = torch.stack(v2_consensus)
      self.n_clusters = self.centroids[0].shape[0]
  def check_views(self, Xs):
    r''' Checks the number of views
    Parameters
    ----------
    Xs : list of torch.Tensor
         - Xs length: n_views
         - Xs[i] shape: (n_samples, n_features_i)
    '''
    if len(Xs) != 2:
      raise ValueError('Number of views of data must be 2')
  def fit(self,Xs):
    r''' Performs clustering algorithm on multi-view data
    Parameters
    ----------
    Xs : list of torch.Tensor
         - Xs length: n_views
         - Xs[i] shape: (n_samples, n_features_i)
    
    '''
    self.check_views(Xs)
    if self.random_state is not None:
      torch.manual_seed(self.random_state)
    if self.n_jobs == -1:
      # Running algorithm only with one centroid seed
      inertia, centroids = self._one_init(Xs)
      self._final_centroids(Xs,centroids)
      self.labels_ = self.predict(Xs)
      return self
    else:
      #Ranning algorithm with n_init centroid seeds
      run_results = Parallel(n_jobs=self.n_jobs)(
      delayed(self._one_init)(Xs) for _ in range(self.n_init))
      intertias, centroids = zip(*run_results)
      max_ind = np.argmax(intertias)
      self._final_centroids(Xs,centroids[max_ind])
      self.labels_ = self.predict(Xs)
      return self

  def predict(self, Xs):
    r''' Predicts for the label for each input data points
    Parameters
    ----------
    Xs : list of torch.Tensor
         - Xs length: n_views
         - Xs[i] shape: (n_samples, n_features_i)
    '''
    dist1 = self._compute_distance(Xs[0], self.centroids[0])
    dist2 = self._compute_distance(Xs[1], self.centroids[1])
    dist_metric = dist1 + dist2
    labels = torch.argmin(dist_metric, dim=1).squeeze()
    return labels
