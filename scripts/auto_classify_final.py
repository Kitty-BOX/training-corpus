#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化语料分类处理工具 - 使用训练语料文件
"""

import json
import os
import shutil
from pathlib import Path
import re

# 配置路径
BASE_DIR = r"C:\Users\smile\AppData\Roaming\CherryStudio\Data\Agents\550b0058-90aa-4921-b369-343ac8f852d3"
DATA_DIR = BASE_DIR
SOURCE_DIR = os.path.join(DATA_DIR, "sources")
TRAINING_FILE = os.path.join(DATA_DIR, "training_corpus.jsonl")

def create_taxonomy():
    """
    创建分类目录结构
    """
    # 创建主要分类目录
    main_categories = [
        "marxist_theory", "indian_revolution", "peru_revolution",
        "gonzalo_interviews", "indian_volume2", "libcom",
        "federals", "holloway", "stalin", "planned_economy",
        "market_economy", "modern_planned", "philosophy",
        "organizational_theory", "work_opposition", "social_development"
    ]

    for category in main_categories:
        category_path = os.path.join(SOURCE_DIR, category)
        os.makedirs(category_path, exist_ok=True)

        # 为特定分类创建子目录
        if category == "marxist_theory":
            sub_cats = ["dialectical_materialism", "historical_materialism", "economic_theory"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)
        elif category == "indian_revolution":
            sub_cats = ["social_characteristics", "revolutionary_strategy", "class_analysis",
                       "peasant_question", "revolutionary_path", "democratic_revolution"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)
        elif category == "peru_revolution":
            sub_cats = ["strategic_objectives", "philosophical_contribution", "world_significance",
                       "people's_war", "party_building", "theory_combination"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)
        elif category == "gonzalo_interviews":
            sub_cats = ["philosophical_theory", "revolutionary_violence", "people's_war_character",
                       "ideological_struggle", "anti_revisionism"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)
        elif category == "indian_volume2":
            sub_cats = ["social_conditions", "economic_structure", "political_system",
                       "cultural_factors", "future_outlook"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)
        elif category == "planned_economy":
            sub_cats = ["basic_principles", "theory_development", "practical_application"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)
        elif category == "market_economy":
            sub_cats = ["socialist_market", "economic_planning"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)
        elif category == "modern_planned":
            sub_cats = ["contemporary_development", "future_trends"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)
        elif category == "philosophy":
            sub_cats = ["philosophical_foundation", "philosophical_analysis"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)
        elif category == "organizational_theory":
            sub_cats = ["party_organization", "organizational_principles"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)
        elif category == "work_opposition":
            sub_cats = ["alienation_theory", "labor_analysis"]
            for sub in sub_cats:
                os.makedirs(os.path.join(category_path, sub), exist_ok=True)

def get_category_for_file(source_name, content):
    """
    根据来源和内容确定分类
    """
    # 简单的基于关键词的分类
    source_lower = source_name.lower()
    content_lower = content.lower()

    # 特定源的分类映射
    if 'libcom' in source_lower or 'libcom' in source_name:
        return 'libcom', 'libcom'
    elif 'federalist' in source_lower:
        return 'federals', 'federalism'
    elif 'holloway' in source_lower:
        return 'holloway', 'capitalism'
    elif 'stalin' in source_lower:
        return 'stalin', 'socialist_construction'
    elif 'planned' in source_lower:
        return 'planned_economy', 'basic_principles'
    elif 'market' in source_lower:
        return 'market_economy', 'socialist_market'
    elif 'modern' in source_lower:
        return 'modern_planned', 'contemporary_development'
    elif 'organise' in source_lower or 'organize' in source_lower:
        return 'organizational_theory', 'organizational_principles'
    elif 'work' in source_lower or 'alienation' in source_lower:
        return 'work_opposition', 'alienation_theory'
    elif 'social' in source_lower and 'development' in source_lower:
        return 'social_development', 'social_development'
    elif 'indian' in source_lower or 'india' in source_lower:
        return 'indian_revolution', 'social_characteristics'
    elif 'peru' in source_lower:
        return 'peru_revolution', 'strategic_objectives'
    elif 'gonzalo' in source_lower or 'gonzalo' in source_name:
        return 'gonzalo_interviews', 'philosophical_theory'
    elif 'marx' in source_lower or 'philosophy' in source_lower:
        return 'marxist_theory', 'dialectical_materialism'
    elif 'philosophy' in source_lower:
        return 'philosophy', 'philosophical_foundation'
    elif 'theory' in source_lower and 'planned' in source_lower:
        return 'planned_economy', 'basic_principles'
    elif 'theory' in source_lower and 'market' in source_lower:
        return 'market_economy', 'socialist_market'
    else:
        # 根据内容关键词来判断
        if any(word in content_lower for word in ['革命', '斗争', '人民', '战争', '马克思', '唯物主义']):
            if any(word in content_lower for word in ['印度']):
                return 'indian_revolution', 'social_characteristics'
            elif any(word in content_lower for word in ['秘鲁', '贡萨罗']):
                return 'peru_revolution', 'strategic_objectives'
            else:
                return 'marxist_theory', 'dialectical_materialism'
        elif any(word in content_lower for word in ['经济', '计划', '市场', '社会主义']):
            return 'planned_economy', 'basic_principles'
        elif any(word in content_lower for word in ['组织', '党', '党的']):
            return 'organizational_theory', 'organizational_principles'
        else:
            return 'misc', 'general'

def classify_training_data():
    """
    自动分类训练数据
    """
    print("开始自动分类训练数据...")
    print(f"源文件: {TRAINING_FILE}")

    # 创建目录结构
    create_taxonomy()

    # 读取数据文件
    try:
        data = []
        with open(TRAINING_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"JSON解析错误: {e}")
                        continue

        print(f"读取到 {len(data)} 条数据")

        # 分类处理
        classified_count = 0
        source_counts = {}
        category_counts = {}

        for i, item in enumerate(data):
            try:
                # 获取数据
                messages = item.get('messages', [])
                source = item.get('source', 'unknown')
                category = item.get('category', 'unknown')

                # 提取内容
                user_content = ""
                assistant_content = ""

                for msg in messages:
                    if msg.get('role') == 'user':
                        user_content = msg.get('content', '')
                    elif msg.get('role') == 'assistant':
                        assistant_content = msg.get('content', '')

                content = user_content + " " + assistant_content

                # 确定分类
                parent_cat, sub_cat = get_category_for_file(source, content)

                # 创建适当目录结构
                if parent_cat == 'libcom':
                    main_dir = os.path.join(SOURCE_DIR, 'libcom')
                elif parent_cat == 'federals':
                    main_dir = os.path.join(SOURCE_DIR, 'federals')
                elif parent_cat == 'holloway':
                    main_dir = os.path.join(SOURCE_DIR, 'holloway')
                elif parent_cat == 'stalin':
                    main_dir = os.path.join(SOURCE_DIR, 'stalin')
                elif parent_cat == 'planned_economy':
                    main_dir = os.path.join(SOURCE_DIR, 'planned_economy')
                elif parent_cat == 'market_economy':
                    main_dir = os.path.join(SOURCE_DIR, 'market_economy')
                elif parent_cat == 'modern_planned':
                    main_dir = os.path.join(SOURCE_DIR, 'modern_planned')
                elif parent_cat == 'organizational_theory':
                    main_dir = os.path.join(SOURCE_DIR, 'organizational_theory')
                elif parent_cat == 'work_opposition':
                    main_dir = os.path.join(SOURCE_DIR, 'work_opposition')
                elif parent_cat == 'social_development':
                    main_dir = os.path.join(SOURCE_DIR, 'social_development')
                elif parent_cat == 'indian_revolution':
                    main_dir = os.path.join(SOURCE_DIR, 'indian_revolution')
                elif parent_cat == 'peru_revolution':
                    main_dir = os.path.join(SOURCE_DIR, 'peru_revolution')
                elif parent_cat == 'gonzalo_interviews':
                    main_dir = os.path.join(SOURCE_DIR, 'gonzalo_interviews')
                elif parent_cat == 'marxist_theory':
                    main_dir = os.path.join(SOURCE_DIR, 'marxist_theory')
                elif parent_cat == 'philosophy':
                    main_dir = os.path.join(SOURCE_DIR, 'philosophy')
                else:
                    main_dir = os.path.join(SOURCE_DIR, 'misc')

                # 确保目录存在
                os.makedirs(main_dir, exist_ok=True)

                # 创建文件名（使用文件名缩写）
                safe_source = re.sub(r'[^\w\-_]', '_', source[:30])
                safe_category = re.sub(r'[^\w\-_]', '_', category[:20])
                filename = f"{i+1:03d}_{safe_source}_{safe_category}.json"

                # 保存文件
                file_path = os.path.join(main_dir, filename)

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(item, f, ensure_ascii=False, indent=2)

                classified_count += 1
                source_counts[source] = source_counts.get(source, 0) + 1
                category_counts[category] = category_counts.get(category, 0) + 1

                if classified_count % 10 == 0:
                    print(f"已处理 {classified_count} 条数据...")

            except Exception as e:
                print(f"处理第 {i+1} 条数据时出错: {e}")
                continue

        print(f"\n分类完成！共处理 {classified_count} 条数据")
        print("\n各来源分类统计:")
        for source, count in sorted(source_counts.items()):
            print(f"  {source}: {count} 条")

        print("\n各主题分类统计:")
        for cat, count in sorted(category_counts.items()):
            print(f"  {cat}: {count} 条")

        return True

    except Exception as e:
        print(f"读取数据文件失败: {e}")
        return False

def print_summary():
    """
    打印分类总结
    """
    print("\n" + "="*60)
    print("分类处理总结")
    print("="*60)

    # 统计各个分类目录中的文件数
    try:
        if os.path.exists(SOURCE_DIR):
            parent_cats = os.listdir(SOURCE_DIR)
            print("\n各分类目录文件统计:")
            total_files = 0

            for cat in sorted(parent_cats):
                cat_path = os.path.join(SOURCE_DIR, cat)
                if os.path.isdir(cat_path):
                    files = [f for f in os.listdir(cat_path) if f.endswith('.json')]
                    file_count = len(files)
                    total_files += file_count
                    print(f"  {cat}: {file_count} 个文件")

            print(f"\n总计: {total_files} 个文件")

        print("="*60)

    except Exception as e:
        print(f"统计信息获取失败: {e}")

def main():
    """
    主函数
    """
    print("自动化语料分类处理工具")
    print("="*50)

    print("正在准备分类处理...")

    # 创建备份
    backup_file = os.path.join(DATA_DIR, "training_corpus_backup.jsonl")
    try:
        shutil.copy2(TRAINING_FILE, backup_file)
        print(f"已创建备份文件: {backup_file}")
    except Exception as e:
        print(f"创建备份失败: {e}")

    # 执行分类
    if classify_training_data():
        print("\n✅ 分类处理完成！")
        print("\n分类后的文件已保存到:")
        print(f"  {SOURCE_DIR}")

        print_summary()
        print("\n现在你可以:")
        print("1. 使用 'git init', 'git add .', 'git commit' 创建 Git 仓库")
        print("2. 推送到 GitHub 仓库")
        print("3. 添加 README.md 和其他文档")
    else:
        print("\n❌ 分类处理失败！")

if __name__ == "__main__":
    main()