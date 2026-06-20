"""
CAMEL 练习 - 角色扮演协作

核心概念：
- RolePlaying: 角色扮演会话
- AI User: 需求方，推动对话
- AI Assistant: 执行方，提供方案
- Inception Prompting: 引导性提示

运行: python camel_practice.py
依赖: pip install camel-ai
"""

import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from camel.societies import RolePlaying
from camel.models import ModelFactory
from camel.types import ModelPlatformType


def main():
    # 1. 创建模型
    print("正在初始化模型...")
    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type=os.getenv("LLM_MODEL_ID"),
        api_key=os.getenv("LLM_API_KEY"),
        url=os.getenv("LLM_BASE_URL"),
    )

    # 2. 定义任务
    task_prompt = "用Python实现一个简单的计算器，支持加减乘除"
    print(f"\n任务: {task_prompt}\n{'='*50}")

    # 3. 创建角色扮演会话
    # user_role = 需求方（产品经理）
    # assistant_role = 执行方（程序员）
    role_play = RolePlaying(
        assistant_role_name="Python程序员",
        user_role_name="产品经理",
        task_prompt=task_prompt,
        model=model,
        with_task_specify=False,
    )

    # 4. 运行对话
    input_msg = role_play.init_chat()
    chat_turn_limit = 10

    for i in range(chat_turn_limit):
        print(f"\n--- 第 {i+1} 轮 ---")
        
        assistant_response, user_response = role_play.step(input_msg)
        
        if assistant_response.msg is None or user_response.msg is None:
            break
        
        # 打印对话
        print(f"[产品经理]: {user_response.msg.content[:200]}...")
        print(f"[程序员]: {assistant_response.msg.content[:200]}...")
        
        # 检查任务完成标志
        if "<CAMEL_TASK_DONE>" in str(assistant_response.msg.content):
            print("\n任务完成!")
            break
        
        input_msg = assistant_response.msg

    print(f"\n总共进行了 {i+1} 轮协作对话")


if __name__ == "__main__":
    main()
