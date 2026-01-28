"""
Base Agent Class for AI Search Optimization.
"""

from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

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

    def _create_llm(self) -> ChatGoogleGenerativeAI:
        """Create the Gemini LLM instance."""
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=self.temperature,
            max_output_tokens=settings.gemini_max_tokens,
            convert_system_message_to_human=True,
        )

    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Get the system prompt for this agent. Must be implemented by subclasses."""
        pass

    def _get_tools_description(self) -> str:
        """Get a description of available tools."""
        if not self.tools:
            return "No tools available."

        descriptions = []
        for tool in self.tools:
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)

    def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Execute a tool by name."""
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    return tool._run(tool_input)
                except Exception as e:
                    return f"Error executing tool: {str(e)}"
        return f"Tool '{tool_name}' not found."

    def run(self, query: str) -> Dict[str, Any]:
        """
        Run the agent with the given query.

        Args:
            query: The input query/task for the agent

        Returns:
            Dictionary containing the output and intermediate steps
        """
        try:
            system_prompt = self._get_system_prompt()
            tools_desc = self._get_tools_description()

            # Build the full prompt
            full_prompt = f"""{system_prompt}

Available Tools:
{tools_desc}

When you need to use a tool, describe which tool you would use and why.
Then provide a comprehensive response to the user's query.

User Query: {query}
"""

            if self.verbose:
                print(f"[{self.name}] Processing query...")

            # Execute with LLM
            messages = [HumanMessage(content=full_prompt)]
            response = self.llm.invoke(messages)

            # Check if any tools should be run based on the query
            tool_results = []
            for tool in self.tools:
                if self.verbose:
                    print(f"[{self.name}] Running tool: {tool.name}")
                try:
                    # Run tool with the query
                    result = tool._run(query)
                    tool_results.append({
                        "tool": tool.name,
                        "result": result
                    })
                except Exception as e:
                    if self.verbose:
                        print(f"[{self.name}] Tool error: {e}")

            # Combine tool results with LLM analysis
            if tool_results:
                tool_output = "\n\n".join([
                    f"=== {tr['tool']} Results ===\n{tr['result']}"
                    for tr in tool_results
                ])

                # Get LLM to synthesize results
                synthesis_prompt = f"""Based on the following analysis results, provide a comprehensive summary and recommendations:

{tool_output}

Original Query: {query}

Please synthesize these results into actionable insights and recommendations."""

                synthesis_response = self.llm.invoke([HumanMessage(content=synthesis_prompt)])

                final_output = f"{tool_output}\n\n=== SYNTHESIS ===\n{synthesis_response.content}"
            else:
                final_output = response.content

            return {
                "success": True,
                "output": final_output,
                "intermediate_steps": tool_results,
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
            system_prompt = self._get_system_prompt()
            tools_desc = self._get_tools_description()

            full_prompt = f"""{system_prompt}

Available Tools:
{tools_desc}

User Query: {query}
"""

            messages = [HumanMessage(content=full_prompt)]
            response = await self.llm.ainvoke(messages)

            return {
                "success": True,
                "output": response.content,
                "intermediate_steps": [],
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
