cd 
cd code/covid_project/COVID-19 && git pull && cd ../covid-19-liguria
python plot.py
cd italy
python plot_italy.py
cd ..
MESSAGE=$(date)
git add plots/*
git commit -m "$MESSAGE"
git push
