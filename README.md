# Self-Healing Coding Agent

一个轻量级「自修复代码 Agent」工程，用于展示 AI Agent 在代码生成、自动执行、错误捕获和迭代修复中的闭环能力。

## 核心能力

- 根据自然语言需求自动生成 Python 程序
- 自动运行生成的代码
- 捕获运行错误和异常日志
- 将错误反馈给大模型进行自我修复
- 支持多轮迭代直到代码成功运行
- 保存每一轮生成结果，方便审计和提交 GitHub

## 项目结构

```txt
self-healing-coding-agent/
├── self_healing_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── utils.py
├── workspace/
│   └── .gitkeep
├── examples/
│   └── example_tasks.txt
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

然后填写：

```txt
OPENAI_API_KEY=your_api_key_here
```

也可以直接使用环境变量：

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 3. 运行 Agent

```bash
python run.py
```

输入任务示例：

```txt
写一个读取 CSV 文件并计算每列平均值的 Python 脚本
```

## 技术亮点

本项目实现了一个简化版 Agent 闭环：

```txt
自然语言需求
    ↓
代码生成 Agent
    ↓
本地执行器
    ↓
错误捕获器
    ↓
自修复 Agent
    ↓
多轮迭代
    ↓
成功运行代码
```

相比普通 AI 编程助手，该 Agent 不只生成代码，还会自动执行并根据真实报错进行修复，具备初步的自主反馈能力。

## 可用于表单填写的项目描述

我构建了一个基于 GPT 系列模型的「自修复代码 Agent」，用于自动完成需求解析、代码生成、执行验证以及迭代修复。该 Agent 可以根据自然语言任务生成 Python 程序，并自动运行代码、捕获错误日志，再将错误反馈给模型进行多轮修复，形成从需求到可运行代码的闭环。

在技术实现上，项目拆分为代码生成模块、执行模块、错误反馈模块和自修复模块。Agent 会保留每轮生成的代码和运行结果，便于后续审计、复盘和持续优化。该方案可用于提升日常开发效率，减少重复性编码与调试时间。

## License

MIT
