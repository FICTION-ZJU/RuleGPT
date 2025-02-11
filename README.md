RuleGPT: A Fine-Tuned LLM for Modeling in Horae
=============

This repository contains the implementation of RuleGPT from the paper titled "HORAE: A Domain-Agnostic Language for Automated Service Regulation" submitted to IJCAI 2025 (AI4Tech). The repository instructs how one can quickly train and deploy RuleGPT.

Note: The dataset SRR-Eval for fine-tuning RuleGPT as well as the so-obtained model weights are also open-sourced; but the concrete links are omitted due to anonymous review.

Below, we provide details about the usage of scripts for supervised fine-tuning RuleGPT with [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory).


Installation
------------

Before you start, make sure you have installed the following packages:

1. Follow the instructions of [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory), and build the environment.
2. Install these packages:

```
pip install deepspeed
pip install flash-attn --no-build-isolation
```

3. If you want to use [FlashAttention-2](https://github.com/Dao-AILab/flash-attention), make sure your CUDA is 11.6 and above.

Data Preparation
----------------

LLaMA-Factory provides several training datasets in ``data`` folder, you can use it directly. If you want use SRR-Eval, download the dataset from huggingface and save it to ``data_process`` folder. 

Training
--------

Execute the following training command:

```
llamafactory-cli train qwen2_5-7b-lora-sft.yaml
```

and enjoy the training process. To make changes to your training, you can modify ``qwen2_5-7b-lora-sft.yaml``.

Merge LoRA
----------

Run the following command to perform the merging of LoRA adapters.

```
llamafactory-cli train qwen2_5-7b-merge-lora.yaml
```

Inference
----------
In `infer` folder, we provide code to either use your local model RuleGPT or other commercial models to get your inference results.
Run `python infer_local.py` to get your RuleGPT results. Run `python infer_gpt.py` to get other models results.


Note
----------

The above instructions give a simple way to train and deploy RuleGPT via LLaMA-Factory. Feel free to dive into the details by checking the official repo!
