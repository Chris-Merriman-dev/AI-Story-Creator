# AI-Driven Narrative Media Pipeline

An automated end-to-end research application that transforms text-based prompts into fully realized narrative films. This project explores the orchestration of multiple AI models to autonomously handle scriptwriting, visual asset generation, voice narration, and musical assembly.

## Key Engineering Features
* **Orchestrated AI Workflow:** Coordinates **Google Gemini** for narrative structure and **Wan 2.1** for temporal video consistency.
* **Context-Aware Media Selection:** Implements logic for AI-driven selection of thematic music and visual assets based on script sentiment.
* **Modular Pipeline Design:** Programmatically manages the synchronization of audio-to-text timestamps (Whisper) with frame-by-frame video assembly.



## Technology Stack
* **LLMs:** Google Gemini (Primary Narrative Logic), g4f.client (Diversity in Storytelling)
* **Generative Video:** Wan 2.1
* **Media Processing:** Python-based automation for multi-media synchronization.

## Technical Challenges & Insights
* **Visual Consistency:** Addressed the complexities of maintaining character consistency across multiple generative prompts.
* **Automated Quality Control:** Identified early-stage limitations in AI vision regarding anatomical accuracy and implemented iterative prompt refinement to mitigate disfigurement.
* **System Evolution:** Designed with a model-agnostic architecture; while currently utilizing specific legacy Gemini/Flux versions, the framework is built for seamless upgrades as Vision-Language Models (VLMs) evolve.

## Demonstration
View the high-fidelity production results of this architecture here: **[AI Synthetic Dreams (YouTube)](https://www.youtube.com/@AISyntheticDreams)**

## Core Components
* `gemini_story_creator.py` – Narrative logic and script generation.
* `audio_to_text.py` – Synchronization of voiceovers via timestamping.
* `video_creator.py` – Programmatic assembly of final visual/audio assets.
* `music_loader.py` – AI-driven thematic soundtrack selection.

---
**Note:** This repository represents a legacy research snapshot. While the core architecture is sound, the internal API hooks utilize earlier iterations of Gemini and Flux. Please refer to the YouTube channel for the most recent production outputs.
