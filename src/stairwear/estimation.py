"""Transparent Python port of the Q2_1 MATLAB MSE objective, not an MLE."""
import numpy as np
from scipy.stats import beta
from scipy.optimize import minimize_scalar

def mixture_profile(x,lam,L=3.,a=2.,b=5.):
    x=np.asarray(x,float)
    if L<=0 or a<=0 or b<=0 or not 0<=lam<=1:
        raise ValueError('L,a,b must be positive and lambda in [0,1].')
    if np.any(np.abs(x)>L): raise ValueError('Profile positions must lie in [-L,L].')
    u=0.95/(1.05*(1-lam+0.95*lam/1.05))
    z=(x+L)/(2*L)
    return beta.pdf(z,a,b)*lam*u+beta.pdf(z,b,a)*(1-u*lam)

def fit_usage_mixture(x,profile,L=3.,a=2.,b=5.):
    x,profile=np.asarray(x,float),np.asarray(profile,float)
    if x.ndim!=1 or x.shape!=profile.shape or len(x)<3 or not np.isfinite(x).all() or not np.isfinite(profile).all():
        raise ValueError('Provide matching finite 1D arrays with at least three samples.')
    result=minimize_scalar(lambda lam:float(np.mean((profile-mixture_profile(x,lam,L,a,b))**2)),
        bounds=(0.,1.),method='bounded',options={'xatol':1e-10})
    return result
