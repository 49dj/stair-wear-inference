import argparse,json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from stairwear.estimation import mixture_profile,fit_usage_mixture
from stairwear.wear_model import Material,Step
from stairwear.simulation import Simulation
from stairwear.plotting import plot_profile

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('results'));args=ap.parse_args()
    x=np.linspace(-2.99,2.99,120);truth=.35
    y=mixture_profile(x,truth)
    fit=fit_usage_mixture(x,y)
    np.random.seed(2026)
    step=Step(Material('Fictional stone',7e9,1e-6),1.,.3,resolution=30)
    Simulation(step,1000,.02,days=1,up_ratio=.5,time_interval_minutes=60,peak_flow=3,off_peak_flow=1).run()
    args.output.mkdir(parents=True,exist_ok=True)
    plot_profile(x,y,mixture_profile(x,fit.x),args.output/'mixture_fit.png')
    report={'synthetic':True,'known_lambda':truth,'estimated_lambda':float(fit.x),'mse':float(fit.fun),
        'optimizer_success':bool(fit.success),'wear_grid_finite':bool(np.isfinite(step.wear_depth).all()),
        'raw_wear_increment_sum':float(step.wear_depth.sum()),'dimension_warning':'Original implementation omits contact area.'}
    (args.output/'demo.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':main()
