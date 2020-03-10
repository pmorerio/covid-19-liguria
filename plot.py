import csv
import matplotlib
import matplotlib.pyplot as plt


CSV_PATH = '../COVID-19/dati-regioni/dpc-covid19-ita-regioni.csv'

REGIONE = 'Liguria'
#REGIONE = 'Lombardia'

regional_data = []

with open(CSV_PATH) as csv_file:
	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:
		if row['denominazione_regione'] == REGIONE:
			regional_data.append(row)

#~ print(regional_data)
#~ print(len(regional_data))

# Say, "the default sans-serif font is COMIC SANS"
matplotlib.rcParams['font.sans-serif'] = "Humor-Sans"
#~ # Then, "ALWAYS use sans-serif fonts"
matplotlib.rcParams['font.family'] = "sans-serif"
#~ myfont = {'fontname':'Humor Sans'}

with plt.xkcd():
	#~ fig = plt.figure()
    p = plt.plot([day_data['data'].split()[0] for day_data in regional_data],[int(day_data['totale_casi']) for day_data in regional_data])
    plt.setp(p, color='r', linewidth=2.0, marker='o')
    plt.xticks(rotation=45)
    #plt.show()
    plt.savefig('plots/totale_casi.png', bbox_inches='tight')
