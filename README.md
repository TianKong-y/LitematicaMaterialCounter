<h1 align="center">Litematica Material Counter</h1>

<p align="center">
  <b>投影材料统计工具</b>
</p>
<p align="center">
    <a href="LICENSE">
        <img src="https://img.shields.io/badge/License-GPL--3.0-important?style=for-the-badge">
    </a>
    <a href="https://qm.qq.com/q/Spt6kcvVwk">
        <img src="https://img.shields.io/badge/QQ-技术交流/反馈群-blue?style=for-the-badge">
    </a>
    <a href="https://space.bilibili.com/288309681">
        <img src="https://img.shields.io/badge/bilibili-TianKong_y-pink?style=for-the-badge">
    </a>
</p>

## > 简介
Litematica Material Counter 是一个 Python 脚本，用于精确统计 `.litematic` 投影文件中的所有建筑材料。它能够深入容器（如箱子、潜影盒）内部进行统计，区分不同NBT数据的物品（例如自定义名称、附魔），最终将统计结果输出为易于阅读和处理的 CSV 文件。

## > 功能特点
*   **全面统计**: 统计投影中的所有方块和可获取的实体（包括各类矿车、船、盔甲架），并递归统计标准容器（箱子、木桶、发射器、投掷器、漏斗等）以及物品展示框上、潜影盒内部的物品。
*   **精确方块状态处理**: 能够精确统计雪（按层数计为雪片或雪块）、海泡菜、蜡烛等一个方块代表多个物品的情况，并能正确处理门和床（仅计为1个物品），忽略活塞头等无效方块。
*   **NBT区分**: 能够识别并区分具有不同NBT标签的同一ID物品，例如不同自定义名称的工具或不同附魔等级的书籍。
*   **CSV输出**: 生成详细的CSV格式报告，包含物品的（中文）名称、命名空间ID、NBT信息摘要、总数量以及按"盒-组-个"格式化的详细数量。

## > 依赖项
*   Python 3.7+
*   `litemapy` (用于解析 `.litematic` 文件)
*   `nbtlib` (用于处理NBT数据)

## > 安装与环境配置

1.  **克隆或下载项目**

2.  **安装依赖项**:
    在项目根目录下，有一个 `requirements.txt` 文件列出了所需的库。通过以下命令安装：
    ```bash
    pip install -r requirements.txt
    ```

## > 使用方法

在项目根目录打开cmd或Powershell，通过命令行运行 `material_counter.py` 脚本。

**示例命令**:
例如，在将投影文件放入本项目的schematics文件夹后
```bash
python ./material_counter.py ./schematics/{投影文件名称}.litematic
```

## > 输出CSV格式说明

在导入的投影文件的同一级目录下，会生成一个{投影文件名称}_materials.csv
输出的CSV文件包含以下列：

*   `物品名称`: 物品的显示名称。如果配置了中文语言文件且找到对应翻译，则为中文名称；否则为处理后的英文ID。
*   `物品ID`: 物品的完整命名空间ID (例如 `minecraft:diamond_pickaxe`)。
*   `NBT信息`: 对物品NBT数据的关键信息摘要。常见的包括：
    *   `标准`: 表示物品没有特殊的、被追踪的NBT标签。
    *   `名称: <自定义名称>`: 显示物品的自定义名称。
    *   `附魔: <附魔1> <等级1>, <附魔2> <等级2>`: 列出物品的附魔及其等级（等级以罗马数字显示）。
    *   `药水: <药水效果ID>`: 显示药水的基本效果ID。
    *   其他NBT信息会以键值对形式简要展示，并用分号分隔不同类型的NBT。
*   `数量 (个)`: 该物品（具有相同ID和NBT信息）在投影中的总数量。
*   `数量 (盒-组-个)`: 根据标准27格潜影盒和物品堆叠上限，将总数格式化为更直观的"n盒 + n组 + n个"的形式。对于不可堆叠物品，将仅显示为"n盒 + n个"。

## > 更新日志

- **v1.1.1 (2025-06-16)**
  - **新增生物统计**: 工具现在可以递归统计投影中的所有生物（mobs），包括作为其他实体（如船、矿车）乘客的生物。
  - **采用黑名单模式**: 移除了原有的实体白名单，改为黑名单模式，默认统计所有非技术性实体，以适应未来游戏更新。
  - **优化输出格式**:
    - 在最终的物料清单中，明确区分ID相同但类型不同的项目（例如，实体"鸡"与物品"生鸡肉"）。
    - 生物在统计时不再错误地按"组"或"盒"计算，而是始终显示为个体总数。
  - **修复翻译系统**: 全面修复了中文翻译系统，确保所有方块、物品和生物都能正确显示其名称。
- v1.0.0 2025.5.11 初始版本
- v1.0.1 2025.5.11 添加相同物品合并映射，使得物品ID不同但本质上相同的物品（如火把物品和火把方块）的数量合并统计，并将映射表提取到主程序之外
- v1.1.0 2025.6.14 修复了大量方块和实体的统计问题：
  - **新增**: 现在可以正确统计各类矿车、船（包括运输船）和盔甲架实体本身。
  - **修复**: 现在可以根据方块状态精确统计多物品方块（如蜡烛、海泡菜）和分层方块（雪）的数量。
  - **修复**: 修复了门和床会被重复统计为两个的问题。
  - **修复**: 活塞头等不可获取的方块现在会被正确忽略。
  - **优化**: CSV输出中的潜影盒数量统计从浮点数优化为更直观的"n盒 + n组 + n个"格式。

## > 作者&技术交流/反馈群

- bilibili：[TianKong_y](https://space.bilibili.com/288309681)
- QQ：[技术交流/反馈群](https://qm.qq.com/q/Spt6kcvVwk)

## > 鸣谢

- Albertchen857 本项目参考了[LitematicaViewer](https://github.com/albertchen857/LitematicaViewer)的投影文件读取、容器分析功能的实现

## > 项目统计

<div align="center">

![Repobeats analytics image](https://repobeats.axiom.co/api/embed/6bcdef5690100bb1d892074eae94d2231d96bee7.svg "Repobeats analytics image")

</div>
