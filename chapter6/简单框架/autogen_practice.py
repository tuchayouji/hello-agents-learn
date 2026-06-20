"""
AutoGen 练习 - 软件开发团队

核心概念：
- AssistantAgent: 思考者，封装LLM
- UserProxyAgent: 执行者，代表用户
- RoundRobinGroupChat: 轮询群聊，顺序协作

运行: python autogen_practice.py
依赖: pip install pyautogen
"""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


# 1. 创建模型客户端
def create_model_client():
    return OpenAIChatCompletionClient(
        model=os.getenv("LLM_MODEL_ID"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        model_info={
            "function_calling": True,
            "max_tokens": 4096,
            "context_length": 32768,
            "vision": False,
            "json_output": True,
            "family": "unknown",
            "structured_output": True,
        }
    )


# 2. 定义智能体
def create_product_manager(model_client):
    return AssistantAgent(
        name="ProductManager",
        model_client=model_client,
        system_message="""你是产品经理，负责需求分析。
分析完需求后，请说"请工程师开始实现"。"""
    )


def create_engineer(model_client):
    return AssistantAgent(
        name="Engineer",
        model_client=model_client,
        system_message="""你是工程师，负责代码实现。
写完代码后，请说"请代码审查员检查"。"""
    )


def create_code_reviewer(model_client):
    return AssistantAgent(
        name="CodeReviewer",
        model_client=model_client,
        system_message="""你是代码审查员，负责审查代码质量。
审查完成后，请说"代码审查完成，请用户代理测试"。"""
    )


def create_user_proxy():
    return UserProxyAgent(
        name="UserProxy",
        description="用户代理，测试完成后回复 TERMINATE。"
    )


# 3. 运行团队协作
async def run_team():
    print("正在初始化...")
    model_client = create_model_client()
    
    print("正在创建智能体团队...")
    product_manager = create_product_manager(model_client)
    engineer = create_engineer(model_client)
    code_reviewer = create_code_reviewer(model_client)
    user_proxy = create_user_proxy()

    team = RoundRobinGroupChat(
        participants=[product_manager, engineer, code_reviewer, user_proxy],
        termination_condition=TextMentionTermination("TERMINATE"),
        max_turns=10,
    )

    task = "开发一个Python函数，计算斐波那契数列第n项"
    print(f"\n任务: {task}\n{'='*50}")
    
    result = await Console(team.run_stream(task=task))
    print("\n协作完成!")
    return result


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(run_team())
