from dataclasses import dataclass


@dataclass(frozen=True)
class RAGTraceEventResult:
    """
    Return type from marking a RAGQueryEvent or RAGIngestionEvent in a trace
    """

    is_success: bool
    message: str


# TODO: Define later what the injestion_trace_types should be
RAGIngestionEvent = str | list[str]
