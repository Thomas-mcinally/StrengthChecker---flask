# StrengthChecker

StengthChecker is a webapplication which enables users to compare their Squat/Bench/Deadlift numbers to people of same sex, age group and weightclass

## Preview of index and result pages

![](static/images/Home_page.JPG)

![](static/images/results_page.JPG)

## Steps to run locally
1. python setup.py install
2. python app.py

## Steps to run with Docker
1. docker build -t strengthchecker_docker .
2. docker run -p 5000:5000 -d strengthchecker_docker
