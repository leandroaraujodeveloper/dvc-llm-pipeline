import json  
import pandas as pd  
import yaml  

from consts import DEFAULT_SYSTEM_PROMPT  

def get_example(question, answer):  
    return {  
        "messages": [  
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},  
            {"role": "user", "content": question},  
            {"role": "assistant", "content": answer},  
        ]  
    }  

if __name__ == "__main__":  
    params = yaml.safe_load(open("params.yaml"))["prepare_dataset"]
    df = pd.read_csv("data/dataset.csv")  
    with open("data/train.jsonl", "w") as f:  
        for i, row in list(df.iterrows())[: params["count"]]:  
            question = row["Question"]  
            answer = row["Answer"]  
            example = get_example(question, answer)  
            example_str = json.dumps(example)  
            f.write(example_str + "\n")