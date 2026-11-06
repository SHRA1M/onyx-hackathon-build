"""The gate, Y.3172 P node (order Task 6): pure functions, no model calls. The model proposes; this decides.

decide(proposal, state, kb) -> Verdict{allow|hold|block|insufficient_evidence, clause_ids, reasons[]}. A proposal
passes only if its quote (20+ characters) is verbatim in a chunk the proposing agent retrieved, every cited chunk is
VERIFIED, the verb is in the agent's mandate, the inject it answers was released to that agent, any deadline it states
comes from rules.json, and every gate for its verb allows it. The strictest gate decides: block, then hold.
A cited id not among the clauses given to the agent first resolves to the one given clause it names without its
language ending (resolve_ids, hq addendum to C4, 2026-10-21); the verdict records each correction.

clause_ids are rules.json ids, binding UAE only (addendum 16). Global examples (IMDA 2.2.2, EU AI Act 50, GDPR 22(3))
appear in reasons[] with kind 'design_basis', never as the deciding clause. reasons[] entries carry 'gate' and 'kind':
check (a condition tested), obligation (what must happen next, for the coordinator), quote, design_basis, override.

Facts the gates read live in State.facts under the scenario files' own names (onyx/data/scenarios/*.json); the
proposal's args say what the agent wants done (change, recipient, payload, price). Ungoverned mode swaps decide for
allow_all and nothing else, so the diff between the runs is the gate alone.
"""

from __future__ import annotations

import copy
import json
import re
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from typing import Any

from onyx import data, kb as kb_store

ALLOW, HOLD, BLOCK, INSUFFICIENT = "allow", "hold", "block", "insufficient_evidence"
SEVERITY = {ALLOW: 0, HOLD: 1, BLOCK: 2}

# Design basis, never deciding (addendum 16). Quotes verbatim from the hq texts the order's sources table names
# (standards-text/global-2026-10-17/).
IMDA_2_2_2 = {"source": "imda-mgf-agentic-v1-5", "clause": "2.2.2",
              "text": "Denying action by default when approval infrastructures fail (e.g. when human supervisors are "
                      "unreachable or agents attempt new actions that do not have any established approval policies in "
                      "place)"}
EU_AI_ACT_50 = {"source": "eu-ai-act-2026-07-27", "clause": "50(1), 50(5)",
                "text": "the natural persons concerned are informed that they are interacting with an AI system"}
GDPR_22_3 = {"source": "gdpr-art22", "clause": "22(3)",
             "text": "at least the right to obtain human intervention on the part of the controller"}


@dataclass
class Verdict:
    verdict: str
    clause_ids: list[str] = field(default_factory=list)
    reasons: list[dict[str, Any]] = field(default_factory=list)
    resolved: list[dict[str, str]] = field(default_factory=list)  # {cited, resolved} per corrected id

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        if not self.resolved:
            del d["resolved"]
        return d


@dataclass
class State:
    agent: str
    inject: str  # the scenario step the proposal answers, e.g. "S2-3"
    released: set[str] = field(default_factory=set)  # injects the coordinator released to this agent
    retrieved: set[str] = field(default_factory=set)  # chunk ids this agent retrieved for this step
    channel: str = ""  # the adviser's classification: app_chat, web, voice, business_centre
    facts: dict[str, Any] = field(default_factory=dict)
    humans: tuple[str, ...] = ()  # named humans reachable now
    resolve: bool = True  # False only to replay a log recorded before resolve_ids
    recipient_resolution: bool = False  # run_start's flag (Task 52b): a log without it replays under the old reading


class Knowledge:
    """What the gate reads: rules.json, the committed chunks, the mandates. Injectable for tests."""

    def __init__(self, rules: dict[str, dict[str, Any]], mandates: dict[str, Any],
                 chunk: Callable[[str], dict[str, Any] | None]) -> None:
        self.rules, self.mandates, self._chunk = rules, mandates, chunk

    @classmethod
    @lru_cache(maxsize=1)
    def load(cls) -> Knowledge:
        def chunk(chunk_id: str) -> dict[str, Any] | None:
            document_id, _, clause = chunk_id.partition(":")
            try:
                return kb_store.get_chunk(document_id, clause)
            except KeyError:
                return None
        return cls({r["id"]: r for r in data.load_rules()}, data.load_mandates(), chunk)

    def chunk(self, chunk_id: str) -> dict[str, Any] | None:
        return self._chunk(chunk_id)

    def verbs(self, agent: str) -> set[str]:
        return {v["verb"] for v in self.mandates.get(agent, {}).get("verbs", [])}


# --- small helpers ----------------------------------------------------------------------------------------

def _yes(value: Any) -> bool:
    """A scenario fact as a boolean: False, None, '' and text starting 'none' or 'no' are no."""
    if isinstance(value, bool) or value is None:
        return bool(value)
    text = str(value).strip().lower()
    return not (text in {"", "no", "false"} or text.startswith(("none", "no ", "no,", "no;")))


def _check(gate: str, text: str, clause: str = "") -> dict[str, Any]:
    return {"gate": gate, "kind": "check", "text": text, **({"clause": clause} if clause else {})}


def _must(gate: str, text: str, clause: str = "", **extra: Any) -> dict[str, Any]:
    return {"gate": gate, "kind": "obligation", "text": text, **({"clause": clause} if clause else {}), **extra}


def _basis(gate: str, basis: dict[str, str]) -> dict[str, Any]:
    return {"gate": gate, "kind": "design_basis", **basis}


def _quote(gate: str, rule: dict[str, Any]) -> dict[str, Any]:
    return {"gate": gate, "kind": "quote", "clause": rule["id"], "label": rule["label"], "en": rule["quote"],
            "ar": rule.get("quote_ar", "")}


def _deadline(kb: Knowledge, rule_id: str, start: Any = None) -> dict[str, Any]:
    rule = kb.rules[rule_id]
    return {"rule": rule_id, "value": rule["value"], "unit": rule["unit"], "from": start}


def _retention(kb: Knowledge, rule_id: str) -> str:
    rule = kb.rules[rule_id]
    years = re.match(r"\d+", rule["value"]).group(0)
    return f"{years} years ({rule['label']})"


def _hours(window: str) -> tuple[str, str]:
    start, end = re.findall(r"\d{2}:\d{2}", window)
    return start, end


def _finding(verdict: str, clauses: list[str], reasons: list[dict[str, Any]]) -> Verdict:
    return Verdict(verdict, clauses, reasons)


THIRD_PARTY_WORDS = ("partner", "third party", "dunes", "شريك", "طرف ثالث", "ديونز")
SUBSCRIBER_WORDS = ("subscriber", "customer", "account holder", "المشترك", "العميل")
SUBSCRIBER, THIRD_PARTY, HUMAN = "subscriber", "third_party", "human"


def _heard(value: Any) -> str:
    return str(value or "").replace("_", " ").replace("-", " ").strip().lower()


def _names_third_party(value: Any) -> bool:
    """A substring match: a third-party word anywhere in the value."""
    return any(word in _heard(value) for word in THIRD_PARTY_WORDS)


def _names_subscriber(value: Any) -> bool:
    """A whole-value match, a subscriber word or "the " plus one: "Subscriber Services LLC" and "not the subscriber"
    never resolve to the subscriber."""
    return _heard(value).removeprefix("the ") in SUBSCRIBER_WORDS


def _on_roster(p: Any, s: State) -> bool:
    return p.target in s.facts.get("human_agents_on_shift", [])


def _resolved(p: Any, s: State) -> tuple[str, str]:
    """(recipient, the reason naming every field read). Reads every populated field together: a third-party word in any
    of them wins; an args.recipient that does not name the subscriber is a named outside party; the subscriber only
    when every populated field names the subscriber; a human for a reply whose target is on the roster, or that says
    human (held unless on the roster); otherwise unresolved, ''."""
    recipient = p.args.get("recipient")
    fields = [(name, value) for name, value in (("recipient", recipient), ("recipient_type", p.args.get("recipient_type")),
                                                ("target", p.target)) if value]
    read = "; ".join(f"{name}: {value}" for name, value in fields) or "no field names a recipient"
    says_human = p.verb == "draft_reply" and _heard(recipient) == HUMAN
    if any(_names_third_party(value) for _, value in fields):
        return THIRD_PARTY, f"{read} → {THIRD_PARTY} (a third-party word wins)"
    if recipient and not _names_subscriber(recipient) and not says_human:
        return THIRD_PARTY, f"{read} → {THIRD_PARTY} (a named outside party)"
    if fields and all(_names_subscriber(value) for _, value in fields):
        return SUBSCRIBER, f"{read} → {SUBSCRIBER}"
    if p.verb == "draft_reply" and (says_human or _on_roster(p, s)):
        return HUMAN, f"{read} → {HUMAN}"
    return "", f"{read} → unresolved"


def _recipient(p: Any, s: State) -> Any:
    """Without the flag, the reading every log before Task 52b was recorded on: an absent recipient is the subscriber."""
    return _resolved(p, s)[0] if s.recipient_resolution else p.args.get("recipient", SUBSCRIBER)


def read_items(values: Any, terms: Iterable[str]) -> set[str]:
    """A model-written list as the set a gate checks (hq ruling 2026-10-22, after a dict in args.data crashed C5 S2
    run2). A string is kept as written and matches exactly. Any other item becomes its canonical JSON text (sorted
    keys, ensure_ascii False), kept in the set so nothing the model wrote goes unread, and each of the check's terms
    that text names as a whole word is added, as the plain string would be."""
    items: set[str] = set()
    for value in values if isinstance(values, list) else [values]:
        if isinstance(value, str):
            items.add(value)
            continue
        text = json.dumps(value, sort_keys=True, ensure_ascii=False)
        items.add(text)
        items |= {t for t in terms if re.search(rf"(?<!\w){re.escape(t)}(?!\w)", text)}
    return items


def _catalogue_item(facts: dict[str, Any], sku: str) -> dict[str, Any] | None:
    return next((item for item in facts.get("catalogue", []) if item.get("sku") == sku), None)


def _languages_needed(facts: dict[str, Any]) -> set[str]:
    preferred = str(facts.get("preferred_language", "unknown")).lower()
    return {"ar"} if preferred.startswith("arabic") else {"en"} if preferred.startswith("english") else {"ar", "en"}


def _language(gate: str, p: Any, s: State) -> Verdict:
    """CPR 3.2.2: the preferred language, both where it is unknown."""
    given = read_items(p.args.get("languages") or ([p.args["language"]] if p.args.get("language") else []),
                       {"ar", "en"})
    needed = _languages_needed(s.facts)
    if needed <= given:
        return _finding(ALLOW, ["cpr-3-2-2"], [_check(gate, f"written in {', '.join(sorted(needed))}", "cpr-3-2-2")])
    return _finding(HOLD, ["cpr-3-2-2"], [_must(gate, f"write it in {', '.join(sorted(needed))} (preferred "
                                                f"language {s.facts.get('preferred_language', 'unknown')})", "cpr-3-2-2")])


# --- the gates ----------------------------------------------------------------------------------------------
# Each takes (proposal, state, kb) and returns a Verdict for its own clauses, or None where it does not apply.

def consent_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """CPR 4.3, 4.6, 4.7.1 to 4.7.3, 4.10 plus 4.11 OTP (strict reading), 4.22, 4.23, 4.17, 5.4.1, 3.9, 4.4 three
    renewal conditions tested not the label, 4.9, 9.4.2 partner cap, 16.9.2; Electronic Transactions 10, 12(2)(b)."""
    g, f, change = "consent_gate", s.facts, p.args.get("change", "")
    if p.verb == "propose_change" and change in {"renew", "upgrade", "migrate"} or p.args.get("basis") == "renewal":
        return _renewal(p, s, kb) if change != "upgrade" and change != "migrate" else _upgrade(p, s)
    if p.verb != "propose_sale" or p.args.get("outbound"):
        return None
    reasons, clauses, missing = [], ["cpr-4-7-1"], []
    if s.channel == "app_chat":
        clauses += ["cpr-4-10", "cpr-4-11", "cpr-4-22-1", "cpr-4-22-2"]
        if not (_yes(f.get("otp_completed")) and _yes(f.get("otp_matches"))):
            missing.append("an OTP completed and matched (4.10 multi-step with 2FA; 4.11 OTP is the default 2FA; "
                           "4.22.1 no single-click purchase)")
        if not _yes(f.get("terms_accepted")):
            missing.append("acceptance of the terms and conditions of the offer (4.22.2)")
        reasons.append(_must(g, "the on-screen yes/no control defaults to 'no' (4.22.3)", "cpr-4-22-3"))
        clauses.append("cpr-4-22-3")
    elif s.channel == "web":
        clauses += ["cpr-4-23-2", "cpr-4-23-3"]
        if not (_yes(f.get("otp_completed")) and _yes(f.get("otp_matches"))):
            missing.append("a 2FA procedure for this purchase (4.23.2)")
        reasons.append(_must(g, "the on-screen yes/no control defaults to 'no' (4.23.3)", "cpr-4-23-3"))
    elif s.channel == "voice":
        clauses += ["cpr-4-17-1", "cpr-4-17-3"]
        if not _yes(f.get("identity_verified")):
            missing.append("the subscriber's identity verified (4.17.1)")
        if not _yes(f.get("call_recorded")):
            missing.append("a voice recording of the verbal consent to the terms (4.17.3)")
    else:
        missing.append(f"a sales channel classified by the adviser (got {s.channel or 'none'})")
    if p.args.get("third_party_charge") and not float(f.get("partner_cap_aed") or 0) > 0:
        clauses.append("cpr-9-4-2")
        missing.append("a partner charge cap above its default of AED 0 per month, set by the subscriber (9.4.2)")
    if p.args.get("out_of_bundle") and not _yes(f.get("out_of_bundle_opt_in")):
        clauses.append("cpr-16-9-2")
        missing.append("a specific opt-in to the out-of-bundle rate (16.9.2)")
    if missing:
        clauses += ["cpr-4-3"]
        return _finding(HOLD, clauses, reasons + [_check(g, f"waits for {m}") for m in missing])
    clauses += ["cpr-4-7-2", "cpr-4-6", "cpr-5-4-1", "et-10", "et-12-2-b"]
    reasons += [_check(g, "positive affirmative action, multi-step, completed (4.7.1)", "cpr-4-7-1"),
                _check(g, f"consent form: {f.get('consent_form', 'electronic interaction')}, stored (4.7.2; ET 10, "
                          "12(2)(b): the system's message is the operator's)", "cpr-4-7-2"),
                _must(g, "store the consent evidence; in a dispute the operator must prove consent (4.6)", "cpr-4-6"),
                _must(g, "send the PSCM right after the purchase: date and time, service, price and term, "
                         "cancellation link (5.4.1)", "cpr-5-4-1")]
    if s.channel == "app_chat":
        clauses.append("cpr-4-22-4")
        reasons.append(_must(g, "the PSCM goes out with immediate effect, via the App (4.22.4)", "cpr-4-22-4"))
    reasons.append(_must(g, f"the PSCM is written in {', '.join(sorted(_languages_needed(f)))} (3.2.2)", "cpr-3-2-2"))
    return _finding(ALLOW, clauses + ["cpr-3-2-2"], reasons)


def _renewal(p: Any, s: State, kb: Knowledge) -> Verdict:
    """CPR 4.4: the exception from 4.3 for an existing service extended or renewed, tested on its three conditions,
    never on the word 'renewal'."""
    g, f = "consent_gate", s.facts
    item = _catalogue_item(f, p.args.get("sku", "")) or {}
    charge = float(p.args.get("price_aed", item.get("price_aed", 0)) or 0)
    tests = {
        "cpr-4-4-1": (bool(item.get("recurring")), "consistent with the terms of the contract for that existing "
                      f"Service: the catalogue says recurring={item.get('recurring')}"),
        "cpr-4-4-2": (charge == 0, f"unquestionably without prejudice: a further charge of AED {charge:g}"),
        "cpr-4-4-3": (charge == 0, f"unquestionably to the advantage: a further charge of AED {charge:g}"),
    }
    reasons = [_check(g, f"4.4 {rid[-1]}: {'met' if ok else 'not met'}, {why}", rid) for rid, (ok, why) in tests.items()]
    clauses = ["cpr-4-4", *tests]
    if any(ok for ok, _ in tests.values()) or _yes(f.get("new_consent")):
        return _finding(ALLOW, clauses, reasons + [_check(g, "the 4.4 exception applies", "cpr-4-4")])
    return _finding(HOLD, clauses + ["cpr-4-3", "cpr-4-7-3"], reasons + [
        _check(g, "no 4.4 condition holds, so 4.3 applies: no charge without an express order", "cpr-4-3"),
        _check(g, "silence is not consent: the subscriber's failure to opt out is no consent (4.7.3)", "cpr-4-7-3")])


def _upgrade(p: Any, s: State) -> Verdict:
    g = "consent_gate"
    if _yes(s.facts.get("new_consent")):
        return _finding(ALLOW, ["cpr-4-9"], [_check(g, "the subscriber consented to the upgrade (4.9)", "cpr-4-9")])
    return _finding(HOLD, ["cpr-4-9", "cabinet-66-2023-34-5"], [
        _check(g, "no upgrade or migration without consent (4.9)", "cpr-4-9"),
        _check(g, "a unilateral change of the service terms is void (66/2023 34(5))", "cabinet-66-2023-34-5")])


def disclosure_before_sale_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """Electronic Transactions 11(2): a contract with an automated system binds only if the person knows, or is
    supposed to know, it is automated. EU AI Act 50(1), 50(5) as the global example."""
    if p.verb != "propose_sale":
        return None
    g = "disclosure_before_sale_gate"
    basis = _basis(g, EU_AI_ACT_50)
    if _yes(s.facts.get("automated_disclosure_logged")):
        return _finding(ALLOW, ["et-11-2"], [_check(g, "the automated-system statement is logged", "et-11-2"), basis])
    return _finding(HOLD, ["et-11-2"], [
        _must(g, "state that an automated system is selling, before any purchase step, and log it", "et-11-2"), basis])


def price_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """CPR 3.3, 5.3: quoted figures from the catalogue only. Consumer Law 29 and Cybercrimes 48 in reasons."""
    if "price_aed" not in p.args:
        return None
    g, sku = "price_gate", p.args.get("sku", "")
    item = _catalogue_item(s.facts, sku)
    if item is not None and float(item["price_aed"]) == float(p.args["price_aed"]):
        return _finding(ALLOW, ["cpr-3-3", "cpr-5-3"], [
            _check(g, f"AED {p.args['price_aed']} for {sku} is the catalogue figure", "cpr-5-3")])
    found = f"the catalogue says AED {item['price_aed']}" if item else "not in the catalogue"
    return _finding(BLOCK, ["cpr-3-3", "cpr-5-3"], [
        _check(g, f"AED {p.args['price_aed']} for {sku or 'no sku'}: {found}; information must be accurate and "
                  "truthful (3.3, 5.3)", "cpr-3-3"),
        _check(g, "a misleading figure is a penalised act: Consumer Law 29; Cybercrimes 48 (inaccurate data in a "
                  "promotion)", "consumer-law-29")])


def price_change_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """CPR 17.2: notice at least 28 calendar days (the English; the Arabic says days) before a price increase, with
    an opt-out route."""
    if p.args.get("change") != "price_increase":
        return None
    g, rule = "price_change_gate", kb.rules["cpr-17-2"]
    days, given = int(rule["value"]), int(p.args.get("notice_days") or 0)
    reasons, ok = [_quote(g, rule)], True
    if given < days:
        ok = False
        reasons.append(_check(g, f"notice of {given} days; at least {days} {rule['unit']} required", "cpr-17-2"))
    if not p.args.get("opt_out_route"):
        ok = False
        reasons.append(_check(g, "the notice names no route for the subscriber to opt out", "cpr-17-2"))
    return _finding(ALLOW if ok else BLOCK, ["cpr-17-2"], reasons)


def cancellation_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """CPR 13.4 as easy as ordering, 13.6 immediate suspension, 13.8 no retention pitch before cancellation."""
    if p.args.get("change") != "cancel":
        return None
    g, clauses, bad = "cancellation_gate", ["cpr-13-4", "cpr-13-6"], []
    if p.args.get("retention_offer"):
        clauses.append("cpr-13-8")
        bad.append(_check(g, "a retention pitch before the cancellation; an exit interview only with consent and "
                             "after it (13.8)", "cpr-13-8"))
    if p.args.get("effective") != "immediate":
        bad.append(_check(g, f"effective {p.args.get('effective') or 'unstated'}: the service and further charges "
                             "are suspended with immediate effect (13.6)", "cpr-13-6"))
    reasons = [_must(g, "the cancellation route is no more complex than the ordering route (13.4)", "cpr-13-4")]
    return _finding(BLOCK if bad else ALLOW, clauses, bad + reasons)


def child_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """Child Digital Safety 7(1), 11(1)(b): an age or caregiver flag before any change or disclosure; absent = unverified."""
    if s.agent != "care" or p.verb not in {"propose_sale", "propose_change", "disclose_account"}:
        return None
    g, flag = "child_gate", str(s.facts.get("age_flag", "")).lower()
    clauses = ["child-digital-safety-7-1", "child-digital-safety-11-1-b"]
    if flag.startswith("adult"):
        return _finding(ALLOW, [], [_check(g, f"age flag: {s.facts['age_flag']}")])
    if flag and _yes(s.facts.get("caregiver_verified")):
        return _finding(ALLOW, clauses, [_check(g, "child account; the caregiver is verified (11(1)(b))",
                                                "child-digital-safety-11-1-b")])
    return _finding(HOLD, clauses, [_check(g, f"age flag {flag or 'absent'}: unverified; a caregiver must be verified "
                                              "and sign the service terms first (7(1), 11(1)(b))",
                                           "child-digital-safety-7-1")])


def verification_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """Electronic Transactions 33 trust level, set by the adviser; account data only at or above it, the level
    logged (CPR 24.10). A loss or theft report: verify the reporter first (Decision 16/2026 4.17), two-hour clock
    from receipt (4.18)."""
    g, f = "verification_gate", s.facts
    if p.verb == "propose_change" and p.args.get("change") == "block_device":
        start = f.get("report_received") or f.get("received") or (f.get("loss_report") or {}).get("received")
        clock = _must(g, "block the device and SIM and notify the other licensee within the 4.18 limits",
                      "d16-4-18", deadline=_deadline(kb, "d16-4-18", start))
        if not _yes(f.get("identity_verified")):
            return _finding(HOLD, ["d16-4-17", "cpr-24-10", "d16-4-18"], [
                _check(g, "the reporter's identity is not verified; verify the report immediately, including the "
                          "reporter's identity, before the block (4.17)", "d16-4-17"),
                _must(g, "disclose nothing about the account to the unverified caller (24.10)", "cpr-24-10"), clock])
        return _finding(ALLOW, ["d16-4-17", "d16-4-18"], [
            _check(g, f"identity verified by {f.get('verified_by', 'a named human')} at {f.get('verified_at', '?')}",
                   "d16-4-17"), clock])
    if p.verb != "disclose_account" or _recipient(p, s) != SUBSCRIBER:
        return None
    required = str(f.get("verification_level_set_by_adviser", "")).split(" ")[0].lower()
    achieved = str(f.get("trust_level") or f.get("verification_level_set_by_adviser", "")).split(" ")[0].lower()
    levels = ["low", "medium", "high"]  # ET 33: the three trust levels
    if required not in levels:
        return _finding(HOLD, ["cpr-24-10", "et-33"], [
            _check(g, "no ET 33 trust level set by the adviser; no account data before an adequate verification "
                      "process (24.10)", "cpr-24-10")])
    if achieved not in levels or levels.index(achieved) < levels.index(required):
        return _finding(HOLD, ["cpr-24-10", "et-33"], [
            _check(g, f"session trust level {achieved or 'none'} is below the level the adviser set ({required})",
                   "et-33")])
    return _finding(ALLOW, ["cpr-24-10", "et-33", "cpr-3-3"], [
        _check(g, f"trust level {achieved}, at or above the adviser's {required} (ET 33); logged before disclosure",
               "et-33"),
        _must(g, "the figures come from the account facts, nothing invented (3.3)", "cpr-3-3")])


DIRECT_IDENTIFIERS = {"name", "msisdn", "number", "emirates_id", "id", "invoice", "invoices", "chat",
                      "account_record", "top_up_history", "interconnection"}


def sharing_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """CPR 24.6 and fn 35 (recorded consent, contractual or later, no opt-out exercised), 24.7 interconnection data
    never for marketing, 24.9 the third party's contract, PDPL 7(5) the processor's guarantees, PDPL 17 objection."""
    if p.verb != "disclose_account" or _recipient(p, s) in {SUBSCRIBER, ""}:  # '' only with the flag: recipient_gate
        return None
    g, f, fields = "sharing_gate", s.facts, read_items(p.args.get("data", []), {"interconnection"})
    bad, clauses = [], ["cpr-24-6", "cpr-24-6-fn-35"]
    if "interconnection" in fields or _yes(f.get("interconnection_data_requested")):
        clauses.append("cpr-24-7")
        bad.append(_check(g, "interconnection data may not be used for any marketing purposes (24.7)", "cpr-24-7"))
    involved = _yes(f.get("partner_directly_involved_in_service"))
    if not involved:
        consent = _yes(f.get("consent_on_file_for_sharing")) and _yes(f.get("consent_to_share_with_third_parties", True))
        if not consent:
            bad.append(_check(g, "no prior consent on record, contractual or later, for this third party (24.6, fn 35); "
                                 f"record: {f.get('consent_to_share_with_third_parties', 'none')}", "cpr-24-6"))
        if _yes(f.get("marketing_opt_out")) or _yes(f.get("marketing_opt_out_on_file")):
            clauses.append("pdpl-17")
            bad.append(_check(g, f"the subscriber objected: {f.get('marketing_opt_out', 'opt-out on file')} "
                                 "(PDPL 17)", "pdpl-17"))
    if bad:
        return _finding(BLOCK, clauses, bad + [_must(g, "nothing about any subscriber leaves; the refusal cites the "
                                                        "clauses")])
    return _finding(ALLOW, clauses + ["cpr-24-9", "pdpl-7-5"], [
        _must(g, "the contract holds the third party responsible for the privacy of the information (24.9)", "cpr-24-9"),
        _must(g, "the processor has sufficient guarantees for technical and organisational measures (PDPL 7(5))",
              "pdpl-7-5")])


def model_provider_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """Minimum de-identified payload, processor contract on file (PDPL 8(1)), foreign-recipient notice (13(2)(d),
    (g)), log what left, cite Telecom Law 72(2). A payload with direct identifiers abroad has no Bureau-approved
    case on file (PDPL 22, 23(2)): block, and a block has no override."""
    provider = p.args.get("model_provider")
    if not provider:
        return None
    g, f = "model_provider_gate", s.facts
    raw = provider.get("payload", [])
    payload = [v if isinstance(v, str) else json.dumps(v, sort_keys=True, ensure_ascii=False)
               for v in (raw if isinstance(raw, list) else [raw])]  # in order: the log says what left
    record = f.get("model_provider", {})
    identifiers = sorted(read_items(raw, DIRECT_IDENTIFIERS) & DIRECT_IDENTIFIERS)
    contract = f.get("processor_contract") or record.get("processor_contract_on_file")
    notice = record.get("foreign_recipient_notice_given_at_contract")
    if identifiers:
        return _finding(BLOCK, ["pdpl-22", "pdpl-22-1", "pdpl-23-2", "pdpl-23-1-a", "pdpl-8-1", "pdpl-13-2-d",
                                "pdpl-13-2-g", "licence-3-4-1", "telecom-law-72-2"], [
            _check(g, f"the payload holds direct identifiers ({', '.join(identifiers)}) for a provider "
                      f"{record.get('location', 'abroad')}", "pdpl-22"),
            _check(g, "no case approved by the Bureau and no named destination country on file, so 22(1) cannot be "
                      "applied; the transfer controls are left to Executive Regulations (23(2))", "pdpl-23-2"),
            _check(g, "the contract route (23(1)(a)) needs the destination to have no data protection law, a fact "
                      "not on file", "pdpl-23-1-a"),
            _check(g, f"processor contract ({'on file' if _yes(contract) else 'none'}, 8(1)) and foreign-recipient "
                      f"notice ({'given' if _yes(notice) else 'none'}, 13(2)(d), (g)) do not make the transfer an "
                      "approved case", "pdpl-8-1"),
            _check(g, "disclosing the content of a message or service without right is an offence for anyone "
                      "connected to the licensee in a way that gives access to it (Telecom Law 72(2))",
                   "telecom-law-72-2"),
            _check(g, "the operator stays fully liable (licence 3.4.1); deny by default", "licence-3-4-1")])
    clauses = ["pdpl-8-1", "pdpl-7-5", "pdpl-13-2-d", "pdpl-13-2-g", "cpr-24-5", "licence-3-4-1", "telecom-law-72-2"]
    missing = []
    if not _yes(contract):
        missing.append(_check(g, "no processor contract on file (PDPL 8(1), 7(5))", "pdpl-8-1"))
    if not _yes(notice):
        missing.append(_check(g, "the subscriber was not told of recipients outside the State (13(2)(d), (g))",
                              "pdpl-13-2-d"))
    if missing:
        return _finding(HOLD, clauses, missing)
    contract_id = re.search(r"PC-[\w-]+", str(contract))
    return _finding(ALLOW, clauses, [
        _check(g, "payload de-identified: no direct identifiers"),
        _must(g, f"log what left: {', '.join(payload)}; to the model provider {record.get('location', '')}; under "
                 f"contract {contract_id.group(0) if contract_id else contract}", "pdpl-8-1"),
        _must(g, "access limited to trained, authorised personnel (24.5); the operator stays fully liable "
                 "(licence 3.4.1)", "cpr-24-5"),
        _must(g, "only the logged fields leave; no other content of the subscriber's messages or services is "
                 "disclosed (Telecom Law 72(2))", "telecom-law-72-2")])


def disconnection_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """CPR 22.1.1 notice and 22.2 content first, 22.1.2 confinement, 22.3 basic services, 22.4 emergency numbers,
    22.5 exception; DPIA on file (PDPL 21(2)(a)); held while a human review is open (18(4)); no reliance on a
    unilateral-termination term (Cabinet 66/2023 34(1), as the frozen keys cite). GDPR 22(3) as the global example."""
    change = p.args.get("change")
    if p.verb != "propose_change" or change not in {"notice", "suspend", "interrupt", "disconnect"}:
        return None
    g, f = "disconnection_gate", s.facts
    if change == "notice":
        needed = {"actions_required", "due_dates", "consequences", "interruption_date"}
        content = read_items(p.args.get("content", []), needed)
        lang = _language(g, p, s)
        reasons = [_check(g, "the individual notice and warning before any interruption (22.1.1)", "cpr-22-1-1")]
        if needed - content:
            return _finding(HOLD, ["cpr-22-1-1", "cpr-22-2"], reasons + [
                _check(g, f"the warning lacks {', '.join(sorted(needed - content))} (22.2)", "cpr-22-2")] + lang.reasons)
        reasons.append(_check(g, "actions required, due dates, consequences and the planned interruption (22.2)",
                              "cpr-22-2"))
        return _finding(lang.verdict, ["cpr-22-1-1", "cpr-22-2", *lang.clause_ids], reasons + lang.reasons)
    if _yes(f.get("authority_request")):
        return _finding(ALLOW, ["cpr-22-5"], [_check(g, "requested by an authorised official of a competent authority "
                                                        "for public or national security (22.5)", "cpr-22-5")])
    bad, held, clauses = [], [], ["cpr-22-1-1", "cpr-22-1-2", "cpr-22-3", "cpr-22-4", "pdpl-21-2-a"]
    if re.search(r"contract|term", str(p.args.get("basis", "")), re.IGNORECASE):
        clauses.append("cabinet-66-2023-34-1")
        bad.append(_check(g, f"relies on {p.args['basis']}: a term letting the provider terminate unilaterally "
                             "without referring to the consumer is void (66/2023 34(1))", "cabinet-66-2023-34-1"))
    if not _yes(f.get("warning_sent")):
        clauses.append("cpr-22-2")
        bad.append(_check(g, "no individual notice and warning yet (22.1.1), with the 22.2 content", "cpr-22-1-1"))
    unpaid = f.get("unpaid_service") or f.get("invoice_service")
    services = read_items(p.args.get("services", []), {unpaid} if unpaid else set())
    if unpaid and services - {unpaid}:
        bad.append(_check(g, f"reaches {', '.join(sorted(services - {unpaid}))}; confine it to {unpaid} (22.1.2)",
                          "cpr-22-1-2"))
    kept = read_items(p.args.get("kept", []), {"incoming calls", "emergency numbers"})
    if "incoming calls" not in kept:
        bad.append(_check(g, "incoming calls, a basic non-substitutable service, are cut (22.3)", "cpr-22-3"))
    if "emergency numbers" not in kept:
        bad.append(_check(g, "emergency numbers are not kept reachable (22.4)", "cpr-22-4"))
    dpia = _yes(f.get("dpia_on_file"))
    held.append(_check(g, f"impact assessment on file: {f['dpia_on_file']} (21(2)(a))" if dpia else
                       "no impact assessment on file for the automated decision (PDPL 21(2)(a))", "pdpl-21-2-a"))
    open_review = _yes(f.get("human_review_open"))
    if open_review:
        clauses.append("pdpl-18-4")
    reasons = [_basis(g, GDPR_22_3)]
    if bad:
        return _finding(BLOCK, clauses, bad + held + reasons)
    if not dpia:
        return _finding(HOLD, clauses, held + reasons)
    if open_review:
        return _finding(HOLD, clauses, held + reasons + [
            _check(g, "a human review of the automated decision is open; every further step waits for it (18(4))",
                   "pdpl-18-4")])
    return _finding(ALLOW, clauses + ["pdpl-18-1"], held + reasons + [
        _must(g, "log it as a decision resulting from automated processing, with the DPIA reference, so the 18(1) "
                 "objection and the 18(4) review attach to it", "pdpl-18-1")])


def complaint_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """On a 2.1.7 Consumer Complaint the AI stops: reference number and time-frame (26.13.2, 26.13.3), hand-over to
    a human (26.7.2 in both languages, licence 9.1), the hand-over logged as the IVR-equivalent moment for QoS
    T1(2a). The AI may draft_reply for the human only."""
    f = s.facts
    if not _yes(f.get("grievance_expressed")):
        return None
    g = "complaint_gate"
    handover = [_quote(g, kb.rules["cpr-26-7-2"]), _quote(g, kb.rules["licence-9-1"])]
    ack_rule = "cpr-26-13-3-phone" if s.channel == "voice" else "cpr-26-13-3-written"
    duties = [
        _must(g, "issue a reference number and the indicative time-frame now (26.13.2)", "cpr-26-13-2",
              deadline=_deadline(kb, ack_rule, f.get("time"))),
        _must(g, "hand the conversation to a named human (26.7.2; licence 9.1)", "cpr-26-7-2"),
        _must(g, "log the hand-over as the IVR-equivalent moment, so the QoS T1(2a) wait is measured from it",
              "qos-v3-0-t1-2a"),
    ]
    clauses = ["cpr-2-1-7", "cpr-26-7-2", "licence-9-1", "cpr-26-13-2", ack_rule, "cpr-26-7-1"]
    trigger = _check(g, "dissatisfaction or grievance expressed: a Consumer Complaint (2.1.7)", "cpr-2-1-7")
    if p.verb in {"escalate_to_human", "request_human_review"}:
        return _finding(ALLOW, clauses, [trigger, *handover, *duties])
    if s.agent != "care" or p.verb not in {"draft_reply", "propose_sale", "disclose_account"}:
        return None
    if p.verb == "draft_reply" and _recipient(p, s) == HUMAN:
        if p.target not in s.humans:
            return _finding(HOLD, ["cpr-26-7-2", "licence-9-1"], [
                trigger, _check(g, f"the draft is for {p.target or 'no one'}, not a named human on shift", "licence-9-1"),
                _basis(g, IMDA_2_2_2)])
        lang = _language(g, p, s)
        return _finding(lang.verdict, ["cpr-26-7-2", "licence-9-1", "cpr-4-6", *lang.clause_ids], [
            trigger, *handover,
            _must(g, f"the draft goes to {p.target}; the actor of the outgoing message is the human, never the agent",
                  "cpr-26-7-2"),
            _must(g, "without evidence of consent, the presumption runs against the operator (4.6)", "cpr-4-6"),
            *lang.reasons])
    return _finding(BLOCK, clauses, [
        trigger, _check(g, f"{p.verb} to the subscriber in a conversation regarding a Consumer Complaint: non-human "
                           "agents are precluded (26.7.2)", "cpr-26-7-2"), *handover, *duties])


def marketing_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """Cabinet 56/2024 Art 4, 5(6), 5(7); Spam Calls v4 9.5, 10.2, 14.3, 15.4 (09:00 to 18:00); CPR 28.25, 28.26;
    PDPL 17."""
    if p.verb != "propose_sale" or not p.args.get("outbound"):
        return None
    g, f = "marketing_gate", s.facts
    start, end = _hours(kb.rules["spam-calls-v4-15-4"]["value"])
    now = str(f.get("time", ""))[:5]
    bad, clauses = [], ["cabinet-56-2024-4", "spam-calls-v4-15-4", "spam-calls-v4-10-2", "cpr-28-26"]
    if not now or not start <= now < end:
        bad.append(_check(g, f"{now or 'no time'} is outside {start} to {end} (Spam Calls v4 15.4)", "spam-calls-v4-15-4"))
    if _yes(f.get("dncr_listed")) or "DNCR" in str(f.get("dncr", "")):
        clauses.append("spam-calls-v4-9-5")
        bad.append(_check(g, "the number is in the DNCR (enrolled by default, 9.5); a call is permissible only after "
                             "verifying it is not (10.2)", "spam-calls-v4-10-2"))
    if _yes(f.get("marketing_opt_out_on_file")) or _yes(f.get("marketing_opt_out")):
        clauses.append("pdpl-17")
        bad.append(_check(g, "the subscriber asked not to be contacted for advertising (28.26) and objected (PDPL 17)",
                          "cpr-28-26"))
    reasons = [_check(g, "marketing calls follow the 56/2024 Article 4 controls", "cabinet-56-2024-4")]
    if bad:
        return _finding(BLOCK, clauses, bad + reasons + [_must(g, "no call is placed and no call-back is scheduled")])
    clauses += ["cabinet-56-2024-5-7", "spam-calls-v4-14-3", "cpr-28-25"]
    if p.args.get("automated"):
        clauses.append("cabinet-56-2024-5-6")
    return _finding(ALLOW, clauses, reasons + [
        _must(g, "ask whether the consumer wants to continue before marketing (56/2024 5(7))", "cabinet-56-2024-5-7"),
        _must(g, "the call set-up continues only on the caller's specific action (14.3)", "spam-calls-v4-14-3"),
        _must(g, "not unduly intrusive or coercive (28.25)", "cpr-28-25")])


def human_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """deny_by_default for a human approver: a hand-over or a review with no named human reachable is held."""
    if p.verb not in {"escalate_to_human", "request_human_review"}:
        return None
    g = "deny_by_default"
    clauses = ["pdpl-18-4"] if p.verb == "request_human_review" else ["licence-9-1", "cpr-26-7-2"]
    if not s.humans:
        return _finding(HOLD, clauses, [_check(g, "no named human is reachable to take this over"),
                                        _basis(g, IMDA_2_2_2)])
    verb = "review the automated decision (PDPL 18(4))" if p.verb == "request_human_review" else "take the conversation"
    reasons = [_must(g, f"{s.humans[0]} is assigned to {verb}; the log's actor for it is the human", clauses[0])]
    terms = [k for k in s.facts if k.startswith("contract_term")]
    if p.verb == "request_human_review" and terms:
        # hq CPR read, gap 4 (key S4 step 4): 18(4) is not conditioned on 18(1), so 18(2) does not remove it.
        clauses += ["pdpl-18-1", "pdpl-18-2", "cabinet-66-2023-34-1"]
        reasons += [
            _check(g, "18(4) applies at the data subject's request, unconditioned on the 18(1) objection right",
                   "pdpl-18-1"),
            _check(g, f"{terms[0]} does not agree the automated processing in the contract, so the 18(2) exception "
                      "does not reach it", "pdpl-18-2"),
            _check(g, "a term letting the provider terminate unilaterally without referring to the consumer is void "
                      "(66/2023 34(1))", "cabinet-66-2023-34-1")]
    return _finding(ALLOW, clauses, reasons)


def records(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """Retention: complaints three years (licence 9.2.4), billing two (9.4.3), consent and 2FA five (CPR 3.9),
    PSCM, notices and recordings two (3.9); an Arabic copy of every contract or notice record (Consumer Law 8(4))."""
    g, f, keep = "records", s.facts, []

    def retain(what: str, rule_id: str) -> None:
        keep.append(_must(g, f"keep {what} for at least {_retention(kb, rule_id)}", rule_id))

    if p.verb == "propose_sale" and _yes(f.get("otp_completed")) and _yes(f.get("terms_accepted")):
        retain("the OTP and the acceptance as the consent record", "cpr-3-9-consent-2fa")
        retain("the PSCM", "cpr-3-9-pscm")
        keep.append(_must(g, "the PSCM record carries an Arabic copy (Consumer Law 8(4))", "consumer-law-8-4"))
    if p.args.get("change") == "notice":
        retain("the notice and warning", "cpr-3-9-notices")
        keep.append(_must(g, "the notice record carries an Arabic copy (Consumer Law 8(4))", "consumer-law-8-4"))
    if p.verb == "disclose_account" and {"invoice", "billing"} & read_items(p.args.get("data", []), {"invoice", "billing"}):
        retain("the billing information", "licence-9-4-3")
    if _yes(f.get("call_recorded")):
        retain("the call recording", "cpr-3-9-recordings")
    if _yes(f.get("grievance_expressed")) and p.verb in {"draft_reply", "escalate_to_human", "request_human_review"}:
        retain("the complaint record", "licence-9-2-4")
    if p.verb == "request_report":
        retain("the complaint record, furnished in the TDRA format and timeframe", "licence-9-2-4")
        keep.append(_must(g, "copies of records go to the TDRA on demand (3.9 complaints and disputes)",
                          "cpr-3-9-complaints"))
        if f.get("complaint_reference") or f.get("open_complaint"):
            keep.append(_must(g, "the record shows each open complaint's conclusion deadline", "cpr-26-14-2",
                              deadline=_deadline(kb, "cpr-26-14-2")))
        if f.get("tdra_dispute") or f.get("deadline"):
            keep.append(_must(g, "the dispute response is due within the 26.16.1 limit; cooperate fully (licence 9.3)",
                              "cpr-26-16-1", deadline=_deadline(kb, "cpr-26-16-1", f.get("submitted"))))
            keep.append(_must(g, "cooperate fully with the TDRA on the dispute (licence 9.3)", "licence-9-3"))
    if p.verb == "raise_dispute":
        keep.append(_must(g, "log the response clock: resolve and respond to the TDRA within the 26.16.1 limit",
                          "cpr-26-16-1", deadline=_deadline(kb, "cpr-26-16-1", f.get("submitted"))))
        keep.append(_must(g, "cooperate fully with the TDRA on the dispute (licence 9.3)", "licence-9-3"))
    if p.verb == "order_restore":
        keep.append(_must(g, "restore within the direction's scope and log the time; the direction is the basis "
                             "(26.11)", "cpr-26-11"))
    if not keep:
        return None
    return _finding(ALLOW, [r["clause"] for r in keep], keep)


def disclosure_recipient_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """Task 52b, only on a run carrying the flag. A disclosure to a recipient the fields do not identify is held, deny
    by default (IMDA 2.2.2: no established approval policy), never blocked: it may be the subscriber (24.10), a third
    party needing consent (24.6) or one directly involved in supplying the service (24.9), and a person confirms which."""
    if not s.recipient_resolution:
        return None
    g = "recipient_gate"
    recipient, read = _resolved(p, s)
    if recipient:
        return _finding(ALLOW, [], [_check(g, read)])
    return _finding(HOLD, ["cpr-24-6", "cpr-24-10", "cpr-24-9"], [
        _check(g, read),
        _check(g, "recipient not identified: the subscriber (24.10, after verification), a third party needing consent "
                  "(24.6), or one directly involved in supplying the ordered service (24.9); a human agent on shift "
                  "confirms which", "cpr-24-6"),
        _basis(g, IMDA_2_2_2)])


def reply_recipient_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """Task 52b, only on a run carrying the flag: a reply goes to the subscriber or a human agent on the roster; to
    anyone else it is held, deny by default. It cites no clause: care's prompt, which gives a verb its gates' clauses,
    does not change before submission."""
    if not s.recipient_resolution:
        return None
    g = "recipient_gate"
    recipient, read = _resolved(p, s)
    if recipient == SUBSCRIBER or (recipient == HUMAN and _on_roster(p, s)):
        return _finding(ALLOW, [], [_check(g, read)])
    return _finding(HOLD, [], [
        _check(g, read),
        _check(g, f"reply addressed to {p.target or 'no one'}: not the subscriber and not a human agent on shift (roster)"),
        _basis(g, IMDA_2_2_2)])


def change_word_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    """Task 52b, only on a run carrying the flag: a change none of the five gates decides (its word missing or
    unlisted) is held for a human, deny by default. Without this an unlisted word passes every gate by not applying."""
    if not s.recipient_resolution:
        return None
    if any(gate(p, s, kb) is not None for gate in (consent_gate, disconnection_gate, verification_gate,
                                                   cancellation_gate, price_change_gate)):
        return None
    g = "deny_by_default"
    return _finding(HOLD, [], [
        _check(g, f"change word {p.args.get('change') or 'none'} is not one the gates decide; held for a human"),
        _basis(g, IMDA_2_2_2)])


# The gates for each mandate verb (onyx/data/mandates.json). A verb listed with no gates passes on the base checks
# alone; a verb not listed has no gate and is held (deny_by_default).
GATES: dict[str, tuple[Callable[..., Verdict | None], ...]] = {
    "propose_sale": (child_gate, disclosure_before_sale_gate, price_gate, consent_gate, marketing_gate,
                     complaint_gate, records),
    "propose_change": (child_gate, consent_gate, price_gate, disconnection_gate, verification_gate,
                       cancellation_gate, price_change_gate, change_word_gate, records),
    "disclose_account": (child_gate, disclosure_recipient_gate, verification_gate, sharing_gate, complaint_gate,
                         records),
    "draft_reply": (reply_recipient_gate, complaint_gate, model_provider_gate, records),
    "classify_channel": (), "cite": (), "flag_gap": (),
    "raise_dispute": (records,), "order_restore": (records,), "request_report": (records,),
    "receive_objection": (), "receive_dpia": (), "request_human_review": (human_gate, complaint_gate, records),
    "release_event": (), "route": (), "escalate_to_human": (human_gate, complaint_gate, records),
}


LANGUAGE_ENDING = re.compile(r"-(?:en|ar)$")


def _bare(chunk_id: str) -> str:
    document_id, sep, clause = chunk_id.partition(":")
    return LANGUAGE_ENDING.sub("", document_id) + sep + clause


def resolve_ids(cited: Iterable[str], given: Iterable[str]) -> tuple[list[str], list[dict[str, str]]]:
    """hq addendum to C4 (2026-10-21): a cited id not among the given clauses resolves to the given clause whose id
    is equal once the language ending (-en, -ar) is removed from the document part of both, only when exactly one
    given clause matches. Never against the whole KB, never fuzzy. Used by the gate and by the eval. Returns the ids
    and a {cited, resolved} record per corrected id."""
    given = set(given)
    ids, corrected = [], []
    for cid in cited:
        matches = [] if cid in given else sorted(g for g in given if _bare(g) == _bare(cid))
        if len(matches) == 1:
            ids.append(matches[0])
            corrected.append({"cited": cid, "resolved": matches[0]})
        else:
            ids.append(cid)
    return ids, corrected


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _base_checks(p: Any, s: State, kb: Knowledge) -> Verdict | None:
    g = "base"
    if p.verb not in GATES:
        return Verdict(HOLD, [], [_check("deny_by_default", f"verb {p.verb} has no gate; held for a human"),
                                  _basis("deny_by_default", IMDA_2_2_2)])
    if p.verb not in kb.verbs(s.agent):
        return Verdict(BLOCK, [], [_check(g, f"verb {p.verb} is outside the {s.agent} mandate (mandates.json)")])
    if not s.inject or s.inject not in s.released:
        return Verdict(BLOCK, [], [_check(g, f"inject {s.inject or 'none'} was not released to {s.agent} "
                                             "(staged release)")])
    if not p.clause_ids:
        return Verdict(INSUFFICIENT, [], [_check(g, "no clause cited")])
    texts = []
    for cid in p.clause_ids:
        if cid not in s.retrieved:
            return Verdict(INSUFFICIENT, [], [_check(g, f"{cid} was not retrieved by {s.agent} for this step")])
        chunk = kb.chunk(cid)
        if chunk is None:
            return Verdict(INSUFFICIENT, [], [_check(g, f"{cid} is not in the knowledge base")])
        if chunk.get("status") != "VERIFIED":
            return Verdict(INSUFFICIENT, [], [_check(g, f"{cid} has status {chunk.get('status')}; only VERIFIED "
                                                        "text can carry a decision")])
        texts += [_normalize(chunk.get("text_en", "")), _normalize(chunk.get("text_ar", ""))]
    quote = _normalize(p.quote)
    if len(quote) < data.MIN_QUOTE or not any(quote in t for t in texts if t):
        return Verdict(INSUFFICIENT, [], [_check(g, f"the quote is not {data.MIN_QUOTE}+ characters verbatim in a "
                                                    "cited clause")])
    deadline = p.args.get("deadline")
    if deadline and not isinstance(deadline, dict):
        return Verdict(BLOCK, [], [_check(g, f"deadline {deadline!r} is not a rules.json rule, value and unit")])
    if deadline:
        rule = kb.rules.get(deadline.get("rule", ""))
        if rule is None or (str(deadline.get("value")), deadline.get("unit")) != (rule["value"], rule["unit"]):
            stated = f"{deadline.get('value')} {deadline.get('unit')}"
            return Verdict(BLOCK, [rule["id"]] if rule else [], [
                _check(g, f"deadline {stated} is not the rules.json value for {deadline.get('rule')}"
                          + (f" ({rule['value']} {rule['unit']})" if rule else ""), rule["id"] if rule else "")])
    return None


def decide(proposal: Any, state: State, kb: Knowledge | None = None) -> Verdict:
    resolved: list[dict[str, str]] = []
    if state.resolve and proposal.clause_ids:
        ids, resolved = resolve_ids(proposal.clause_ids, state.retrieved)
        if resolved:
            proposal = copy.copy(proposal)
            proposal.clause_ids = ids
    verdict = _decide(proposal, state, kb or Knowledge.load())
    verdict.resolved = resolved
    return verdict


def _decide(proposal: Any, state: State, kb: Knowledge) -> Verdict:
    failed = _base_checks(proposal, state, kb)
    if failed is not None:
        return failed
    findings = [v for gate in GATES[proposal.verb] if (v := gate(proposal, state, kb)) is not None]
    if not findings:
        return Verdict(ALLOW, [], [_check("base", "every base check passed; this verb has no further condition")])
    worst = max(SEVERITY[v.verdict] for v in findings)
    verdict = next(k for k, v in SEVERITY.items() if v == worst)
    deciding = [c for v in findings if SEVERITY[v.verdict] == worst for c in v.clause_ids]
    supporting = [c for v in findings for c in v.clause_ids]
    clause_ids = list(dict.fromkeys(deciding + supporting))
    reasons = [r for v in findings for r in v.reasons]
    if verdict == ALLOW and proposal.verb == "disclose_account" and state.recipient_resolution:
        reasons.append(_check("recipient_gate", f"allowed for recipient: {_recipient(proposal, state)}"))
    return Verdict(verdict, clause_ids, reasons)


MODEL_UNAVAILABLE = "model unavailable"  # args.reason of the coordinator's plain-code proposal (Task 29 Part A)


def decide_pending(proposal: Any, state: State, kb: Knowledge | None = None) -> Verdict:
    """Addendum 29: the action an abstention step is about, submitted by the coordinator after the adviser answered
    INSUFFICIENT_EVIDENCE. It cites nothing (no VERIFIED clause answers it), so the evidence checks do not apply;
    the verb must be in the agent's mandate, a gate rule that blocks or holds decides, and otherwise deny by
    default gives hold. Task 29 Part A sends the coordinator's hand-over here too when the model is down; its hold
    reason says the model was unavailable, not that the adviser answered (hq, 2026-10-29)."""
    kb = kb or Knowledge.load()
    if proposal.verb not in GATES:
        return _base_checks(proposal, state, kb)  # no gate: held (deny_by_default)
    if proposal.verb not in kb.verbs(state.agent):
        return Verdict(BLOCK, [], [_check("base", f"verb {proposal.verb} is outside the {state.agent} mandate "
                                                  "(mandates.json)")])
    findings = [v for gate in GATES[proposal.verb] if (v := gate(proposal, state, kb)) is not None]
    worst = max((SEVERITY[v.verdict] for v in findings), default=0)
    if worst:
        verdict = next(k for k, v in SEVERITY.items() if v == worst)
        deciding = [c for v in findings if SEVERITY[v.verdict] == worst for c in v.clause_ids]
        clause_ids = list(dict.fromkeys(deciding + [c for v in findings for c in v.clause_ids]))
        return Verdict(verdict, clause_ids, [r for v in findings for r in v.reasons])
    why = (f"the model was unavailable on {state.inject}: no model proposed and"
           if (proposal.args or {}).get("reason") == MODEL_UNAVAILABLE else
           f"the adviser answered INSUFFICIENT_EVIDENCE on {state.inject}:")
    return Verdict(HOLD, list(dict.fromkeys(c for v in findings for c in v.clause_ids)), [
        _check("deny_by_default", f"{why} no VERIFIED clause permits {proposal.verb}; held for a human"),
        _basis("deny_by_default", IMDA_2_2_2), *(r for v in findings for r in v.reasons)])


def allow_all(proposal: Any, state: State, kb: Knowledge | None = None) -> Verdict:
    """Ungoverned mode: the same pipeline with the gate removed."""
    return Verdict(ALLOW, [], [{"gate": "ungoverned", "kind": "check", "text": "ungoverned run: no gate"}])


DECIDERS = {"governed": decide, "ungoverned": allow_all}


def override(verdict: Verdict, approver: str, reason: str, log: Any, entity_id: str) -> Verdict:
    """Addendum 17: a named human may release a hold, logged under the human's name with the reason; a block has no
    override, and the attempt is refused and logged with the name that tried."""
    if not approver.strip():
        raise ValueError("an override needs the approver's name")
    event = {"actor": approver, "entity_type": "verdict", "entity_id": entity_id, "old_value": verdict.to_dict(),
             "clause_ids": verdict.clause_ids, "source": "onyx/gate.py override"}
    if verdict.verdict == HOLD:
        released = Verdict(ALLOW, verdict.clause_ids, verdict.reasons + [
            {"gate": "override", "kind": "override", "approver": approver, "text": reason}])
        log.append({**event, "action": "override_release", "new_value": released.to_dict(), "verdict": ALLOW,
                    "reason": reason})
        return released
    log.append({**event, "action": "override_refused", "verdict": verdict.verdict,
                "reason": f"override refused: only a hold can be released, this is {verdict.verdict}; attempted by "
                          f"{approver}, reason given: {reason}"})
    return verdict
