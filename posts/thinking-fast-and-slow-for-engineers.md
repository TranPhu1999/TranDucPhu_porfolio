---
title: "Thinking, Fast and Slow, read by an engineer"
date: 2026-10-10
tags: [Books, Psychology]
summary: "Kahneman's System 1 and System 2 map uncomfortably well onto how we build, evaluate and trust machine learning systems — and onto how I make decisions at work."
---

I first read *Thinking, Fast and Slow* as a student and filed it under "interesting psychology". Rereading it years into a career building machine learning systems, it reads less like a psychology book and more like a bug report about the hardware I use to do my job.

Here are the ideas that stuck the second time around.

## Two systems, two kinds of model

Kahneman's central framing is that we run two modes of thought. **System 1** is fast, automatic and associative: it reads faces, completes "bread and..." and flinches at loud noises. **System 2** is slow, effortful and deliberate: it multiplies 17 × 24 and checks whether an argument actually holds.

The tempting engineering analogy is obvious — a single forward pass of a language model looks a lot like System 1, and chain-of-thought or tool use looks a bit like System 2. I don't want to push the analogy too far; brains are not transformers. But it's a useful lens on *my* behavior: most of my judgments about a model's quality are System 1 judgments. I look at five outputs, they feel good, and a confident story assembles itself.

## WYSIATI: What You See Is All There Is

The most useful phrase in the book is Kahneman's acronym **WYSIATI**. System 1 builds the most coherent story it can from the information in front of it, and it does not stop to ask what information is missing.

In ML work, WYSIATI is the cherry-picked demo. It's the evaluation set that quietly shares a distribution with the training data. It's the dashboard that shows accuracy but not the slice where the model fails for a specific group of users. The story feels complete precisely because you can't see the gaps.

My practical defense is a habit I now apply before trusting any result: *write down what data would make this conclusion wrong, then go look for it.*

## Substitution

When faced with a hard question, System 1 quietly answers an easier one. "Is this model better for our users?" becomes "Do I like these outputs more?" "Will this project succeed?" becomes "Does the team seem excited?"

Substitution is why vibes-based evaluation is so seductive. The easy question has an immediate, satisfying answer. Recognizing substitution doesn't make the hard question easier, but it does make me notice when I've stopped asking it.

## The planning fallacy

Kahneman describes a curriculum project where the team estimated two years and took eight. The fix he proposes is the **outside view**: instead of reasoning from the specifics of your plan, ask how long projects *like this* usually take.

Every engineer has lived this. "Fine-tune, evaluate, ship — two weeks." The inside view lists the steps; the outside view remembers that data cleaning alone took three weeks last time. I now try to estimate twice — once from the plan, once from the reference class — and take the uglier number seriously.

## Where the book has aged

It would be dishonest not to mention that some studies cited in the book, especially in the chapter on priming, have not replicated well. Kahneman himself acknowledged this. For me this made the book *more* useful, not less: it's a reminder that even careful experts fall for compelling stories with small samples. That's precisely the trap the book warns about, which is a strange and humbling kind of recursion.

## What changed in how I work

A few small habits came out of this reread:

- **Pre-register expectations.** Before running an eval, I write down what result I expect. Surprises are only informative if you recorded what you expected.
- **Look at failures first.** Random samples of errors before any aggregate score.
- **Slow down for irreversible decisions.** System 1 is fine for choosing a variable name. It is not fine for deciding which model goes to production.

The book's most lasting gift is not a list of biases to memorize — I forget most of them. It's a persistent, slightly uncomfortable awareness that the feeling of being sure is not evidence of anything.
