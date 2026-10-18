---
title: "Why I'm starting this blog"
date: 2026-10-05
tags: [Life/Other, Tech]
summary: "Writing is how I find out what I actually think. Here's what this blog is for, what I'll write about, and what I won't pretend to know."
---

For years my notes lived in a graveyard of half-finished Markdown files, Jupyter notebooks named `untitled_final_v3.ipynb`, and chat messages to myself. Some of those notes were good. Most of them were never read again, including by me.

This blog is an attempt to fix that, and to hold myself to a slightly higher standard than "it made sense at 2am".

## Writing as debugging for thoughts

When I explain a system to a colleague, I usually find the bug halfway through the sentence. Rubber-duck debugging works because speaking forces you to serialize a fuzzy mental model into a linear sequence of claims, and fuzzy models do not survive serialization.

Writing is the same trick with a longer attention span. If I can't write a clear paragraph about why an agent loop keeps failing, I probably don't understand why it keeps failing. The paragraph is the test.

So the first audience of this blog is me. If anyone else finds it useful, that's a bonus I'll gladly take.

## What to expect

I work as an AI engineer, mostly around large language models and agentic systems, so a good share of posts will be about that:

- **Tech and AI** — practical notes on building with LLMs: evaluation, agents, latency, the unglamorous plumbing that decides whether a demo survives contact with real users. Code where it helps.
- **Books** — I read outside my field on purpose. Expect reflections on books like *Thinking, Fast and Slow* or *Meditations*, read through the eyes of someone who spends the day staring at loss curves.
- **Philosophy and psychology** — how old ideas about attention, judgment and character turn out to be surprisingly useful when you are debugging a model or yourself.
- **Life and other things** — the occasional post that doesn't fit anywhere else.

You can filter by any of these on the [blog page](../), or subscribe via [RSS](../feed.xml) if you still believe in RSS (I do).

## What I won't do

I won't write "Top 10 AI tools you need in 2026". I won't summarize papers I haven't read carefully. And I'll try to be explicit about confidence: when something is a hunch, I'll call it a hunch; when it's a result I've reproduced, I'll say so.

I also won't write about the internal details of the work I do for employers. The ideas here are my own, built from public knowledge, side projects and general experience — not anyone's confidential roadmap.

## A note on being wrong

A blog is a public record of what you believed at a certain time. Some of what I write will age badly; the field moves fast enough that a confident post about best practices can look naive within a year. I'm fine with that. I would rather leave a trail of honest, dated thinking than a polished set of opinions that never risked anything.

If you spot a mistake, please tell me — the [contact links](../../#contact) are on the homepage. Being corrected is the cheapest education there is.

## The setup, briefly

For the curious: this site is plain HTML and CSS. Posts are Markdown files with a bit of front matter; a small Python script turns them into pages, an RSS feed and a sitemap. No framework, no build step on the server. I wanted publishing to be as low-friction as writing, because friction is where good intentions go to die.

Let's see how long I keep this up. My goal is modest: one thoughtful post a month, written carefully enough that I would want to read it a year from now.
