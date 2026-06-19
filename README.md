# Hello Agents Learn

基于 [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) 的学习练习记录

## 学习进度

| 章节 | 内容 | 状态 |
|------|------|------|
| 第一章 | 初识智能体 | ✅ |
| 第二章 | 智能体发展史 | ✅ |
| 第三章 | 大语言模型基础 | ✅ |
| 第四章 | 智能体经典范式构建 | ✅ |
| 第五章 | 基于低代码平台的智能体搭建 | 🔲 |
| 第六章 | 框架开发实践 | 🔲 |
| ... | ... | 🔲 |

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

## 环境配置

```bash
pip install openai python-dotenv tavily-python
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
