
import numpy as np
import random
import numpy as np
import glob
# import matplotlib.pyplot as plt

# seed for reproducibility
np.random.seed(12038)
random.seed(12038)

def split_data(X, y, num_test, seed = 123):
    random.seed(seed)
    n,_ = X.shape

    test_idx = random.sample(range(n), k = num_test)
    train_idx = list( set(range(n)) - set(test_idx) )

    X_train, X_test = X[train_idx,:], X[test_idx,:]
    y_train, y_test = y[train_idx]  , y[test_idx]

    return X_train, X_test, y_train, y_test

def split_data_vcv(X,y,vcv, num_test, seed = 123):
    random.seed(seed)
    n,_ = X.shape

    test_idx = random.sample(range(n), k = num_test)
    train_idx = list( set(range(n)) - set(test_idx) )

    X_train, X_test = X[train_idx,:], X[test_idx,:]
    y_train, y_test = y[train_idx]  , y[test_idx]
    vcv_train, vcv_test = vcv[train_idx,:][:,train_idx], vcv[test_idx,:][:,test_idx]

    return X_train, X_test, y_train, y_test, vcv_train, vcv_test

def R2(y, r):
    """
    Coefficient of determination
    r = y - y_pred
    """

    # r = y - y_pred
    u = r.T @ r
    v = y.T @ y - (len(y) * np.mean(y)**2)
    return 1 - (u/v)

def rmse(r):
    """
    Root Mean Squared Error
    r = y - y_pred
    """
    # r = y - y_pred
    return np.sqrt( np.mean( r**2 ) )

def distance_matrix(a, b):
    """
    l2 norm squared matrix
    """
    return np.linalg.norm(a[:, None, :] - b[None, :, :], axis=-1)**2

def RBF_kernel(a, b, gamma):
    """
    Radial Basis Function
    """

    tmp_rbf = -gamma * distance_matrix(a, b)
    np.exp(tmp_rbf, tmp_rbf) # RBF kernel. Inplace exponentiation
    return tmp_rbf

def linear_kernel(a, b, c):
    """
    Linear Kernel
    """
    XXt = a.dot(b.T)
    C = c * np.ones(XXt.shape)

    return XXt + C

def P_mat_simple(vcv):
    """
    get the square root of the inverse of the
    """

    # Kr = np.diag(1/np.sqrt(np.diag(vcv)))
    # vcv = Kr @ vcv @ Kr

    if isinstance(vcv, type(None)):
        return None

    L,Q = np.linalg.eig( vcv )
    P = Q @ np.diag( L**(-1/2) ) @ Q.T

    return P

def _scaler(ref, dat, use_sd = False):
    """
    Center and scale data
    """

    u = np.mean(ref, axis=0)
    centered = dat - u

    if use_sd:
        sd = np.std(ref, axis=0)
        sted = centered / sd

        return sted
    else:

        return centered

def scale_weighted_data(X, vcv, use_sd = False):
    """
    scale data by the square root of the inverse of the
    covariance matrix

    X: np.array
        data

    vcv: np.array
        covariance matrix
    """

    P = P_mat_simple(vcv)
    X_w_uc = P @ X
    return _scaler(X_w_uc, X_w_uc, use_sd)

def k_fold_cv(X, y, model, num_folds):
    """
    k-fold cross-validation
    """

    n, p = X.shape
    fold_size = n // num_folds

    all_errors = []
    for i in range(num_folds):

        test_idx = list(range(i * fold_size, (i + 1) * fold_size))
        train_idx = list(set(range(n)) - set(test_idx))

        X_train, X_test = X[train_idx, :], X[test_idx, :]
        y_train, y_test = y[train_idx], y[test_idx]
    
        model.fit(X_train, y_train)
        tmp_err = model.score(X_test, y_test, metric='rmse')
        all_errors.append(tmp_err)

    return np.mean(all_errors)

def k_fold_cv_random(X, y, model, params, folds=3, sample=500, verbose=True, seed=123):
    """
    Random search for hyperparameter tuning using k-fold cross-validation
    """
    np.random.seed(seed=seed)

    # make random choice from the grid of hyperparameters
    all_params = params.keys()
    tested_params = np.zeros((sample, len(all_params)))

    for n, k in enumerate(all_params):
        tested_params[:, n] = np.random.choice(params[k], sample)

    if verbose:
        # check tested_params are unique
        tested_params = np.unique(tested_params, axis=0)
        print("Number of unique hyperparameters: ", tested_params.shape[0])

    # shuffle the data
    n = X.shape[0]
    idx = np.arange(n)
    np.random.shuffle(idx)
    X = X[idx]
    y = y[idx]

    all_errors = []
    for vec in tested_params:
        tmp_params = dict(zip(all_params, vec))
        model.set_params(**tmp_params)
        tmp_err = k_fold_cv(X, y, model, folds)
        all_errors.append([tmp_params, tmp_err])

        if verbose:
            print("CV score: %s, Parameters %s" % (tmp_err, tmp_params))

    # take the best hyperparameters
    best_ = sorted(all_errors, key=lambda kv: kv[1], reverse=False)[0]

    if verbose:
        print("Best CV score: ", best_[1])

    return best_[0]


class LS:
    def __init__(self, fit_intercept=False, weighted=False) -> None:
        self.fit_intercept = fit_intercept
        self.weighted = weighted
        self.intercept = 0
        self.beta = np.array([])

    def fit(self, X, y,):
        n, p = X.shape

        if self.weighted:
            tmp_beta = np.linalg.solve(X.T @ X, X.T @ y)

        if self.fit_intercept:
            self.intercept = np.mean(y - X @ tmp_beta)

        self.beta = np.hstack((self.intercept, tmp_beta)) if self.fit_intercept else tmp_beta

    def predict(self, X):
        n, p = X.shape

        if self.fit_intercept:
            X = np.hstack((np.ones((n, 1)), X))

        return X @ self.beta

    def score(self, X_test, y_test, metric='rmse'):
        y_pred = self.predict(X_test)

        if metric == 'rmse':
            return np.sqrt(np.mean((y_pred - y_test) ** 2))
        else:
            u = ((y_test - y_pred) ** 2).sum()
            v = ((y_test - y_test.mean()) ** 2).sum()

            return 1 - (u / v)

class WKRR:
    def __init__(self, kernel='rbf', fit_intercept=True, check_cov=False) -> None:
        self.kernel = kernel

        if self.kernel == 'rbf':
            self.params = {'gamma': 0.1, 'lambda': 0.1}

        else:
            self.params = {'c': 0.1, 'lambda': 0.1}

        self.fit_intercept = fit_intercept
        self.check_cov = check_cov
        self.intercept = 0
        self.alpha = np.array([])
        self.X = np.array([])
        self.chol = False

    def set_params(self, **params):
        if self.kernel == 'rbf':
            self.params['gamma'] = params['gamma']

        else:
            self.params['c'] = params['c']

        self.params['lambda'] = params['lambda']

    def get_params(self):
        return self.params

    def P_mat(self, vcv):
        if isinstance(vcv, type(None)):
            return None

        if self.check_cov:
            self.assert_COV_sym(vcv)

        if self.chol:
            C = np.linalg.cholesky(vcv)
            P = np.linalg.inv(C)

        else:
            L, Q = np.linalg.eig(vcv)
            P = Q @ np.diag(L ** (-1 / 2)) @ Q.T

        if self.check_cov:
            self.assert_COV_decom(P, vcv)

        return P

    def assert_COV_sym(self, vcv, tol=1e-8):
        assert np.all(np.abs(vcv - vcv.T) < tol), 'not symmetric matrix'

    def assert_COV_decom(self, P, vcv):
        assert np.all(np.round(P.T @ P, 2) == np.round(np.linalg.inv(vcv), 2)), "P.T @ P != vcv^-1"

    def fit(self, X, y, vcv=None):
        self.X = X
        P = self.P_mat(vcv)

        if self.kernel == 'rbf':
            K_train = RBF_kernel(self.X, self.X, self.params['gamma'])
        else:
            K_train = linear_kernel(self.X, self.X, self.params['c'])

        self.alpha = self.opt_alpha(K_train, y, self.params['lambda'], P)

        if self.fit_intercept:
            self.intercept = np.mean(y - K_train @ self.alpha)

    def predict(self, X_test):
        assert len(self.alpha) > 0, "The model needs to be fitted first"

        if self.kernel == 'rbf':
            K_test = RBF_kernel(X_test, self.X, self.params['gamma'])
        else:
            K_test = linear_kernel(X_test, self.X, self.params['c'])

        return K_test @ self.alpha + self.intercept

    def score(self, X_test, y_test, vcv_test, metric='rmse'):
        y_pred = self.predict(X_test)

        if isinstance(vcv_test, type(None)):
            P = np.eye(X_test.shape[0])
        else:
            P = self.P_mat(vcv_test)

        werr = P @ (y_pred - y_test)  # weighted residuals

        if metric == 'rmse':
            return rmse(werr)
        else:
            Py = P @ y_test  # weighted targets
            return R2(Py, werr)

    def opt_alpha(self, K, y, reg_lam=None, P=None):

        n, _ = self.X.shape
        I = np.eye(K.shape[0])
        nlI = n * reg_lam * I

        if isinstance(P, type(None)):
            return np.linalg.solve(K + nlI, y)
        
        else:
            return P @ np.linalg.solve(P @ K @ P + nlI, P @ y)

class KRR(WKRR):

    def __init__(self, kernel='rbf', fit_intercept=True) -> None:
        super().__init__(kernel, fit_intercept)
        self.intercept = 0
        self.alpha = np.array([])
        self.X = np.array([])

    def fit(self, X, y):
        self.X = X
        self.y = y

        if self.kernel == 'rbf':
            K_train = RBF_kernel(self.X, self.X, self.params['gamma'])
            
        else:
            K_train = linear_kernel(self.X, self.X, self.params['c'])

        self.alpha = self.opt_alpha(K_train, self.y, self.params['lambda'])

        if self.fit_intercept:
            self.intercept = np.mean(y - K_train @ self.alpha)

    def opt_alpha(self, K, y, reg_lam=None):
        
        n, _ = self.X.shape
        I = np.eye(K.shape[0])
        nlI = n * reg_lam * I

        return np.linalg.solve(K + nlI, y)
        

    def score(self, X_test, y_test, metric='rmse'):
        y_pred = self.predict(X_test)

        if metric == 'rmse':
            return np.sqrt(np.mean((y_pred - y_test) ** 2))
        else:
            u = ((y_test - y_pred) ** 2).sum()
            v = ((y_test - y_test.mean()) ** 2).sum()

            return 1 - (u / v)


def myfunc(x, b=0, type='sin'):

    if type == 'sin':
        return np.sin( np.sum(x, axis=1) * 2).ravel()
    
    else:
        return np.sum(x, axis=1) ** b

def sim_data(vcv, mean_vector, b, 
             on_weighted=False, 
             add_noise = False, 
             noise_var = 1,
             n_var = 3, 
             extra_weights = [1,1,1], 
             type='pol',
             weight_with_vcv = True,
             vcv2 = None
             ):
    """
    Simulate data for n_var independent variables

    Parameters
    ----------
    vcv: np.array
        covariance matrix where data is simulated from
    
    mean_vector: np.array
        mean vector
    
    b: int
        power of the polynomial function

    on_weighted: bool
        whether to use weighted data or not to obtain the response variable.
        the weights are obtained using the 
        squared root of the inverse of 
        the covariance matrix

    add_noise: bool
        whether to add noise to the response variable

    noise_var: float
        variance of the noise

    extra_weights: list
        weights for the independent variables

    type: str
        type of the function to simulate the data
        if 'sin' then a sine function is used over the
        sum of the independent variables
        if 'pol' then a polynomial function is used over the
        sum of the independent variables
    
    weight_with_vcv: bool
        if true (default) the weighting of the values is 
        done using vcv. Otherwise, vcv2 is used

    vcv2: np.array
        if weight_with_vcv is false, then we use this covariance matrix
        to weight the data
    
    Returns
    -------
    X_w_uc: np.array
        weighted independent variables (uncentered)
    
    y_w_uc: np.array
        weighted response variable (uncentered)
    """
    # n_var = 3

    assert len(extra_weights) == n_var, "extra weights must have the same length as the number of predictors"

    X_uw_uc = np.zeros((vcv.shape[0], n_var))
    for j in range(n_var):
        X_uw_uc[:,j] = np.random.multivariate_normal(mean=mean_vector, cov=vcv)*extra_weights[j]


    if weight_with_vcv:
        P = P_mat_simple(vcv)

    else:
        assert isinstance(vcv2, np.ndarray), 'vcv2 must be a numpy array'
        P = P_mat_simple(vcv2)

    noise = np.random.normal(0, noise_var, X_uw_uc.shape[0])

    if on_weighted:
        X_w_uc = P @ X_uw_uc
        y_w_uc = myfunc(X_w_uc, b=b, type=type).ravel()

        if add_noise:
            y_w_uc += noise

        # plt.scatter(np.sum(X_w_uc, 1), y_w_uc, color='blue', alpha=0.5)
    else:
        y_uw_uc = myfunc(X_uw_uc, b=b, type=type).ravel()

        if add_noise:
            y_uw_uc += noise        

        X_w_uc = P @ X_uw_uc
        y_w_uc = P @ y_uw_uc

    return X_w_uc, y_w_uc

def get_Xy_w_uc(X_uw_uc, P, b, type, on_weighted, add_noise, noise):    

    if on_weighted:

        X_w_uc = P @ X_uw_uc
        y_w_uc = myfunc(X_w_uc, b=b, type=type).ravel()

        if add_noise:
            y_w_uc += noise

    else:
        y_uw_uc = myfunc(X_uw_uc, b=b, type=type).ravel()

        if add_noise:
            y_uw_uc += noise        

        X_w_uc = P @ X_uw_uc
        y_w_uc = P @ y_uw_uc

    return X_w_uc, y_w_uc

def get_Xy_wc(X_uw_uc, P_mat, b, type, on_weighted, add_noise, noise):    

    if on_weighted:
        
        X_w_uc = P_mat @ X_uw_uc
        y_w_uc = myfunc(X_w_uc, b=b, type=type).ravel()

        if add_noise:
            y_w_uc += noise

    else:
        y_uw_uc = myfunc(X_uw_uc, b=b, type=type).ravel()

        if add_noise:
            y_uw_uc += noise        

        X_w_uc = P_mat @ X_uw_uc
        y_w_uc = P_mat @ y_uw_uc

    X_wc = _scaler(X_w_uc, X_w_uc, use_sd= not False)
    y_wc = _scaler(y_w_uc, y_w_uc, use_sd=  False)

    return X_wc, y_wc

def sim_data_signal(vcv, mean_vector, b, 
             on_weighted=False, 
             add_noise = False, 
             noise_var = 1,
             n_var = 3, 
             extra_weights = [1,1,1], 
             type='pol'):
    """
    Simulate data for n_var independent variables

    Parameters
    ----------
    vcv: np.array
        covariance matrix where data is simulated from
    
    mean_vector: np.array
        mean vector
    
    b: int
        power of the polynomial function

    on_weighted: bool
        whether to use weighted data or not to obtain the response variable.
        the weights are obtained using the 
        squared root of the inverse of 
        the covariance matrix

    add_noise: bool
        whether to add noise to the response variable

    noise_var: float
        variance of the noise

    extra_weights: list
        weights for the independent variables

    type: str
        type of the function to simulate the data
        if 'sin' then a sine function is used over the
        sum of the independent variables
        if 'pol' then a polynomial function is used over the
        sum of the independent variables
    
    weight_with_vcv: bool
        if true (default) the weighting of the values is 
        done using vcv. Otherwise, vcv2 is used

    vcv2: np.array
        if weight_with_vcv is false, then we use this covariance matrix
        to weight the data
    
    Returns
    -------
    X_w_uc: np.array
        weighted independent variables (uncentered)
    
    y_w_uc: np.array
        weighted response variable (uncentered)
    """
    # n_var = 3

    assert len(extra_weights) == n_var, "extra weights must have the same length as the number of predictors"

    X_uw_uc = np.zeros((vcv.shape[0], n_var))
    for j in range(n_var):
        X_uw_uc[:,j] = np.random.multivariate_normal(mean=mean_vector, cov=vcv)*extra_weights[j]


    noise = np.random.normal(0, noise_var, X_uw_uc.shape[0])


    P1 = P_mat_simple(vcv)
    P2 = P_mat_simple(np.diag(np.diag(vcv)))
    
    (X_w_uc_1, y_w_uc_1) = get_Xy_w_uc(X_uw_uc, P1, b, type,
                                       on_weighted,
                                       add_noise, noise)

    (X_w_uc_2, y_w_uc_2) = get_Xy_w_uc(X_uw_uc, P2, b, type,
                                       on_weighted,
                                       add_noise, noise)

    return (X_w_uc_1, X_w_uc_2, y_w_uc_1, y_w_uc_2)


rbf_grid_params = {
    'lambda': np.logspace(-10, 5, 100, dtype=float, base=2),
    'gamma': np.logspace(-10, 5, 100, dtype=float, base=2),
}


path_trees = '/Users/ulises/Desktop/ABL/software/phylokrr/data/r_coal_sim_500spps_100trees'
vcvs = glob.glob(path_trees + '/*.csv')

vcv = np.loadtxt(vcvs[0], delimiter=',')
I_vcv = np.diag(np.diag(vcv))

# other_vcvs  = [ np.loadtxt(v, delimiter=',') for v in vcvs[1:2] ]
# other_vcvs += [ I_vcv ]
testing_covs = [vcv, I_vcv]


b = 3
on_weighted = True
add_noise = True
noise_var = 1
sample = 200
n_var = 2

n = vcv.shape[0]
mean_vector = np.zeros(n)
num_test = round(0.50 * n)

X_uw_uc = np.zeros((vcv.shape[0], n_var))
for j in range(n_var):
    X_uw_uc[:,j] = np.random.multivariate_normal(mean=mean_vector, cov=vcv)

# calculate the covariance matrix from X_uw_uc
# mean_vector = np.zeros(n)
# vcv = (1/n)*( X_uw_uc - np.mean(X_uw_uc, 0)) @ (X_uw_uc - np.mean(X_uw_uc, 0)).T
# vcv = np.cov(X_uw_uc, rowvar=not False)
np.cov(X_uw_uc)



# X_uw_uc = np.random.multivariate_normal(mean=mean_vector, cov=vcv, size=1).T
noise = np.random.normal(0, noise_var, X_uw_uc.shape[0])

# (1/n)*( X_uw_uc - np.mean(X_uw_uc, 0)) @ (X_uw_uc - np.mean(X_uw_uc, 0)).T
# np.cov(X_uw_uc, rowvar=False)



Y = np.zeros((n, len(testing_covs)))
F = np.zeros((n, len(testing_covs)))

krr_rbf_tmp = KRR(kernel='rbf', fit_intercept=  False)

for i in range(len(testing_covs)):
    # vcv_i
    # i = 5
    vcv_i = testing_covs[i]
    print("Testing cov matrix ", i)
    
    Pi = P_mat_simple(vcv_i)
    # np.sqrt(np.linalg.inv(vcv_i))

    (X_wc_tmp, y_wc_tmp) = get_Xy_wc(X_uw_uc, Pi, b, 'pol',
                                   on_weighted,
                                   add_noise, noise)

    (X_wc_train_tmp, X_wc_test_tmp,
     y_wc_train_tmp, y_wc_test_tmp,) = split_data(X_wc_tmp, y_wc_tmp, num_test=num_test, seed=12038)

    # if i == 0:
    rbf_param_tmp = k_fold_cv_random(X_wc_train_tmp, y_wc_train_tmp, krr_rbf_tmp, rbf_grid_params, verbose=False, folds=2, sample=sample)
    
    krr_rbf_tmp.set_params(**rbf_param_tmp)
    krr_rbf_tmp.fit(X_wc_train_tmp, y_wc_train_tmp)
    print(krr_rbf_tmp.score(X_wc_test_tmp, y_wc_test_tmp, metric='rmse'))

    # if i == 0:
    rbf_param_tmp2 = k_fold_cv_random(X_wc_test_tmp, y_wc_test_tmp, krr_rbf_tmp, rbf_grid_params, verbose=False, folds=2, sample=sample)

    krr_rbf_tmp.set_params(**rbf_param_tmp2)
    krr_rbf_tmp.fit(X_wc_test_tmp, y_wc_test_tmp)
    print(krr_rbf_tmp.score(X_wc_train_tmp, y_wc_train_tmp, metric='rmse'))

    Y[:,i] = np.hstack((y_wc_test_tmp, y_wc_train_tmp))
    F[:,i] = np.hstack((krr_rbf_tmp.predict(X_wc_test_tmp), krr_rbf_tmp.predict(X_wc_train_tmp)))

# krr_rbf1 = KRR(kernel='rbf', fit_intercept= not True)
# krr_rbf_2 = KRR(kernel='rbf', fit_intercept= not True)

# (X_w_uc_1,X_w_uc_2, 
#  y_w_uc_1,y_w_uc_2) = sim_data_signal(vcv, mean_vector, b=b, 
#                                       on_weighted=on_weighted,
#                                       add_noise=add_noise,
#                                       noise_var=noise_var)

# X_wc_1 = _scaler(X_w_uc_1, X_w_uc_1, use_sd= False)
# y_wc_1 = _scaler(y_w_uc_1, y_w_uc_1, use_sd= False)

# (X_wc_train_1, X_wc_test_1,
#  y_wc_train_1, y_wc_test_1,) = split_data(X_wc_1, y_wc_1, num_test=num_test, seed=12038)

# rbf_param_1 = k_fold_cv_random(X_wc_train_1, y_wc_train_1, krr_rbf1, rbf_grid_params, verbose=False, folds=3, sample=sample)

# krr_rbf1.set_params(**rbf_param_1)
# krr_rbf1.fit(X_wc_train_1, y_wc_train_1)
# print(krr_rbf1.score(X_wc_test_1, y_wc_test_1, metric='rmse'))

# X_wc_2 = _scaler(X_w_uc_2, X_w_uc_2, use_sd= False)
# y_wc_2 = _scaler(y_w_uc_2, y_w_uc_2, use_sd= False)

# (X_wc_train_2, X_wc_test_2,
#  y_wc_train_2, y_wc_test_2,) = split_data(X_wc_2, y_wc_2, num_test=num_test, seed=12038)

# rbf_param_2 = k_fold_cv_random(X_wc_train_2, y_wc_train_2, krr_rbf_2, rbf_grid_params, verbose=False, folds=3, sample=sample)

# krr_rbf_2.set_params(**rbf_param_2)
# krr_rbf_2.fit(X_wc_train_2, y_wc_train_2)
# print(krr_rbf_2.score(X_wc_test_2, y_wc_test_2, metric='rmse'))



# # merge two columns
# Y = np.stack((y_wc_test_1, y_wc_test_2), axis=1)
# F = np.stack((krr_rbf1.predict(X_wc_test_1), krr_rbf_2.predict(X_wc_test_2)), axis=1)

# Q = (Y - F).T @ (Y - F)

# print(Q)

# Import packages.
import cvxpy as cp
import numpy as np
# Y = 
Q = (Y - F).T @ (Y - F)
m = Q.shape[0]
ones = np.ones(m)

# Define and solve the CVXPY problem.
w = cp.Variable(m)
prob = cp.Problem(cp.Minimize( cp.quad_form(w, Q) ),
                 [ones.T @ w == 1, w >= 0])
prob.solve()

# Print result.
print(np.round(w.value,3))


