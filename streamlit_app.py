import streamlit as st

import json
from openai import OpenAI

client = OpenAI(
 api_key = st.secrets["key"]
)

sauces = ["Ketchup", "Mustard", "Mayo", "BBQ Sauce", "Hot Sauce"]

def print_article(article):
    st.write("HISTORY")
    st.write("   ", article['History'])
    st.write("")
    st.write("CHARACTERISTICS")
    st.write("   ", article['Characteristics'])
    st.write("")
    st.write("TRIVIA")
    for i in range(len(article["Trivia"])):
        st.write('    ', article['Trivia'][i])

st.write("Welcome to the saucy encyclopedia")

st.write("Please wait while we write the encyclopedia articles....")


if not "s" in st.session_state:

    st.session_state["s"] = {}

    for sauce in sauces:
        system_prompt = """
        sauce = {sauce}
        Provide facts about sauce entered in by the user.
        Return a JSON object.
        The format should look like this:
        {
            "History": "The history of the sauce.",
            "Characteristics": "The characteristics of the sauce.",
            "Trivia": "A numbered list of interesting facts about the sauce."
        }
        """

        user_prompt = sauce

        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
            {"role": "user", "content": user_prompt},
            {"role": "system", "content": system_prompt}
        ]
        )

        res = json.loads(response.choices[0].message.content)
        st.session_state["s"][sauce] = res
        st.write("generated", sauce)

# ketchup, mustard, mayo, BBQ sauce, hot sauce

choice = st.selectbox("What sauce would you like to know about?",
         [
             "Ketchup",
             "Mustard",
             "Mayo",
             "BBQ Sauce",
             "Hot Sauce"
         ] 
)

st.write(choice)
print_article(st.session_state["s"][choice])