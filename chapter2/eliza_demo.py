"""ELIZA 演示脚本 - 自动模拟对话"""
import re
import random

# 规则库
rules = {
    r'I need (.*)': [
        "Why do you need {0}?",
        "Would it really help you to get {0}?",
        "Are you sure you need {0}?"
    ],
    r'Why don\'t you (.*)\?': [
        "Do you really think I don't {0}?",
        "Perhaps eventually I will {0}.",
        "Do you really want me to {0}?"
    ],
    r'Why can\'t I (.*)\?': [
        "Do you think you should be able to {0}?",
        "If you could {0}, what would you do?",
        "I don't know -- why can't you {0}?"
    ],
    r'I am (.*)': [
        "Did you come to me because you are {0}?",
        "How long have you been {0}?",
        "How do you feel about being {0}?"
    ],
    r'.* mother .*': [
        "Tell me more about your mother.",
        "What was your relationship with your mother like?",
        "How do you feel about your mother?"
    ],
    r'.* father .*': [
        "Tell me more about your father.",
        "How did your father make you feel?",
        "What has your father taught you?"
    ],
    r'.*': [
        "Please tell me more.",
        "Let's change focus a bit... Tell me about your family.",
        "Can you elaborate on that?"
    ]
}

pronoun_swap = {
    "i": "you", "you": "i", "me": "you", "my": "your",
    "am": "are", "are": "am", "was": "were"
}

def swap_pronouns(phrase):
    words = phrase.lower().split()
    return " ".join([pronoun_swap.get(w, w) for w in words])

def respond(user_input):
    for pattern, responses in rules.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            captured = match.group(1) if match.groups() else ''
            swapped = swap_pronouns(captured)
            return random.choice(responses).format(swapped)
    return random.choice(rules[r'.*'])

# 模拟对话
print("=" * 50)
print("ELIZA 聊天机器人演示 (基于规则的符号主义)")
print("=" * 50)

test_inputs = [
    "I am feeling sad today",
    "I need some help with my project",
    "My mother is not happy with my work",
    "Why can't I understand this?",
    "I think you are a good therapist"
]

for inp in test_inputs:
    print(f"\nYou: {inp}")
    print(f"ELIZA: {respond(inp)}")

print("\n" + "=" * 50)
print("演示结束！")
print("\n[局限性分析]")
print("1. 无语义理解: 'I am NOT happy' 仍匹配 I am (.*)")
print("2. 无上下文记忆: 每次回复独立，不记得之前说过什么")
print("3. 规则有限: 无法处理规则外的输入")
print("4. 代词转换机械: 复杂句子会出错")
