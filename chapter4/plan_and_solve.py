import os
import ast
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# ============== LLM 客户端 ==============

class HelloAgentsLLM:
    def __init__(self):
        self.model = os.getenv("LLM_MODEL_ID")
        self.client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL")
        )
    
    def think(self, messages):
        print("[LLM] 调用模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
                stream=False
            )
            content = response.choices[0].message.content
            print("[LLM] 响应成功")
            return content
        except Exception as e:
            print(f"[LLM] 错误: {e}")
            return None

# ============== 提示词 ==============

PLANNER_PROMPT = """你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。

请确保计划中的每个步骤都是独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表格式。

问题: {question}

请严格按照以下格式输出（必须包含 ```python 和 ``` 前后缀）:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""

EXECUTOR_PROMPT = """你是一位顶级的AI执行专家。请严格按照给定的计划，一步步地解决问题。

原始问题: {question}

完整计划: {plan}

历史步骤与结果:
{history}

当前步骤: {current_step}

请仅输出针对"当前步骤"的回答，不要输出额外解释:
"""

# ============== 组件 ==============

class Planner:
    def __init__(self, llm):
        self.llm = llm
    
    def plan(self, question):
        print("\n--- 规划阶段 ---")
        prompt = PLANNER_PROMPT.format(question=question)
        response = self.llm.think([{"role": "user", "content": prompt}])
        
        if not response:
            return []
        
        try:
            # 解析 Python 列表
            plan_str = response.split("```python")[1].split("```")[0].strip()
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except Exception as e:
            print(f"[!] 解析计划失败: {e}")
            return []


class Executor:
    def __init__(self, llm):
        self.llm = llm
    
    def execute(self, question, plan):
        print("\n--- 执行阶段 ---")
        history = ""
        
        for i, step in enumerate(plan):
            print(f"\n-> 步骤 {i+1}/{len(plan)}: {step}")
            
            prompt = EXECUTOR_PROMPT.format(
                question=question,
                plan=plan,
                history=history if history else "无",
                current_step=step
            )
            
            response = self.llm.think([{"role": "user", "content": prompt}]) or ""
            
            history += f"步骤 {i+1}: {step}\n结果: {response}\n\n"
            print(f"[OK] 结果: {response}")
        
        return response

# ============== 智能体 ==============

class PlanAndSolveAgent:
    def __init__(self, llm):
        self.planner = Planner(llm)
        self.executor = Executor(llm)
    
    def run(self, question):
        print(f"\n{'='*50}")
        print(f"问题: {question}")
        print('='*50)
        
        # 1. 生成计划
        plan = self.planner.plan(question)
        if not plan:
            print("[!] 无法生成计划")
            return
        
        print(f"\n[Plan] 生成计划:")
        for i, step in enumerate(plan):
            print(f"  {i+1}. {step}")
        
        # 2. 执行计划
        final_answer = self.executor.execute(question, plan)
        
        print(f"\n{'='*50}")
        print(f"[Done] 最终答案: {final_answer}")
        print('='*50)

# ============== 主程序 ==============

if __name__ == "__main__":
    llm = HelloAgentsLLM()
    agent = PlanAndSolveAgent(llm)
    
    question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
    agent.run(question)
