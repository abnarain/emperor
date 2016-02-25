from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams.update({'font.size': 10})
import pylab as plot

params = {'legend.labelspacing': 1}
plot.rcParams.update(params)

fig, ax = plt.subplots(1, 1,figsize=(8,5) )

x = np.linspace(norm.ppf(0.01), norm.ppf(0.9999), 100)
y1= norm.pdf(x,loc=-1)
y2= norm.pdf(x,loc=1)
ax.annotate('Threshold', xy=(.3, .4),  xycoords='data',
            xytext=(.4,.8), textcoords='axes fraction', arrowprops=dict(facecolor='black'),
                                    horizontalalignment='right',verticalalignment='top', )


ax.plot(x, y1,'b-', lw=2,  label='True Noise Distribtion')
ax.plot(x, y2,'r-', lw=2, label='Noise Distribution after Injection')
ax.plot((.4,.4),(0,0.5),color='black',lw=2)
ax.fill_between(x,y2,0, x<0, facecolor='green', alpha=0.6, label='Prob. of False Negative')
z,i,idx=[],-1,[]
for i in range(0,len(x)):
    if x[i] >= -.01 and x[i] <0.45:
        z.append(x[i])
        idx.append(i)
#ax.text(2, 6, 'Threshold detector', fontsize=4)


ax.fill_between(z,y1[idx[0]:idx[0]+len(idx)],0, facecolor='green', alpha=0.6 )
ax.fill_between(x,y1,0,x>.4 , facecolor='yellow', alpha=0.6, label='Prob. of False Positve')
#ax.legend(loc='best', frameon=False)
ax.set_xlabel(r'Weight of Amplitude of quadrature samples. wt$(y_{w})$')
ax.set_ylabel(r'Probability of Occurence P(wt($y_{w}$))')
#ax.set_title('Distribution of Amplitude of Noise')
plt.savefig('noise.pdf')
