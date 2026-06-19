import re
import random

# 中文规则库
rules_cn = {
    r'我需要(.*)': [
        "你为什么需要{0}？",
        "得到{0}真的能帮到你吗？",
        "你确定你需要{0}吗？"
    ],
    r'我觉得(.*)': [
        "你为什么会觉得{0}？",
        "这种感觉持续多久了？",
        "还有其他想法吗？"
    ],
    r'我很(.*)': [
        "你有多{0}？",
        "是什么让你感到{0}？",
        "你能详细说说为什么{0}吗？"
    ],
    r'我(.*)不开心': [
        "是什么让你不开心？",
        "能告诉我更多关于{0}的事吗？",
        "不开心的时候你会怎么做？"
    ],
    r'我(.*)妈妈(.*)': [
        "跟我说说你妈妈吧。",
        "你和妈妈的关系怎么样？",
        "你对妈妈有什么感觉？"
    ],
    r'我(.*)爸爸(.*)': [
        "跟我说说你爸爸吧。",
        "爸爸对你有什么影响？",
        "你和爸爸的关系如何？"
    ],
    r'工作(.*)': [
        "工作上遇到什么困难了？",
        "你喜欢现在的工作吗？",
        "能具体说说工作的事吗？"
    ],
    r'学习(.*)': [
        "学习上有什么困惑吗？",
        "你觉得学习难在哪里？",
        "需要什么帮助吗？"
    ],
    r'你好': [
        "你好！今天过得怎么样？",
        "嗨！有什么想聊的吗？",
        "你好呀！请说说你的情况。"
    ],
    r'谢谢': [
        "不客气！还有什么想说的吗？",
        "很高兴能帮到你。",
        "没关系，继续说吧。"
    ],
    r'再见': [
        "再见！祝你一切顺利！",
        "保重！下次再聊。",
        "拜拜，期待下次对话。"
    ],
    r'.*': [
        "请继续说。",
        "能详细描述一下吗？",
        "我在听，请继续。",
        "然后呢？"
    ]
}

def respond_cn(user_input):
    for pattern, responses in rules_cn.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            groups = match.groups()
            captured = groups[0] if groups else ''
            response = random.choice(responses)
            try:
                response = response.format(captured)
            except:
                pass
            return response
    return random.choice(rules_cn[r'.*'])

# 主聊天循环
if __name__ == '__main__':
    print("ELIZA 中文版: 你好！有什么想聊的吗？")
    print("(输入 退出/结束/拜拜 退出)\n")
    while True:
        user_input = input("你: ")
        if user_input in ["退出", "结束", "拜拜", "再见"]:
            print(f"ELIZA: {respond_cn(user_input)}")
            break
        response = respond_cn(user_input)
        print(f"ELIZA: {response}")
