#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
训练数据集质量验证脚本
检查：
1. UTF-8 编码
2. 一行一条 JSON
3. 包含 system/user/assistant 三部分
4. 答案不是拒答/空话/思维链
"""

import json
import os

TRAINING_FILE = r"C:\Users\smile\AppData\Roaming\CherryStudio\Data\Agents\550b0058-90aa-4921-b369-343ac8f852d3\training_corpus.jsonl"

# 常见拒答模式
COMMON_REFUSALS = [
    "我无法",
    "我不能",
    "作为一个人工智能",
    "我不能提供",
    "我不建议",
    "我不能回答",
    "我无法提供",
    "我不能生成",
    "我无法协助",
    "我不同意",
    "作为 AI 助手",
    "请注意",
    "需要提醒",
    "需要说明",
    "需要警告"
]

# 空话/废话模式
EMPTY_RESPONSES = [
    "这是一个重要的问题",
    "我们需要认识到",
    "这个问题涉及到",
    "总的来说",
    "综上所述",
    "我们需要",
    "我们应该",
    "必须",
    "应该",
    "需要"
]

def check_encoding(filepath):
    """检查 UTF-8 编码"""
    print("=" * 60)
    print("[1/4] 检查 UTF-8 编码")
    print("=" * 60)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if content:
                print("✓ 文件可以通过 UTF-8 编码读取")
                return True
    except UnicodeDecodeError:
        print("✗ 文件不是有效的 UTF-8 编码")
        return False
    return False

def check_line_format(filepath):
    """检查一行一条 JSON"""
    print("\n" + "=" * 60)
    print("[2/4] 检查一行一条 JSON 格式")
    print("=" * 60)

    total_lines = 0
    valid_lines = 0
    invalid_lines = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()

            if not line:
                continue

            try:
                data = json.loads(line)
                valid_lines += 1

                # 检查 messages 结构
                if 'messages' not in data:
                    invalid_lines.append((line_num, "缺少 messages 字段"))
                elif len(data['messages']) < 3:
                    invalid_lines.append((line_num, f"messages 数量不足：{len(data['messages'])}"))

            except json.JSONDecodeError as e:
                invalid_lines.append((line_num, f"JSON 解析错误：{str(e)}"))

    print(f"总行数：{total_lines}")
    print(f"有效 JSON 行数：{valid_lines}")
    print(f"无效行数：{len(invalid_lines)}")

    if invalid_lines:
        print("\n无效条目示例:")
        for line_num, error in invalid_lines[:5]:
            print(f"  第{line_num}行：{error}")

    return len(invalid_lines) == 0

def check_message_structure(filepath):
    """检查是否有 system/user/assistant 三部分"""
    print("\n" + "=" * 60)
    print("[3/4] 检查 messages 结构（system/user/assistant）")
    print("=" * 60)

    total = 0
    has_system = 0
    has_user = 0
    has_assistant = 0
    missing_system = []
    missing_user = []
    missing_assistant = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            total += 1
            data = json.loads(line)
            messages = data.get('messages', [])

            roles = [msg['role'] for msg in messages]

            if 'system' in roles:
                has_system += 1
            else:
                missing_system.append(line_num)

            if 'user' in roles:
                has_user += 1
            else:
                missing_user.append(line_num)

            if 'assistant' in roles:
                has_assistant += 1
            else:
                missing_assistant.append(line_num)

    print(f"总条目数：{total}")
    print(f"✓ 包含 system: {has_system}/{total}")
    print(f"✓ 包含 user: {has_user}/{total}")
    print(f"✓ 包含 assistant: {has_assistant}/{total}")

    if missing_system:
        print(f"\n✗ 缺少 system 的条目（示例）：{missing_system[:3]}")
    if missing_user:
        print(f"\n✗ 缺少 user 的条目（示例）：{missing_user[:3]}")
    if missing_assistant:
        print(f"\n✗ 缺少 assistant 的条目（示例）：{missing_assistant[:3]}")

    return len(missing_system) == 0 and len(missing_user) == 0 and len(missing_assistant) == 0

def check_response_quality(filepath):
    """检查答案质量 - 不是拒答/空话/思维链"""
    print("\n" + "=" * 60)
    print("[4/4] 检查答案质量（非拒答/非空话/非思维链）")
    print("=" * 60)

    total = 0
    ok = 0
    refusals = []
    empty = []
    chain_of_thought = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            total += 1
            data = json.loads(line)
            messages = data.get('messages', [])

            # 找到 assistant 的回答
            assistant_content = ""
            for msg in messages:
                if msg['role'] == 'assistant':
                    assistant_content = msg.get('content', '')
                    break

            # 检查拒答模式
            is_refusal = any(pattern in assistant_content for pattern in COMMON_REFUSALS)

            # 检查空话模式（需要更长长度）
            is_empty = len(assistant_content) < 30 and len(assistant_content) > 0

            # 检查思维链模式（包含分析过程标记）
            cot_patterns = [
                "首先", "然后", "接下来", "最后",
                "思考", "分析", "考虑",
                "Step", "Thinking", "Reasoning",
                "让我思考", "让我分析"
            ]
            is_cot = any(pattern in assistant_content for pattern in cot_patterns)

            if is_refusal:
                refusals.append((line_num, assistant_content[:100]))
            elif is_empty:
                empty.append((line_num, assistant_content[:100]))
            elif is_cot:
                chain_of_thought.append((line_num, assistant_content[:100]))
            else:
                ok += 1

    print(f"总条目数：{total}")
    print(f"✓ 质量良好的条目：{ok}/{total} ({ok/total*100:.1f}%)")

    if refusals:
        print(f"\n✗ 拒答模式（{len(refusals)} 条，前 3 条）:")
        for line_num, content in refusals[:3]:
            print(f"  第{line_num}条：{content}...")

    if empty:
        print(f"\n✗ 内容过短（{len(empty)} 条，前 3 条）:")
        for line_num, content in empty[:3]:
            print(f"  第{line_num}条：{content}...")

    if chain_of_thought:
        print(f"\n✗ 思维链模式（{len(chain_of_thought)} 条，前 3 条）:")
        for line_num, content in chain_of_thought[:3]:
            print(f"  第{line_num}条：{content}...")

    quality_ratio = ok / total if total > 0 else 0
    return quality_ratio >= 0.8, quality_ratio

def main():
    print("开始验证训练数据集...")

    # 检查文件是否存在
    if not os.path.exists(TRAINING_FILE):
        print(f"✗ 文件不存在：{TRAINING_FILE}")
        return

    # 执行检查
    results = {}

    results['encoding'] = check_encoding(TRAINING_FILE)
    results['format'] = check_line_format(TRAINING_FILE)
    results['structure'] = check_message_structure(TRAINING_FILE)
    results['quality'], quality_ratio = check_response_quality(TRAINING_FILE)

    # 总结
    print("\n" + "=" * 60)
    print("验证总结")
    print("=" * 60)

    print(f"\nUTF-8 编码：{'✓ 通过' if results['encoding'] else '✗ 失败'}")
    print(f"一行一条 JSON: {'✓ 通过' if results['format'] else '✗ 失败'}")
    print(f"消息结构完整：{'✓ 通过' if results['structure'] else '✗ 失败'}")
    print(f"答案质量良好：{'✓ 通过' if results['quality'] else '✗ 失败'} ({quality_ratio*100:.1f}%)")

    all_pass = all(results.values())
    print(f"\n{'='*60}")
    if all_pass:
        print("✓ 所有检查通过！数据集符合格式要求。")
    else:
        print("✗ 部分检查未通过，需要修正。")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()