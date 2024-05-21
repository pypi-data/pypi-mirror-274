import re
from enum import Enum


class Strategy:
    """策略接口，所有策略需要实现此接口"""

    def apply(self, text):
        pass


class FractionToChineseStrategy(Strategy):
    """将 LaTeX 分数转换为中文格式"""

    def apply(self, text):
        pattern = r"\\frac{(\d+)}{(\d+)}"
        return re.sub(pattern, lambda m: f"{m.group(2)}分之{m.group(1)}", text)


class CleanLatexStrategy(Strategy):
    """清理 LaTeX 特定语法"""

    def apply(self, text):
        text = re.sub(r"\\\(\\|\\\)\\", "", text)
        text = re.sub(r"\\", "", text)
        text = re.sub(r"[()]", "", text)
        text = re.sub(r"\$\$(.*?)\$\$", r"\1", text)
        return re.sub(r"\$(.*?[^\\])\$", r"\1", text)


class MinusToChineseStrategy(Strategy):
    """将减号转换为中文字符"""

    def apply(self, text):
        return re.sub(r"-", "减", text)


class TextFormatter:
    def __init__(self):
        self.strategies = [
            FractionToChineseStrategy(),
            MinusToChineseStrategy(),
            CleanLatexStrategy(),
        ]

    def format_text(self, text):
        """应用所有策略格式化文本"""
        for strategy in self.strategies:
            try:
                text = strategy.apply(text)
            except Exception as e:
                print(f"Error applying strategy: {e}")
        return text


# 使用示例
formatter = TextFormatter()
text = "\\frac{1}{2} - \\frac{3}{4} is a fraction"
formatted_text = formatter.format_text(text)
print(formatted_text)
