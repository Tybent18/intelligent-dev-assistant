# Obsidian Architecture

## Stage One

```text
Browser HoloLab
  ├── holographic visual layer
  ├── text command console
  ├── browser speech recognition
  └── browser speech synthesis
           │
           ▼
Flask API
  ├── GET /api/status
  └── POST /api/command
           │
           ▼
Obsidian Core
  ├── intent routing
  ├── repository inventory
  ├── safe Python syntax analysis
  ├── UI action protocol
  └── deterministic local demo responses
```

## Action protocol

The core returns speech and structured UI actions separately. Examples include focusing a panel, pulsing the holographic core, expanding the laboratory, or rendering diagnostic results. This prevents assistant text from directly executing arbitrary browser code.

## Local-first boundary

Stage One requires no API key and sends no repository content to a model provider. It performs local inventory and Python abstract-syntax-tree parsing only. A future model connection should sit behind a provider interface with explicit configuration, data disclosure, and human approval for consequential tool calls.

## What “holographic” means here

The current HoloLab is a screen-based spatial illusion: layered panels, depth, parallax, orbiting geometry, particles, transparency, glow, and voice interaction. It is software-complete enough to run on ordinary hardware. True volumetric or reflected-light projection requires a separate physical display layer.

## Future interfaces

- WebXR headset or spatial-browser mode
- Hand tracking and gesture commands
- Multi-monitor laboratory layout
- Pepper's Ghost pyramid or transparent-display projection
- Depth-camera user tracking
- Local or hosted language-model provider
- Sandboxed developer tools with reviewable execution plans

