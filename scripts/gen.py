#!/usr/bin/env python3
"""
Pollinations.ai Image Generator
Free image generation with no API key required.
https://pollinations.ai
"""

import os
import sys
import argparse
import json
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime


def generate_image(
    prompt: str,
    output_dir: str = "./tmp/pollinations-image-gen",
    width: int = 1024,
    height: int = 768,
    seed: int = None,
    nologo: bool = True,
    enhance: bool = True,
    count: int = 1,
) -> list:
    """
    Generate images using Pollinations.ai (completely free, no API key).
    
    Args:
        prompt: The image generation prompt
        output_dir: Directory to save generated images
        width: Image width (default: 1024)
        height: Image height (default: 768)
        seed: Random seed for reproducibility (optional)
        nologo: Remove Pollinations logo (default: True)
        enhance: Enhance prompt with AI (default: True)
        count: Number of images to generate
    
    Returns:
        List of paths to generated images
    """
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = Path(output_dir) / timestamp
    out_path.mkdir(parents=True, exist_ok=True)
    
    generated_files = []
    prompts_log = []
    
    for i in range(count):
        print(f"Generating image {i+1}/{count}...")
        print(f"Prompt: {prompt}")
        
        try:
            # Build URL with parameters
            params = {
                "width": width,
                "height": height,
                "nologo": str(nologo).lower(),
                "enhance": str(enhance).lower(),
            }
            if seed is not None:
                params["seed"] = seed + i  # Vary seed for multiple images
            
            # URL encode the prompt
            encoded_prompt = urllib.parse.quote(prompt)
            
            # Build full URL
            base_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            query_string = urllib.parse.urlencode(params)
            full_url = f"{base_url}?{query_string}"
            
            print(f"  URL: {full_url[:100]}...")
            
            # Download the image
            filename = f"image_{i+1:02d}.jpg"
            filepath = out_path / filename
            
            req = urllib.request.Request(
                full_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
            )
            
            with urllib.request.urlopen(req, timeout=120) as response:
                with open(filepath, "wb") as f:
                    f.write(response.read())
            
            generated_files.append(str(filepath))
            prompts_log.append({
                "prompt": prompt,
                "file": filename,
                "width": width,
                "height": height,
                "seed": seed + i if seed is not None else None,
            })
            print(f"  Saved: {filepath}")
                
        except Exception as e:
            print(f"  Error generating image {i+1}: {e}")
            continue
    
    # Save prompts log
    if prompts_log:
        prompts_log_full = {
            "service": "pollinations.ai",
            "generated_at": timestamp,
            "images": prompts_log
        }
        prompts_file = out_path / "prompts.json"
        with open(prompts_file, "w") as f:
            json.dump(prompts_log_full, f, indent=2)
        print(f"\nPrompts saved to: {prompts_file}")
    
    # Create HTML gallery
    if generated_files:
        create_gallery(out_path, prompts_log)
    
    return generated_files


def create_gallery(out_dir: Path, prompts_log: list):
    """Create a simple HTML gallery of generated images."""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pollinations.ai Gallery</title>
    <style>
        body { font-family: system-ui, sans-serif; margin: 40px; background: #f5f5f5; }
        h1 { color: #333; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 20px; }
        .item { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .item img { width: 100%; height: auto; border-radius: 4px; }
        .prompt { margin-top: 10px; font-size: 14px; color: #666; font-style: italic; }
        .meta { margin-top: 5px; font-size: 12px; color: #999; }
    </style>
</head>
<body>
    <h1>🎨 Pollinations.ai Gallery (Free!)</h1>
    <div class="gallery">
"""
    
    for entry in prompts_log:
        html_content += f"""
        <div class="item">
            <img src="{entry['file']}" alt="Generated image">
            <div class="prompt">"{entry['prompt']}"</div>
            <div class="meta">{entry['width']}x{entry['height']}</div>
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    gallery_path = out_dir / "index.html"
    with open(gallery_path, "w") as f:
        f.write(html_content)
    print(f"Gallery saved to: {gallery_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Pollinations.ai (free, no API key required)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="The image generation prompt"
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=1,
        help="Number of images to generate (default: 1)"
    )
    parser.add_argument(
        "--out-dir", "-o",
        default="./tmp/pollinations-image-gen",
        help="Output directory for generated images (default: ./tmp/pollinations-image-gen)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1024,
        help="Image width (default: 1024)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=768,
        help="Image height (default: 768)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (optional)"
    )
    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Disable AI prompt enhancement"
    )
    
    args = parser.parse_args()
    
    try:
        files = generate_image(
            prompt=args.prompt,
            output_dir=args.out_dir,
            width=args.width,
            height=args.height,
            seed=args.seed,
            enhance=not args.no_enhance,
            count=args.count,
        )
        
        if files:
            print(f"\n✅ Generated {len(files)} image(s)")
            for f in files:
                print(f"   - {f}")
        else:
            print("\n❌ No images were generated")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
