import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgen.utils import read_file, get_table_data
from src.mcqgen.logger import logging

#importing required libraries for longchain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from langchain.chains import SequentialChain
import PyPDF2

#load environment variable from dotenv
load_dotenv()
os.getenv("OPENAI_API_KEY")