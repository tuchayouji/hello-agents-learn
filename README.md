# Hello Agents Learn

基于 [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) 的学习练习记录

## 学习进度

| 章节 | 内容 | 状态 |
|------|------|------|
| 第一章 | 初识智能体 | ✅ |
| 第二章 | 智能体发展史 | ✅ |
| 第三章 | 大语言模型基础 | ✅ |
| 第四章 | 智能体经典范式构建 | ✅ |
| 第五章 | 基于低代码平台的智能体搭建 | ✅ |
| 第六章 | 框架开发实践 | ✅ |

## 目录结构

```
├── chapter1/          # 智能体定义、Agent Loop、Thought-Action-Observation
│   ├── travel_agent.py
│   └── 知识点.md
├── chapter2/          # 符号主义、专家系统、心智社会、联结主义
│   ├── eliza.py
│   └── 知识点.md
├── chapter3/          # Transformer、提示工程、分词
│   └── 知识点.md
├── chapter4/          # ReAct、Plan-and-Solve、Reflection
│   ├── react_agent.py
│   ├── plan_and_solve.py
│   └── 知识点.md
├── chapter5/          # 低代码平台（Coze、Dify、FastGPT、n8n）
│   └── 知识点.md
├── chapter6/          # 框架开发（AutoGen、AgentScope、CAMEL、LangGraph）
│   ├── AgentScopeDemo/
│   ├── AutoGenDemo/
│   ├── CAMEL/
│   ├── Langgraph/
│   ├── 简单框架/
│   └── 知识点.md
└── .env               # API 配置（已 gitignore）
```

## 核心知识点

### 第一章：智能体循环
```
感知 → 思考(规划+工具选择) → 行动 → 观察 → 循环
```

### 第二章：发展脉络
```
符号主义 → 专家系统 → 心智社会 → 联结主义 → 强化学习 → LLM智能体
```

### 第三章：Transformer 核心
- 自注意力：`Attention(Q,K,V) = softmax(QK^T/√dk) × V`
- Decoder-Only：自回归，预测下一个词

### 第四章：三种范式

| 范式 | 特点 | 适用场景 |
|------|------|----------|
| ReAct | 边想边做 | 需要外部信息 |
| Plan-and-Solve | 先规划后执行 | 结构化推理 |
| Reflection | 自我反思优化 | 需要高质量输出 |

### 第五章：低代码平台

| 平台 | 特点 | 适用场景 |
|------|------|----------|
| Coze | 零代码、插件丰富 | 快速验证、个人创作 |
| Dify | 开源、企业级 | 专业开发、企业应用 |
| FastGPT | 知识库问答专精 | 知识库客服 |
| n8n | 通用自动化 | 业务流程集成 |

### 第六章：四大框架

| 框架 | 核心思想 | 适用场景 |
|------|----------|----------|
| AutoGen | 对话驱动协作 | 流程化任务、软件开发 |
| AgentScope | 消息驱动平台 | 大规模、高可靠性系统 |
| CAMEL | 角色扮演协作 | 双智能体深度协作 |
| LangGraph | 图结构工作流 | 复杂循环、反思迭代 |

## 环境配置

```bash
pip install openai python-dotenv tavily-python
pip install pyautogen agentscope camel-ai langgraph langchain-openai
```

创建 `.env` 文件：
```
LLM_API_KEY=your_key
LLM_BASE_URL=your_url
LLM_MODEL_ID=your_model
TAVILY_API_KEY=your_key
```

## 参考资料

- [Hello-Agents 在线阅读](https://hello-agents.datawhale.cc)
- [GitHub 仓库](https://github.com/datawhalechina/hello-agents)
