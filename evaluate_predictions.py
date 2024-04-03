import json  

import evaluate  
import pandas as pd  
if __name__ == "__main__":  
    rouge = evaluate.load("rouge")  
    df = pd.read_csv("result/predicted_dataset.csv")  
    results = rouge.compute(predictions=df["bot_answer"], references=df["true_answer"])  
    with open("result/scores.json", "w") as fp:  
        fp.write(json.dumps(results))