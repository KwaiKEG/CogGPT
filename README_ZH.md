<p align="left">
    <a href="README.md">English</a> ｜ 中文
</p>
<br><br>

论文 "<a href="https://arxiv.org/abs/2401.08438"> CogGPT: Unleashing the Power of Cognitive Dynamics on Large Language Models </a>" 相关代码和数据

## CogBench

**<a href="https://huggingface.co/datasets/kwaikeg/CogBench">CogBench</a>** 是一个专门用于评估大型语言模型的认知动态（the cognitive dynamics of LLMs）的基准测试，支持中文和英文两种语言。根据信息流的类型，CogBench 分为两个部分：针对文章流的 CogBench<sub>a</sub> 和针对短视频流的 CogBench<sub>v</sub>。

在这个基准测试中，LLM和人类被赋予相同的初始人设，在10轮迭代中接收相同的信息流。每接收完一轮迭代的信息流，他们需要填写同一份认知问卷。这份问卷使用 Likert 五点量表，通过参与者的评分来展示其对当前问题的态度。

CogBench 旨在评估 LLM 与人类在认知一致性方面的表现。评估指标包括：

1. **真实性（Authenticity）**：衡量 LLM 与人类评分的一致性。
2. **合理性（Rationality）**：评估 LLM 提出评分理由的合理性。

## CogGPT

**CogGPT** 是一个基于大型语言模型（LLM）的智能体，旨在展现LLM的认知动态特性。面对不断变化的信息流，CogGPT 能够定期更新其人设，并根据自身兴趣将知识结构化地存储在长期记忆中。这一独特的能力使得CogGPT能够维持基于特定角色的认知动态，进而实现终生学习。

<br>

<p align="center">
    <img src="blob/model.png" alt="CogGPT"/>
<p>

## 动态

* 2024.01.17 - [论文](https://arxiv.org/abs/2401.08438)公开
* 2024.01.12 - <a href="https://huggingface.co/datasets/kwaikeg/CogBench">CogBench</a>公开
* 2024.01.05 - 项目公开

## 使用指南

### 设置

按照以下步骤来配置 CogBench:

1. **克隆仓库**：在本地环境中克隆此仓库。
2. **切换目录**：使用 `cd` 命令进入仓库目录。
3. **下载数据**：下载 <a href="https://huggingface.co/datasets/kwaikeg/CogBench">CogBench</a> 数据集，并将其保存在 `dataset` 目录下。
4. **运行实验**：基于 `cogbench_a.json` 和 `cogbench_v.json`，分别在 CogBench<sub>a</sub> 和 CogBench<sub>v</sub> 上运行你的方法，并获取实验结果。
5. **评估结果**：将基于 CogBench<sub>a</sub> 和 CogBench<sub>v</sub> 的实验结果分别填入 `eval_cogbench_a.json` 和 `eval_cogbench_v.json` 文件中，以便进行评估。

### 如何运行CogGPT

1. 申明环境变量以使用GPT-4 API:

```bash
export OPENAI_API_KEY=sk-xxxxx
```

2. 运行默认设置下的CogGPT:

```bash
python coggpt/agent.py
```

### 评价

为了评估您的方法基于真实性（Authenticity）和合理性（Rationality）两个指标的表现，我们建议运行以下命令：

```bash
python evaluation.py --file_path <YOUR_FILE_PATH> --method <YOUR_METHOD_NAME> --authenticity --rationality
```

例如，要在 CogBench<sub>v</sub> 上评估 `CoT` 方法，请执行：

```bash
python evaluation.py --file_path dataset/english/eval_cogbench_v.json --method CoT --authenticity --rationality
```

评估完成后，您将看到类似于下面的输出，展示了 `CoT` 方法在不同评价指标下的表现：

```bash
======= CoT Authenticity =======
Average authenticity: 0.15277666156947955
5th iteration authenticity: 0.3023255813953488
10th iteration authenticity: 0.13135593220338992
======= CoT Rationality =======
Average rationality: 3.058333333333333
5th iteration rationality: 3.7666666666666666
10th iteration rationality: 3.0833333333333335
```

更多关于 CogBench 和其评价方法的详细信息，请访问 <a href="https://huggingface.co/datasets/kwaikeg/CogBench">CogBench</a> 。

## 引用
```
@misc{lv2024coggpt,
      title={CogGPT: Unleashing the Power of Cognitive Dynamics on Large Language Models}, 
      author={Yaojia Lv and Haojie Pan and Ruiji Fu and Ming Liu and Zhongyuan Wang and Bing Qin},
      year={2024},
      eprint={2401.08438},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```