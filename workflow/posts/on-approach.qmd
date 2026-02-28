---
title: "Not Wrong, Just Weak"
subtitle: "Framing technical discussions around trade-offs instead of correctness"
author: "Daniel Lumian, PhD"
date: "2026-02-23"
categories: [methodology, model-selection, best-practices]
---

There's a reflex in technical discussions to frame every decision as right or wrong. Someone proposes a model, a preprocessing step, or an inference strategy, and the instinct is to evaluate it on a pass/fail basis. That framing feels decisive and rigorous. **It isn't**. In most cases its overly simplistic and deadens legitimate discussion.

A more useful framing is a strengths and weaknesses assessment.

## When Right vs. Wrong Actually Applies

Right and wrong do have a place, but the bar should be a clear, demonstrable violation. The approach is logically incompatible with the task, the data violates the model's core assumptions, or the usage is fundamentally misaligned — like running an NLP model on image data, or applying a classifier trained on balanced classes to a heavily skewed distribution without adjustment.

In these cases, a clear decision makes sense because there's a specific, articulable reason why the approach won't work correctly, and that boundary is worth stating clearly.

The problem is that this framing gets applied far outside those boundaries. Most notably, this absolute approach is applied in situations where there's no actual violation but rather a set of trade-offs.

## The Trade-Off Problem

Consider model selection for image classification. Using an XGBoost classifier on flattened pixel data is not current best practice. It's not SOTA. A CNN with appropriate architecture will almost certainly produce better results on a sufficiently large dataset.

But it is not *wrong*.

XGBoost on flattened image data offers a meaningful set of genuine advantages: minimal training data requirements, fast iteration cycles, low compute overhead, interpretable feature importance, and essentially zero infrastructure complexity. For a problem where you have limited labeled examples, tight time constraints, or resource restrictions, it may be the most defensible choice on the table.

Calling it "weak" for a given context may be accurate and opens the trade-off disucssion.

The CNN approach, meanwhile, carries its own costs that rarely get surfaced in the same breath: development time, data requirements, training compute, deployment infrastructure, and the overhead of hyperparameter search. Even the act of comparing multiple models rigorously has a cost(benchmarking time, evaluation complexity, the risk of overfitting to your validation set during model selection).

This means there is **not a "correct"** approach.

## What a Strengths and Weaknesses Frame Buys You

When you shift to pros and cons, you're forced to establish **criteria** which leads to options, discussion, and prioritization.

Better performance is one criterion. It's not the only one. Development velocity, computational cost, interpretability, data efficiency, robustness to distribution shift, and ease of debugging are all also legitimate criteria, and they don't all point in the same direction. A strengths and weaknesses frame makes criteria explicit and forces you to weight them against each other relative to the actual constraints of the problem.

This also changes what a productive disagreement looks like. If one practitioner favors a simpler approach and another favors a more complex one, the right vs. wrong frame turns that into a contest. The strengths and weaknesses frame turns it into a conversation about which criteria matter most given the specifics.

## This Generalizes Beyond Model Selection

The same pattern shows up across the full ML workflow:

**Inference.** A model that performs well on a benchmark is not necessarily a model that should be trusted in deployment. Applying a model to a population it wasn't trained on, or in a domain where its outputs contradict real-world ground truth, isn't a performance problem but a validity problem. Racial bias in facial recognition, risk-scoring tools applied outside their validated populations, or predictions that consistently diverge from expert judgment in high-stakes fields are all examples where the question isn't "does the model run" but "should we believe what it says." The right vs. wrong frame doesn't help here. A strengths and weaknesses assessment forces the question of where the model's inferences are trustworthy and where they aren't.

**Data augmentation and synthesis.** Synthetic upsampling of a minority class can improve class balance metrics. Whether it improves anything meaningful depends entirely on why that imbalance exists in the first place. In fields like social work or psychology, underrepresentation in a dataset often reflects real structural factors (e.g., access barriers, stigma, documentation practices) that don't disappear because you've oversampled the minority class. A model trained on synthetically balanced data may perform well on paper while encoding a fundamentally distorted picture of the population it's supposed to serve. Better metrics at the cost of ecological validity is a trade-off worth naming explicitly, not a problem that gets solved by augmentation alone.

**Edge case handling.** "It should handle every edge case" sounds like a reasonable standard. It isn't, because it treats completeness as the only criterion and ignores cost. An application that crashes is wrong because there's a clear threshold, and it matters. An application that renders imperfectly on an obscure browser configuration or fails gracefully with a logged error is making a different kind of trade-off: ship something functional now versus invest additional development time chasing diminishing returns. The appropriate level of edge case coverage is a function of who's affected, how often, and what the failure costs.

In each of these areas, the right vs. wrong frame collapses meaningful distinctions. The strengths and weaknesses frame highlights them.


## The Bottom Line

Right and wrong is a binary. It's appropriate when there's a genuine violation such as a logical incompatibility, a broken assumption, a category error. In those cases, name it clearly and explain exactly where the line is.

For everything else, reach for a strengths and weaknesses assessment instead. It forces you to articulate criteria, name trade-offs, and engage with the actual constraints of the problem. It also produces better conversations where disagreement generates insight and prioritization rather than just friction.

"Not wrong, just weak for this context" is frequently a more open-ended and valid stance than "this is wrong".