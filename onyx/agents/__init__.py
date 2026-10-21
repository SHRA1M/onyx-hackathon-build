"""The five agents (order Task 5). Roles from hq hackathon-plan-2026-10-15.docx; verbs from onyx/data/mandates.json."""

from onyx.agents.adviser import Adviser
from onyx.agents.care import Care
from onyx.agents.coordinator import Coordinator
from onyx.agents.data_office import DataOffice
from onyx.agents.tdra import Tdra

AGENTS = {cls.name: cls for cls in (Care, Adviser, Tdra, DataOffice, Coordinator)}
