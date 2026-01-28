"""
MCP (Model Context Protocol) Server Generator for Website Optimization.

Generates complete MCP server implementations for websites to optimize
their visibility and integration with AI assistants.
"""

import re
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


@dataclass
class MCPTool:
    """Represents an MCP tool definition."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler_code: str


@dataclass
class MCPResource:
    """Represents an MCP resource definition."""
    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"


@dataclass
class MCPPrompt:
    """Represents an MCP prompt definition."""
    name: str
    description: str
    arguments: List[Dict[str, str]]
    template: str


class MCPServerGenerator:
    """
    Generates MCP server configurations and code for websites.

    This enables websites to be optimally integrated with AI assistants
    like Claude, ChatGPT, and others that support MCP.
    """

    def __init__(self):
        self.analysis_cache = {}

    def analyze_website(self, url: str) -> Dict[str, Any]:
        """Analyze a website to determine optimal MCP configuration."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; MCPGenerator/1.0)'}
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')

            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace('www.', '')
            domain_name = domain.split('.')[0]

            analysis = {
                'url': url,
                'domain': domain,
                'domain_name': domain_name,
                'title': self._get_title(soup),
                'description': self._get_description(soup),
                'content_types': self._detect_content_types(soup),
                'has_api': self._detect_api(soup, url),
                'has_search': self._detect_search(soup),
                'has_docs': self._detect_documentation(soup),
                'has_blog': self._detect_blog(soup),
                'has_products': self._detect_products(soup),
                'has_faq': self._detect_faq(soup),
                'navigation': self._extract_navigation(soup),
                'main_topics': self._extract_topics(soup),
            }

            self.analysis_cache[url] = analysis
            return analysis

        except Exception as e:
            return {'error': str(e), 'url': url}

    def generate_mcp_server(self, url: str) -> Dict[str, Any]:
        """Generate complete MCP server configuration and code."""

        # Analyze website if not cached
        if url not in self.analysis_cache:
            analysis = self.analyze_website(url)
        else:
            analysis = self.analysis_cache[url]

        if 'error' in analysis:
            return analysis

        # Generate components
        tools = self._generate_tools(analysis)
        resources = self._generate_resources(analysis)
        prompts = self._generate_prompts(analysis)

        # Generate server code
        server_code = self._generate_server_code(analysis, tools, resources, prompts)

        # Generate configuration
        config = self._generate_config(analysis)

        return {
            'analysis': analysis,
            'tools': [self._tool_to_dict(t) for t in tools],
            'resources': [self._resource_to_dict(r) for r in resources],
            'prompts': [self._prompt_to_dict(p) for p in prompts],
            'server_code': server_code,
            'config': config,
            'setup_instructions': self._generate_setup_instructions(analysis),
        }

    def _get_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('title')
        return title.get_text().strip() if title else ""

    def _get_description(self, soup: BeautifulSoup) -> str:
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '').strip() if meta else ""

    def _detect_content_types(self, soup: BeautifulSoup) -> List[str]:
        """Detect types of content on the website."""
        types = []

        # Check for articles/blog posts
        if soup.find('article') or soup.find(class_=re.compile(r'post|article|blog', re.I)):
            types.append('articles')

        # Check for products
        if soup.find(class_=re.compile(r'product|item|price', re.I)):
            types.append('products')

        # Check for documentation
        if soup.find(class_=re.compile(r'docs|documentation|api', re.I)):
            types.append('documentation')

        # Check for FAQ
        if soup.find(class_=re.compile(r'faq|accordion|question', re.I)):
            types.append('faq')

        # Check for tutorials
        if soup.find(class_=re.compile(r'tutorial|guide|how-to', re.I)):
            types.append('tutorials')

        return types if types else ['general']

    def _detect_api(self, soup: BeautifulSoup, url: str) -> bool:
        """Detect if site has API documentation."""
        text = soup.get_text().lower()
        return any(term in text for term in ['api', 'endpoint', 'rest', 'graphql'])

    def _detect_search(self, soup: BeautifulSoup) -> bool:
        """Detect if site has search functionality."""
        return bool(soup.find('input', attrs={'type': 'search'}) or
                   soup.find('form', attrs={'role': 'search'}) or
                   soup.find(class_=re.compile(r'search', re.I)))

    def _detect_documentation(self, soup: BeautifulSoup) -> bool:
        """Detect documentation sections."""
        return bool(soup.find(class_=re.compile(r'docs|documentation', re.I)) or
                   'documentation' in soup.get_text().lower()[:1000])

    def _detect_blog(self, soup: BeautifulSoup) -> bool:
        """Detect blog sections."""
        return bool(soup.find(class_=re.compile(r'blog|posts', re.I)) or
                   soup.find('article'))

    def _detect_products(self, soup: BeautifulSoup) -> bool:
        """Detect product listings."""
        return bool(soup.find(class_=re.compile(r'product|price|cart', re.I)))

    def _detect_faq(self, soup: BeautifulSoup) -> bool:
        """Detect FAQ sections."""
        return bool(soup.find(class_=re.compile(r'faq|accordion', re.I)) or
                   soup.find('details'))

    def _extract_navigation(self, soup: BeautifulSoup) -> List[str]:
        """Extract main navigation items."""
        nav = soup.find('nav') or soup.find(class_=re.compile(r'nav|menu', re.I))
        if nav:
            links = nav.find_all('a')
            return [link.get_text().strip() for link in links[:10] if link.get_text().strip()]
        return []

    def _extract_topics(self, soup: BeautifulSoup) -> List[str]:
        """Extract main topics from headings."""
        topics = []
        for h in soup.find_all(['h1', 'h2', 'h3'])[:10]:
            text = h.get_text().strip()
            if text and len(text) < 100:
                topics.append(text)
        return topics

    def _generate_tools(self, analysis: Dict[str, Any]) -> List[MCPTool]:
        """Generate MCP tools based on website analysis."""
        tools = []
        domain_name = analysis['domain_name']

        # Search tool (if search detected)
        if analysis['has_search']:
            tools.append(MCPTool(
                name=f"search_{domain_name}",
                description=f"Search content on {analysis['domain']}",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum results",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                },
                handler_code=self._generate_search_handler(analysis)
            ))

        # Content fetch tool
        tools.append(MCPTool(
            name=f"get_{domain_name}_content",
            description=f"Fetch and parse content from {analysis['domain']}",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "URL path to fetch"
                    }
                },
                "required": ["path"]
            },
            handler_code=self._generate_content_handler(analysis)
        ))

        # FAQ tool (if FAQ detected)
        if analysis['has_faq']:
            tools.append(MCPTool(
                name=f"get_{domain_name}_faq",
                description=f"Get FAQ entries from {analysis['domain']}",
                input_schema={
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Topic to filter FAQs"
                        }
                    }
                },
                handler_code=self._generate_faq_handler(analysis)
            ))

        # Documentation tool (if docs detected)
        if analysis['has_docs']:
            tools.append(MCPTool(
                name=f"get_{domain_name}_docs",
                description=f"Get documentation from {analysis['domain']}",
                input_schema={
                    "type": "object",
                    "properties": {
                        "section": {
                            "type": "string",
                            "description": "Documentation section"
                        }
                    }
                },
                handler_code=self._generate_docs_handler(analysis)
            ))

        # Products tool (if products detected)
        if analysis['has_products']:
            tools.append(MCPTool(
                name=f"get_{domain_name}_products",
                description=f"Get product information from {analysis['domain']}",
                input_schema={
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Product category"
                        },
                        "search": {
                            "type": "string",
                            "description": "Product search term"
                        }
                    }
                },
                handler_code=self._generate_products_handler(analysis)
            ))

        return tools

    def _generate_resources(self, analysis: Dict[str, Any]) -> List[MCPResource]:
        """Generate MCP resources based on website analysis."""
        resources = []
        domain_name = analysis['domain_name']
        domain = analysis['domain']

        # Sitemap resource
        resources.append(MCPResource(
            uri=f"{domain_name}://sitemap",
            name="Sitemap",
            description=f"Website sitemap for {domain}",
            mime_type="application/xml"
        ))

        # Dynamic content resource
        resources.append(MCPResource(
            uri=f"{domain_name}://content/{{path}}",
            name="Content",
            description=f"Dynamic content from {domain}",
            mime_type="text/html"
        ))

        # Add type-specific resources
        if 'articles' in analysis['content_types']:
            resources.append(MCPResource(
                uri=f"{domain_name}://articles",
                name="Articles",
                description="Blog posts and articles",
                mime_type="application/json"
            ))

        if analysis['has_faq']:
            resources.append(MCPResource(
                uri=f"{domain_name}://faq",
                name="FAQ",
                description="Frequently asked questions",
                mime_type="application/json"
            ))

        if analysis['has_docs']:
            resources.append(MCPResource(
                uri=f"{domain_name}://documentation",
                name="Documentation",
                description="Product/service documentation",
                mime_type="text/markdown"
            ))

        return resources

    def _generate_prompts(self, analysis: Dict[str, Any]) -> List[MCPPrompt]:
        """Generate MCP prompts for common use cases."""
        prompts = []
        domain_name = analysis['domain_name']
        domain = analysis['domain']

        # General query prompt
        prompts.append(MCPPrompt(
            name=f"query_{domain_name}",
            description=f"Query information from {domain}",
            arguments=[
                {"name": "question", "description": "Question to answer", "required": True}
            ],
            template=f"""Answer the following question using information from {domain}:

Question: {{{{question}}}}

Search the website content and provide a comprehensive answer based on the available information."""
        ))

        # Summary prompt
        prompts.append(MCPPrompt(
            name=f"summarize_{domain_name}_page",
            description=f"Summarize a page from {domain}",
            arguments=[
                {"name": "url", "description": "Page URL to summarize", "required": True}
            ],
            template=f"""Fetch and summarize the content from the following page on {domain}:

URL: {{{{url}}}}

Provide a concise summary of the main points and key information."""
        ))

        # Comparison prompt (if products)
        if analysis['has_products']:
            prompts.append(MCPPrompt(
                name=f"compare_{domain_name}_products",
                description=f"Compare products from {domain}",
                arguments=[
                    {"name": "products", "description": "Products to compare", "required": True}
                ],
                template="""Compare the following products:

Products: {{products}}

Provide a detailed comparison including features, pricing, and recommendations."""
            ))

        return prompts

    def _generate_search_handler(self, analysis: Dict[str, Any]) -> str:
        """Generate search handler code."""
        return f'''async def handle_search_{analysis["domain_name"]}(query: str, limit: int = 10):
    """Search {analysis["domain"]} content."""
    import requests
    from bs4 import BeautifulSoup

    search_url = "{analysis["url"]}/search"
    params = {{"q": query, "limit": limit}}

    try:
        response = requests.get(search_url, params=params, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for item in soup.find_all(class_=re.compile(r'result|item'))[:limit]:
            title = item.find(['h2', 'h3', 'a'])
            snippet = item.find(['p', 'span'])
            results.append({{
                "title": title.get_text().strip() if title else "",
                "snippet": snippet.get_text().strip() if snippet else "",
            }})

        return {{"results": results, "total": len(results)}}
    except Exception as e:
        return {{"error": str(e)}}
'''

    def _generate_content_handler(self, analysis: Dict[str, Any]) -> str:
        """Generate content handler code."""
        return f'''async def handle_get_{analysis["domain_name"]}_content(path: str):
    """Fetch content from {analysis["domain"]}."""
    import requests
    from bs4 import BeautifulSoup

    url = f"{analysis["url"].rstrip('/')}/{{path}}"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove non-content elements
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()

        title = soup.find('title')
        main_content = soup.find('main') or soup.find('article') or soup.find('body')

        return {{
            "title": title.get_text().strip() if title else "",
            "content": main_content.get_text(separator='\\n', strip=True) if main_content else "",
            "url": url
        }}
    except Exception as e:
        return {{"error": str(e)}}
'''

    def _generate_faq_handler(self, analysis: Dict[str, Any]) -> str:
        """Generate FAQ handler code."""
        return f'''async def handle_get_{analysis["domain_name"]}_faq(topic: str = None):
    """Get FAQs from {analysis["domain"]}."""
    import requests
    from bs4 import BeautifulSoup

    url = "{analysis["url"]}/faq"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        faqs = []
        # Look for FAQ patterns
        for item in soup.find_all(['details', 'div'], class_=re.compile(r'faq|question')):
            question = item.find(['summary', 'h3', 'h4'])
            answer = item.find(['p', 'div'], class_=re.compile(r'answer|content'))

            if question:
                faq = {{
                    "question": question.get_text().strip(),
                    "answer": answer.get_text().strip() if answer else ""
                }}
                if not topic or topic.lower() in faq["question"].lower():
                    faqs.append(faq)

        return {{"faqs": faqs, "total": len(faqs)}}
    except Exception as e:
        return {{"error": str(e)}}
'''

    def _generate_docs_handler(self, analysis: Dict[str, Any]) -> str:
        """Generate documentation handler code."""
        return f'''async def handle_get_{analysis["domain_name"]}_docs(section: str = None):
    """Get documentation from {analysis["domain"]}."""
    import requests
    from bs4 import BeautifulSoup

    url = "{analysis["url"]}/docs"
    if section:
        url = f"{{url}}/{{section}}"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract documentation content
        doc_content = soup.find('main') or soup.find(class_=re.compile(r'docs|content'))

        return {{
            "section": section or "index",
            "content": doc_content.get_text(separator='\\n', strip=True) if doc_content else "",
            "url": url
        }}
    except Exception as e:
        return {{"error": str(e)}}
'''

    def _generate_products_handler(self, analysis: Dict[str, Any]) -> str:
        """Generate products handler code."""
        return f'''async def handle_get_{analysis["domain_name"]}_products(category: str = None, search: str = None):
    """Get products from {analysis["domain"]}."""
    import requests
    from bs4 import BeautifulSoup

    url = "{analysis["url"]}/products"
    if category:
        url = f"{{url}}/{{category}}"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []
        for item in soup.find_all(class_=re.compile(r'product|item')):
            name = item.find(['h2', 'h3', 'a'])
            price = item.find(class_=re.compile(r'price'))
            desc = item.find(['p', 'span'], class_=re.compile(r'desc'))

            product = {{
                "name": name.get_text().strip() if name else "",
                "price": price.get_text().strip() if price else "",
                "description": desc.get_text().strip() if desc else ""
            }}

            if not search or search.lower() in product["name"].lower():
                products.append(product)

        return {{"products": products, "total": len(products)}}
    except Exception as e:
        return {{"error": str(e)}}
'''

    def _generate_server_code(
        self,
        analysis: Dict[str, Any],
        tools: List[MCPTool],
        resources: List[MCPResource],
        prompts: List[MCPPrompt]
    ) -> str:
        """Generate complete MCP server code."""

        domain_name = analysis['domain_name']

        tools_code = "\n\n".join(t.handler_code for t in tools)

        tools_list = ",\n        ".join([
            f'''Tool(
            name="{t.name}",
            description="{t.description}",
            inputSchema={json.dumps(t.input_schema, indent=12)}
        )''' for t in tools
        ])

        resources_list = ",\n        ".join([
            f'''Resource(
            uri="{r.uri}",
            name="{r.name}",
            description="{r.description}",
            mimeType="{r.mime_type}"
        )''' for r in resources
        ])

        return f'''#!/usr/bin/env python3
"""
MCP Server for {analysis['domain']}
Auto-generated by AI Search Optimizer

This server provides AI assistants with access to content from {analysis['domain']}.
"""

import asyncio
import json
import re
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, TextContent, Prompt, PromptArgument


# Initialize server
server = Server("{domain_name}-mcp-server")

# Base URL
BASE_URL = "{analysis['url']}"


# ============ TOOL HANDLERS ============

{tools_code}


# ============ SERVER SETUP ============

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        {tools_list}
    ]


@server.list_resources()
async def list_resources() -> List[Resource]:
    """List available resources."""
    return [
        {resources_list}
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    handlers = {{
        {", ".join([f'"{t.name}": handle_{t.name.replace("-", "_")}' for t in tools])}
    }}

    if name in handlers:
        result = await handlers[name](**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=f"Unknown tool: {{name}}")]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read resource content."""
    # Parse URI and fetch content
    if uri.endswith("/sitemap"):
        response = requests.get(f"{{BASE_URL}}/sitemap.xml", timeout=10)
        return response.text

    # Handle dynamic content URIs
    if "/content/" in uri:
        path = uri.split("/content/")[-1]
        response = requests.get(f"{{BASE_URL}}/{{path}}", timeout=10)
        return response.text

    return "Resource not found"


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
'''

    def _generate_config(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate MCP configuration file content."""
        domain_name = analysis['domain_name']

        return {
            "mcpServers": {
                f"{domain_name}-server": {
                    "command": "python",
                    "args": [f"{domain_name}_mcp_server.py"],
                    "env": {
                        "BASE_URL": analysis['url']
                    }
                }
            }
        }

    def _generate_setup_instructions(self, analysis: Dict[str, Any]) -> str:
        """Generate setup instructions."""
        domain_name = analysis['domain_name']

        return f"""
# MCP Server Setup Instructions for {analysis['domain']}

## 1. Install Dependencies

```bash
pip install mcp requests beautifulsoup4
```

## 2. Save the Server Code

Save the generated server code as `{domain_name}_mcp_server.py`

## 3. Configure Claude Desktop

Add to your Claude Desktop config (`~/.config/claude/claude_desktop_config.json`):

```json
{{
  "mcpServers": {{
    "{domain_name}-server": {{
      "command": "python",
      "args": ["/path/to/{domain_name}_mcp_server.py"]
    }}
  }}
}}
```

## 4. Test the Server

```bash
python {domain_name}_mcp_server.py
```

## 5. Usage in Claude

Once configured, you can ask Claude:
- "Search {analysis['domain']} for [topic]"
- "Get the FAQ from {analysis['domain']}"
- "Summarize the documentation on {analysis['domain']}"

## Benefits of This MCP Server

1. **Direct Content Access**: AI can fetch live content from your website
2. **Structured Queries**: Enables semantic search and FAQ retrieval
3. **Always Up-to-Date**: Fetches current content, not cached
4. **AI-Optimized**: Content is parsed and formatted for AI consumption
"""

    def _tool_to_dict(self, tool: MCPTool) -> Dict[str, Any]:
        return {
            "name": tool.name,
            "description": tool.description,
            "inputSchema": tool.input_schema
        }

    def _resource_to_dict(self, resource: MCPResource) -> Dict[str, Any]:
        return {
            "uri": resource.uri,
            "name": resource.name,
            "description": resource.description,
            "mimeType": resource.mime_type
        }

    def _prompt_to_dict(self, prompt: MCPPrompt) -> Dict[str, Any]:
        return {
            "name": prompt.name,
            "description": prompt.description,
            "arguments": prompt.arguments
        }


def generate_mcp_for_website(url: str) -> str:
    """
    Generate MCP server for a website and return formatted report.

    Args:
        url: Website URL to generate MCP server for

    Returns:
        Formatted report with MCP configuration and code
    """
    generator = MCPServerGenerator()
    result = generator.generate_mcp_server(url)

    if 'error' in result:
        return f"Error: {result['error']}"

    output = []
    output.append("=" * 70)
    output.append("MCP SERVER GENERATION REPORT")
    output.append("=" * 70)

    analysis = result['analysis']
    output.append(f"\nWebsite: {analysis['domain']}")
    output.append(f"Title: {analysis['title'][:60]}")
    output.append(f"Content Types: {', '.join(analysis['content_types'])}")

    output.append("\n--- DETECTED FEATURES ---")
    output.append(f"Search: {'Yes' if analysis['has_search'] else 'No'}")
    output.append(f"Documentation: {'Yes' if analysis['has_docs'] else 'No'}")
    output.append(f"Blog: {'Yes' if analysis['has_blog'] else 'No'}")
    output.append(f"Products: {'Yes' if analysis['has_products'] else 'No'}")
    output.append(f"FAQ: {'Yes' if analysis['has_faq'] else 'No'}")

    output.append("\n--- GENERATED TOOLS ---")
    for tool in result['tools']:
        output.append(f"  • {tool['name']}: {tool['description'][:50]}...")

    output.append("\n--- GENERATED RESOURCES ---")
    for resource in result['resources']:
        output.append(f"  • {resource['uri']}: {resource['description']}")

    output.append("\n" + "=" * 70)
    output.append("SETUP INSTRUCTIONS")
    output.append("=" * 70)
    output.append(result['setup_instructions'])

    output.append("\n" + "=" * 70)
    output.append("CLAUDE DESKTOP CONFIG")
    output.append("=" * 70)
    output.append(json.dumps(result['config'], indent=2))

    return "\n".join(output)
