---
layout: default
title: "Horizon Summary: 2026-10-25 (EN)"
date: 2026-10-25
lang: en
---

> From 16 items, 1 important content pieces were selected

---

1. [Pretrained Music Transformer Jams Live Using Sampling Bias](#item-1) ⭐️ 5.0/10

---

<a id="item-1"></a>
## [Pretrained Music Transformer Jams Live Using Sampling Bias](https://www.reddit.com/r/MachineLearning/comments/1xe4pex/got_a_pretrained_music_transformer_to_jam_with_me/) ⭐️ 5.0/10

A developer created Duetto, a system in which the pretrained Anticipatory Music Transformer (music-medium-800k) plays a second piano alongside a live MIDI keyboard performer without fine-tuning. The system tracks the performer’s key, chord, tempo, and hand position, then applies real-time biases to the model’s logits before sampling. The project shows that inference-time steering can turn a general pretrained symbolic-music model into a responsive live collaborator without collecting custom data or retraining. Running on a Jetson Orin Nano also suggests that such interactive AI music experiments can be deployed on compact edge hardware. Out-of-key notes are suppressed, chord tones and tensions are promoted, notes near the performer’s hands are reduced to avoid overlap, and melodic registers are encouraged when the performer stops. The model plans about one second ahead, discards and resamples when the chord changes, and all bias offsets are currently hand-tuned by ear; code and video are available on GitHub.

reddit · r/MachineLearning · /u/GGAllin43 · Oct 24, 09:58

**Background**: Symbolic music models operate on note-level representations such as MIDI rather than raw audio. An autoregressive transformer generates music by repeatedly predicting the next symbolic event from probability scores called logits. Logit biasing changes those scores before sampling, making certain notes or musical choices more or less likely. The Anticipatory Music Transformer is a controllable autoregressive model designed for symbolic music generation and conditioning tasks.

<details><summary>References</summary>
<ul>
<li><a href="https://arxiv.org/abs/2306.08620">[2306.08620] Anticipatory Music Transformer</a></li>
<li><a href="https://www.emergentmind.com/topics/anticipatory-music-transformer">Anticipatory Music Transformer</a></li>
<li><a href="https://www.vellum.ai/llm-parameters/logit-bias">Logit Bias - LLM Parameter Guide - Vellum</a></li>

</ul>
</details>

**Tags**: `#AI music`, `#music technology`, `#machine learning`, `#live performance`, `#generative AI`

---