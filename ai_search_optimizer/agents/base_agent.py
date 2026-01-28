"""
Base Agent Class for AI Search Optimization.
"""

from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import BaseTool
from langchain_core.prompts import PromptTemplate

from ai_search_optimizer.config import settings


class BaseSearchOptimizationAgent(ABC):
    """
    Base class for all search optimization agents.
    Provides common functionality and Gemini LLM integration.
    """

    def __init__(
        self,
        name: str,
        description: str,
        tools: List[BaseTool],
        temperature: float = None,
        max_iterations: int = None,
        verbose: bool = None,
    ):
        """
        Initialize the base agent.

        Args:
            name: Agent name
            description: Agent description
            tools: List of LangChain tools
            temperature: LLM temperature (default from settings)
            max_iterations: Max agent iterations (default from settings)
            verbose: Enable verbose output (default from settings)
        """
        self.name = name
        self.description = description
        self.tools = tools
        self.temperature = temperature or settings.gemini_temperature
        self.max_iterations = max_iterations or settings.max_iterations
        self.verbose = verbose if verbose is not None else settings.verbose

        # Initialize Gemini LLM
        self.llm = self._create_llm()

        # Create the agent
        self.agent = self._create_agent()
        self.agent_executor = self._create_executor()

    def _create_llm(self) -> ChatGoogleGenerativeAI:
        """Create the Gemini LLM instance."""
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=self.temperature,
            max_output_tokens=settings.gemini_max_tokens,
            convert_system_message_to_human=True,
        )

    def _create_agent(self):
        """Create the ReAct agent with the specified tools."""
        prompt = self._get_prompt_template()
        return create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
        )

    def _create_executor(self) -> AgentExecutor:
        """Create the agent executor."""
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.verbose,
            max_iterations=self.max_iterations,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
        )

    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Get the system prompt for this agent. Must be implemented by subclasses."""
        pass

    def _get_prompt_template(self) -> PromptTemplate:
        """Get the prompt template for the ReAct agent."""
        system_prompt = self._get_system_prompt()

        template = f"""{system_prompt}

You have access to the following tools:

{{tools}}

To use a tool, please use the following format:

```
Thought: I need to think about what to do
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: I now have enough information to respond
Final Answer: [your response here]
```

Begin!

Question: {{input}}
Thought: {{agent_scratchpad}}"""

        return PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
        )

    def run(self, query: str) -> Dict[str, Any]:
        """
        Run the agent with the given query.

        Args:
            query: The input query/task for the agent

        Returns:
            Dictionary containing the output and intermediate steps
        """
        try:
            result = self.agent_executor.invoke({"input": query})
            return {
                "success": True,
                "output": result.get("output", ""),
                "intermediate_steps": result.get("intermediate_steps", []),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None,
            }

    async def arun(self, query: str) -> Dict[str, Any]:
        """
        Asynchronously run the agent with the given query.

        Args:
            query: The input query/task for the agent

        Returns:
            Dictionary containing the output and intermediate steps
        """
        try:
            result = await self.agent_executor.ainvoke({"input": query})
            return {
                "success": True,
                "output": result.get("output", ""),
                "intermediate_steps": result.get("intermediate_steps", []),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None,
            }

    def get_tool_names(self) -> List[str]:
        """Get the names of all tools available to this agent."""
        return [tool.name for tool in self.tools]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', tools={self.get_tool_names()})"
