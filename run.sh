cd 
cd code/covid_project/COVID-19 && git pull && cd ../covid-19-liguria
python plot.py
MESSAGE=$(date)
git add plots/*
git commit -m "$MESSAGE"
git pull
git push
