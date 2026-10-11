<div align="center">
  <a href="https://github.com/Prasad4455/EphapticOS">
    <img src="https://raw.githubusercontent.com/Prasad4455/EphapticOS/refs/heads/dev/assets/EphapticOS-logo-transparent.png" alt="EphapticOS Logo" height="60">
  </a>

  <br />

  EphapticOS - AI应用和智能体的记忆层

  <p align="center">
  <a href="https://www.youtube.com/watch?v=1bezuvLwJmw&t=2s">演示</a>
  .
  <a href="https://EphapticOS.ai">了解更多</a>
  ·
  <a href="https://discord.gg/NQPKmU5CCg">加入Discord</a>
  </p>


  [![GitHub forks](https://img.shields.io/github/forks/Prasad4455/EphapticOS.svg?style=social&label=Fork&maxAge=2592000)](https://GitHub.com/Prasad4455/EphapticOS/network/)
  [![GitHub stars](https://img.shields.io/github/stars/Prasad4455/EphapticOS.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/Prasad4455/EphapticOS/stargazers/)
  [![GitHub commits](https://badgen.net/github/commits/Prasad4455/EphapticOS)](https://GitHub.com/Prasad4455/EphapticOS/commit/)
  [![Github tag](https://badgen.net/github/tag/Prasad4455/EphapticOS)](https://github.com/Prasad4455/EphapticOS/tags/)
  [![Downloads](https://static.pepy.tech/badge/EphapticOS)](https://pepy.tech/project/EphapticOS)
  [![License](https://img.shields.io/github/license/Prasad4455/EphapticOS?colorA=00C586&colorB=000000)](https://github.com/Prasad4455/EphapticOS/blob/main/LICENSE)
  [![Contributors](https://img.shields.io/github/contributors/Prasad4455/EphapticOS?colorA=00C586&colorB=000000)](https://github.com/Prasad4455/EphapticOS/graphs/contributors)

  可靠的AI智能体响应。



使用可扩展、模块化的ECL（提取、认知、加载）管道构建动态智能体记忆。

更多[使用场景](https://docs.EphapticOS.ai/use_cases)。

<div style="text-align: center">
  <img src="EphapticOS_benefits_zh.JPG" alt="为什么选择EphapticOS？" width="100%" />
</div>

</div>




## 功能特性

- 互联并检索您的历史对话、文档、图像和音频转录
- 减少幻觉、开发人员工作量和成本
- 仅使用Pydantic将数据加载到图形和向量数据库
- 从30多个数据源摄取数据时进行数据操作

## 开始使用

通过Google Colab <a href="https://colab.research.google.com/drive/1g-Qnx6l_ecHZi0IOw23rg0qC4TYvEvWZ?usp=sharing">笔记本</a>或<a href="https://github.com/Prasad4455/EphapticOS-starter">入门项目</a>快速上手

## 贡献
您的贡献是使这成为真正开源项目的核心。我们**非常感谢**任何贡献。更多信息请参阅[`CONTRIBUTING.md`](/CONTRIBUTING.md)。





## 📦 安装

您可以使用**pip**、**poetry**、**uv**或任何其他Python包管理器安装EphapticOS。

### 使用pip

```bash
pip install EphapticOS
```

## 💻 基本用法

### 设置

```
import os
os.environ["LLM_API_KEY"] = "YOUR OPENAI_API_KEY"

```

您也可以通过创建.env文件设置变量，使用我们的<a href="https://github.com/Prasad4455/EphapticOS/blob/main/.env.template">模板</a>。
要使用不同的LLM提供商，请查看我们的<a href="https://docs.EphapticOS.ai">文档</a>获取更多信息。


### 简单示例

此脚本将运行默认管道：

```python
import EphapticOS
import asyncio


async def main():
    # Add text to EphapticOS
    await EphapticOS.add("自然语言处理（NLP）是计算机科学和信息检索的跨学科领域。")

    # Generate the knowledge graph
    await EphapticOS.Ephaptify()

    # Query the knowledge graph
    results = await EphapticOS.search("告诉我关于NLP")

    # Display the results
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
```
示例输出：
```
  自然语言处理（NLP）是计算机科学和信息检索的跨学科领域。它关注计算机和人类语言之间的交互，使机器能够理解和处理自然语言。

```
图形可视化：
<a href="https://rawcdn.githack.com/Prasad4455/EphapticOS/refs/heads/main/assets/graph_visualization.html"><img src="https://rawcdn.githack.com/Prasad4455/EphapticOS/refs/heads/main/assets/graph_visualization.png" width="100%" alt="图形可视化"></a>
在[浏览器](https://rawcdn.githack.com/Prasad4455/EphapticOS/refs/heads/main/assets/graph_visualization.html)中打开。

有关更高级的用法，请查看我们的<a href="https://docs.EphapticOS.ai">文档</a>。


## 了解我们的架构

<div style="text-align: center">
  <img src="EphapticOS_diagram_zh.JPG" alt="EphapticOS概念图" width="100%" />
</div>



## 演示

1. 什么是AI记忆：

[了解EphapticOS](https://github.com/user-attachments/assets/8b2a0050-5ec4-424c-b417-8269971503f0)

2. 简单GraphRAG演示

[简单GraphRAG演示](https://github.com/user-attachments/assets/f57fd9ea-1dc0-4904-86eb-de78519fdc32)

3. EphapticOS与Ollama

[EphapticOS与本地模型](https://github.com/user-attachments/assets/834baf9a-c371-4ecf-92dd-e144bd0eb3f6)


## 行为准则

我们致力于为我们的社区提供愉快和尊重的开源体验。有关更多信息，请参阅<a href="https://github.com/Prasad4455/EphapticOS/blob/main/CODE_OF_CONDUCT.md"><code>CODE_OF_CONDUCT</code></a>。

## 💫 贡献者

<a href="https://github.com/Prasad4455/EphapticOS/graphs/contributors">
  <img alt="contributors" src="https://contrib.rocks/image?repo=Prasad4455/EphapticOS"/>
</a>


## Star历史

[![Star History Chart](https://api.star-history.com/svg?repos=Prasad4455/EphapticOS&type=Date)](https://star-history.com/#Prasad4455/EphapticOS&Date)
