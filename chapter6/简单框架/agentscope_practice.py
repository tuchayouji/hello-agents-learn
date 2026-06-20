"""
AgentScope 练习 - 消息驱动智能体 (v2.0)

核心概念：
- Agent: 基础智能体类
- Msg: 统一消息格式
- 消息驱动架构

运行: python agentscope_practice.py
依赖: pip install agentscope
"""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


async def main():
    from agentscope.agent import Agent
    from agentscope.message import Msg
    from agentscope.model import OpenAIChatModel
    from agentscope.credential import OpenAICredential

    # 1. 创建认证和模型
    print("正在初始化...")
    credential = OpenAICredential(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
    )
    model = OpenAIChatModel(
        credential=credential,
        model=os.getenv("LLM_MODEL_ID"),
    )

    # 2. 创建智能体 (v2.0 需要 system_prompt 和 model 参数)
    assistant = Agent(
        name="Assistant",
        system_prompt="你是一个有帮助的AI助手，简洁明了地回答问题。",
        model=model,
    )

    # 3. 多轮对话
    questions = [
        "什么是智能体？",
        "智能体和传统程序有什么区别？",
        "列举3个智能体的应用场景。",
    ]

    for q in questions:
        print(f"\n[用户]: {q}")
        user_msg = Msg(name="User", content=[{"text": q}], role="user")
        response = await assistant.reply(user_msg)
        print(f"[{response.name}]: {response.content}")


if __name__ == "__main__":
    asyncio.run(main())
