import re


class FractionToChineseStrategy:
    """具体策略实现：分数转中文"""

    def apply(self, text):
        pattern = r"\\frac{(\d+)}{(\d+)}"

        # 替换逻辑：将分数转换为中文读法 "x分之y"
        def replace_fraction(match):
            numerator = match.group(1)  # 分子
            denominator = match.group(2)  # 分母
            return f"{denominator}分之{numerator}"

        # 在整个字符串中替换所有匹配的 LaTeX 分数
        chinese_text = re.sub(pattern, replace_fraction, text)

        # 去除 LaTeX 公式外围的 \() 和 \\
        cleaned_text = re.sub(r"\\\(\\|\\\)\\", "", chinese_text)
        # 去除单独的 \, 保留文字
        cleaned_text = re.sub(r"\\", "", cleaned_text)
        cleaned_text = re.sub(r"[()]", "", cleaned_text)
        cleaned_text = re.sub(r"\$\$(.*?)\$\$", r"\1", cleaned_text)
        cleaned_text = re.sub(r"\$(.*?[^\\])\$", r"\1", cleaned_text)
        return cleaned_text

        return re.sub(
            r"\\frac{(\d+)}{(\d+)}", lambda m: f"{m.group(2)}分之{m.group(1)}", text
        )


class CleanLatexSyntaxStrategy:
    """具体策略实现：清理LaTeX语法"""

    def apply(self, text):
        expression_with_chinese_minus = re.sub(r"-", "减", text)
        return expression_with_chinese_minus
