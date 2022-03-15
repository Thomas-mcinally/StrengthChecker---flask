'''
Code for StrengthChecker webapplication
- A website to easily be able to compare your SBD results to other lifters

TODO:
- Limit user inputs
- Improve aesthetics
- Get more balanced dataset
'''
from flask import Flask, render_template, request
import pandas as pd
import sqlite3

app = Flask(__name__)

def calculate_results(form_data:dict):
    '''
    Function to take in form_data dictionary and return dictionary with squat, bench deadlift score 
    
    Parameters:
        form_data (dict) - 

    Returns:
        results (dict) - 
    '''
    user_equipment = form_data['Equipment']
    user_sex = form_data['Sex']
    user_age = float(form_data['Age'])
    user_weight = float(form_data['Bodyweight'])
    user_squat = float(form_data['Squat'])
    user_bench = float(form_data['Bench'])
    user_deadlift = float(form_data['Deadlift'])
    user_total = user_bench + user_squat + user_deadlift

    df_M, df_F = get_data_tables()

    #define user dataframe
    user_df = pd.DataFrame({'Sex': [user_sex], 'Equipment': [user_equipment], 'Age': [user_age], 'BodyweightKg': [user_weight], 'Best3SquatKg': [user_squat], 'Best3BenchKg': [user_bench], 'Best3DeadliftKg': [user_deadlift], 'TotalKg': [user_total]})

    F_weight_cutoffs = [0,47,52,57,63,69,76,84,1000]
    F_weight_labels = ['47kg','52kg','57kg','63kg','69kg','76kg','84kg','84kg+']
    M_weight_cutoffs = [0,59,66,74,83,93,105,120,1000]
    M_weight_labels = ['59kg','66kg','74kg','83kg','93kg','105kg','120kg','120kg+']
    if user_sex == 'M':
        user_df['weight_bin'] = pd.cut(user_df['BodyweightKg'], bins=M_weight_cutoffs, labels=M_weight_labels)

    elif user_sex == 'F':
        user_df['weight_bin'] = pd.cut(user_df['BodyweightKg'], bins=F_weight_cutoffs, labels=F_weight_labels)

    cutoff_age = [15,20,25,30,35,40,45,50,55,60,100]
    age_labels = ['15-20','20-25','25-30','30-35','35-40','40-45','45-50','50-55','55-60','60-100']
    user_df['age_bin'] = pd.cut(user_df['Age'], bins=cutoff_age, labels=age_labels)

    

    #calculate results
    if user_sex == 'M':
        people_in_group = len(df_M[(df_M['age_bin'] == user_df.loc[0,'age_bin']) & (df_M['weight_bin'] == user_df.loc[0,'weight_bin']) & (df_M['equipment'] == user_equipment)])

        #squat analysis
        people_with_lower_squat = len(df_M[(df_M['best3SquatKg'] < user_squat ) & (df_M['age_bin'] == user_df.loc[0,'age_bin']) & (df_M['weight_bin'] == user_df.loc[0,'weight_bin']) & (df_M['equipment'] == user_equipment)])
        squat_result = str(round(people_with_lower_squat/people_in_group *100,1))+'%'
        #bench analysis
        people_with_lower_bench = len(df_M[(df_M['best3BenchKg'] < user_bench) & (df_M['age_bin'] == user_df.loc[0,'age_bin']) & (df_M['weight_bin'] == user_df.loc[0,'weight_bin']) & (df_M['equipment'] == user_equipment)])
        bench_result = str(round(people_with_lower_bench/people_in_group *100,1))+'%'
        #deadlift analysis
        people_with_lower_deadlift = len(df_M[(df_M['best3DeadliftKg'] < user_deadlift) & (df_M['age_bin'] == user_df.loc[0,'age_bin']) & (df_M['weight_bin'] == user_df.loc[0,'weight_bin']) & (df_M['equipment'] == user_equipment)])
        deadlift_result = str(round(people_with_lower_deadlift/people_in_group *100,1))+'%'
        #total analysis
        people_with_lower_total = len(df_M[(df_M['totalKg'] < user_total) & (df_M['age_bin'] == user_df.loc[0,'age_bin']) & (df_M['weight_bin'] == user_df.loc[0,'weight_bin']) & (df_M['equipment'] == user_equipment)])
        total_result = str(round(people_with_lower_total/people_in_group *100,1))+'%'

    if user_sex == 'F':
        people_in_group = len(df_F[(df_F['age_bin'] == user_df.loc[0,'age_bin']) & (df_F['weight_bin'] == user_df.loc[0,'weight_bin']) & (df_F['equipment'] == user_equipment)])
        
        #squat analysis
        people_with_lower_squat = len(df_F[(df_F['best3SquatKg'] < user_squat ) & (df_F['age_bin'] == user_df.loc[0,'age_bin']) & (df_F['weight_bin'] == user_df.loc[0,'weight_bin']) & (df_F['equipment'] == user_equipment)])
        squat_result = str(round(people_with_lower_squat/people_in_group *100,1))+'%'
        #bench analysis
        people_with_lower_bench = len(df_F[(df_F['best3BenchKg'] < user_bench) & (df_F['age_bin'] == user_df.loc[0,'age_bin']) & (df_F['weight_bin'] == user_df.loc[0,'weight_bin']) & (df_F['equipment'] == user_equipment)])
        bench_result = str(round(people_with_lower_bench/people_in_group *100,1))+'%'
        #deadlift analysis
        people_with_lower_deadlift = len(df_F[(df_F['best3DeadliftKg'] < user_deadlift) & (df_F['age_bin'] == user_df.loc[0,'age_bin']) & (df_F['weight_bin'] == user_df.loc[0,'weight_bin']) & (df_F['equipment'] == user_equipment)])
        deadlift_result = str(round(people_with_lower_deadlift/people_in_group *100,1))+'%'
        #total analysis
        people_with_lower_total = len(df_F[(df_F['totalKg'] < user_total) & (df_F['age_bin'] == user_df.loc[0,'age_bin']) & (df_F['weight_bin'] == user_df.loc[0,'weight_bin']) & (df_F['equipment'] == user_equipment)])
        total_result = str(round(people_with_lower_total/people_in_group *100,1))+'%'
    
    results = {
        'squat_result':squat_result,
        'bench_result':bench_result,
        'deadlift_result':deadlift_result,
        'total_result':total_result,
        'equipment_category':user_equipment,
        'sex_category':user_sex,
        'age_category':user_df.loc[0,'age_bin'],
        'weight_category':user_df.loc[0,'weight_bin']
    }

    return results

def get_data_tables():
    cnx = sqlite3.connect('database.db')

    df_M = pd.read_sql_query("SELECT * FROM male_lifters", cnx)
    df_F = pd.read_sql_query("SELECT * FROM female_lifters", cnx)
    return df_M, df_F




#startpage
@app.route('/')
def index():
    return render_template('index.html')

#result page
@app.route('/results', methods = ['POST', 'GET'])
def results():
    '''
    Note: request.form has a dictionary structure:
    form_data = {
        'field1_name' : 'field1_value',
        'field2_name' : 'field2_value',
        }
    '''
    if request.method == 'GET':
        return render_template('results_unavailable.html')
    if request.method == 'POST':
        form_data = request.form.copy()
        results = calculate_results(form_data)
        return render_template('results.html',results = results)


#page with info about deadlifts
@app.route('/deadlifts')
def deadlifts():
    return render_template('deadlifts.html')


if __name__=='__main__':
    app.run(debug=True, host='localhost', port=5000)