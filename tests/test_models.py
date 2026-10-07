import numpy as np
import pytest
from stairwear.wear_model import archard_wear,Material,Step,User
from stairwear.estimation import mixture_profile,fit_usage_mixture

def test_archard_linear_accumulation():
    material=Material('fictional',7e9,1e-6);step=Step(material,1.,.3,20)
    force=np.ones((20,20))*500
    step.apply_wear(force,.02);one=step.wear_depth.copy();step.apply_wear(force,.02)
    assert np.allclose(step.wear_depth,2*one,rtol=1e-12,atol=0.)
    assert archard_wear(1e-6,0,.02,7e9)==0

def test_synthetic_usage_recovery():
    x=np.linspace(-2.99,2.99,100);truth=.35;y=mixture_profile(x,truth)
    fit=fit_usage_mixture(x,y)
    assert fit.success
    assert fit.x==pytest.approx(truth,abs=1e-6)
    with pytest.raises(ValueError):mixture_profile([4.],truth)

def test_seeded_directional_force_centres():
    step=Step(Material('fictional',7e9,1e-6),1.,.3,100)
    np.random.seed(42);up=User('up',500,.02).get_force_distribution(step)
    np.random.seed(42);down=User('down',500,.02).get_force_distribution(step)
    assert step.Y[np.unravel_index(up.argmax(),up.shape)] < step.depth/2
    assert step.Y[np.unravel_index(down.argmax(),down.shape)] > step.depth/2
