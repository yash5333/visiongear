from django.core.management.base import BaseCommand
from store.models import Product
from django.conf import settings
import os

def make_svg_png(width, height, category_slug, product_name):
    """Create an SVG, then convert to PNG if Pillow available, else save SVG."""
    
    icons = {
        'cameras':  ('📷', '#c9a84c', '1a1518'),
        'tripods':  ('🎬', '#c9a84c', '151a18'),
        'lighting': ('💡', '#c9a84c', '1a1a12'),
        'bags':     ('🎒', '#c9a84c', '151518'),
    }
    
    icon_char, gold, dark = icons.get(category_slug, ('📷', '#c9a84c', '1a1518'))
    
    # Short name for display
    short = product_name[:28] + ('…' if len(product_name) > 28 else '')
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#{dark};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f0f0f;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#e6c97a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#c9a84c;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bg)"/>
  
  <!-- Gold corner accent -->
  <polygon points="0,0 80,0 0,80" fill="#c9a84c" opacity="0.12"/>
  <polygon points="{width},{height} {width-60},{height} {width},{height-60}" fill="#c9a84c" opacity="0.08"/>
  
  <!-- Center glow circle -->
  <circle cx="{width//2}" cy="{height//2 - 20}" r="70" fill="#c9a84c" opacity="0.04" filter="url(#glow)"/>
  
  <!-- Icon background circle -->
  <circle cx="{width//2}" cy="{height//2 - 20}" r="55" fill="none" stroke="#c9a84c" stroke-width="1" opacity="0.2"/>
  <circle cx="{width//2}" cy="{height//2 - 20}" r="48" fill="#c9a84c" opacity="0.07"/>
  
  <!-- Category icon (text-based) -->
  <text x="{width//2}" y="{height//2 + 8}" font-size="52" text-anchor="middle" dominant-baseline="middle">{icon_char}</text>
  
  <!-- Gold separator line -->
  <line x1="{width//2 - 40}" y1="{height//2 + 42}" x2="{width//2 + 40}" y2="{height//2 + 42}" 
        stroke="url(#gold)" stroke-width="1" opacity="0.6"/>
  
  <!-- Product name -->
  <text x="{width//2}" y="{height//2 + 62}" 
        font-family="Georgia, serif" font-size="11" fill="#d8d8d8" 
        text-anchor="middle" dominant-baseline="middle">{short}</text>
  
  <!-- VisionGear watermark -->
  <text x="{width//2}" y="{height - 14}" 
        font-family="Courier New, monospace" font-size="8" fill="#c9a84c" 
        text-anchor="middle" opacity="0.4" letter-spacing="3">VISIONGEAR</text>
  
  <!-- Corner dots -->
  <circle cx="12" cy="12" r="2" fill="#c9a84c" opacity="0.3"/>
  <circle cx="{width-12}" cy="12" r="2" fill="#c9a84c" opacity="0.3"/>
  <circle cx="12" cy="{height-12}" r="2" fill="#c9a84c" opacity="0.3"/>
  <circle cx="{width-12}" cy="{height-12}" r="2" fill="#c9a84c" opacity="0.3"/>
</svg>'''
    return svg


class Command(BaseCommand):
    help = 'Generate placeholder product images using SVG/PNG'

    def handle(self, *args, **kwargs):
        self.stdout.write('🎨 Generating product placeholder images...\n')

        media_root = settings.MEDIA_ROOT
        products_dir = os.path.join(media_root, 'products')
        os.makedirs(products_dir, exist_ok=True)

        # Try Pillow first, fall back to SVG
        try:
            from PIL import Image, ImageDraw, ImageFont
            use_pillow = True
            self.stdout.write('  Using Pillow for PNG generation')
        except ImportError:
            use_pillow = False
            self.stdout.write('  Pillow not available, using SVG files')

        for product in Product.objects.all():
            try:
                if use_pillow:
                    self._make_pillow_image(product, products_dir)
                else:
                    self._make_svg_image(product, products_dir)
                self.stdout.write(f'  ✓ {product.name}')
            except Exception as e:
                self.stdout.write(f'  ✗ {product.name}: {e}')

        self.stdout.write(self.style.SUCCESS('\n✅ Done! Refresh your browser to see images.'))

    def _make_pillow_image(self, product, products_dir):
        from PIL import Image, ImageDraw
        import math

        W, H = 800, 600
        slug = product.category.slug

        # Color schemes per category
        schemes = {
            'cameras':  {'bg': (18, 14, 20),  'accent': (201, 168, 76), 'mid': (30, 20, 35)},
            'tripods':  {'bg': (14, 18, 20),  'accent': (201, 168, 76), 'mid': (20, 30, 35)},
            'lighting': {'bg': (20, 18, 10),  'accent': (201, 168, 76), 'mid': (35, 30, 15)},
            'bags':     {'bg': (14, 14, 20),  'accent': (201, 168, 76), 'mid': (20, 20, 35)},
        }
        s = schemes.get(slug, schemes['cameras'])
        bg, accent, mid = s['bg'], s['accent'], s['mid']

        img = Image.new('RGB', (W, H), bg)
        draw = ImageDraw.Draw(img)

        # Gradient background (manual)
        for y in range(H):
            ratio = y / H
            r = int(bg[0] + (mid[0] - bg[0]) * ratio * 0.4)
            g = int(bg[1] + (mid[1] - bg[1]) * ratio * 0.4)
            b = int(bg[2] + (mid[2] - bg[2]) * ratio * 0.4)
            draw.line([(0, y), (W, y)], fill=(r, g, b))

        # Radial glow in center
        cx, cy = W // 2, H // 2 - 30
        for r in range(120, 0, -1):
            alpha = int(255 * (1 - r/120) * 0.08)
            color = (accent[0], accent[1], accent[2])
            # Draw filled circle with low opacity approximation
            draw.ellipse([cx-r, cy-r, cx+r, cy+r],
                        fill=tuple(int(bg[i] + (color[i]-bg[i]) * alpha/255) for i in range(3)))

        # Outer ring
        draw.ellipse([cx-80, cy-80, cx+80, cy+80], outline=(*accent, ), width=1)
        draw.ellipse([cx-70, cy-70, cx+70, cy+70],
                    fill=tuple(int(c * 1.15) if int(c * 1.15) < 255 else 255 for c in bg))

        # Draw category icon shape
        if slug == 'cameras':
            self._draw_camera(draw, cx, cy, accent, bg)
        elif slug == 'tripods':
            self._draw_tripod(draw, cx, cy, accent, bg)
        elif slug == 'lighting':
            self._draw_light(draw, cx, cy, accent, bg)
        else:
            self._draw_bag(draw, cx, cy, accent, bg)

        # Gold separator
        sep_y = cy + 90
        for x in range(W//2 - 60, W//2 + 61):
            ratio = 1 - abs(x - W//2) / 60
            a = int(ratio * 180)
            existing = img.getpixel((x, sep_y))
            blended = tuple(int(existing[i] + (accent[i] - existing[i]) * a/255) for i in range(3))
            draw.point((x, sep_y), fill=blended)

        # Product name text (chunked)
        name = product.name
        chunks = [name[i:i+32] for i in range(0, min(len(name), 64), 32)]
        for i, chunk in enumerate(chunks):
            y_pos = sep_y + 18 + i * 16
            # Simple text rendering - draw each char
            draw.text((cx, y_pos), chunk, fill=(180, 180, 180), anchor='mm')

        # Category label
        draw.text((cx, H - 22), 'VISIONGEAR', fill=(*accent,), anchor='mm')

        # Corner accents
        sz = 20
        draw.polygon([(0,0),(sz,0),(0,sz)], fill=(*accent,))
        a2 = int(255 * 0.15)
        dim_accent = tuple(int(c * 0.5) for c in accent)
        draw.polygon([(W,H),(W-sz,H),(W,H-sz)], fill=dim_accent)

        # Corner dots
        dot_r = 3
        for px, py in [(10,10),(W-10,10),(10,H-10),(W-10,H-10)]:
            draw.ellipse([px-dot_r, py-dot_r, px+dot_r, py+dot_r],
                        fill=tuple(int(c * 0.5) for c in accent))

        filename = f'{product.slug}.png'
        filepath = os.path.join(products_dir, filename)
        img.save(filepath, 'PNG', quality=95)
        product.image = f'products/{filename}'
        product.save(update_fields=['image'])

    def _draw_camera(self, draw, cx, cy, accent, bg):
        # Camera body
        bw, bh = 90, 62
        body_color = tuple(min(255, c + 25) for c in bg)
        draw.rounded_rectangle([cx-bw, cy-bh//2, cx+bw, cy+bh//2], radius=8, fill=body_color, outline=accent, width=2)
        # Lens
        draw.ellipse([cx-30, cy-30, cx+30, cy+30], outline=accent, width=3)
        draw.ellipse([cx-20, cy-20, cx+20, cy+20], outline=tuple(int(c*0.6) for c in accent), width=1)
        draw.ellipse([cx-8, cy-8, cx+8, cy+8], fill=accent)
        # Viewfinder bump
        draw.rounded_rectangle([cx+30, cy-bh//2-14, cx+60, cy-bh//2+2], radius=4, fill=body_color, outline=accent, width=1)
        # Flash
        draw.rectangle([cx-bw+8, cy-bh//2+8, cx-bw+22, cy-bh//2+18], fill=tuple(int(c*0.7) for c in accent))

    def _draw_tripod(self, draw, cx, cy, accent, bg):
        head_color = tuple(min(255, c + 20) for c in bg)
        # Head
        draw.rounded_rectangle([cx-35, cy-55, cx+35, cy-30], radius=5, fill=head_color, outline=accent, width=2)
        # Center pole
        draw.line([cx, cy-30, cx, cy+10], fill=accent, width=4)
        # Legs
        draw.line([cx, cy+10, cx-55, cy+65], fill=accent, width=3)
        draw.line([cx, cy+10, cx+55, cy+65], fill=accent, width=3)
        draw.line([cx, cy+10, cx, cy+70], fill=accent, width=3)
        # Feet
        for fx, fy in [(cx-55, cy+65), (cx+55, cy+65), (cx, cy+70)]:
            draw.ellipse([fx-5, fy-3, fx+5, fy+3], fill=accent)

    def _draw_light(self, draw, cx, cy, accent, bg):
        import math
        # Bulb
        draw.ellipse([cx-38, cy-52, cx+38, cy+24], outline=accent, width=3)
        draw.ellipse([cx-28, cy-42, cx+28, cy+14], fill=tuple(int(c*0.15) for c in accent))
        # Base
        draw.rectangle([cx-18, cy+24, cx+18, cy+40], fill=tuple(min(255,c+30) for c in bg), outline=accent, width=2)
        draw.rectangle([cx-25, cy+40, cx+25, cy+48], fill=tuple(min(255,c+20) for c in bg), outline=accent, width=2)
        # Rays
        for i in range(8):
            angle = i * math.pi / 4 - math.pi/2
            x1 = int(cx + math.cos(angle) * 48)
            y1 = int(cy - 14 + math.sin(angle) * 48)
            x2 = int(cx + math.cos(angle) * 62)
            y2 = int(cy - 14 + math.sin(angle) * 62)
            draw.line([x1, y1, x2, y2], fill=accent, width=2)

    def _draw_bag(self, draw, cx, cy, accent, bg):
        body_color = tuple(min(255, c + 22) for c in bg)
        # Body
        draw.rounded_rectangle([cx-55, cy-35, cx+55, cy+55], radius=10, fill=body_color, outline=accent, width=2)
        # Handle
        draw.arc([cx-30, cy-65, cx+30, cy-20], start=0, end=180, fill=accent, width=3)
        # Pocket
        draw.rounded_rectangle([cx-38, cy+5, cx+38, cy+45], radius=6, outline=accent, width=1)
        # Zipper line
        draw.line([cx-45, cy-5, cx+45, cy-5], fill=tuple(int(c*0.7) for c in accent), width=2)
        # Zipper pull
        draw.ellipse([cx-5, cy-10, cx+5, cy], fill=accent)

    def _make_svg_image(self, product, products_dir):
        svg = make_svg_png(800, 600, product.category.slug, product.name)
        filename = f'{product.slug}.svg'
        filepath = os.path.join(products_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg)
        product.image = f'products/{filename}'
        product.save(update_fields=['image'])
