import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as dt
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('Agg')

def logistic_model(x,a,b,c):
    return c/(1+np.exp(-(x-b)/a))
    
print('Creating plot for Italy...')
df = pd.read_csv('../../COVID-19/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv')
df = df.loc[:,['data','totale_casi']]
FMT = '%Y-%m-%dT%H:%M:%S'
date = df['data']
#~ print(date)
# Prepare data
df['data'] = date.map(lambda x : (datetime.strptime(x, FMT) - datetime.strptime("2020-01-01T00:00:00", FMT)).days  )
print(df)

x = list(df.iloc[:,0])
y = list(df.iloc[:,1])
print('Observed data')
print('Day number:',x)
print('Observed infected people:',y)

fit, cov = curve_fit(logistic_model,x,y,p0=[10,100,100000])
# logistic model estimated parameters
a=fit[0] # infection speed
b=fit[1] # logistic function inflection point
c=fit[2] # the number of infected people at the end of the infection
print(a,b,c)

errors = np.sqrt(np.diag(cov))
print('peak uncertainty day:',int(b), 'pm', int(errors[1]))

expected_epsilon = 1 # percentage to reach the final infected people 
sol = int(fsolve(lambda x : logistic_model(x,a,b,c) - (int(c) - expected_epsilon*int(c)/100),b))
print('The approximated end of the infection is the day:',sol)
print('The number of the final infected people is:',int(logistic_model(sol,a,b,c)),'pm',int(errors[2]) )

print('The approximated end of the infection will be in',sol-max(x),'days') # subtract today
print('The peak will be in',int(b)-max(x),'days')

print('Expected infected people (tomorrow):',int(logistic_model(max(x)+1,a,b,c)))
print('Expected infected people (after tomorrow):',int(logistic_model(max(x)+2,a,b,c)))

with plt.xkcd():  
    nstd = 1.0 # to draw 1-sigma uncertainty intervals
    #~ plt.annotate('Dati: https://github.com/pcm-dpc/COVID-19', xy=(0, y[-1]))
    pred_x = list(range(max(x),sol+1))
    plt.rcParams['figure.figsize'] = [8, 8]
    plt.rc('font', size=14)

    fit_up = fit + nstd * errors
    fit_dw = fit - nstd * errors
    fit_p    = logistic_model(x+pred_x, *fit)
    fit_up_p = logistic_model(x+pred_x, *fit_up)
    fit_dw_p = logistic_model(x+pred_x, *fit_dw)

    plt.plot(x+pred_x, fit_p, label="Expected infected", color="gray")
    plt.fill_between(x+pred_x, fit_up_p, fit_dw_p, alpha=.35, color="gray", label="1-$\sigma$ uncertainty interval")
    plt.scatter(x, y, label="Observed data", zorder=10, color="red", s=20)
    plt.scatter(b, logistic_model(b,a,b,c), zorder=10, facecolors='white', label="Expected peak", color="green", s=70)
    plt.scatter(sol, logistic_model(sol,a,b,c),zorder=10, label="Expected $\epsilon$-end", color="blue")
    plt.axhline(y=c,label='Final expected infected',color="magenta",linestyle="--",linewidth=0.9)
    ax = plt.axes()
    plt.grid(which='minor', alpha=0.2)
    ax.minorticks_on()
    plt.grid()
    ax.set_title('Logistic Model Covid-19 (Italy)')
    plt.legend(loc='lower right', prop={'size': 13})

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.gcf().autofmt_xdate()
    plt.xticks(fontsize=12)

    plt.xlabel("Date")
    plt.ylabel("Total number of infected people")
    #~ plt.show()
    plt.savefig('../plots/italy.png', bbox_inches='tight')
