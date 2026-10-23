---
layout: default
title: "Horizon Summary: 2026-10-23 (EN)"
date: 2026-10-23
lang: en
---

> From 25 items, 3 important content pieces were selected

---

1. [De Staat’s “Freedom” Video Features Striking VFX Pelican Moment](#item-1) ⭐️ 4.0/10
2. [I built Open-XTTS-Trainer: Now you can add new language scripts and train all 3 XTTS v2 components in 1 click (P)](#item-2) ⭐️ 4.0/10
3. [SteerTTS Edge Shrinks to 11.84 MB](#item-3) ⭐️ 4.0/10

---

<a id="item-1"></a>
## [De Staat’s “Freedom” Video Features Striking VFX Pelican Moment](https://simonwillison.net/2026/Oct/22/de-staat-freedom/) ⭐️ 4.0/10

Simon Willison shared the official music video for “Freedom” by Dutch alternative rock band De Staat, highlighting a striking visual-effects sequence at 0:44. The effects are credited to Matties Grooten of Fake it or Leave it. The video is a useful creative reference for artists and producers exploring surreal, generative-AI-style visuals in music content. However, it does not provide direct platform, monetization, or founder-IP strategy insights. Willison embedded a looping 1280×720 excerpt with a pelican-themed poster frame, and the post is tagged “generative-ai” and “pelican-riding-a-bicycle.” The exact production technique is not disclosed, so the visual should be treated as a VFX reference rather than a confirmed technical workflow.

rss · Simon Willison · Oct 22, 19:42

**Background**: De Staat is a Dutch alternative rock band, and “Freedom” is the track promoted by the shared official video. Modern music videos increasingly combine conventional visual effects with generative AI tools to create impossible or surreal imagery. Crediting the effects artist helps viewers trace the creative work back to its maker.

**Tags**: `#music video`, `#visual effects`, `#creative reference`, `#alternative rock`

---

<a id="item-2"></a>
## [I built Open-XTTS-Trainer: Now you can add new language scripts and train all 3 XTTS v2 components in 1 click (P)](https://www.reddit.com/r/MachineLearning/comments/1xcurgj/i_built_openxttstrainer_now_you_can_add_new/) ⭐️ 4.0/10

开发者发布开源Open-XTTS-Trainer，支持一键训练XTTS v2的三个组件并添加阿拉伯语、印地语等新语言脚本。

reddit · r/MachineLearning · /u/yashubhakt · Oct 22, 21:03

**Tags**: `#AI语音合成`, `#开源工具`, `#XTTS`, `#机器学习`, `#AIGC内容创作`

---

<a id="item-3"></a>
## [SteerTTS Edge Shrinks to 11.84 MB](https://www.reddit.com/r/MachineLearning/comments/1xcum4s/we_shrank_our_steerable_small_tts_to_1184_mb_wer/) ⭐️ 4.0/10

WhissleAI released steer-tts-edge, a package totaling 11.84 MB including weights, voices, text front end, and Python runtime. Its 9.25M-parameter acoustic model uses attention plus bidirectional Mamba-3 with int4 quantization-aware training, while a 6.2M-parameter Vocos-style vocoder is distilled and also int4 quantized; local testing kept WER at 0.96% and reduced UTMOS from 4.20 to 4.11. The release shows that a controllable neural TTS model can fit into a very small application bundle while preserving intelligibility and most steering behavior, making offline or embedded speech synthesis more practical. However, because weights are dequantized to fp32 at load, the current gain is primarily storage rather than inference speed, so mobile or WASM deployment still needs specialized kernels. All 12 controls retain at least 95% of their fp32 effect, and the model supports 50 style tags plus inline markup such as pauses, slow speech, and whispers; it includes 200 English voices out of the full model’s 2,825. On a loaded 2018 Threadripper using four CPU threads, it reaches RTF 0.053, about 19 times realtime, with roughly 120 ms to first audio and sentence-level streaming, but it is English-only and lacks on-device voice cloning, free-text prompts, and a flow refiner.

reddit · r/MachineLearning · /u/Working_Hat5120 · Oct 22, 20:57

**Background**: A TTS system typically uses an acoustic model to convert text into acoustic features and a vocoder to convert those features into an audible waveform. Vocos is a fast GAN-trained neural vocoder that predicts spectral coefficients and reconstructs audio through an inverse Fourier transform, while Mamba-3 is an efficient state-space-model architecture for sequence processing. Quantization-aware training simulates low-precision int4 arithmetic during training so the model can be stored more compactly, and WER and UTMOS respectively measure speech intelligibility and predicted perceptual quality.

<details><summary>References</summary>
<ul>
<li><a href="https://github.com/gemelo-ai/vocos">GitHub - gemelo-ai/vocos: Vocos: Closing the gap between time ...</a></li>
<li><a href="https://pub.towardsai.net/why-researchers-are-excited-about-mamba-3-9c273cf4b870">Why Researchers Are Excited About Mamba - 3 | by... | Towards AI</a></li>
<li><a href="https://picovoice.ai/blog/measuring-tts-quality/">How to Evaluate TTS Quality : MOS Scores, Benchmarks, and Testing</a></li>

</ul>
</details>

**Tags**: `#TTS`, `#AI语音`, `#模型压缩`, `#边缘AI`, `#AIGC工具`

---