import re

from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from story_master.log import logger


class SummaryHandler:
    PROMPT = """
    You are a summary agent for a simulation game.

    -Goal-
    Summarize the provided information.

    -Steps-
    1. Read the context explaining what information is needed.
    2. Read provided information.
    3. Summarize the information.
        Include all important details that are relevant to the context.
    4. Output the summary in XML format.
        Format: <Summary>Summary</Summary>
        Don't output anything else apart from the summary.

    -Context-
    {context}

    -Information-
    {information}

    ########
    Output:
    """

    def __init__(self, llm_model: BaseChatModel):
        self.prompt = PromptTemplate.from_template(self.PROMPT)
        self.pattern = re.compile(r"<\s*Summary\s*>(.*?)</\s*Summary\s*>")
        self.chain = self.prompt | llm_model | StrOutputParser() | self.parse_output

    def parse_output(self, output: str):
        try:
            output = output.replace("\n", " ")
            match = self.pattern.search(output)
            return match.group(1)
        except Exception:
            logger.error(f"SummaryHandler. Could not parse: {output}")
            return None

    def get_summary(self, context: str, information: str):
        summary = self.chain.invoke(
            {
                "context": context,
                "information": information,
            }
        )
        if summary:
            return summary
        return information
