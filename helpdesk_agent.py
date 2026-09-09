"""
====================================================================
 AI IT HELPDESK AGENT
 Naan Mudhalvan - AI Agents Bootcamp Project
 Use Case #4 : Diagnoses common technical issues and recommends
               troubleshooting steps using a knowledge base.
 Key Capabilities implemented : Agent + RAG + Tools
====================================================================

HOW THE 3 CAPABILITIES ARE IMPLEMENTED IN THIS FILE
-----------------------------------------------------
1. RAG (Retrieval Augmented Generation)
   -> retrieve_best_match() searches knowledge_base.py using a
      keyword / cosine-similarity scorer and RETRIEVES the most
      relevant IT issue + solution before generating a reply.

2. TOOLS (Tool Calling)
   -> create_support_ticket()  : simulates raising a ticket in a
      helpdesk system (writes to tickets.json like a real API call)
   -> check_system_status()    : simulates checking a live "system
      health" service.
   These behave like external tools/functions an agent can call.

3. AGENT (decision making / orchestration loop)
   -> HelpdeskAgent.handle_query() decides, step by step:
        a) understand the query
        b) call the RAG tool to retrieve knowledge
        c) if confidence is low OR severity is high -> call the
           create_ticket TOOL automatically (autonomous action)
        d) otherwise respond directly with the retrieved solution
      This decision-making loop is what makes it an "agent" and
      not just a simple chatbot.
====================================================================
"""

import re
import json
import os
import math
from datetime import datetime
from collections import Counter

from knowledge_base import KNOWLEDGE_BASE

TICKETS_FILE = os.path.join(os.path.dirname(__file__), "tickets.json")


# --------------------------------------------------------------
# Utility: turn text into a "bag of words" vector for similarity
# --------------------------------------------------------------
def tokenize(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text.split()


def cosine_similarity(vec1: Counter, vec2: Counter) -> float:
    common = set(vec1.keys()) & set(vec2.keys())
    dot = sum(vec1[w] * vec2[w] for w in common)
    mag1 = math.sqrt(sum(v * v for v in vec1.values()))
    mag2 = math.sqrt(sum(v * v for v in vec2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


# --------------------------------------------------------------
# 1) RAG COMPONENT: retrieve the most relevant KB article
# --------------------------------------------------------------
def retrieve_best_match(user_query: str):
    """Searches the knowledge base and RETRIEVES the best matching
    article, returning (article, confidence_score 0-1)."""
    query_vec = Counter(tokenize(user_query))

    best_article = None
    best_score = 0.0

    for article in KNOWLEDGE_BASE:
        kb_text = article["issue"] + " " + " ".join(article["keywords"])
        kb_vec = Counter(tokenize(kb_text))
        score = cosine_similarity(query_vec, kb_vec)

        # Boost score if an exact keyword appears in the query
        for kw in article["keywords"]:
            if kw in user_query.lower():
                score += 0.3

        if score > best_score:
            best_score = score
            best_article = article

    confidence = min(best_score, 1.0)
    return best_article, confidence


# --------------------------------------------------------------
# 2) TOOLS: functions the agent can call on its own
# --------------------------------------------------------------
def create_support_ticket(user_query: str, article: dict, priority: str) -> dict:
    """TOOL: Simulates calling a real Helpdesk/ITSM API to raise a
    ticket, and 'persists' it to tickets.json."""
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, "r") as f:
            tickets = json.load(f)
    else:
        tickets = []

    ticket = {
        "ticket_id": f"TCK{1000 + len(tickets) + 1}",
        "query": user_query,
        "matched_issue": article["issue"] if article else "Unclassified issue",
        "priority": priority,
        "status": "Open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tickets.append(ticket)

    with open(TICKETS_FILE, "w") as f:
        json.dump(tickets, f, indent=2)

    return ticket


def check_system_status() -> dict:
    """TOOL: Simulates pinging a system-health monitoring service."""
    # In a real deployment this would call a monitoring API.
    return {
        "server": "Online",
        "network": "Stable",
        "helpdesk_queue": "Normal load",
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# --------------------------------------------------------------
# 3) AGENT: the decision-making orchestrator
# --------------------------------------------------------------
class HelpdeskAgent:
    CONFIDENCE_THRESHOLD = 0.35  # below this -> agent is not sure

    def __init__(self):
        self.conversation_history = []

    def handle_query(self, user_query: str) -> str:
        self.conversation_history.append(("user", user_query))

        # Step A: quick tool check for system-status style questions
        if any(w in user_query.lower() for w in
               ["system status", "server status", "is everything working",
                "uptime"]):
            status = check_system_status()
            reply = (f"[TOOL: check_system_status called]\n"
                      f"Server: {status['server']} | "
                      f"Network: {status['network']} | "
                      f"Helpdesk Queue: {status['helpdesk_queue']}")
            self.conversation_history.append(("agent", reply))
            return reply

        # Step B: RAG retrieval
        article, confidence = retrieve_best_match(user_query)

        # Step C: Agent decides next action based on confidence + severity
        if article and confidence >= self.CONFIDENCE_THRESHOLD:
            steps = "\n".join(f"   {i+1}. {s}"
                               for i, s in enumerate(article["solution"]))
            reply = (f"[RAG match: '{article['issue']}' | "
                      f"confidence={confidence:.2f} | KB-ID={article['id']}]\n"
                      f"Here are the recommended troubleshooting steps:\n{steps}")

            # Agent autonomously escalates HIGH severity issues even if solved
            if article["severity"] == "high":
                ticket = create_support_ticket(user_query, article, priority="High")
                reply += (f"\n\n[TOOL: create_support_ticket called - this is a "
                           f"high severity issue]\nA support ticket "
                           f"{ticket['ticket_id']} has been raised for the IT "
                           f"team to follow up, in case the above steps don't "
                           f"fully resolve it.")
        else:
            # Low confidence -> agent doesn't guess, it escalates instead
            ticket = create_support_ticket(user_query, article, priority="Medium")
            reply = (f"[RAG confidence too low ({confidence:.2f}) - "
                      f"no reliable match found]\n"
                      f"I couldn't confidently diagnose this from the "
                      f"knowledge base, so I've raised support ticket "
                      f"{ticket['ticket_id']} for a human IT agent to assist you.")

        self.conversation_history.append(("agent", reply))
        return reply


# --------------------------------------------------------------
# CLI Chat Loop - run this file directly to try the agent
# --------------------------------------------------------------
def main():
    agent = HelpdeskAgent()
    print("=" * 60)
    print(" AI IT HELPDESK AGENT  (type 'exit' to quit)")
    print(" Try things like: 'my wifi is not connecting'")
    print("                  'laptop is very slow'")
    print("                  'I forgot my password'")
    print("                  'system status'")
    print("=" * 60)

    while True:
        user_query = input("\nYou: ").strip()
        if user_query.lower() in ("exit", "quit"):
            print("Agent: Thank you for using the IT Helpdesk Agent. Bye!")
            break
        if not user_query:
            continue
        response = agent.handle_query(user_query)
        print(f"\nAgent:\n{response}")


if __name__ == "__main__":
    main()
