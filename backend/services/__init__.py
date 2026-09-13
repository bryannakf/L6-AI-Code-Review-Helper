from .ai_service import analyse_code
from .csharp_service import analyse_csharp
from .eslint_service import analyse_javascript
from .pylint_service import analyse_python
from .scoring_service import calculate_score

__all__ = [
    "analyse_code",
    "analyse_csharp",
    "analyse_javascript",
    "analyse_python",
    "calculate_score",
]
