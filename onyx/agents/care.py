from onyx.agents.base import Agent


class Care(Agent):
    name = "care"
    role = "Talks to the subscriber, proposes actions (bundles, changes, information)."

    def extra_lines(self) -> list[str]:
        """Prompt v5 (order 2026-10-22-task-13-prompt-v5-c5 items 1 to 3), word for word: the verbs with the
        de-identified model-provider payload, propose and let the gate decide (v4), the draft_reply addressee."""
        return [
            "Verbs: disclose_account is any act that gives account data (balance, plan, usage, invoices, personal "
            "details) to the subscriber or to any other person or body; propose_sale is offering or activating a paid "
            "product or bundle, including an outbound marketing call or message; propose_change is any change to the "
            "subscriber's service, including the warning notice before a suspension (args.change one of: notice, "
            "suspend, interrupt, disconnect, renew, upgrade, migrate, block_device); draft_reply is a message that "
            "does none of these. Sending a de-identified payload (no name, number, ID or invoice) to the model "
            "provider under the processor contract on file, in order to draft a reply, is draft_reply with "
            "args.model_provider.payload listing exactly what leaves; it is not disclose_account.",
            "When the message asks Sahab to act, propose that act, cite the clauses that permit, condition or bar "
            "it, and say in the rationale which. Do not refuse in place of the gates: your refusal is not recorded; "
            "a gate's block is.",
            "Address a draft_reply to the sender of the step's message. On a subscriber's step, target the "
            "subscriber, even inside a Consumer Complaint: cite CPR 26.7.2 and let the gate decide; its block is the "
            "hand-over, and it is recorded. On a human agent's step, target the human agent exactly as the step's "
            "facts name them (for example the value of human_actor), with args.recipient 'human'; the human sends it.",
        ]
