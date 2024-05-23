import tiktoken
from .brainchain import Brainchain
from transformers import AutoTokenizer, AutoModel
import torch
from .products import ProductsAPI
from .tools.web import web_search, web_content, web_cache, web_scanner
from .tools.coding import python_agent, sql_database_agent, terminal
from .tools.memory import insert_memory, lookup_similar_memories, delete_memories
from .tools.tokens import encode_text, decode_tokens
from .tools.fts import fts_ingest_document, fts_search_index, fts_document_qa, fts_extract, fts_indices, fts_health_check
from .tools.graph import execute_cypher_query, graph_query
from .tools.factual import fact_check
from .tools.diffbot import diffbot_analyze
from .tools.plan import generate_plan, improve_plan, execute_plan
from .graph.schema import GraphSchema
from .graph.base import GraphBase
from .logger import log_function_info
from .assistants import AssistantClient

import os

try:
    BC_EMBEDDING_MODEL = os.getenv("BC_EMBEDDING_MODEL", "BAAI/bge-m3")
    BC_TOKENIZER_MODEL = os.getenv("BC_TOKEN_ENCODING", "cl100k_base")
except:
    pass

# Load the global tokenizer and model from Hugging Face
hf_tokenizer = AutoTokenizer.from_pretrained(BC_EMBEDDING_MODEL)
hf_model = AutoModel.from_pretrained(BC_EMBEDDING_MODEL)
hf_model.eval()  # Set the model to evaluation mode

class Silk(str):
    def __new__(cls, content: str):
        obj = super().__new__(cls, content)
        # Using tiktoken for initial tokenization to count tokens
        obj.tokenizer = tiktoken.get_encoding(BC_TOKENIZER_MODEL)
        obj.tokens = obj.tokenizer.encode(content)
        obj._token_count = len(obj.tokens)
        return obj

    @property
    def token_count(self):
        """Returns the count of tokens."""
        return self._token_count

    def embed(self):
        """Generates embeddings for the string using the pretrained Hugging Face model."""
        # Convert tiktoken tokens to a string, then re-tokenize using Hugging Face tokenizer
        text = self.tokenizer.decode(self.tokens)
        encoded_input = hf_tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            model_output = hf_model(**encoded_input)
        # Use the [CLS] token's embedding as the sentence embedding
        sentence_embedding = model_output.last_hidden_state[:, 0, :]
        # Normalize the embedding
        normalized_embedding = torch.nn.functional.normalize(sentence_embedding, p=2, dim=1)
        return normalized_embedding

    def cosim(self, other):
        """Calculates the cosine similarity between two TokenAwareString instances."""
        if not isinstance(other, Silk):
            raise ValueError("Both objects must be instances of TokenAwareString")
        embedding1 = self.embed()
        embedding2 = other.embed()
        # Calculate the cosine similarity
        cos_sim = torch.dot(embedding1.flatten(), embedding2.flatten())
        return cos_sim.item()

    def __add__(self, other):
        combined = super().__add__(other)
        return Silk(combined)
