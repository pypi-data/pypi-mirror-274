from abc import abstractmethod

class BaseCluster():
  r'''
  A base class for all clustering algorithms. 

  Parameters
  ----------
  n_clusters: int, default: 2
              The number of clusters to form
    
  max_iter: int, default: 5
            The maximum number of iterations for the clustering algorithm.
    
  n_init: int, default: 1
          The number of times the algorithm will be run with different centroid seeds
  
  random_state: int, default: None 
                The seed used by the random number generator for reproducibility
  '''

  def __init__(self,n_clusters=1,max_iter=1,n_init=1,random_state = None):
    self.n_clusters = n_clusters
    self.max_iter = max_iter
    self.n_init = n_init
    self.random_state = random_state

  @abstractmethod
  def fit(self, Xs, y=None):
    return self

  @abstractmethod
  def predict(self, Xs):
    pass

  def fit_predict(self, Xs, y=None):
    self.fit(Xs)
    labels = self.labels_
    return labels
