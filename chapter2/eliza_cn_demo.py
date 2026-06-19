"""ELIZA 中文版 - 添加中文规则"""
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
    """根据中文规则库生成响应"""
    for pattern, responses in rules_cn.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            # 获取捕获组
            groups = match.groups()
            captured = groups[0] if groups else ''
            # 格式化响应
            response = random.choice(responses)
            try:
                response = response.format(captured)
            except:
                pass
            return response
    return random.choice(rules_cn[r'.*'])

# 演示
print("=" * 50)
print("ELIZA 中文版演示")
print("=" * 50)

test_inputs = [
    "你好",
    "我今天很不开心",
    "我觉得工作压力很大",
    "我很累",
    "我需要一些帮助",
    "我妈妈说我不够努力",
    "学习好难啊",
    "谢谢你的帮助",
    "再见"
]

for inp in test_inputs:
    print(f"\n你: {inp}")
    print(f"ELIZA: {respond_cn(inp)}")

print("\n" + "=" * 50)
print("中文规则演示结束！")

print("\n[新添加的中文规则]")
print("- 问候: 你好 → 回应问候")
print("- 情绪: 我很XX → 询问原因")
print("- 家庭: 妈妈/爸爸 → 引导谈论家庭")
print("- 工作/学习: 引导描述具体困难")
print("- 告别: 再见 → 礼貌结束")
