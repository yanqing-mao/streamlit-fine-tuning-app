# Streamlit App for Fine-Tuning GPT-2

This project is a web application built with **Streamlit** that allows users to fine-tune GPT-2 models using the Hugging Face `transformers` library. The app is also containerized using Docker, enabling easy deployment across different environments.

## Project Overview

This Streamlit app allows users to:
- Load datasets (like Wikitext) from Hugging Face’s `datasets` library.
- Fine-tune GPT-2 (or smaller models like `distilgpt2`) on these datasets.
- Visualize the training process interactively through a web-based UI.

## Setup and Installation

### Prerequisites

- Python 3.9 or higher
- Docker (if using the containerized version)

### Running Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/streamlit-fine-tuning-app.git
   cd streamlit-fine-tuning-app
