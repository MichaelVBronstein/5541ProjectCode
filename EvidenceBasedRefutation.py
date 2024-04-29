# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 09:24:34 2024

@author: brons139
"""

import pandas as pd
import openai
import os
import datatable as dt
from datetime import datetime

os.chdir("F:\\UMN Data Science MS\\CSCI 5541\\Project") #change to the path with the relevant article CSVs
data = dt.fread('TestSet_text.csv',fill=True)
DF=data.to_pandas()
DF = DF[DF['Label'] == 'unreliable']

#before continuing, need to have called:
    #openai.api_key = XXX.

article = DF.iloc[0][1] #here, want to change the [0] to i. 
prompt1 = "Articles sometimes make claims that conflict with reality. For example, an article might claim a person said something, when in fact they did not say that. Or, it might claim that covid vaccines cause autism, which is not correct. Your job is to do the following. Step 1: Summarize the main claims in the article. Step 2: identify which, if any, of these claims conflict with reality. Step 3: Summarize the claim and explain why it conflicts with reality in 3 sentences or less. Only output the results of Step 3. Do not output the result from any other step. "
prompt1 += article
def EBR(prompt):
#prompt is a string with the article containing misinformation.       
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[
                {"role": "system", "content": 'You are ChatGPT4, a helpful assistant that corrects misinformation in news articles. The current date is: '+str(datetime.today()).split()[0]},
                {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=1,
        top_p=1,
        n=1,
        stream=False,
        stop=None,
        presence_penalty=0,
        frequency_penalty=0,
        logit_bias={}
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
    
out1=EBR(prompt1)
prompt2="Your job is to revise refutations of incorrect information. You need to make the refutation follow a specific format. That format is: \
[State the facts – the correct version of the incorrect information]. [State the incorrect information and explicitly call it a myth or misconception]. [Point out the misleading nature of the incorrect information, including by explaining how it is logically flawed]. [Restate and reinforce the facts].  \
For example, if the original refutation was: ‘The article claims that current climate change is natural, just like past climate change. This statement conflicts with reality. Studies suggest current climate change is dramatically faster than past natural change, implying a different causal process. Furthermore, studies suggest that gasses emitted by industrial processes cause climate warming.’ \
Your revised refutation should be: \
‘Scientists observe human fingerprints all over our climate. The warming effect from greenhouse gases like carbon dioxide has been confirmed by many lines of evidence. Aircraft and satellites measure less heat escaping to space at the exact wavelengths that carbon dioxide absorbs energy. The upper atmosphere cools while the lower atmosphere warms—a distinct pattern of greenhouse warming.’ ‘A common climate myth is that climate has always changed naturally in the past, therefore modern climate change must be natural also.’ ‘This argument commits the single cause fallacy, falsely assuming that because natural factors have caused climate change in the past, then they must always be the cause of climate change. This logic is the same as seeing a murdered body and concluding that people have died of natural causes in the past, so the murder victim must have also died of natural causes.’ ‘Just as a detective finds clues in a crime scene, scientists have found many clues in climate measurements confirming humans are causing global warming. Human-caused global warming is a measured fact.’ \
Please revise the following refutation to follow the aforementioned format: "
prompt2 += out1
out2=EBR(prompt2)
