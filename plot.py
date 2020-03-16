import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


print('Creating plot...')
CSV_PATH = '../COVID-19/dati-regioni/dpc-covid19-ita-regioni.csv'

REGIONE = 'Liguria'
#REGIONE = 'Lombardia'

regional_data = []

with open(CSV_PATH) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if row['denominazione_regione'] == REGIONE:
            regional_data.append(row)

matplotlib.rcParams['font.sans-serif'] = "Humor-Sans"
matplotlib.rcParams['font.family'] = "sans-serif"

fields2plot = ['totale_casi', 'terapia_intensiva', 'deceduti']
colors = ['r','g','b']
markers = ['o','v','s']

with plt.xkcd():   
    fig = plt.figure()
    plt.annotate('Dati: https://github.com/pcm-dpc/COVID-19', xy=(0,int(regional_data[-1]['totale_casi'])))
    plt.title('Situazione liguria')
    for data_field, col, mark in zip(fields2plot, colors, markers):
        readable_field = data_field.replace("_"," ")
        #~ print(readable_field)
        p = plt.plot([day_data['data'].split()[0] for day_data in regional_data],[int(day_data[data_field]) for day_data in regional_data])
        plt.setp(p, color=col, linewidth=2.0, marker=mark)
        plt.xticks(rotation=90)
        #~ if 'totale_casi' in data_field:
	    #~ plt.annotate('(??)', xy=(4.8,42), arrowprops=dict(arrowstyle='->'), xytext=(2, 50))
    plt.legend([data_field.replace("_"," ") for data_field in fields2plot], loc=6)
    plt.savefig('plots/all.png', bbox_inches='tight')
    #~ plt.show()


with plt.xkcd():   
    for data_field in fields2plot:
        readable_field = data_field.replace("_"," ")
        fig = plt.figure()
        p = plt.plot([day_data['data'].split()[0] for day_data in regional_data],[int(day_data[data_field]) for day_data in regional_data])
        plt.setp(p, color='r', linewidth=2.0, marker='o')
        plt.xticks(rotation=90)
        plt.annotate('Dati: https://github.com/pcm-dpc/COVID-19', xy=(0,int(regional_data[-1][data_field])))
        plt.title(readable_field+' liguria')
	    #~ if 'totale_casi' in data_field:
	    #~ plt.annotate('(??)', xy=(4.8,42), arrowprops=dict(arrowstyle='->'), xytext=(2, 50))
        plt.savefig('plots/'+data_field+'.png', bbox_inches='tight')
        #~ plt.show()

