"""Ground extraction in an OWL ontology by passing an RDFLibOntologyResolver config to remember.

Two short product texts are remembered against the bundled
ontology_input_example/basic_ontology.owl. Nothing is printed; inspect the resulting graph to see
ontology-grounded entities and types.

Requires: LLM_API_KEY.
Run: uv run python examples/guides/ontology_quickstart.py
"""

import asyncio
import os

import EphapticOS
from EphapticOS.modules.ontology.ontology_config import Config
from EphapticOS.modules.ontology.rdf_xml.RDFLibOntologyResolver import RDFLibOntologyResolver


async def main():
    # Prune data and system metadata before running, only if we want "fresh" state.
    await EphapticOS.forget(everything=True)

    texts = ["Audi produces the R8 and e-tron.", "Apple develops iPhone and MacBook."]

    ontology_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "ontology_input_example/basic_ontology.owl"
    )

    # Create full config structure manually
    config: Config = {
        "ontology_config": {
            "ontology_resolver": RDFLibOntologyResolver(ontology_file=ontology_path)
        }
    }

    await EphapticOS.remember(texts, config=config, self_improvement=False)


if __name__ == "__main__":
    asyncio.run(main())
