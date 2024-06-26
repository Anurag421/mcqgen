import os
import json
import pandas as pd
import traceback
import PyPDF2
from dotenv import load_dotenv
from src.mcqgen.utils import read_file, get_table_data
from src.mcqgen.logger import logging

#importing required libraries for longchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from langchain.chains import SequentialChain


#load environment variable from dotenv
load_dotenv()

#access the environment variable from os.environment
key=os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(openai_api_key=key, model_name='gpt-3.5-turbo', temperature=0.5) #from 0-2 you can mention values of temprature

#define the prompt template imput vairable and template 
template="""
Text:{text}
You are an expert mcq maker. Given the above text , it is your job to \
create a quiz of {number} multiple choice question for {subject} student in {tone} tone.
Make sure the question are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
## RESPONSE_JSON
{response_json}"""
# tone will decide the difficulty level

quize_generation_prompt = PromptTemplate(
    input_variable=['text','number','subject','tone','response_json'],
    template=template)

quiz_chain=LLMChain(llm=llm,prompt=quize_generation_prompt,output_key="quiz",verbose=True)

template2="""You are an expert english and writer. Given a Multiple choice Quiz for {subject} Student.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity if 
the quiz is not at per the congnitive and analytical abilities of the student,\
update the quiz question which needs to be changed and change the tone such that it perfectly fits the students ability
Quiz_MCQs:
{quiz}
Check from an expert English Writer of the above quiz:
"""

#template for the correct question pickup

quiz_evaluate_prompt=PromptTemplate(input_variable=['subject','quiz'],template=template2)
#Creating a new template and chreating a chain for this chain

review_chain=LLMChain(llm=llm,prompt=quiz_evaluate_prompt,output_key='review',verbose=True)
#creating the review chain
#now connect both the chains- quiz chain and review chain

#using sequential chain to create the and combined chain
generate_evaluate_chain = SequentialChain(chains=[quiz_chain,review_chain],input_variables=['text','number','subject','tone','response_json'], 
                                          output_variables=['subject','quiz'],verbose=True)
#first we connected to tempalated using llmchains 
# second we are connecting two chains using sequential chains
