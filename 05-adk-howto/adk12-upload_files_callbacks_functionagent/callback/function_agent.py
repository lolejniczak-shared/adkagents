import functools
from typing import Callable, Any

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional

class FunctionAgent:

    def __init__(self, name: str, model: str,  **kwargs: Any):
        self.name = name
        self.model = model
        self.kwargs = kwargs

    def __call__(self, func: Callable[[CallbackContext, LlmRequest], Optional[LlmResponse]]) -> LlmAgent:

        return LlmAgent(
            name=self.name,
            model = self.model,
            **self.kwargs,
            before_model_callback=func,
        )