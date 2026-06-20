"""
LangGraph 练习 - 图结构工作流

核心概念：
- State: TypedDict，全局状态
- Node: Python函数，处理状态
- Edge: 连接节点，支持条件路由
- StateGraph: 状态图，编排工作流

运行: python langgraph_practice.py
依赖: pip install langgraph langchain-openai
"""

import os
from typing import TypedDict, List
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


# 1. 定义状态
class AgentState(TypedDict):
    messages: List[str]      # 对话历史
    current_step: str        # 当前步骤
    user_query: str          # 用户查询
    intent: str              # 意图分析
    search_result: str       # 搜索结果
    final_answer: str        # 最终答案


# 2. 初始化模型
def create_llm():
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL_ID"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
    )


# 3. 定义节点
def understand_node(state: AgentState) -> AgentState:
    """理解用户意图"""
    print("[节点] 理解意图...")
    llm = create_llm()
    query = state["user_query"]
    
    response = llm.invoke([HumanMessage(content=f"分析用户意图，用一句话概括: {query}")])
    
    return {
        **state,
        "messages": state["messages"] + [f"意图: {response.content}"],
        "intent": response.content,
        "current_step": "understand"
    }


def search_node(state: AgentState) -> AgentState:
    """模拟搜索信息"""
    print("[节点] 搜索信息...")
    intent = state["intent"]
    
    # 模拟搜索结果
    search_result = f"关于'{intent}'的相关信息..."
    
    return {
        **state,
        "messages": state["messages"] + [f"搜索: {search_result}"],
        "search_result": search_result,
        "current_step": "search"
    }


def answer_node(state: AgentState) -> AgentState:
    """生成最终答案"""
    print("[节点] 生成答案...")
    llm = create_llm()
    
    context = f"用户问题: {state['user_query']}\n意图: {state['intent']}\n搜索结果: {state['search_result']}"
    response = llm.invoke([HumanMessage(content=f"基于以下信息回答问题:\n{context}")])
    
    return {
        **state,
        "messages": state["messages"] + [f"答案: {response.content}"],
        "final_answer": response.content,
        "current_step": "done"
    }


# 4. 定义条件路由
def should_continue(state: AgentState) -> str:
    """根据当前步骤决定路由"""
    if state["current_step"] == "understand":
        return "search"
    elif state["current_step"] == "search":
        return "answer"
    return "end"


# 5. 构建图
def build_workflow():
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("understand", understand_node)
    workflow.add_node("search", search_node)
    workflow.add_node("answer", answer_node)
    
    # 设置入口
    workflow.set_entry_point("understand")
    
    # 添加条件边
    workflow.add_conditional_edges("understand", should_continue, {
        "search": "search",
        "end": END
    })
    workflow.add_conditional_edges("search", should_continue, {
        "answer": "answer",
        "end": END
    })
    
    # 添加普通边
    workflow.add_edge("answer", END)
    
    return workflow.compile()


# 6. 运行
def main():
    print("LangGraph 三步问答助手")
    print("=" * 50)
    
    app = build_workflow()
    
    query = "什么是机器学习？"
    print(f"用户问题: {query}\n")
    
    result = app.invoke({
        "messages": [],
        "current_step": "",
        "user_query": query,
        "intent": "",
        "search_result": "",
        "final_answer": ""
    })
    
    print(f"\n{'='*50}")
    print(f"最终答案: {result['final_answer']}")


if __name__ == "__main__":
    main()
