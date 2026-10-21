from __future__ import annotations

from onyx import kb
from onyx.agents.base import Agent, AgentOutput, Proposal

CPR = "tdra-cpr-v2-en"

# The rules differ by sales channel, so the conversation is classified first and that channel's conditions applied:
# plain code, not model judgement (hq hackathon-plan-2026-10-15.docx, "The checks"). Voice 4.17, app 4.22 plus 4.10,
# web 4.23 (order Task 5); 4.11 with the app, the strict reading (key S1 step 1); 4.15 is the clause's own words.
CHANNELS = {
    "business_centre": ("4.15",),
    "voice": ("4.17",),
    "app_chat": ("4.22", "4.10", "4.11"),
    "web": ("4.23",),
}


class Adviser(Agent):
    name = "adviser"
    role = "Checks each proposed action against the knowledge base and returns the clause that allows or blocks it."

    def classify_channel(self, request_id: str, channel: str) -> AgentOutput:
        if channel not in CHANNELS:
            raise ValueError(f"unknown channel {channel!r}: one of {', '.join(CHANNELS)}")
        clauses = CHANNELS[channel]
        clause_ids = [f"{CPR}:{clause}" for clause in clauses]
        quote = kb.get_chunk(CPR, clauses[0])["text_en"].split(":")[0]
        proposal = Proposal(verb="classify_channel", target=channel, args={"channel": channel, "clauses": list(clauses)},
                            clause_ids=clause_ids, quote=quote,
                            rationale=f"{channel}: CPR {', '.join(clauses)} apply")
        self._append({"action": "classify_channel", "entity_type": "conversation", "entity_id": request_id,
                      "new_value": {"channel": channel, "clauses": list(clauses)}, "clause_ids": clause_ids,
                      "quote": quote, "source": "onyx/agents/adviser.py CHANNELS", "reason": proposal.rationale})
        return AgentOutput(self.name, [proposal], sources_used=clause_ids, reasoning_chain=[proposal.rationale])
