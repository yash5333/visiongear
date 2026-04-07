from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seed the database with sample VisionGear data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding VisionGear database...')

        # ── Categories ──────────────────────────────
        cats_data = [
            {'name': 'Cameras',             'slug': 'cameras',  'icon': 'camera',    'description': 'DSLR, mirrorless and cinema cameras'},
            {'name': 'Tripods',             'slug': 'tripods',  'icon': 'podcast',   'description': 'Fluid head, carbon fibre and mini tripods'},
            {'name': 'Lighting Equipment',  'slug': 'lighting', 'icon': 'lightbulb', 'description': 'LED panels, softboxes and strobe lights'},
            {'name': 'Camera Bags',         'slug': 'bags',     'icon': 'briefcase', 'description': 'Backpacks, sling bags and hard cases'},
        ]
        categories = {}
        for c in cats_data:
            cat, _ = Category.objects.get_or_create(slug=c['slug'], defaults=c)
            categories[c['slug']] = cat
            self.stdout.write(f'  ✓ Category: {cat.name}')

        # ── Products ─────────────────────────────────
        products_data = [
            # CAMERAS
            {
                'category': 'cameras', 'name': 'Sony Alpha a7 IV Full-Frame Mirrorless', 'slug': 'sony-alpha-a7-iv',
                'brand': 'Sony', 'price': 249999, 'discount_price': 224999, 'stock': 15, 'is_featured': True,
                'short_description': '33MP BSI-CMOS sensor, 4K 60p video, real-time tracking AF.',
                'description': 'The Sony Alpha a7 IV is a high-resolution, versatile full-frame mirrorless camera. Its 33-megapixel Exmor R BSI-CMOS sensor delivers stunning image quality. Featuring advanced Real-time Tracking AF, 4K 60p 10-bit video recording, and a robust weather-sealed body — this camera is built for professional creators.',
                'specifications': 'Sensor: 33MP Full-Frame Exmor R BSI-CMOS\nISO Range: 100-51200 (expandable to 204800)\nAF Points: 759 phase-detection\nVideo: 4K 60p, Full HD 120p\nBattery Life: 520 shots\nWeight: 659g\nWeather Sealed: Yes',
            },
            {
                'category': 'cameras', 'name': 'Canon EOS R5 Mirrorless Camera Body', 'slug': 'canon-eos-r5',
                'brand': 'Canon', 'price': 329999, 'stock': 8, 'is_featured': True,
                'short_description': '45MP full-frame sensor, 8K RAW video, IBIS.',
                'description': 'The Canon EOS R5 pushes the boundaries of what is possible in a mirrorless camera. With 45 megapixels of resolution, 8K RAW internal video recording, and in-body image stabilisation, the R5 is the definitive tool for photographers and filmmakers who demand the absolute best.',
                'specifications': 'Sensor: 45MP Full-Frame CMOS\nISO Range: 100-51200\nVideo: 8K RAW, 4K 120p\nIBIS: Yes (up to 8 stops)\nWeight: 738g\nWeather Sealed: Yes',
            },
            {
                'category': 'cameras', 'name': 'Fujifilm X-T5 APS-C Mirrorless', 'slug': 'fujifilm-xt5',
                'brand': 'Fujifilm', 'price': 159999, 'discount_price': 144999, 'stock': 20,
                'short_description': '40MP X-Trans CMOS 5 HR sensor with 6.2K video.',
                'description': 'The Fujifilm X-T5 brings 40.2MP resolution into a compact, retro-inspired body. The X-Trans CMOS 5 HR sensor combined with X-Processor 5 delivers incredible detail and Fujifilm\'s legendary Film Simulations for distinct, artistic imagery straight out of camera.',
                'specifications': 'Sensor: 40.2MP X-Trans CMOS 5 HR\nISO: 125-12800\nVideo: 6.2K 30p, 4K 60p\nIBIS: Yes (7 stops)\nWeight: 476g',
            },
            {
                'category': 'cameras', 'name': 'Nikon Z8 Full-Frame Flagship', 'slug': 'nikon-z8',
                'brand': 'Nikon', 'price': 349999, 'stock': 6, 'is_featured': True,
                'short_description': '45.7MP stacked BSI-CMOS, 8K video, Pro AF.',
                'description': 'The Nikon Z8 packs the power of the Z9 into a more compact, ergonomic body. With a 45.7MP stacked BSI-CMOS sensor, subject-detection autofocus, and internal 8K RAW video, the Z8 is Nikon\'s most versatile professional camera.',
                'specifications': 'Sensor: 45.7MP Stacked BSI-CMOS\nISO: 64-25600\nAF: Subject Detection\nVideo: 8K 60p RAW\nWeight: 910g\nWeather Sealed: Yes',
            },
            {
                'category': 'cameras', 'name': 'DJI Pocket 3 Cinema Premium Combo', 'slug': 'dji-pocket-3',
                'brand': 'DJI', 'price': 62990, 'discount_price': 57999, 'stock': 25,
                'short_description': '1-inch CMOS, 4K 120fps, 3-axis gimbal stabilisation.',
                'description': 'The DJI Osmo Pocket 3 features a 1-inch CMOS sensor that captures exceptional 4K 120fps video with stunning dynamic range. Its 3-axis mechanical stabilisation keeps every shot silky smooth, even during fast-paced action shoots.',
                'specifications': 'Sensor: 1-inch CMOS\nVideo: 4K 120fps\nStabilization: 3-axis mechanical\nBattery: 1300mAh\nWeight: 179g',
            },

            # TRIPODS
            {
                'category': 'tripods', 'name': 'Benro TMA38CL Mach3 Carbon Fibre Tripod', 'slug': 'benro-tma38cl-carbon',
                'brand': 'Benro', 'price': 42999, 'discount_price': 37999, 'stock': 30, 'is_featured': True,
                'short_description': '10-layer carbon fibre legs, 25kg load capacity, 180° leg angle.',
                'description': 'The Benro Mach3 TMA38CL is a professional-grade carbon fibre tripod built for demanding photographers. The 10-layer carbon fibre construction provides extreme rigidity while keeping weight to a minimum. Supports loads up to 25kg with a maximum height of 190cm.',
                'specifications': 'Material: 10-layer Carbon Fibre\nMax Load: 25kg\nMax Height: 190cm\nMin Height: 8cm\nWeight: 2.2kg\nLeg Sections: 3\nFolded Length: 67cm',
            },
            {
                'category': 'tripods', 'name': 'Manfrotto MT055CXPRO4 Carbon Tripod', 'slug': 'manfrotto-055-carbon',
                'brand': 'Manfrotto', 'price': 34999, 'stock': 18,
                'short_description': '4-section carbon fibre, 90° column system, Easy Link.',
                'description': 'The Manfrotto 055 Carbon Fibre Tripod is a professional studio and location tripod. The patented 90-degree column system allows the centre column to be positioned horizontally for unique low-angle shots. Features Easy Link attachment for accessories.',
                'specifications': 'Material: Carbon Fibre\nMax Load: 9kg\nMax Height: 170cm\nSections: 4\nWeight: 1.9kg',
            },
            {
                'category': 'tripods', 'name': 'Joby GorillaPod 5K Kit with Ball Head', 'slug': 'joby-gorillapod-5k',
                'brand': 'Joby', 'price': 9999, 'discount_price': 8499, 'stock': 50,
                'short_description': 'Flexible legs, 5kg load, 360° ball head included.',
                'description': 'The Joby GorillaPod 5K is the ultimate flexible tripod for on-the-go photographers. Its unique ball-and-socket leg design lets you wrap, bend and position it around any surface. Includes the BH-5K ball head with Arca-Swiss quick-release.',
                'specifications': 'Max Load: 5kg\nBall Head: BH-5K (included)\nWeight: 540g\nMaterial: ABS/TPE\nQuick Release: Arca-Swiss compatible',
            },
            {
                'category': 'tripods', 'name': 'Gitzo GT3543LS Series 3 Traveler Carbon', 'slug': 'gitzo-gt3543ls',
                'brand': 'Gitzo', 'price': 89999, 'stock': 5, 'is_featured': True,
                'short_description': 'Ultra-compact travel tripod, 18kg load, Carbon eXact tubes.',
                'description': 'The Gitzo Series 3 Traveler is the finest travel tripod ever engineered. Carbon eXact tubes offer the best stiffness-to-weight ratio. Leg sections fold upward for an incredibly compact packed size — perfect for travel photographers who refuse to compromise.',
                'specifications': 'Material: Carbon eXact\nMax Load: 18kg\nMax Height: 166cm\nFolded Length: 42cm\nWeight: 1.65kg\nSections: 4',
            },

            # LIGHTING
            {
                'category': 'lighting', 'name': 'Godox AD600 Pro Witstro All-in-One Flash', 'slug': 'godox-ad600-pro',
                'brand': 'Godox', 'price': 54999, 'discount_price': 49999, 'stock': 12, 'is_featured': True,
                'short_description': '600Ws HSS lithium battery strobe with built-in Godox X system.',
                'description': 'The Godox AD600Pro is a professional portable flash delivering 600Ws of power with High Speed Sync support up to 1/8000s. The built-in Godox X wireless system allows remote control from the transmitter. A complete portable lighting solution for location photographers.',
                'specifications': 'Power Output: 600Ws\nFlash Duration: 1/220s - 1/10200s\nHSS: Yes (up to 1/8000s)\nRecycle Time: 0.01-2.5s\nBattery: 28.8V 2600mAh Li-ion\nFlash Count: ~500 full power\nWeight: 2.5kg',
            },
            {
                'category': 'lighting', 'name': 'Aputure LS 600x Pro LED Light', 'slug': 'aputure-ls-600x',
                'brand': 'Aputure', 'price': 129999, 'stock': 7,
                'short_description': '600W bi-color LED, 2700–6500K, Sidus Link app control.',
                'description': 'The Aputure Light Storm 600x Pro is a 600W bi-color LED light designed for cinematic productions. With a 2700–6500K colour temperature range, ultra-high TLCI/CRI, and Sidus Link Bluetooth app control, it is the go-to LED powerhouse for film sets and commercial photography.',
                'specifications': 'Power: 600W\nColor Temp: 2700-6500K\nCRI/TLCI: 96+\nIlluminance: 83,460 lux @ 1m\nControl: Sidus Link app, 0-100% dimming\nWeight: 10.6kg',
            },
            {
                'category': 'lighting', 'name': 'Profoto B10X Plus Off-Camera Flash', 'slug': 'profoto-b10x-plus',
                'brand': 'Profoto', 'price': 149999, 'stock': 4,
                'short_description': '500Ws portable strobe with HSS, TTL, built-in LED modelling.',
                'description': 'The Profoto B10X Plus packs 500Ws into an ultra-compact, battery-powered flash. With TTL and High Speed Sync support across major camera brands, plus a built-in 30W LED modelling light, this is the most versatile portable studio flash available.',
                'specifications': 'Power: 500Ws\nHSS: Yes\nTTL: Yes (Sony, Canon, Nikon, Fuji)\nModelling Light: 30W LED\nRecycle Time: 2s (full power)\nWeight: 1.2kg',
            },
            {
                'category': 'lighting', 'name': 'Neewer 18" LED Ring Light Kit 55W', 'slug': 'neewer-18-ring-light',
                'brand': 'Neewer', 'price': 7999, 'discount_price': 5999, 'stock': 60,
                'short_description': '18-inch ring light, 3200-5600K, includes phone holder and stand.',
                'description': 'The Neewer 18-inch ring light is perfect for portrait photography, YouTube videos, and live streaming. The dimmable LED ring provides even, flattering light with a colour temperature range from warm to daylight. Kit includes adjustable stand and smartphone holder.',
                'specifications': 'Diameter: 18 inches\nPower: 55W\nColor Temp: 3200-5600K\nCRI: 95+\nDimming: 0-100%\nIncludes: Stand, phone holder, carrying bag',
            },

            # BAGS
            {
                'category': 'bags', 'name': 'Lowepro ProTrekker BP 450 AW II Backpack', 'slug': 'lowepro-protrekker-bp450',
                'brand': 'Lowepro', 'price': 24999, 'discount_price': 21999, 'stock': 22, 'is_featured': True,
                'short_description': 'Large capacity camera backpack, fits 15" laptop, all-weather cover.',
                'description': 'The Lowepro ProTrekker BP 450 AW II is built for the adventurous photographer. The main compartment holds a full camera kit, and the separate laptop section accommodates up to a 15-inch laptop. An included all-weather cover ensures your gear stays protected in any conditions.',
                'specifications': 'Interior: 30 x 19 x 47 cm\nLaptop Compartment: Up to 15 inches\nMaterial: 400D HDP Nylon\nWaterproof Cover: Included\nWeight: 2.24kg\nCapacity: 30L',
            },
            {
                'category': 'bags', 'name': 'Peak Design Everyday Backpack 30L V2', 'slug': 'peak-design-everyday-30l',
                'brand': 'Peak Design', 'price': 39999, 'stock': 10,
                'short_description': 'FlexFold dividers, MagLatch closure, recycled weatherproof nylon.',
                'description': 'The Peak Design Everyday Backpack is the world\'s most adaptable bag. FlexFold dividers customise the interior in seconds. The MagLatch top closure secures your belongings and looks sleek. Made from 100% recycled weatherproof nylon with full lifetime guarantee.',
                'specifications': 'Capacity: 30L\nLaptop: Up to 16 inches\nMaterial: 400D Recycled nylon canvas\nDivider System: FlexFold\nAccess: Top, side, front\nWeight: 1.85kg\nGuarantee: Lifetime',
            },
            {
                'category': 'bags', 'name': 'Wandrd PRVKE 41 Litre Camera Backpack', 'slug': 'wandrd-prvke-41',
                'brand': 'Wandrd', 'price': 29999, 'discount_price': 26499, 'stock': 14,
                'short_description': 'Roll-top design, tarpaulin base, camera cube included.',
                'description': 'The Wandrd PRVKE 41 is the ultimate hybrid backpack for photographers who adventure. The expandable roll-top closure adds 10L of additional capacity. The tarpaulin base and waterproof zippers ensure your gear is protected from the elements.',
                'specifications': 'Capacity: 31-41L\nLaptop: Up to 15 inches\nMaterial: 840D ballistic nylon\nBase: Tarpaulin\nCamera Cube: Included\nWeight: 2.0kg',
            },
            {
                'category': 'bags', 'name': 'Nanuk 935 Hard Case with Foam Insert', 'slug': 'nanuk-935-hard-case',
                'brand': 'Nanuk', 'price': 18999, 'stock': 8,
                'short_description': 'IP67 waterproof hard case, PowerClaw latch, crushproof.',
                'description': 'The Nanuk 935 is a professional-grade hard case for storing and transporting sensitive camera equipment. The patented PowerClaw superior latch system is incredibly strong yet easy to open. Fully waterproof (IP67) and dustproof — your gear is protected against the harshest conditions.',
                'specifications': 'Interior: 45.7 x 25.4 x 17.8 cm\nMaterial: NK-7 Resin\nWaterproof: IP67 certified\nLatch: PowerClaw\nWeight: 2.0kg\nFoam Insert: Included (customisable)',
            },
        ]

        for pd in products_data:
            cat = categories[pd.pop('category')]
            product, created = Product.objects.get_or_create(
                slug=pd['slug'],
                defaults={**pd, 'category': cat}
            )
            if created:
                self.stdout.write(f'  ✓ Product: {product.name}')
            else:
                self.stdout.write(f'  ~ Exists: {product.name}')

        # ── Admin user ─────────────────────────────
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@visiongear.com', 'admin123')
            self.stdout.write('  ✓ Superuser: admin / admin123')
        else:
            self.stdout.write('  ~ Superuser already exists')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write('   Admin: admin / admin123')
        self.stdout.write('   Run: python manage.py runserver')
