# AI IT Helpdesk Agent

**Naan Mudhalvan – AI Agents Bootcamp | Final Project**
**Use Case 4: AI IT Helpdesk Agent** — Diagnoses common technical issues
and recommends troubleshooting steps using a knowledge base.
**Capabilities: Agent + RAG + Tools**

## What this project does
A command-line AI agent that:
1. **Retrieves (RAG):** searches a curated IT-issues knowledge base for
   the closest matching problem to what the user typed.
2. **Uses Tools:** can call `create_support_ticket()` (simulated ITSM
   ticketing) and `check_system_status()` (simulated monitoring API)
   as callable tools.
3. **Acts as an Agent:** decides on its own — based on match confidence
   and issue severity — whether to just answer, or to also raise a
   support ticket automatically, without the user asking for one.

## Files
| File | Purpose |
|---|---|
| `knowledge_base.py` | The IT issues + solutions database (RAG source) |
| `helpdesk_agent.py` | Main program: RAG retrieval, tools, agent logic, CLI |
| `tickets.json` | Auto-created; stores tickets the agent raises |
| `requirements.txt` | Dependencies (none outside Python standard library) |

## How to run
```bash
python3 helpdesk_agent.py
```
Then type an IT problem, for example:
```
You: my wifi is not connecting
You: laptop is very slow
You: I forgot my password
You: system status
You: exit
```

## How the 3 capabilities map to the code
- **RAG** → `retrieve_best_match()` in `helpdesk_agent.py`
- **Tools** → `create_support_ticket()` and `check_system_status()`
- **Agent (decision loop)** → `HelpdeskAgent.handle_query()`

## Tech stack
Pure Python 3 (standard library only — `re`, `json`, `math`,
`collections`, `datetime`). No external API key required, so it runs
anywhere instantly.
