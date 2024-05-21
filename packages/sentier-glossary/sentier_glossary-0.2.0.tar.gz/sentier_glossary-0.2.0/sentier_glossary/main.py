import locale
from enum import Enum
from functools import reduce
from urllib.parse import urljoin

import requests
import torch
from sentence_transformers import SentenceTransformer, util  # type: ignore

from sentier_glossary.settings import Settings


class CommonSchemes(Enum):
    cn2024 = "http://data.europa.eu/xsp/cn2024/cn2024"
    nace21 = "http://data.europa.eu/ux2/nace2.1/nace2.1"
    low2015 = "http://data.europa.eu/6p8/low2015/scheme"
    icst2009 = "http://data.europa.eu/z1e/icstcom2009/icst"
    prodcom2023 = "http://data.europa.eu/qw1/prodcom2023/prodcom2023"
    isic4 = "https://unstats.un.org/classifications/ISIC/rev4/scheme"


DEFAULT_COMPONENTS = {
    "process": CommonSchemes.cn2024,
    "product": CommonSchemes.nace21,
    "unit": None,
    "place": None,
}


class GlossaryAPI:
    def __init__(self, cfg: Settings | None = None, default_language: str | None = None):
        self._cfg = cfg if cfg is not None else Settings()
        if not self._cfg.base_url.endswith("/"):
            self._cfg.base_url += "/"

        self._semantic_search = False
        # self._catalogues = {}
        self.language_code = self.get_language_code()
        print(f"Using language code '{self.language_code}'; change with `set_language_code()`")

    def _requests_get(self, url: str, params: dict | None = None) -> dict:
        """Perform a `requests.get(api_url, …)` with given parameters.

        Args:
            url: The API endpoint.
            params: Any additional parameters to pass.

        Returns:
            dict: A dictionary containing the parsed JSON response.

        Raises:
            requests.exceptions.RequestException: If there is an error with the request,
            such as a connection error or an invalid URL.

        """
        params = self._params | params if params is not None else self._params
        response = requests.get(
            reduce(urljoin, [self._cfg.base_url, f"{self._cfg.api_version}/", url]),
            params=params,
        )
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            msg = f"Error fetching data: {error}"
            if response is not None:
                status_code = response.status_code
                msg += f"\nHTTP {status_code}"
                if 400 <= status_code < 600:
                    try:
                        error_data = response.json()
                        msg += f"\nResponse: {error_data}"
                    except ValueError:
                        msg += f"\nResponse: {response.text}"
            raise requests.exceptions.RequestException(msg) from error
        return response.json()

    @property
    def _params(self) -> dict:
        """Default parameters for every request."""
        return {"lang": self.language_code}

    def get_language_code(self, default: str = "en") -> str:
        """Get 2-letter (Set 1) ISO 639 language code."""
        code = locale.getlocale()[0] or default
        if isinstance(code, str) and len(code) >= 2:
            return code[:2]
        raise ValueError(f"Invalid language code {code} found; set locale or `default_language`")

    def set_language_code(self, language_code: str) -> None:
        """Override language code from system locale or input argument."""
        if not isinstance(language_code, str) and len(language_code) >= 2:
            raise ValueError(
                f"Invalid language code {language_code} given. Must be `str` of length two."
            )
        self.language_code = language_code[:2]

    def setup_semantic_search(
        self,
        model_id: str = "all-mpnet-base-v2",
        components: dict[str, CommonSchemes | None] = DEFAULT_COMPONENTS,
    ) -> None:
        """Download data and metadata to perform semantic search queries"""
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def schemes(self) -> list:
        """Get all concept schemes, regardless of type"""
        return self._requests_get("schemes")["concept_schemes"]

    def concepts_for_scheme(self, scheme_iri: str | Enum) -> list:
        if isinstance(scheme_iri, Enum):
            scheme_iri = scheme_iri.value
        # TBD: Validate input arg
        data = self._requests_get("concepts", {"concept_scheme_iri": scheme_iri})["concepts"]
        if not data and scheme_iri not in {obj["iri"] for obj in self.schemes()}:
            raise KeyError(f"Given concept scheme IRI '{scheme_iri}' not present in glossary")
        return data

    def search(self, query: str) -> str:
        """Search the the whole concept library

        Args:
            query (str): the search query string

        Returns:
            list of results
        """
        return self._requests_get("search", {"search_term": query})["concepts"]


# # Corpus with example sentences
# corpus = [
#     "A man is eating food.",
#     "A man is eating a piece of bread.",
#     "The girl is carrying a baby.",
#     "A man is riding a horse.",
#     "A woman is playing violin.",
#     "Two men pushed carts through the woods.",
#     "A man is riding a white horse on an enclosed ground.",
#     "A monkey is playing drums.",
#     "A cheetah is running behind its prey.",
# ]
# corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

# # Query sentences:
# queries = [
#     "A man is eating pasta.",
#     "Someone in a gorilla costume is playing a set of drums.",
#     "A cheetah chases prey on across a field.",
# ]


# # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
# top_k = min(5, len(corpus))
# for query in queries:
#     query_embedding = embedder.encode(query, convert_to_tensor=True)

#     # We use cosine-similarity and torch.topk to find the highest 5 scores
#     cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
#     top_results = torch.topk(cos_scores, k=top_k)

#     print("\n\n======================\n\n")
#     print("Query:", query)
#     print("\nTop 5 most similar sentences in corpus:")

#     for score, idx in zip(top_results[0], top_results[1]):
#         print(corpus[idx], "(Score: {:.4f})".format(score))

#     """
#     # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
#     hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
#     hits = hits[0]      #Get the hits for the first query
#     for hit in hits:
#         print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
#     """
