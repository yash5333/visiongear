# 📷 VisionGear — Photography & Videography E-Commerce

A complete, full-stack Django e-commerce application for photography and videography equipment. Features a dark luxury aesthetic with gold accents, built for professional creators.

---

## ✨ Features Implemented

### 1. User Authentication Module
- ✅ User registration with profile auto-creation
- ✅ Login / Logout
- ✅ Profile management (avatar, bio, address)
- ✅ Password change

### 2. Product Management Module
- ✅ Products with categories (Cameras, Tripods, Lighting, Bags)
- ✅ Product images, descriptions, specifications
- ✅ Brand, stock, pricing with discount support
- ✅ Django Admin CRUD for all products
- ✅ Featured product flagging

### 3. Product Catalog Module
- ✅ Full product listing with beautiful card grid
- ✅ Category-wise browsing with sidebar filter
- ✅ Product detail page with image gallery
- ✅ Search by name, description, brand, category
- ✅ Price range filter
- ✅ Sort (newest, price low/high, name)

### 4. Shopping Cart Module
- ✅ Add to cart (AJAX — no page reload)
- ✅ Remove items (AJAX)
- ✅ Update quantity (AJAX)
- ✅ Live cart total with tax & shipping

### 5. Order Management Module
- ✅ Full checkout flow with shipping form
- ✅ Order history page
- ✅ Order detail with status timeline
- ✅ Order cancellation

### 6. Payment Module
- ✅ Demo payment (instant confirmation)
- ✅ Card / UPI / COD UI (mock)
- ✅ Payment confirmation & order success page
- ✅ Printable invoice generation

### 7. Review & Rating Module
- ✅ Star rating (1–5) with interactive input
- ✅ Review title + body
- ✅ One review per user per product
- ✅ Average rating calculation + display

### 8. Admin Dashboard Module
- ✅ Sales analytics with Chart.js revenue graph
- ✅ Order management with status update
- ✅ User management table
- ✅ Product management table
- ✅ Key stats (revenue, orders, users, products)

### 9. Wishlist Module
- ✅ Add/remove products from wishlist (AJAX)
- ✅ Wishlist page with all saved items
- ✅ Move wishlist item to cart

### 🎠 Homepage Carousel
- ✅ Auto-playing hero slider (3 slides, 6s interval)
- ✅ Prev/next navigation arrows
- ✅ Dot indicators
- ✅ Keyboard/click navigation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Navigate to project
cd visiongear

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Run the setup script (installs deps, migrates, seeds data)
bash setup.sh

# 4. Start the server
python manage.py runserver
```

### Manual Setup (alternative)
```bash
pip install -r requirements.txt
python manage.py makemigrations users store orders
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

---

## 🔑 Access

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/ | Home page |
| http://127.0.0.1:8000/products/ | Shop |
| http://127.0.0.1:8000/admin/ | Django Admin |
| http://127.0.0.1:8000/orders/dashboard/ | Custom Admin Dashboard |

**Default credentials:** `admin` / `admin123`

---

## 🗂️ Project Structure

```
visiongear/
├── visiongear/          # Django project settings
│   ├── settings.py
│   └── urls.py
├── store/               # Products, cart, wishlist, reviews
│   ├── models.py        # Category, Product, Cart, Wishlist, Review
│   ├── views.py         # All store views
│   ├── urls.py
│   └── management/commands/seed_data.py
├── users/               # Authentication & profiles
│   ├── models.py        # Profile model
│   ├── views.py
│   └── forms.py
├── orders/              # Orders, checkout, payment, admin
│   ├── models.py        # Order, OrderItem
│   ├── views.py         # Checkout, invoice, admin dashboard
│   └── urls.py
├── templates/           # All HTML templates
│   ├── base.html        # Master layout (navbar, footer)
│   ├── store/
│   │   ├── home.html    # Homepage with carousel
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   └── wishlist.html
│   ├── users/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   └── orders/
│       ├── checkout.html
│       ├── order_success.html
│       ├── order_history.html
│       ├── order_detail.html
│       ├── invoice.html
│       └── admin_dashboard.html
├── static/              # CSS, JS, images
├── media/               # Uploaded images
├── requirements.txt
├── setup.sh
└── manage.py
```

---

## 🎨 Design System

- **Font Display:** Cormorant Garamond (elegant serif)
- **Font Body:** DM Sans (clean, modern)
- **Font Mono:** Space Mono (technical details)
- **Theme:** Dark luxury — obsidian blacks with warm gold accents
- **Palette:** #080808 (black), #c9a84c (gold), #f5f5f0 (white)

---

## 🛠️ Tech Stack

- **Backend:** Django 4.2
- **Database:** SQLite (production-ready with PostgreSQL)
- **Frontend:** Vanilla HTML/CSS/JavaScript — no frameworks needed
- **Charts:** Chart.js (admin dashboard)
- **Icons:** Font Awesome 6
- **Fonts:** Google Fonts

---

## 📝 Adding Products

1. Go to http://127.0.0.1:8000/admin/
2. Login with `admin` / `admin123`
3. Click **Products → Add Product**
4. Fill in details, upload image, set featured/active flags
5. Save

Or use the custom Admin Dashboard at `/orders/dashboard/`
