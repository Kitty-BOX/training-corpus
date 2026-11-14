# 方法论说明

## 数据来源与收集

本语料库的 209 条问答对来源于以下公开政治理论与历史文献，按主题整理为九个分类：

| 分类目录 | 主题 | 文件数 |
| :--- | :--- | :--- |
| `federals` | 联邦党人文集 | 10 |
| `holloway` | 霍洛韦文选 | 10 |
| `indian_revolution` | 印度革命 | 14 |
| `libcom` | libcom.org 理论文献 | 45 |
| `marxist_theory` | 马克思主义理论 | 37 |
| `organizational_theory` | 组织理论 | 15 |
| `peru_revolution` | 秘鲁革命 | 19 |
| `planned_economy` | 计划经济理论 | 19 |
| `work_opposition` | 反对劳动理论 | 15 |

## 数据结构

每条数据采用 OpenAI ChatML 格式，包含 `messages`（system/user/assistant 三角色）、`source`（来源标注）与 `category`/`topic`（分类标签）。

原始文件（`data/training_corpus.jsonl`）为逐行 JSON（JSON Lines）；`data/training_data.json` 为等价的 JSON 数组形式，二者内容一致，便于不同加载器使用。

## 分类方法

- `scripts/auto_classify_final.py` 依据来源文件与主题关键词，将 txt 源文件归入 `sources/` 下的九个主题目录，并生成训练语料。
- 分类遵循"来源优先、主题次之"的原则：可明确追溯来源的文献归入对应作者/刊物目录，跨主题文献归入最贴近的理论板块。

## 质量验证

- `scripts/validate_training_data.py` 校验每条数据的 JSON 结构与字段完整性。
- `scripts/final_validate.py` 执行全量验证并输出来源分布统计，确保 209 条数据全部有效、无结构损坏。

## 使用与扩展

新文献以 `.txt` 放入相应主题后，运行 `auto_classify_final.py` 即可增量生成新的问答对并追加至训练数据。所有处理脚本无外部网络依赖，可离线运行。
