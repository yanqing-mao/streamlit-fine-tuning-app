# -*- coding: utf-8 -*-
"""streamlit_fine_tuning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WtnHeYXttTf69i0RaCPbHm-T5SPbP9-I
"""

import streamlit as st
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
import torch

# Title
st.title("Fine-Tuning GPT-2 with Streamlit")

# Sidebar for user input
st.sidebar.title("Model Configuration")
model_name = st.sidebar.selectbox("Choose a model:", ["distilgpt2", "gpt2", "gpt-neo"])
block_size = st.sidebar.slider("Block Size", min_value=16, max_value=128, value=64, step=16)
dataset_name = st.sidebar.selectbox("Choose Dataset:", ["wikitext-2-raw-v1", "wikitext-103-raw-v1"])

# Load Dataset
@st.cache_data
def load_data(dataset_name):
    dataset = load_dataset("wikitext", dataset_name)
    return dataset


dataset = load_data(dataset_name)
st.write(f"Loaded Dataset: {dataset_name}")

# Tokenizer
@st.cache_resource
def get_tokenizer(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    return tokenizer

tokenizer = get_tokenizer(model_name)

# Tokenize Function
def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, padding=True)

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

# Grouping texts
def group_texts(examples):
    concatenated = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated[list(examples.keys())[0]])
    total_length = (total_length // block_size) * block_size
    result = {k: [t[i:i + block_size] for i in range(0, total_length, block_size)] for k, t in concatenated.items()}
    result["labels"] = result["input_ids"].copy()
    return result

# Tokenized & grouped data
lm_datasets = tokenized_dataset.map(group_texts, batched=True)

# Display dataset info
st.write(f"Dataset has been tokenized and grouped into blocks of {block_size}.")

# Model
@st.cache_resource
def get_model(model_name):
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.resize_token_embeddings(len(tokenizer))
    return model

model = get_model(model_name)

# Training Arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Train Button
if st.button("Start Fine-Tuning"):
    st.write("Fine-tuning model...")

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=lm_datasets["train"].select(range(500)),  # Reduce dataset size for quicker training
        eval_dataset=lm_datasets["validation"].select(range(100)),
    )

    trainer.train()
    st.write("Training Complete.")

# Display Logs
st.write("Model Training Logs Will Appear Here...")
