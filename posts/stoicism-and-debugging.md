---
title: "Stoicism and the art of debugging"
date: 2026-10-13
tags: [Philosophy, Psychology, Tech]
summary: "The dichotomy of control, the view from above, and premeditatio malorum — three Stoic ideas that turned out to be excellent debugging tools."
---

At 1am, staring at a training run whose loss has just turned into `NaN` for the third time, I am not at my most philosophical. But some of the most useful debugging advice I've received comes from people who died nearly two thousand years ago.

The Stoics — Epictetus, Seneca, Marcus Aurelius — were not writing about software, obviously. They were writing about how to keep a clear head when things go wrong. That turns out to be most of debugging.

## The dichotomy of control

Epictetus opens his *Enchiridion* with a simple split: some things are up to us, and some things are not. Our judgments and actions are up to us. Everything else — other people, the weather, outcomes — is not.

A broken system is the perfect place to practice this. The bug already exists; being annoyed about it does not make it exist less. What *is* up to me is the next action: reading the stack trace, forming a hypothesis, writing a smaller reproduction.

When I'm frustrated, I've noticed my debugging becomes random. I change three things at once, rerun, and hope. The Stoic move is to drop the emotional commentary ("why does this *always* happen") and return to the only thing in my control: one deliberate, testable step.

## Judgments, not events, disturb us

Another line from Epictetus: people are disturbed not by things, but by their judgments about things.

The production incident is an event. "I'm going to look incompetent" is a judgment layered on top. In my experience the second one does far more damage, because it pushes you toward the fastest fix rather than the right one — the patch that makes the alert go away instead of the change that addresses the cause.

Separating the event from the story I'm telling about it is a skill, and like any skill it gets easier with repetition. Incidents provide plenty of repetitions.

## Premeditatio malorum

Seneca recommended imagining in advance the things that could go wrong — exile, loss, illness — not to wallow in them, but to blunt their shock and prepare.

Engineers reinvented this and called it a **pre-mortem**: before launching, imagine it's six months later and the project has failed. What happened? It's remarkable how quickly a team can list the actual risks once it has permission to be pessimistic. The rate limiter nobody tested. The model that degrades on long inputs. The data pipeline with a single owner who's about to go on holiday.

The Stoic version adds a personal layer: also imagine your own reaction. If this fails, how do I want to behave? Deciding that in advance, while calm, is far easier than deciding it at 1am.

## The view from above

Marcus Aurelius often zoomed out — picturing the earth as a speck, his own life as a moment in a long stream of time. In *Meditations* it's a tool for humility.

In debugging it is a tool for escaping tunnel vision. After an hour deep in one function, I try to step back and ask: what is the *system* doing? Is the bug even in this layer? More than once, the bug I spent an afternoon chasing in model code was a stale cache, a misconfigured environment variable, or a dataset that changed under me. The view from above would have found it faster.

## A caveat

Stoicism is sometimes misread as "suppress your emotions and push through". That's not what the texts say, and it's not healthy advice for engineers who already overwork. Frustration is information — often that the task is too big, or that you need sleep. The Stoic practice is to notice it and choose what to do with it, which sometimes means closing the laptop.

## The short version

When something breaks:

1. Separate what happened from the story about what it means.
2. Focus on the next controllable step, and make it small and testable.
3. Zoom out before you dig deeper.
4. Next time, imagine the failure before it happens.

Marcus Aurelius wrote that the impediment to action advances action; what stands in the way becomes the way. I doubt he imagined it being applied to a `NaN` loss. I think he'd approve anyway.
