import flask
import pandas as pd
import sqlite3

app = flask.Flask(__name__)

def get_data_tables(sex:str) -> pd.DataFrame:
    '''
    Returns historic data from 'database.db', for the given sex.

        Parameters:
            sex (str): 'M' or 'F'

        Returns:
            df (pd.DataFrame): Dataframe containing data about lifters in this sex category
    '''

    database = sqlite3.connect('database.db')
    if sex =='M':
        df = pd.read_sql_query("SELECT * FROM male_lifters", database)
    elif sex =='F':
        df = pd.read_sql_query("SELECT * FROM female_lifters", database)

    return df

def find_weight_bin(weight:float, sex:str) -> str:
    '''
    Finds which weight group a user belongs to.

        Parameters:
            weight (float): weight of user
            sex (str): sex of user

        Returns:
            weight_group (str): weight bin of user
    '''
    weight_cutoffs = {
        'F':[0, 47, 52, 57, 63, 69, 76, 84, 1000], 
        'M':[0, 59, 66, 74, 83, 93, 105, 120, 1000]
    }
    weight_labels = {
        'F':['47kg', '52kg', '57kg', '63kg', '69kg', '76kg', '84kg', '84kg+'], 
        'M':['59kg', '66kg', '74kg', '83kg', '93kg', '105kg', '120kg', '120kg+']
    }

    if weight == 0:
        return weight_labels[sex][0]
    else:
        for i, y in enumerate(weight_cutoffs[sex]):
            if y >= weight:
                return weight_labels[sex][i-1]

def find_age_bin(age:float) -> str:
    '''
    Finds which age group a user belongs to.

        Parameters:
            age (float): age of user

        Returns:
            age_group (str): age group of user
    '''
    cutoff_age = [0, 20, 25, 30, 35, 40, 45, 50, 55, 60, 1000]
    age_labels = ['15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60+']
    if age == 0:
        return age_labels[0]
    else:
        for i, y in enumerate(cutoff_age):
            if y >= age:
                return age_labels[i-1]

def calculate_results(form_data:dict) -> dict:
    '''
    Takes in data from input form and returns dictionary with squat, bench deadlift score. 
    
        Parameters:
            form_data (dict): Dictionary containing values from input form

        Returns:
            user_data (dict): Dictionary containing all information about user, including results
    '''
    user_data = {
        'equipment' : form_data['Equipment'],
        'sex' : form_data['Sex'],
        'age' : float(form_data['Age']),
        'weight' : float(form_data['Bodyweight']),
        'best3SquatKg' : float(form_data['Squat']),
        'best3BenchKg' : float(form_data['Bench']),
        'best3DeadliftKg' : float(form_data['Deadlift']),
        'totalKg' : float(form_data['Squat']) + float(form_data['Bench']) + float(form_data['Deadlift']),
        'age_bin' : find_age_bin(float(form_data['Age'])),
        'weight_bin' : find_weight_bin(float(form_data['Bodyweight']), form_data['Sex'])
    }

    historic_data_df = get_data_tables(user_data['sex'])

    #user is in the group
    people_in_group = 1 + len(historic_data_df[(historic_data_df['age_bin'] == user_data['age_bin']) &
                                               (historic_data_df['weight_bin'] == user_data['weight_bin']) &
                                               (historic_data_df['equipment'] == user_data['equipment'])])

    for lift in ['best3SquatKg','best3BenchKg','best3DeadliftKg','totalKg']:
        people_with_lower_lift = len(historic_data_df[(historic_data_df[lift] < user_data[lift]) & 
                                                      (historic_data_df['age_bin'] == user_data['age_bin']) &
                                                      (historic_data_df['weight_bin'] == user_data['weight_bin']) &
                                                      (historic_data_df['equipment'] == user_data['equipment'])])
        lift_result = str(round(people_with_lower_lift/people_in_group * 100, 1)) + '%'

        user_data[lift + '_result'] = lift_result        

    return user_data



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
        return flask.render_template('results.html', results = results)


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)