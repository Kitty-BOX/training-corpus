#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
训练数据集验证 - 实际数据验证脚本
"""

import json
import os

def validate_training_data(file_path):
    """验证训练数据集质量"""
    print("开始验证训练数据集...")
    print("=" * 60)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"✗ 文件不存在：{file_path}")
        return False

    # 统计信息
    total_lines = 0
    valid_count = 0
    invalid_count = 0

    # 记录错误详情
    errors = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            total_lines += 1
            try:
                data = json.loads(line)

                # 检查必需字段
                if 'messages' not in data:
                    errors.append(f"第{line_num}行：缺少 messages 字段")
                    invalid_count += 1
                    continue

                messages = data['messages']
                if len(messages) < 3:
                    errors.append(f"第{line_num}行：messages 数量不足：{len(messages)}")
                    invalid_count += 1
                    continue

                # 检查消息角色
                roles = [msg.get('role') for msg in messages]
                if 'system' not in roles:
                    errors.append(f"第{line_num}行：缺少 system 角色")
                    invalid_count += 1
                    continue
                if 'user' not in roles:
                    errors.append(f"第{line_num}行：缺少 user 角色")
                    invalid_count += 1
                    continue
                if 'assistant' not in roles:
                    errors.append(f"第{line_num}行：缺少 assistant 角色")
                    invalid_count += 1
                    continue

                # 检查关键字段存在性
                if not data.get('source'):
                    errors.append(f"第{line_num}行：缺少 source 字段")
                    invalid_count += 1
                    continue

                if not data.get('category'):
                    errors.append(f"第{line_num}行：缺少 category 字段")
                    invalid_count += 1
                    continue

                # 检查 assistant 内容质量（简单版）
                assistant_content = ""
                for msg in messages:
                    if msg.get('role') == 'assistant':
                        assistant_content = msg.get('content', '')
                        break

                if len(assistant_content) < 20:  # 太短的内容
                    errors.append(f"第{line_num}行：assistant 内容过短 ({len(assistant_content)}字符)")
                    # 不计入无效，只是警告
                else:
                    valid_count += 1

            except json.JSONDecodeError as e:
                errors.append(f"第{line_num}行：JSON 解析错误 - {str(e)}")
                invalid_count += 1
                continue

    print(f"验证结果：")
    print(f"  总条目数：{total_lines}")
    print(f"  有效条目：{valid_count}")
    print(f"  无效条目：{invalid_count}")

    if errors:
        print(f"\n详细错误信息：")
        for error in errors[:10]:  # 只显示前10个错误
            print(f"  {error}")
        if len(errors) > 10:
            print(f"  ... 还有 {len(errors) - 10} 个错误")

    # 按来源统计
    sources = {}
    categories = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                source = data.get('source', 'unknown')
                category = data.get('category', 'unknown')

                sources[source] = sources.get(source, 0) + 1
                categories[category] = categories.get(category, 0) + 1
            except:
                continue

    print(f"\n数据来源分布：")
    for source, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {source}: {count}")

    print(f"\n主题分类数量：{len(categories)}")
    print("前 10 个分类:")
    for i, (cat, cnt) in enumerate(sorted(categories.items(), key=lambda x: -x[1])[:10]):
        print(f"  {cat}: {cnt}")

    if invalid_count == 0:
        print("\n✓ 所有数据格式验证通过！")
        return True
    else:
        print(f"\n✗ 存在 {invalid_count} 个格式问题，但大部分数据格式良好。")
        return False

if __name__ == "__main__":
    # 使用你的训练数据文件路径
    TRAINING_FILE = "training_corpus.jsonl"
    validate_training_data(TRAINING_FILE)