import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Type

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

from core.nodes.base import Node
from core.task import TaskContext

load_dotenv()

class ModelProvider(str, Enum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    OLLAMA = "ollama"
    BEDROCK = "bedrock"

@dataclass
class AgentConfig:
    system_prompt: str
    output_type: Optional[Type[Any]]
    deps_type: Optional[Type[Any]]
    model_provider: ModelProvider
    model_name: str  # Use standard strings to prevent strict version import crashes!


class AgentNode(Node, ABC):
    class DepsType(BaseModel):
        pass

    class OutputType(BaseModel):
        pass

    def __init__(self):
        agent_wrapper = self.get_agent_config()
        
        # THE MODERN FIX: Calculate the universal string identifier format dynamically
        # Pydantic AI natively parses these strings and handles providers automatically!
        model_string = self.__calculate_model_string(
            agent_wrapper.model_provider, 
            agent_wrapper.model_name
        )
        
        self.agent = Agent(
            model=model_string,  # e.g., "openai:gpt-4o-mini"
            system_prompt=agent_wrapper.system_prompt,
            output_type=agent_wrapper.output_type, # modern naming mapping rule
        )

    @abstractmethod
    def get_agent_config(self) -> AgentConfig:
        pass

    @abstractmethod
    def process(self, task_context: TaskContext) -> TaskContext:
        pass

    def __calculate_model_string(self, provider: ModelProvider, model_name: str) -> str:
        """
        Translates internal enums into native Pydantic AI connection strings
        """
        match provider:
            case ModelProvider.OPENAI:
                return f"openai:{model_name}"
            case ModelProvider.GEMINI:
                return f"google:{model_name}"
            case ModelProvider.ANTHROPIC:
                return f"anthropic:{model_name}"
            case ModelProvider.BEDROCK:
                return f"aws-bedrock:{model_name}"
            case ModelProvider.OLLAMA:
                # Fallback handler for local development endpoints
                return f"ollama:{model_name}"
            case _:
                return f"openai:gpt-4o-mini"