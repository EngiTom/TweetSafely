import streamlit as st
import pandas as pd
from PIL import Image
import cohere
import newtwitter
import os
import altair as alt
tweetsafelylogo = Image.open("tweetSafelyLogo.png")
st.set_page_config(page_title="Tweet Safely", layout="wide", page_icon="tweetSafelyLogo.png")

headerlogo = Image.open("metrohackslogo.png")
st.image(headerlogo)

st.subheader("Welcome to Tweet Safely")

st.image(tweetsafelylogo, width=300)
st.title("A Mental Health MetroHack by Tom, Andrew, and Rafe")
st.write("Made with the Co:here API and the Twitter API, to inspect the toxicity of a user for your mental health.")
st.write("[Come watch our YouTube walkthrough >](https://google.com)")

#####
# Input for username
#####

st.header('Enter a user to inspect: ') 

username_input = "BarackObama"

username = st.text_area("Username input: ", username_input, height=10)

st.header("Now searching for tweets by @"+username+"...")


#####
# Use Twitter API to get 100 posts from timeline of selected person
#####

# Data type to be stored in variable "inputs": list of strings
if len(username) > 0:
    inputs = newtwitter.main(username)
    if inputs == "ERROR":
        st.header("ERROR: This user could not be found")
    else:
        # show the top 3 most recent tweets text
        st.header("3 most recent tweets by this user:")
        for i, n in enumerate(inputs[:3]):
            recent = "{}. {}".format(i+1, n)
            recent

        ##### 
        # Run Cohere on the 100 posts on timeline
        #####
        st.header("Analyzing tweets with AI...")
        cohereAPIKEY = os.environ.get("COHERE_TOKEN")
        co = cohere.Client(cohereAPIKEY) # API key
        response = co.classify(
            model='592e1b8e-86e9-4081-93b3-c25cf8eab61c-ft',
            inputs=inputs # put inputs from twitter api here
        )
        classifications, confidences = [], []
        for r in response.classifications:
            classifications.append(r.prediction)
            confidences.append(r.confidence)

        counts_list = [0] * 3
        for c in classifications:
            counts_list[int(c)] += 1

        #####
        # Output stats of person's 100 most recent things on timeline
        #####

        catnames = ['hateful', 'offensive', 'normal']

        percentages = [round(c/len(inputs)*100, 2) for c in counts_list]

        source = pd.DataFrame({"Category": ['Hateful', 'Offensive', 'Normal'], "value": percentages})

        st.subheader("Toxicity Visualized")
        piechart = alt.Chart(source).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color(field="Category", type="nominal"),
        )
        st.write(piechart)

        for i in range(3):
            st.header("@{}'s timeline is {}% {}".format(username, percentages[i], catnames[i]))

        #####
        # Place pie graph of tweet categories
        #####

        toxicness = round(sum(percentages[0:2]), 2) 
        if toxicness > 20:
            st.header('For your mental health, we recommend that you block this user.')
        elif toxicness > 5:
            st.header('According to our AI, this user is marginally toxic, feel free to ignore their tweets.')
        else:
            st.header('According to our AI, this user is not toxic, feel free to engage with their tweets.')

        st.subheader("Our algorithm has detected that this user's recent tweets are {}% toxic".format(toxicness))

