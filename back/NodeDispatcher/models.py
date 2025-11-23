from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class NodeModel(BaseModel):
    id: str
    type: str
    params: Optional[Dict[str, Any]] = None
    bits: Optional[int] = None
    inputs: Optional[List[str]] = None
    outputs: Optional[List[str]] = None

class EdgeModel(BaseModel):
    source: str
    target: str
    source_port: Optional[str] = None
    target_port: Optional[str] = None

class GraphSpec(BaseModel):
    algorithm: Optional[str] = None
    block_size: int
    word_size: Optional[int] = None
    rounds: Optional[int] = 1
    nodes: List[NodeModel]
    edges: List[EdgeModel]
    inputs: Optional[List[str]] = None
    outputs: Optional[List[str]] = None
    variables: Optional[Dict[str, Dict[str, Any]]] = None
    stp_semantics: Optional[Dict[str, str]] = None
