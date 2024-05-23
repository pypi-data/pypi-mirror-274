"""
Interface for defining the methods for adding rag-specific events
"""

import abc
from typing import Any, Optional

from llama_index.core.callbacks import CBEventType
from opentelemetry.trace.span import Span

from ..common.types import Node, RetrievedNode

# TODO: Add exception handling events


class AddRagEventInterface(abc.ABC):
    """
    Interface for defining the rag-specific events. Each rag-specific event
    calls into `add_rag_event_for_span()` to add the event for a span

    The method `add_rag_event_for_span` needs to be implemented by whichever
    class implements this interface (Python does not have interfaces so this
    is done through a child class inheriting AddRagEventInterface).
    """

    def add_query_event(
        self,
        query: str,
        llm_output: list[str],
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Use this to keep track of the start and end of a query.
        """
        self.add_rag_event_for_span(
            event_name=event_name or str(CBEventType.QUERY),
            span=span,
            input=query,
            output=llm_output,
            event_data=metadata,
        )

    def add_chunking_event(
        self,
        output_nodes: list[Node],
        filepath: Optional[str] = None,
        retrieved_node: Optional[RetrievedNode] = None,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Use this to keep track of nodes generated either from:
            1. a file (ingestion)
            2. RetrievedNode (retrieval)
                if you desire to sub-chunk your retrieved nodes

        @param filepath: The path to the file that was chunked
            If this is not provided, retrieved_node must be provided
        @param retrieved_node: The retrieved node that was chunked
            If this is not provided, filepath must be provided
        @param output_nodes: The nodes generated from the chunking process
        """
        if filepath is None and retrieved_node is None:
            print(
                "Warning: You must either provide a filepath or a retrieved node in order to chunk text"
            )
            return
        if filepath is not None and retrieved_node is not None:
            print(
                "Warning: You must provide either a filepath or a retrieved node, not both"
            )
            return
        input_text: str = ""
        if filepath:
            input_text = filepath
        if retrieved_node:
            input_text = retrieved_node.text

        output_nodes_dict = map(lambda node: node.model_dump(), output_nodes)
        self.add_rag_event_for_span(
            event_name=event_name or str(CBEventType.CHUNKING),
            span=span,
            input=input_text,
            output=output_nodes_dict,
            event_data=metadata,
        )

    def add_embedding_event(
        self,
        text: str,
        embedding_vector: list[float],
        # Don't think I should make embedding_model_name first class, can be
        # added to the metadata
        # embedding_model_name: str,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Use this to keep track of the embeddings generated from text in either:
            1. the query during retrieval
            2. the documents during ingestion

        You can use metadata to store other information such as the embedding
        model name.
        """
        self.add_rag_event_for_span(
            event_name=event_name or str(CBEventType.EMBEDDING),
            span=span,
            input=text,
            output=embedding_vector,
            event_data=metadata,
        )

    def add_sub_question_event(
        self,
        original_query: str,
        subqueries: list[str],
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Use this to keep track of whenever a query is split into smaller
        sub-questions to be handled separately later.
        """
        self.add_rag_event_for_span(
            event_name=event_name or str(CBEventType.SUB_QUESTION),
            span=span,
            input=original_query,
            output=subqueries,
            event_data=metadata,
        )

    def add_retrieval_event(
        self,
        query: str,
        retrieved_nodes: list[RetrievedNode],  # Can also make this str
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Use this to keep track fo the nodes retrieved for a query.
        """
        retrieved_nodes_dict = map(
            lambda node: node.model_dump(), retrieved_nodes
        )
        self.add_rag_event_for_span(
            event_name=event_name or str(CBEventType.RETRIEVE),
            span=span,
            input=query,
            output=retrieved_nodes_dict,
            event_data=metadata,
        )

    def add_reranking_event(
        self,
        input_nodes: list[Node],
        output_nodes: list[Node],
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Use this to keep track on how nodes that were retrieved are re-ordered

        You can use metadata to store other information such as the re-ranking
        model name.
        """
        input_nodes_dict = map(lambda node: node.model_dump(), input_nodes)
        output_nodes_dict = map(lambda node: node.model_dump(), output_nodes)
        self.add_rag_event_for_span(
            event_name=event_name or str(CBEventType.RERANKING),
            span=span,
            input=input_nodes_dict,
            output=output_nodes_dict,
            event_data=metadata,
        )

    def add_template_event(
        self,
        prompt_template: str,
        resolved_prompt: str,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Use this to keep track on how a query is re-written using a prompt
        template

        You can use metadata to store other information such as the original
        user question, retrieved context, prompt template id, etc.
        """
        self.add_rag_event_for_span(
            event_name=event_name or str(CBEventType.TEMPLATING),
            span=span,
            input=prompt_template,
            output=resolved_prompt,
            event_data=metadata,
        )

    def add_tool_call_event(
        self,
        tool_name: str,
        # TODO: Result and value of tool_arguments can't actually be Any,
        # it must be JSON-serializable
        tool_arguments: dict[str, Any],
        tool_result: Any,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Use this to keep track on how a query invokes a tool call

        You can use metadata to store other information such as the tool
        parameter schema, tool parameter values, pre-processed result, etc.
        """
        self.add_rag_event_for_span(
            event_name=event_name or str(CBEventType.FUNCTION_CALL),
            span=span,
            input={"tool_name": tool_name, "tool_arguments": tool_arguments},
            output=tool_result,
            event_data=metadata,
        )

    def add_synthesize_event(
        self,
        input: Any,
        output: Any,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Use this as a catch-all to summarize the input and ouput of several
        nested events
        """
        self.add_rag_event_for_span(
            event_name=event_name or str(CBEventType.SYNTHESIZE),
            span=span,
            input=input,
            output=output,
            event_data=metadata,
        )

    @abc.abstractmethod
    def add_rag_event_for_span(
        self,
        event_name: str,
        span: Optional[Span] = None,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Any = None,
        output: Any = None,
        event_data: Optional[dict[Any, Any]] = None,
        indexing_trace_id: Optional[str] = None,
    ) -> None:
        """
        Add a RagEvent for a specific span within a trace. This event gets
        saved at the end of the trace to the RagEvents table, where you can use
        these events to generate test cases and run evaluation metrics on them.
        To run evaluations, you can either use the (`input`, `output`) data
        fields explicitly, or you can use the unstructured `event_data` JSON.

        If all three of those fields aren't included (`input`, `output`,
        `event_data`), an error will be thrown.

        You can only call this method once per span, otherwise it will raise
        an error.

        @param event_name (str): The name of the event
        @param span Optional(Span): The span to add the event to. If None, then
            we use the current span
        @param input Optional(dict[Any, Any]): The input data for the event
        @param output Optional(dict[Any, Any]): The output data for the event
        @param event_data Optional(dict[Any, Any]): The unstructured event data
            in JSON format where you can customize what fields you want to use
            later in your evaluation metrics
        @param indexing_trace_id Optional(str): The id of a trace used during
            indexing or ingesting your data pipeline to help link the query
            flow to the state of your RAG data state
        """

    @abc.abstractmethod
    def add_rag_event_for_trace(
        self,
        event_name: str,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Any = None,
        output: Any = None,
        event_data: Optional[dict[Any, Any]] = None,
        indexing_trace_id: Optional[str] = None,
    ) -> None:
        """
        This is the same functionality as `add_rag_event_for_span()` except
        this is for recording events at the overall trace level. This is useful
        in case you want to run evaluations on the entire trace, rather than
        individual span events.

        You can only call this method once per trace, otherwise it will raise
        an error.
        """
