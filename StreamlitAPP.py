import os
import json
import pandas as pd
import traceback

from dotenv import load_dotenv
from src.mcqgen.utils import read_file, get_table_data
from src.mcqgen.logger import logging
import streamlit as st
from langchain.callbacks import get_openai_callback

# importing required libraries for longchain
from src.mcqgen.mcqgenerator import generate_evaluate_chain

# loading json file
with open('E:\\mcqgen\\response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# creating title for the app
st.title("MCQ Creator Application with LanagChain")

# creating a form using st.form
with st.form('user_inputs'):

    # file uploader
    uploaded_file = st.file_uploader("Upload a PDF or TXT file")
    # input feilds
    mcq_count = st.number_input("Number of MCQs", min_value=3, max_value=50)
    # subject
    subject = st.text_input("Insert Subject ", max_chars=20)
    # quiz tone
    tone = st.text_input("Complexity of the porblem ", max_chars=20,
                         placeholder="simple")
    # add button
    button = st.form_submit_button("Create MCQ")

    # check if button is clicked and all feilds have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)

                # count tokens and cost of api
                # Use the variables in your function call
                with get_openai_callback() as cb:
                    # How to setup token usages tack record we are using get 
                    # openai callback
                    response = generate_evaluate_chain(
                          {
                            'text': text,
                            'number': mcq_count,
                            'subject': subject,
                            'tone': tone,
                            'response_json': json.dumps(RESPONSE_JSON)
                          }
                     )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Errors")
                     
            else:
                print(f"Total tokens :{cb.total_token}")
                print(f"Prompt token :{cb.prompt_token}")
                print(f"Completion Tokens : {cb.completion_tokens}")
                print(f"Total Cost : {cb.total_cost}")
                if isinstance(response, dict):
                    # Extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)
                            st.text_area(label="Review",
                                         value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)
