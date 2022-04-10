import flask
import pandas as pd
import sqlite3

app = flask.Flask(__name__)

def calculate_results(form_data:dict) -> dict:
    '''
    Function to take in form_data dictionary and return dictionary with squat, bench deadlift score 
    
    Parameters:
        form_data (dict) - Dictionary containing values from input form

    Returns:
        results (dict) - Dictionary containing users sex, age, weight and equipment categories,
                         in addition to squat, bench and deadlift strength scores
    '''
    user_equipment = form_data['Equipment']
    user_sex = form_data['Sex']
    user_age = float(form_data['Age'])
    user_weight = float(form_data['Bodyweight'])
    user_squat = float(form_data['Squat'])
    user_bench = float(form_data['Bench'])
    user_deadlift = float(form_data['Deadlift'])
    user_total = user_bench + user_squat + user_deadlift

    #Define dataframe with user data
    user_df = pd.DataFrame({'Sex': [user_sex], 'Equipment': [user_equipment], 'Age': [user_age], 'BodyweightKg': [user_weight], 'Best3SquatKg': [user_squat], 'Best3BenchKg': [user_bench], 'Best3DeadliftKg': [user_deadlift], 'TotalKg': [user_total]})

    weight_cutoffs = {'F':[0,47,52,57,63,69,76,84,1000], 'M':[0,59,66,74,83,93,105,120,1000]}
    weight_labels = {'F':['47kg','52kg','57kg','63kg','69kg','76kg','84kg','84kg+'],'M':['59kg','66kg','74kg','83kg','93kg','105kg','120kg','120kg+']}
    user_df['weight_bin'] = pd.cut(user_df['BodyweightKg'], bins=weight_cutoffs[user_sex], labels=weight_labels[user_sex])

    cutoff_age = [15,20,25,30,35,40,45,50,55,60,100]
    age_labels = ['15-20','20-25','25-30','30-35','35-40','40-45','45-50','50-55','55-60','60-100']
    user_df['age_bin'] = pd.cut(user_df['Age'], bins=cutoff_age, labels=age_labels)


    #Calculate how user compares to historic data
    historic_data_df = get_data_tables(user_sex)

    people_in_group = len(historic_data_df[(historic_data_df['age_bin'] == user_df.loc[0,'age_bin']) & (historic_data_df['weight_bin'] == user_df.loc[0,'weight_bin']) & (historic_data_df['equipment'] == user_equipment)])
    #squat analysis
    people_with_lower_squat = len(historic_data_df[(historic_data_df['best3SquatKg'] < user_squat ) & (historic_data_df['age_bin'] == user_df.loc[0,'age_bin']) & (historic_data_df['weight_bin'] == user_df.loc[0,'weight_bin']) & (historic_data_df['equipment'] == user_equipment)])
    squat_result = str(round(people_with_lower_squat/people_in_group *100,1))+'%'
    #bench analysis
    people_with_lower_bench = len(historic_data_df[(historic_data_df['best3BenchKg'] < user_bench) & (historic_data_df['age_bin'] == user_df.loc[0,'age_bin']) & (historic_data_df['weight_bin'] == user_df.loc[0,'weight_bin']) & (historic_data_df['equipment'] == user_equipment)])
    bench_result = str(round(people_with_lower_bench/people_in_group *100,1))+'%'
    #deadlift analysis
    people_with_lower_deadlift = len(historic_data_df[(historic_data_df['best3DeadliftKg'] < user_deadlift) & (historic_data_df['age_bin'] == user_df.loc[0,'age_bin']) & (historic_data_df['weight_bin'] == user_df.loc[0,'weight_bin']) & (historic_data_df['equipment'] == user_equipment)])
    deadlift_result = str(round(people_with_lower_deadlift/people_in_group *100,1))+'%'
    #total analysis
    people_with_lower_total = len(historic_data_df[(historic_data_df['totalKg'] < user_total) & (historic_data_df['age_bin'] == user_df.loc[0,'age_bin']) & (historic_data_df['weight_bin'] == user_df.loc[0,'weight_bin']) & (historic_data_df['equipment'] == user_equipment)])
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

def get_data_tables(sex:str) -> pd.DataFrame:
    '''
    Function to read data stored in sql-lite database file 'database.db'
    Parameters:
        sex (str) - 'M' or 'F'
    Returns:
        df (pd.DataFrame) - Pandas dataframe containing data about lifters in this sex category
    '''

    database = sqlite3.connect('database.db')
    if sex =='M':
        df = pd.read_sql_query("SELECT * FROM male_lifters", database)
    elif sex =='F':
        df = pd.read_sql_query("SELECT * FROM female_lifters", database)
    return df



@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/results', methods = ['POST', 'GET'])
def results():
    if flask.request.method == 'GET':
        #user tries to access results URL directly
        return flask.render_template('results_unavailable.html')
    if flask.request.method == 'POST':
        #user tries to access results URL through data submission form
        form_data = flask.request.form.copy()
        results = calculate_results(form_data)
        return flask.render_template('results.html',results = results)


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)