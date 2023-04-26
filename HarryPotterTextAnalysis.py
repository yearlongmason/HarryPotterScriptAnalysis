import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from pandasql import sqldf
import streamlit as st
from PIL import Image
import base64

#Data cleaning

#Harry Potter and The Sorcerer's Stone (hp1) data cleaning
hp1 = pd.read_csv('HarryPotter1.csv', sep=';')

#Normalizing text (all lowercase, no special characters)
alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ',\
         '0','1','2','3','4','5','6','7','8','9', '-'] #Defines all characters I want to keep
hp1['normText']=[x.lower() for x in hp1['Sentence']] #Sets normalized text to the lowercase Sentence
for i in range(len(hp1)): #Gets rid of all special characters
    hp1.at[i, 'normText'] = ''.join([str(x.lower()) if x in alphabet else '' for x in hp1.iloc[i]['normText']])

#fixes some mistakes in name formatting
hp1['Character'] = [x.replace(' ', '') for x in hp1['Character']] #Remove spaces from Character names
hp1['Character'] = ['Barkeep' if x=='Barkeep\xa0Tom' else x for x in hp1['Character']]
hp1['Character'] = ['Train Master' if x=='Trainmaster' else x for x in hp1['Character']]
hp1['Character'] = ['Sorting Hat' if x=='SortingHat' else x for x in hp1['Character']]
hp1['Character'] = ['Sir Nicholas' if x=='SirNicholas' else x for x in hp1['Character']]
hp1['Character'] = ['Man in Painting' if x=='Maninpaint' else x for x in hp1['Character']]
hp1['Character'] = ['Fat Lady' if x=='FatLady' else x for x in hp1['Character']]
hp1['Character'] = ['Madam Hooch' if x=='MadamHooch' else x for x in hp1['Character']]
hp1['Character'] = ['Ron and Harry' if x=='RonandHarry' else x for x in hp1['Character']]
hp1['Character'] = ['Oliver Wood' if x=='OIiver' else x for x in hp1['Character']]
hp1['Character'] = ['Oliver Wood' if x=='Oliver' else x for x in hp1['Character']]
hp1['Character'] = ['Harry, Ron, and Hermione' if x=='All3' else x for x in hp1['Character']]
hp1['Character'] = ['Hermione' if x=='Hermoine' else x for x in hp1['Character']]
hp1['Character'] = ['Draco' if x=='Malfoy' else x for x in hp1['Character']]
hp1['Character'] = ['Students' if x=='Class' else x for x in hp1['Character']]
hp1['Character'] = ['Trolley Witch' if x=='Woman' else x for x in hp1['Character']]
hp1.at[729, 'Character'] = 'Harry, Ron, and Hermione' #Very specific case that I researched
hp1.at[928, 'Character'] = 'Crowd' #Very specific case that I researched
hp1.at[463, 'Character'] = 'Neville'
#People I would classify as a general "Other" category
backgroundCharacters=['Someone', 'Man', 'Witch', 'Boy', 'Girl', 'Crowd', 'Gryffindors', 'Goblin']
hp1['Character'] = ['Background Character' if x in backgroundCharacters else x for x in hp1['Character']]

#Creating column for number of words per sentence
hp1['numWords'] = [len(x.split(' ')) for x in hp1['Sentence']]

#Defining houses
Gryffindor=['Dumbledore', 'McGonagall', 'Hagrid', 'Harry', 'Mrs.Weasley', 'George', 'Fred', 'Ginny', 'Ron',\
           'Hermione', 'Neville', 'Seamus', 'Percy', 'Sir Nicholas', 'Fat Lady', 'Dean', 'Harry, Ron, and Hermione',\
           'Oliver Wood', 'Ron and Harry', 'LeeJordan']
Slytherin=['Draco', 'Snape', 'Flint', 'Voldemort']
Ravenclaw=['Quirrell', 'Ollivander', 'Madam Hooch', 'Flitwick']
Hufflepuff=[]
Other=['Petunia', 'Dudley', 'Vernon', 'Snake', 'Background Character', 'Barkeep', 'Griphook', 'Train Master',\
      'Trolley Witch', 'Sorting Hat', 'Man in Painting', 'Students', 'Filch', 'Firenze']

#Making a list of all housing assignments per line
hp1House=[]
for i in hp1['Character']:
    if i in Gryffindor:
        hp1House.append('Gryffindor')
    elif i in Slytherin:
        hp1House.append('Slytherin')
    elif i in Ravenclaw:
        hp1House.append('Ravenclaw')
    elif i in Hufflepuff:
        hp1House.append('Hufflepuff')
    else:
        hp1House.append('Muggle')
hp1['House'] = hp1House

#Creates movie name and movie number column for when all dataframes are combined
hp1['MovieName'] = 'Harry Potter and the Sorcerer\'s Stone'
hp1['MovieNumber'] = 1


#Harry Potter and The Chamber of Secrets (hp2) data cleaning

#Streamlit components
st.set_page_config(page_title="Harry Potter Text Analysis", layout="wide") #Setting page title

#Displaying the HogwartsLogo.png at the top of the page
with open("HogwartsLogo.png", "rb") as file:
    contents = file.read()
    imgurl = base64.b64encode(contents).decode("utf-8")
st.markdown(f'<center><img src="data:image/gif;base64,{imgurl}" alt="Hogwarts Logo"></center>', unsafe_allow_html=True)


st.markdown("<h3 style='text-align: center; color: #000000;'>An analysis of the first three Harry Potter movies by Mason Lee</h3>", unsafe_allow_html=True)
st.markdown("As a kid, I was always a big fan of the Harry Potter movies. There was always something about the idea of magic, the worldbuilding, and the aesthetic that came with the movies that was something really enjoyable as a kid, and was something I never really stopped enjoying. With that in mind, I figured it could be fun to do some sort of analysis on them. While looking for available data about the movies to analyze as a fun side project, I stumbled across this dataset that contained every line from the first three movies. What started as a fun project to work on in my freetime ended up turning into my final project for my data visualization class!")
st.markdown("fundamental research question will go here")
st.markdown("Describe the data here")
st.markdown(hp1.iloc[0]['Character'] + ' ' + hp1.iloc[0]['House'] + ' ' + hp1.iloc[0]['Sentence'] + ' Number of words: ' + hp1.iloc[0]['numWords'])


tab1, tab2, tab3, tab4 = st.tabs(["First 3 Movies Combined", "Sorcerer's Stone", "Chamber of Secrets", "Prizoner of Azkaban"])

with tab1:
    st.title("Analysis of Harry Potter and the Sorcerer's Stone, Chamber of Secrets, and Prizoner of Azkaban")
    col1, col2 = st.columns(2)
    with col1:
        image = Image.open('hpChart.png')
        st.image(image, caption='This will be a description of the chart')
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.image(image, caption='This will be a description of the chart')
    with col2:
        image = Image.open('hpChart.png')
        st.image(image, caption='This will be a description of the chart')
        #fig, ax = plt.subplots()
        #st.pyplot(fig)
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")

        source = pd.DataFrame({'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]})
        chart = alt.Chart(source).mark_bar().encode(x='a', y='b')
        chart = chart.properties(width=700, height=375) #Set figure size
        chart = chart.properties(title='HP Data')
        st.altair_chart(chart)
    
    st.markdown('This is just some text at the end of each page saying something about the findings of this tab in particular')
  
  
with tab2:
    st.title("Analysis of Harry Potter and the Sorcerer's Stone")
    col1, col2 = st.columns(2)
    with col1:
        image = Image.open('hpChart.png')
        st.image(image, caption='This will be a description of the chart')
    with col2:
        image = Image.open('hpChart.png')
        st.image(image, caption='This will be a description of the chart')
  
  
with tab3:
    st.title("Analysis of Harry Potter and the Chamber of Secrets")
    col1, col2 = st.columns(2)
    with col1:
        image = Image.open('hpChart.png')
        st.image(image, caption='This will be a description of the chart')
    with col2:
        image = Image.open('hpChart.png')
        st.image(image, caption='This will be a description of the chart')
  
  
with tab4:
    st.title("Analysis of Harry Potter and the Prizoner of Azkaban")
    col1, col2 = st.columns(2)
    with col1:
        image = Image.open('hpChart.png')
        st.image(image, caption='This will be a description of the chart')
    with col2:
        image = Image.open('hpChart.png')
        st.image(image, caption='This will be a description of the chart')
