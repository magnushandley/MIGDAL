import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

file = open("/Users/magnus/Documents/MIGDAL/stripreader/argonitoenergies2.csv", 'r')
data = np.loadtxt(file,delimiter = ",")
data = np.transpose(data)
#data[1] = -data[1]*2e-9
numbins = 100
plotmax = 15


def fit_function(x, A, beta, B, mu, sigma):
    return (A * np.exp(-x/beta) + B * np.exp(-1.0 * (x - mu)**2 / (2 * sigma**2)))

print(data[0])
freq, bins = np.histogram(data,numbins)
#print(freq,bins)


binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
#
popt, pcov = curve_fit(fit_function, xdata=binscenters, ydata=freq,p0=[120, 2, 600, 3.75, 1],maxfev=1200)
print('popt=',popt)
xspace = np.linspace(0, plotmax, 100000)

#plt.hist(data[1], numbins,label=r'Rise times')
data = data*(5.9/popt[3])
plt.hist(data, numbins,color='gray')

plt.annotate('CF4 PE,\n5.9keV',
xy=(5.9, 1760), xycoords='data',
xytext=(20, 15), textcoords='offset points',size=6,
arrowprops=dict(
    arrowstyle="->",
    connectionstyle="arc,angleA=180,armA=40,angleB=90,armB=30,rad=7"))

plt.annotate('Ar PE+Auger,\n5.3keV \n(lost in CF4 peak)',
xy=(5.3, 1650), xycoords='data',
xytext=(-55, 15), textcoords='offset points',size=6,
arrowprops=dict(
    arrowstyle="->",
    connectionstyle="arc,angleA=0,armA=40,angleB=90,armB=30,rad=7"))

plt.annotate('Ar PE,\nPred: 2.7keV,\n seen: 2.6keV',
xy=(2.6, 320), xycoords='data',
xytext=(-25, 25), textcoords='offset points',size=6,
arrowprops=dict(
    arrowstyle="->",
    connectionstyle="arc,angleA=0,armA=40,angleB=90,armB=30,rad=7"))
    
plt.xlim(0,15)
plt.ylim(0,2200)
#plt.plot(xspace*(5.9/popt[3]), fit_function(xspace, *popt), color='darkorange', linewidth=1.5, label=r'$\sigma$ = 0.791 keV')

plt.xlabel('Energy [keV]')
plt.ylabel('Events')
plt.title('Energy spectrum of Fe55 in 80% CF4 20% Ar, based on ITO data')
#plt.legend()

#plt.savefig('fe55_cf4_ar_itospectrum_cropped.png', dpi=300)
plt.show()
