<p align="left">
    English ｜ <a href="README_ZH.md">中文</a>
</p>
<br><br>

<p align="center">
      📚 CogBench (upcoming) | 📑 Paper (upcoming)
<br>

CogGPT is a series of Agent-related works open-sourced by the [KwaiKEG](https://github.com/KwaiKEG) from [Kuaishou Technology](https://www.kuaishou.com/en). The open-sourced content includes:

1. **CogBench**: a benchmark tailored to assess the cognitive dynamics of LLMs. 
2. **CogGPT**: an LLM-driven agent featuring an iterative cognitive mechanism. 
<br>

## What is Cognitive Dynamics
Here is a case of human cognitive dynamics. A man (on the left) experiences a gradual shift in his perspective of the universe, influenced by continuous information flows (on the right).
<p align="center">
    <img src="blob/example.png"/>
<p>

<br>

## Overview of CogGPT

<p align="center">
    <img src="blob/model.png"/>
<p>

## News
* 2024.01.05 - Initial release

## User Guide

### Evaluation
```bash
git clone git@github.com:KwaiKEG/CogGPT.git
cd CogGPT
python evaluation.py --file_path datasets/english/eval_cogbench_v.json --authenticity --rationality
```
