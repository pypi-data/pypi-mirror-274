from enum import Enum, auto
import importlib


class StrategyType(Enum):
    FractionToChineseStrategy = auto()
    CleanLatexSyntaxStrategy = auto()

    @staticmethod
    def get_strategy_class(strategy_enum):
        """获取策略类的实际类引用"""
        strategy_mapping = {
            StrategyType.FractionToChineseStrategy: "FractionToChineseStrategy",
            StrategyType.CleanLatexSyntaxStrategy: "CleanLatexSyntaxStrategy",
        }
        strategy_name = strategy_mapping[strategy_enum]
        module = importlib.import_module("strategies")
        return getattr(module, strategy_name)
