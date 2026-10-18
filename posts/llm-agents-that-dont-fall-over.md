---
title: "Notes on building LLM agents that don't fall over"
date: 2026-10-16
tags: [AI, Tech]
summary: "Agents fail in boring, predictable ways: unbounded loops, malformed tool calls, and silent drift. A few patterns that make them sturdier, with a minimal Python loop."
---

Every LLM agent demo looks magical for the first five minutes. Then someone asks it a question slightly outside the happy path, and it calls the same search tool eleven times, invents a function argument, and confidently answers a question nobody asked.

Most agent failures I've seen are not exotic. They are the same handful of boring problems, and boring problems have boring solutions. Here are the ones I keep coming back to.

## 1. Bound everything

An agent is a `while` loop whose exit condition is decided by a probabilistic text generator. Read that sentence again and the first rule writes itself: **never let the model be the only thing that decides when to stop.**

Put hard limits on steps, wall-clock time, tokens and cost. When a limit trips, fail loudly with whatever partial state you have, rather than silently returning the last message.

## 2. Treat tool calls as untrusted input

The model's tool call is user input wearing a nice suit. Validate it with a schema, and when validation fails, feed the error back to the model *as an observation* instead of crashing. Models are surprisingly good at fixing their own arguments when told exactly what was wrong.

Here's the skeleton I start from. It's deliberately small — no framework — because the important ideas fit on one screen:

```python
import json, time
from pydantic import BaseModel, ValidationError

class Search(BaseModel):
    query: str
    top_k: int = 5

TOOLS = {"search": (Search, lambda a: search_index(a.query, a.top_k))}

def run_agent(llm, task, max_steps=8, budget_s=60):
    history = [{"role": "user", "content": task}]
    seen = set()
    start = time.monotonic()
    for step in range(max_steps):
        if time.monotonic() - start > budget_s:
            return {"status": "timeout", "history": history}
        msg = llm(history, tools=list(TOOLS))
        history.append(msg)
        if not msg.get("tool_call"):
            return {"status": "done", "answer": msg["content"]}

        name, raw = msg["tool_call"]["name"], msg["tool_call"]["args"]
        key = (name, json.dumps(raw, sort_keys=True))
        if key in seen:  # same call twice = probably looping
            obs = "You already called this with identical arguments. Use the earlier result or try something different."
        elif name not in TOOLS:
            obs = f"Unknown tool '{name}'. Available: {list(TOOLS)}"
        else:
            schema, fn = TOOLS[name]
            try:
                obs = fn(schema(**raw))
            except ValidationError as e:
                obs = f"Invalid arguments: {e.errors()}"
            except Exception as e:  # tool failures are observations, not crashes
                obs = f"Tool error: {type(e).__name__}: {e}"
        seen.add(key)
        history.append({"role": "tool", "name": name, "content": str(obs)[:4000]})
    return {"status": "max_steps", "history": history}
```

Notice what the loop does *not* trust: the tool name, the arguments, the tool itself, the length of the output, or the model's sense of when it's finished.

## 3. Detect loops cheaply

The duplicate-call check above catches a surprising fraction of runaway agents. It's crude — a model can loop with slightly different arguments — but crude and always-on beats clever and never-shipped. A next step is to track whether the agent's state is actually changing: new information retrieved, new files touched, new sub-goals completed.

## 4. Keep the context honest

Long-running agents drown in their own transcripts. Truncate tool outputs (note the `[:4000]`), summarize old steps, and keep the original task pinned near the top. A lot of "the agent forgot what it was doing" bugs are really "we buried the instruction under 30k tokens of JSON".

## 5. Make it observable before you make it smart

Before tuning prompts, log every step: input, tool call, observation, latency, tokens. Then read the traces. Actually read them. In my experience, one afternoon of reading fifty failed traces teaches more than a week of tweaking prompts by vibes, because you start to see that failures cluster into maybe three or four categories.

## 6. Evaluate trajectories, not just answers

A correct final answer reached through nine redundant tool calls is a latency and cost bug waiting to happen. Score the path too: number of steps, invalid calls, repeated calls. Those metrics are cheap to compute from the logs you already have from point 5.

## The meta-lesson

Agents look like an AI problem, but making them reliable is mostly a software engineering problem: input validation, timeouts, idempotency, observability, tests. The model is the most interesting component, and also the one you should trust least.

None of this is glamorous. That's sort of the point.
