from pydantic import BaseModel

class GraphConfig(BaseModel):
    type: str            
    x_label: str        
    y_label: str         
    is_graph_required: bool

class FilterResult(BaseModel):
    filter_script: str
    graph: GraphConfig | None = None
