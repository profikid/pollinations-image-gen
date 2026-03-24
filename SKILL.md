---
name: pollinations-image-gen
description: Generate images using Pollinations.ai - completely free image generation API with no signup, no API key, and no credit card required. Use when the user wants to create images for free without any authentication or account setup, or when other image generation APIs are rate-limited or require payment.
---

# Pollinations Image Gen

Free image generation using **Pollinations.ai** — no API key, no signup, no credit card. Just works.

## Features

- ✅ Completely free
- ✅ No API key required
- ✅ No account signup
- ✅ No credit card
- ✅ AI prompt enhancement
- ✅ Custom resolution
- ✅ Seed for reproducibility

## Run

```bash
python3 {baseDir}/scripts/gen.py --prompt "your prompt here"
```

### Options

```bash
# Generate multiple images
python3 {baseDir}/scripts/gen.py --prompt "tropical beach" --count 4

# Custom resolution
python3 {baseDir}/scripts/gen.py --prompt "mountain landscape" --width 1920 --height 1080

# Specific seed for reproducibility
python3 {baseDir}/scripts/gen.py --prompt "cyberpunk city" --seed 42

# Disable AI prompt enhancement
python3 {baseDir}/scripts/gen.py --prompt "simple drawing" --no-enhance
```

## Output

- `*.jpg` images
- `prompts.json` — generation metadata
- `index.html` — thumbnail gallery

## How It Works

Pollinations.ai uses a simple GET request format:
```
https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&enhance=true
```

The script handles URL encoding, downloading, and gallery creation automatically.

## Tips

- Use `--enhance` (default) for better results — Pollinations improves your prompt with AI
- Higher resolutions take longer to generate
- Add descriptive terms like "4K", "photorealistic", "highly detailed" for better quality
