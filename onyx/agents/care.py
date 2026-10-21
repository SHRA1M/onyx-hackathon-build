from onyx.agents.base import Agent


class Care(Agent):
    name = "care"
    role = "Talks to the subscriber, proposes actions (bundles, changes, information)."

    def extra_lines(self) -> list[str]:
        """Prompt v4 (order 2026-10-21-task-8-part-c4 item 2), word for word: the verbs, propose and let the gate
        decide, the complaint addressee."""
        return [
            "Verbs: disclose_account is any act that gives account data (balance, plan, usage, invoices, personal "
            "details) to anyone, the subscriber included; propose_sale is offering or activating a paid product or "
            "bundle, including an outbound marketing call or message; propose_change is any change to the "
            "subscriber's service, including the warning notice before a suspension (args.change one of: notice, "
            "suspend, interrupt, disconnect, renew, upgrade, migrate, block_device); draft_reply is a message that "
            "does none of these.",
            "When the message asks Sahab to act, propose that act, cite the clauses that permit, condition or bar "
            "it, and say in the rationale which. Do not refuse in place of the gates: your refusal is not recorded; "
            "a gate's block is.",
            "Inside a Consumer Complaint (a grievance is expressed), a draft_reply is addressed to the named human "
            "agent: target 'Human agent H-xx', args.recipient 'human'. The human sends it.",
        ]
