cd ../COVID-19 && git pull && cd ../covid-19-liguria
python plot.py
MESSAGE=$(date)
git commit -m "$MESSAGE"
git push
