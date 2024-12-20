import streamlit as st
import pandas as pd
import pickle


teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Gujarat Titans',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']
cities = ['Hyderabad', 'Rajkot', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata',
       'Delhi', 'Chandigarh', 'Kanpur', 'Jaipur', 'Chennai', 'Cape Town',
       'Port Elizabeth', 'Durban', 'Centurion', 'East London',
       'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad',
       'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune',
       'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali',
       'Bengaluru']

pipe = pickle.load(open('artifacts/pipe.pkl', 'rb'))
st.title('Tata IPL Win Predictor')



selected_city = st.selectbox('Select host city', sorted(cities))
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', [team for team in sorted(teams) if team != batting_team])
target = st.number_input('Target',step=1)
col3, col4, col5 =st.columns(3)
with col3:
    overs = st.number_input('Overs completed', max_value=19,step=1)
with col4:
    score = st.number_input('Score', min_value=0, step=1)
with col5:
    wickets_out = st.number_input('Wickets out', max_value=9, step=1)

if st.button('Predict Probability'):
    runs_left = target-score
    balls_left = 120 - (overs*6)
    wickets = 10 - wickets_out
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left*6)/balls_left
    input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [selected_city],
                             'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets_left': [wickets],
                             'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win * 100)) + "%")
    st.header(bowling_team + "- " + str(round(loss * 100)) + "%")