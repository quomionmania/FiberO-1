# FiberO-1 Open Source

Open-source release containing two separate systems:

- **FiberO-1** - a standalone, class-based general-purpose agent/system with an optional Windows PC-control prototype.
- **Fiberglass 5.0** - the Fiberglass 5.0 agent prompts packaged for Claude, OpenCode, and ChatGPT.

> This repository/package is intentionally in **English**.

## Contents

```text
FiberO-1-open-source/
  README.md
  LICENSE
  install.ps1
  FiberO-1/
    docs/
    opencode/
    claude/
    chatgpt/
    pc-control/
  Fiberglass-5.0/
    docs/
    opencode/
    claude/
    chatgpt/
  scripts/
```

## FiberO-1

FiberO-1 is **separate** from the Fiberglass family persona/DNA. It is designed as a multi-class agent:

| Class | Purpose | Posture |
|---|---|---|
| `3d` | 3D modeling, scene setup, asset generation, rendering pipelines | Maximum design/detail, token/credit-intensive by design |
| `coding` | Software engineering, debugging, refactoring, architecture, tests | Uses coding skills/workflows, best coding models |
| `design` | UI/UX, visual systems, branding, layout, graphics | High visual quality, no generic slop |
| `music` | Composition, sound design, lyrics, audio production guidance | Creative + structured output |
| `motion` | Motion design, animation, video editing direction, timing | Frame/beat-aware, production-oriented |
| `video` | Video generation/editing pipelines, scripts, shot planning | End-to-end delivery |
| `research` | Web/docs research, synthesis, comparisons | Evidence-first |
| `general` | Catch-all for mixed tasks | Practical and explicit |

### Model routing (recommended defaults)

These are **recommendations**, not hard locks. Pick the best available model in your environment.

| Class | Recommended model profile | Notes |
|---|---|---|
| 3D | Strong spatial/visual reasoning + tool use | Prefer models good at geometry, Blender/Three.js, procedural generation |
| Coding | Strong coding/reasoning model | Prefer repo-aware, test-aware, long-context models |
| Design | Strong visual/UI reasoning model | Prefer models good at layout, typography, design critique |
| Music | Creative + structured model | Pair with audio tools/MCP when available |
| Motion | Visual + timing-aware model | Pair with Remotion/HyperFrames/Motion tools |
| Video | Multimodal/video-capable model | Pair with ffmpeg/Remotion/video MCP |
| Research | Fast, broad, citation-capable model | Verify claims before stating as fact |

## PC Control Prototype (Windows)

`FiberO-1/pc-control/` contains a Windows prototype that demonstrates:

- A dark overlay glow with the text: **"FiberO using the PC"**
- Mouse/keyboard control primitives
- **Esc** global kill switch to interrupt control immediately

> **Safety note:** PC control can move your mouse and type into apps. Use only on your own machine, save work first, and keep Esc reachable. The prototype is experimental.

## Fiberglass 5.0

`Fiberglass-5.0/` contains the Fiberglass 5.0 Nature and Atmosphere prompts packaged for:

- **OpenCode** - agent markdown files with frontmatter
- **Claude** - system prompt markdown files
- **ChatGPT** - custom-instructions/system-prompt markdown files

## Install

Run the PowerShell installer:

```powershell
# From the extracted folder
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

The installer can:

- Copy OpenCode agent files into `%USERPROFILE%\.config\opencode\agents\`
- Copy Claude prompt files into `Documents\FiberO-1\claude\` (reference copy)
- Copy ChatGPT prompt files into `Documents\FiberO-1\chatgpt\` (reference copy)
- Optionally install PC-control Python dependencies

## Open Source

- License: MIT (see `LICENSE`)
- Intended for local use, modification, and redistribution under MIT terms.
- Do not include secrets, API keys, or private data when redistributing.

## Verification Status

This package includes source/prompts/prototype code. Before calling it "production ready", verify in your environment:

- OpenCode loads the agent files
- Claude/ChatGPT prompts behave as expected
- PC-control prototype runs and Esc interrupts reliably
- Dependencies install cleanly on a fresh machine
