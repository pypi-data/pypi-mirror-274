"""
The :mod:`fairbalance.tools` module includes classes for fairness analysis and bais mitigation.
"""

from ._fairness_analysis import FairnessAnalysis
from ._mitigator import Mitigator, BalanceOutput, BalanceAttributes, BalanceOutputForAttributes
from ._processor import _Processor, RandomOverSamplerProcessor, SMOTENCProcessor, RandomUnderSamplerProcessor

__all__ = [
    "FairnessAnalysis",
    "Mitigator",
    "BalanceOutput",
    "BalanceAttributes",
    "BalanceOutputForAttributes",
    "SMOTENCProcessor",
    "RandomOverSamplerProcessor",
    "RandomUnderSamplerProcessor",
]