import matplotlib.pyplot as plt

def plot_profile(x,observed,fitted,path):
    fig,(ax,res)=plt.subplots(2,1,figsize=(7,6),sharex=True)
    ax.plot(x,observed,label='Synthetic profile');ax.plot(x,fitted,'--',label='MSE fit')
    ax.set(ylabel='Profile amplitude');ax.legend()
    res.plot(x,fitted-observed);res.axhline(0,color='black',linewidth=.7)
    res.set(xlabel='Lateral position (model units)',ylabel='Residual')
    fig.tight_layout();fig.savefig(path,dpi=160);plt.close(fig)
