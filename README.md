# AI-Driven Narrative Media Pipeline

An automated end-to-end research application that transforms text-based prompts into fully realized narrative films. This project explores the orchestration of multiple AI models to autonomously handle scriptwriting, high-fidelity visual generation, automated Quality Control (QC), and musical assembly.

## Key Engineering Features
* **Multi-Model Orchestration:** Primary visual pipeline utilizing **FLUX .1 (Cloud API)** for state-of-the-art image fidelity, with **Wan 2.1** utilized via **Hugging Face** for dynamic cinematic sequences.
* **AI-in-the-Loop Vision Critic:** Leveraged **Gemini Vision** as an automated QC layer to evaluate and select the highest-quality visual assets, mitigating issues with anatomical disfigurement or prompt misalignment.
* **Automated Audio Composition:** Integrated **Google AI Music** (MusicFX/MusicLM) to generate thematic soundtracks tailored to the narrative's emotional tone.
* **Modular Pipeline Design:** Programmatically manages the synchronization of audio-to-text timestamps (Whisper) with frame-by-frame video assembly.

## Technology Stack
* **Image Generation:** FLUX .1 (Cloud-based Generation)
* **Video Generation:** Wan 2.1 (Hugging Face Hosted Inference)
* **Vision Analysis (QC):** Google Gemini (Vision-Language Model Critic)
* **Audio & Music:** Google AI Music (Thematic Composition), OpenAI Whisper (Transcription)
* **LLMs:** Google Gemini (Narrative Logic), g4f.client
* **Media Processing:** Python-based automation for multi-media synchronization.

## Technical Challenges & Insights
* **Hybrid Asset Synthesis:** Engineered a workflow to blend static high-fidelity imagery with generative video transitions (Wan 2.1) to create a cohesive viewer experience.
* **Automated Quality Filtering:** Solved the "hallucination" problem in image generation by using Gemini Vision to perform pass/fail checks on generated frames.
* **System Evolution:** Designed with a model-agnostic architecture; while currently utilizing specific legacy versions, the framework is built for seamless upgrades as the Generative AI landscape evolves.

## Demonstration
View the high-fidelity production results of this architecture here: **[AI Synthetic Dreams (YouTube)](https://www.youtube.com/@AISyntheticDreams)**

## Core Components
* `audio_to_text.py`
* `gemini_story_creator.py`
* `gf4_image_creator.py`
* `image_description.py`
* `music_loader.py`
* `video_creator.py`

---
**Note:** This repository represents a legacy research snapshot. While the core architecture is sound, the internal API hooks utilize earlier iterations of Gemini and Flux. Please refer to the YouTube channel for the most recent production outputs.
