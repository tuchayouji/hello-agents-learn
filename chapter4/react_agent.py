import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from tavily import TavilyClient

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
        print("[LLM] 正在调用模型...")
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

# ============== 工具 ==============

def search(query: str) -> str:
    """使用 Tavily 搜索网页"""
    print(f"[Search] {query}")
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "错误: TAVILY_API_KEY 未配置"
    
    tavily = TavilyClient(api_key=api_key)
    try:
        response = tavily.search(query=query, search_depth="basic", include_answer=True)
        if response.get("answer"):
            return response["answer"]
        results = [f"- {r['title']}: {r['content'][:100]}" for r in response.get("results", [])[:3]]
        return "\n".join(results) if results else "未找到结果"
    except Exception as e:
        return f"搜索错误: {e}"

class ToolExecutor:
    def __init__(self):
        self.tools = {}
    
    def register(self, name, desc, func):
        self.tools[name] = {"desc": desc, "func": func}
        print(f"工具 '{name}' 已注册")
    
    def get_desc(self):
        return "\n".join([f"- {n}: {t['desc']}" for n, t in self.tools.items()])
    
    def execute(self, name, input_text):
        if name in self.tools:
            return self.tools[name]["func"](input_text)
        return f"错误: 未找到工具 '{name}'"

# ============== ReAct 提示词 ==============

REACT_PROMPT = """你是一个能调用外部工具的智能助手。

可用工具（必须使用下面列出的准确工具名）:
{tools}

请严格按以下格式回复:

Thought: 分析问题，规划下一步
Action: 选择一个:
- 调用工具: 工具名[输入内容]  (例如: Search[华为最新手机])
- 结束任务: Finish[最终答案]

重要: Action中的工具名必须与上面列出的完全一致，不要用"ToolName"占位符！

Question: {question}
History: {history}
"""

# ============== ReAct Agent ==============

class ReActAgent:
    def __init__(self, llm, tools, max_steps=5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
    
    def run(self, question):
        history = []
        
        for step in range(1, self.max_steps + 1):
            print(f"\n--- 第 {step} 步 ---")
            
            # 格式化提示词
            prompt = REACT_PROMPT.format(
                tools=self.tools.get_desc(),
                question=question,
                history="\n".join(history)
            )
            
            # 调用 LLM
            response = self.llm.think([{"role": "user", "content": prompt}])
            if not response:
                break
            
            print(response.encode("gbk", errors="replace").decode("gbk"))
            
            # 解析 Action
            action_match = re.search(r"Action:\s*(.*?)$", response, re.DOTALL)
            if not action_match:
                print("[!] 未解析到 Action")
                break
            
            action = action_match.group(1).strip()
            
            # 检查是否结束
            if action.startswith("Finish"):
                final = re.match(r"Finish\[(.*)\]", action, re.DOTALL)
                if final:
                    print(f"\n[Done] 最终答案: {final.group(1)}")
                    return final.group(1)
            
            # 解析工具调用
            tool_match = re.match(r"(\w+)\[(.*)\]", action, re.DOTALL)
            if tool_match:
                tool_name, tool_input = tool_match.group(1), tool_match.group(2)
                print(f"[Action] 调用: {tool_name}[{tool_input}]")
                
                observation = self.tools.execute(tool_name, tool_input)
                print(f"[Result] 结果: {observation[:200]}...")
                
                history.append(f"Action: {action}")
                history.append(f"Observation: {observation}")
        
        print("[!] 达到最大步数")
        return None

# ============== 主程序 ==============

if __name__ == "__main__":
    # 初始化
    llm = HelloAgentsLLM()
    tools = ToolExecutor()
    tools.register("Search", "搜索引擎，查询实时信息、新闻、事实", search)
    
    agent = ReActAgent(llm, tools)
    
    # 运行
    question = "华为最新的手机是哪一款？它的主要卖点是什么？"
    print(f"问题: {question}\n{'='*50}")
    agent.run(question)
