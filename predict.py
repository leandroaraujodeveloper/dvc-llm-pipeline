import json  

import pandas as pd  
from dotenv import load_dotenv  
from tqdm import tqdm  
from consts import DEFAULT_SYSTEM_PROMPT  
load_dotenv(".env", override=True)  
import openai  
openai.api_key = '<YOUR-KEY-HERE>'
def get_fine_tuned_model_name():  
    with open("result/new_model_name.txt") as fp:  
        return fp.read()  

def get_dataset_items():  
    with open("data/train.jsonl", "r") as f:  
        for line in f.readlines():  
            question = json.loads(line)["messages"][1]["content"]  
            answer = json.loads(line)["messages"][2]["content"]  
            yield question, answer  

def call_openai(model_name, prompt):  
    attempt = 1  
    max_attempts = 3  
    while attempt < max_attempts:  
        try:  
            response = openai.ChatCompletion.create(  
                messages=[  
                    {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},  
                    {"role": "user", "content": prompt},  
                ],  
                model=model_name,  
            )  
            return response.choices[0]["message"]["content"]  
        except openai.error.ServiceUnavailableError as e:  
            print(f"Error: {e}")  
            attempt += 1  
    raise ValueError("Max attempts exceeded")  

if __name__ == "__main__":  
    dataset = [(question, answer) for (question, answer) in get_dataset_items()]  
    evaluation_results = []  
    model_name = get_fine_tuned_model_name()  
    for question, true_answer in tqdm(dataset):  
        print(f"User: {question}")  
        print(f"True answer: {true_answer}")
        bot_answer = call_openai(model_name, question)  
        print(f"Bot answer: {bot_answer}")  
        evaluation_results.append(  
            {"question": question, "true_answer": true_answer, "bot_answer": bot_answer}  
        )  
    df = pd.DataFrame.from_records(evaluation_results)  
    df.to_csv("result/predicted_dataset.csv", index=False)