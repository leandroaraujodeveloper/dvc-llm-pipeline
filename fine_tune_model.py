import json  
from time import sleep  

import yaml  
from dotenv import load_dotenv  
load_dotenv(".env", override=True)  
import openai
openai.api_key = '<YOUR-KEY-HERE>'
def wait_untill_done(job_id):  
    events = {}  
    while True:  
        response = openai.FineTuningJob.list_events(id=job_id, limit=10)  
        print(response)  
        for event in response["data"]:  
            if "data" in event and event["data"]:  
                events[event["data"]["step"]] = event["data"]["train_loss"]  
        messages = [it["message"] for it in response.data]  
        for m in messages:  
            if m.startswith("New fine-tuned model created: "):  
                return m.split("created: ")[1], events  
        sleep(10)  


if __name__ == "__main__":  
    params = yaml.safe_load(open("params.yaml"))["fine_tune_model"]  
    response = openai.File.create(  
        file=open("data/train.jsonl", "rb"), purpose="fine-tune"  
    )  
    uploaded_id = response.id  
    print("Dataset is uploaded")  
    SLEEP_TIMEOUT = 120  
    print(f"Sleep {SLEEP_TIMEOUT} seconds...")  
    sleep(SLEEP_TIMEOUT)  
    response = openai.FineTuningJob.create(  
        training_file=uploaded_id,  
        model=params["model"],  
        hyperparameters={  
            "n_epochs": params["n_epochs"],  
        },  
    )  
    print("Fine-tune job is started")  
    ft_job_id = response.id  
    new_model_name, events = wait_untill_done(ft_job_id)  
    with open("result/new_model_name.txt", "w") as fp:  
        fp.write(new_model_name)  
    with open("result/events.json", "w") as fp:  
        fp.write(json.dumps(events))