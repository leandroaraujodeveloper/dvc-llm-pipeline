## DVC and LLM Fine-Tuning
This project is an example about how DVC might be used for LLM tasks by use Openapi Api for fine tune a simple dataset.

### Requirements

You need [DVC cli](https://dvc.org/doc/install) installed on your environment to run the commands.

You will need credits on the [Openapi API](https://openai.com/blog/openai-api) to get the key required on the `fine_tune_model.py` and `predict.py` scripts.


### Usage

Install project required packages.

```
pip install -r requirements.txt
```

Add the dataset

```
dvc add data/dataset.csv
```

Create the stage `prepare_dataset` of the pipeline.

```
dvc stage add \
    -n prepare_dataset \
    -d data/dataset.csv \
    -d prepare_dataset.py \
    -d consts.py \
    -p prepare_dataset.count \
    -o data/train.jsonl 
    python prepare_dataset.py
```

Create the stage `fine_tune_model` of the pipeline.

```
dvc stage add \
    -n fine_tune_model \
    -d data/train.jsonl \
    -d fine_tune_model.py \
    -p fine_tune_model.n_epochs \
    -o result/new_model_name.txt \
    python fine_tune_model.py
```
Create the stage `predict` of the pipeline.

```
dvc stage add \
    -n predict \
    -p prepare_dataset.count \
    -d predict.py \
    -d result/new_model_name.txt \
    -d train.jsonl \
    -o result/predicted_dataset.csv \
    python predict.py
```

Create the stage `evaluate` of the pipeline.

```
dvc stage add \
    -n evaluate \
    -d result/predicted_dataset.csv \
    -d evaluate_predictions.py
    -o result/scores.json \
    python evaluate_predictions.py
```

At the end visualize your pipepiline by use the command `dvc dag`. And run all stages of the pipeline:

```
dvc repro
```

For troubloshooting the stages individualy you can run for example `dvc repro prepare_dataset` to run this stage only.
