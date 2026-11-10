#!/usr/bin/env python3
"""Static site generator for the Anitha Techsolutions website.

Edit the settings and page content below, then run:
    python3 build.py
The finished site is written to ./public — upload that folder to any static host
(Netlify, Cloudflare Pages, GitHub Pages, cPanel, Nginx ...).
"""
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

# ── Settings ────────────────────────────────────────────────────────────────
SITE_URL = 'https://anithatechsolutions.github.io'   # live site URL (no trailing slash); change if you add a custom domain
BRAND = 'Anitha Techsolutions'
LEGAL = 'Anitha Tech Solutions Pvt. Ltd.'
EMAIL = 'anithatechsolutions@gmail.com'
TAGLINE = 'Odoo ERP & Mobile App Development Company'
APP_STORE_URL = ''                          # Odoo Apps Store link for Sale Order Split, once published
UPDATED = date.today().isoformat()

ROOT = Path(__file__).parent
SRC, OUT = ROOT / 'src', ROOT / 'public'

# ── Icons (inline SVG, stroke style) ────────────────────────────────────────
_P = {
    'rocket': '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.1 2.1 0 0 0-2.9-.1z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.9A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
    'code': '<path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/>',
    'upgrade': '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M12 8v8M8.5 11.5L12 8l3.5 3.5"/>',
    'plug': '<path d="M12 22v-5M9 8V2M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8z"/>',
    'compass': '<circle cx="12" cy="12" r="10"/><path d="M16.2 7.8l-2.1 6.4-6.4 2.1 2.1-6.4z"/>',
    'support': '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="M4.9 4.9l4.3 4.3M14.8 14.8l4.3 4.3M14.8 9.2l4.3-4.3M4.9 19.1l4.3-4.3"/>',
    'server': '<rect x="2" y="3" width="20" height="8" rx="2"/><rect x="2" y="13" width="20" height="8" rx="2"/><path d="M6 7h.01M6 17h.01"/>',
    'chart': '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
    'receipt': '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1z"/><path d="M8 7h8M8 11h8M8 15h5"/>',
    'cart': '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>',
    'school': '<path d="M22 10L12 5 2 10l10 5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
    'phone': '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>',
    'app': '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><path d="M17.5 14v7M14 17.5h7"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    'users': '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    'layers': '<path d="M12 2L2 7l10 5 10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>',
    'target': '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'globe': '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    'arrow': '<path d="M5 12h14M12 5l7 7-7 7"/>',
    'truck': '<path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>',
    'factory': '<path d="M2 20V8l6 4V8l6 4V4h8v16z"/><path d="M6 16h.01M10 16h.01M14 16h.01M18 16h.01"/>',
    'store': '<path d="M3 9l1.5-5h15L21 9"/><path d="M3 9v11h18V9M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M9 20v-6h6v6"/>',
    'heart': '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21.2l8.8-8.8a5.5 5.5 0 0 0 0-7.8z"/>',
    'building': '<rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    'briefcase': '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    'wifi-off': '<path d="M1 1l22 22M16.7 11.1A11 11 0 0 1 19 12.6M5 12.6a11 11 0 0 1 5.2-2.5M10.7 5A16 16 0 0 1 22.6 9M1.4 9a16 16 0 0 1 4.3-2.8M8.5 16.1a5 5 0 0 1 7 0M12 20h.01"/>',
    'bell': '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0"/>',
    'scan': '<path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2M7 12h10"/>',
    'map': '<path d="M1 6v16l7-4 8 4 7-4V2l-7 4-8-4z"/><path d="M8 2v16M16 6v16"/>',
    'menu': '<path d="M3 6h18M3 12h18M3 18h18"/>',
}


def icon(name):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_P[name]}</svg>')


# ── Content ─────────────────────────────────────────────────────────────────
SERVICES = [
    ('odoo-implementation', 'rocket', 'Odoo Implementation',
     'End-to-end rollout of Odoo Community or Enterprise, from requirement study to go-live.',
     ['Business process study and fit-gap analysis', 'Module setup: Sales, CRM, Inventory, Accounting, Manufacturing, POS, HR and more',
      'Master data and opening balance import', 'User acceptance testing, go-live and hypercare']),
    ('odoo-customization', 'code', 'Odoo Customization & Module Development',
     'Custom modules, workflows, views and automation built to OCA coding standards.',
     ['New modules and extensions of standard apps', 'Custom workflows, approvals and automated actions',
      'Views, wizards, portal pages and website snippets', 'Automated tests and clean, upgrade-friendly code']),
    ('odoo-migration', 'upgrade', 'Odoo Migration & Upgrade',
     'Move from older versions (Odoo 12 and later) to Odoo 18, 19 or 20 safely.',
     ['Version-to-version database upgrade', 'Porting custom modules to the new ORM and view syntax',
      'Community to Enterprise migration', 'Test upgrades, data validation and a rollback plan']),
    ('odoo-integration', 'plug', 'Odoo Integration',
     'Connect Odoo with payment gateways, marketplaces, shipping, banks and your own systems.',
     ['Payment gateways and bank statement feeds', 'eCommerce, marketplace and shipping carriers',
      'REST / JSON-RPC / XML-RPC APIs and webhooks', 'Data sync with legacy ERP, CRM and BI tools']),
    ('odoo-consulting', 'compass', 'Odoo Functional Consulting',
     'Practical advice on how to run your processes in Odoo — before you spend on development.',
     ['Process mapping and best-practice recommendations', 'Choosing between configuration, apps and custom code',
      'Edition, hosting and licensing guidance', 'Project planning and phased roadmaps']),
    ('odoo-support', 'support', 'Odoo Support & Maintenance (AMC)',
     'Ongoing help after go-live: fixes, small changes, updates and monitoring.',
     ['Bug fixing and functional support', 'Small enhancements and report changes',
      'Module updates and security patches', 'Annual maintenance contracts']),
    ('odoo-hosting', 'server', 'Odoo Hosting, Server Setup & Performance Tuning',
     'Reliable Odoo servers on Odoo.sh, cloud VPS or on-premise — fast, secure and backed up.',
     ['Odoo.sh, AWS, Azure, DigitalOcean and on-premise setup', 'Odoo workers, PostgreSQL and Nginx tuning',
      'SSL, firewall and security hardening', 'Automated backups and monitoring']),
    ('odoo-reports', 'chart', 'Odoo Reports & Dashboards',
     'Custom PDF documents, Excel reports and dashboards your team will actually use.',
     ['QWeb PDF invoices, quotations and delivery slips', 'Excel / XLSX reports and exports',
      'KPI dashboards, pivot and graph views', 'Branded document layouts']),
    ('odoo-localization', 'receipt', 'Localization, VAT & e-Invoicing',
     'Set up taxes, chart of accounts and e-invoicing to meet local rules.',
     ['Chart of accounts and fiscal positions', 'VAT / GST configuration and tax reports',
      'e-Invoicing setup', 'Multi-company and multi-currency']),
    ('odoo-website-ecommerce', 'cart', 'Odoo Website & eCommerce',
     'Fast, SEO-friendly Odoo websites and online stores connected to your stock and accounts.',
     ['Website design and custom themes', 'Online shop, payments and delivery methods',
      'Customer portal and B2B pricing', 'SEO setup and page speed']),
    ('odoo-training', 'school', 'Odoo Training & Documentation',
     'Hands-on training so your team uses Odoo confidently from day one.',
     ['Role-based user training', 'Admin and power-user training', 'Step-by-step user guides', 'Remote or on-site sessions']),
    ('odoo-apps', 'app', 'Ready-made Odoo Apps',
     'Our own Odoo Apps Store modules that solve common gaps quickly and affordably.',
     ['Sale Order Split for Odoo 18, 19 and 20', 'Maintained and updated for new Odoo versions',
      'Installation help included', 'Custom versions on request']),
]

MOBILE_FEATURES = [
    ('phone', 'Android & iOS from one codebase', 'Cross-platform Flutter apps that look and feel native on both platforms.'),
    ('plug', 'Live Odoo connection', 'Apps read and write directly to your Odoo through secure APIs — no double entry.'),
    ('wifi-off', 'Offline mode', 'Field teams keep working without signal; data syncs automatically when back online.'),
    ('bell', 'Push notifications', 'Alerts for approvals, new orders, deliveries and reminders.'),
    ('scan', 'Barcode & camera', 'Scan products, capture photos and signatures right from the phone.'),
    ('map', 'GPS & routes', 'Customer locations, check-ins and route planning for sales and delivery teams.'),
]

MOBILE_USECASES = [
    ('truck', 'Van Sales & Field Sales', 'Take orders, invoice, collect payments and manage van stock on the road.'),
    ('scan', 'Warehouse & Delivery', 'Picking, packing, receipts and proof of delivery with barcode scanning.'),
    ('users', 'Employee Self-Service', 'Attendance, leave requests, payslips and expenses for every employee.'),
    ('store', 'Ordering & POS', 'Customer ordering apps and mobile point of sale linked to Odoo stock.'),
    ('globe', 'Customer Portal Apps', 'Let customers track orders, invoices and support tickets on their phone.'),
    ('chart', 'Management Dashboards', 'Sales, cash and stock KPIs for owners and managers, anywhere.'),
]

INDUSTRIES = [
    ('truck', 'Trading & Distribution'), ('factory', 'Manufacturing'), ('store', 'Retail & POS'), ('heart', 'Healthcare & Clinics'),
    ('building', 'Construction & Projects'), ('briefcase', 'Professional Services'), ('school', 'Education'), ('map', 'Logistics'),
]

WHY = [
    ('layers', 'Odoo specialists', 'We work with Odoo every day, across versions 12 to 20, Community and Enterprise.'),
    ('code', 'Clean, standard code', 'Modules follow OCA guidelines and include tests, so upgrades stay simple.'),
    ('target', 'Clear scope & estimates', 'You know what will be delivered, when, and what it costs before work starts.'),
    ('users', 'Direct developer access', 'Talk to the people building your solution — no long chains of hand-offs.'),
    ('phone', 'ERP + mobile in one team', 'Odoo and the mobile apps that connect to it come from the same team.'),
    ('shield', 'Support after go-live', 'We stay with you after launch with support, fixes and improvements.'),
]

PROCESS = [
    ('Discover', 'We study your processes, goals and current systems.'),
    ('Plan', 'Fit-gap analysis, scope, timeline and a clear estimate.'),
    ('Build', 'Configuration, custom modules, integrations and mobile apps.'),
    ('Launch', 'Data migration, testing, training and go-live.'),
    ('Support', 'Hypercare, maintenance and continuous improvement.'),
]

HOME_FAQ = [
    ('What Odoo services does Anitha Techsolutions provide?',
     'We provide Odoo implementation, customization and module development, migration and upgrades, integrations, hosting and performance tuning, reports, localization, training, and ongoing support — plus mobile apps connected to Odoo.'),
    ('Which Odoo versions do you work with?',
     'We work with Odoo 12 through Odoo 20, on both Community and Enterprise editions, hosted on Odoo.sh, cloud servers or on-premise.'),
    ('Can you build a mobile app that connects to our Odoo?',
     'Yes. We build Android and iOS apps with Flutter that read and write data in your Odoo in real time, with offline mode, push notifications, barcode scanning and GPS where needed.'),
    ('Can you migrate our existing Odoo to the latest version?',
     'Yes. We upgrade the database, port your custom modules to the new version, validate the data and run a test upgrade before the final switch.'),
    ('How do we start a project?',
     f'Email us at {EMAIL} or use the contact form with a short description of your needs. We will reply with next steps and, if needed, set up a discovery call.'),
]

POSTS = [
    {
        'slug': 'split-sale-order-odoo',
        'title': 'How to Split a Sale Order in Odoo 18, 19 and 20',
        'description': 'Step-by-step guide to splitting a quotation in Odoo by product quantity: move partial or full quantities to a new sale order while keeping prices and taxes.',
        'thumb': 'Split a Sale Order in Odoo',
        'date': '2026-11-10',
        'tags': ['Odoo Sales', 'Odoo Apps'],
        'body': f'''
<p>Customers often change their minds after a quotation is sent: part of the order is needed now, the rest next month; one branch takes some items, another takes the rest. Standard Odoo has no button to divide a quotation, so teams end up duplicating orders and editing quantities by hand — which is slow and easy to get wrong.</p>
<p>This guide shows how to split a sale order in Odoo 18, 19 and 20 in a few clicks using our <a href="../../odoo-apps/">Sale Order Split</a> app.</p>
<h2>What "splitting a sale order" means</h2>
<p>You choose how much of each product moves to a <strong>new quotation</strong>. The <strong>original quotation</strong> is reduced by the same amount. Unit price, discount and taxes stay the same on both orders, so the two totals add up exactly to the original total.</p>
<h2>Step 1: Open the split option</h2>
<p>Open the quotation and click <strong>Split Order</strong> in the header. From the quotation list, you can also select one quotation and choose <strong>Actions › Split Order</strong>.</p>
<img src="../../img/apps/split_action_menu.png" alt="Odoo quotation list with the Actions menu open showing the Split Order option" loading="lazy" width="1600" height="950">
<h2>Step 2: Enter the quantity to split</h2>
<p>A window lists every product on the order with its ordered quantity. Type the <strong>Qty to Split</strong> for each product you want to move. The remaining quantity and the amount being moved update as you type. Use <em>Move All Quantities</em> or <em>Reset</em> to fill or clear every line at once.</p>
<img src="../../img/apps/split_wizard.png" alt="Split Order window in Odoo with ordered quantity, quantity to split, remaining quantity and subtotal per product" loading="lazy" width="1600" height="950">
<h2>Step 3: Split and review both orders</h2>
<p>Click <strong>Split Order</strong>. The new quotation opens for the same customer. The original quotation keeps the remaining quantities, lines moved in full are removed, and a <strong>Split Orders</strong> smart button links the two. Both orders also get a note in the chatter.</p>
<img src="../../img/apps/split_original_order.png" alt="Original Odoo quotation after the split with reduced quantities and a Split Orders smart button" loading="lazy" width="1600" height="950">
<h2>Good to know</h2>
<ul>
<li>Only quotations (Quotation and Quotation Sent) can be split. This keeps deliveries and invoices consistent.</li>
<li>You cannot move more than the ordered quantity, and at least one line (or part of one) must stay on the original order.</li>
<li>Sections, notes and down payment lines stay on the original order.</li>
</ul>
<blockquote>Need to split confirmed orders, or split into more than two orders at once? We can customize the app for your workflow — <a href="../../contact/">get in touch</a>.</blockquote>
''',
    },
    {
        'slug': 'odoo-migration-checklist',
        'title': 'Odoo Migration Checklist: Upgrading to Odoo 19 or 20',
        'description': 'A practical checklist for upgrading Odoo to version 19 or 20: audit modules, port custom code, test the upgrade, validate data and plan the cutover.',
        'thumb': 'Odoo Migration Checklist',
        'date': '2026-11-10',
        'tags': ['Odoo Migration'],
        'body': '''
<p>Each new Odoo version brings real improvements, but an upgrade touches your data, your custom modules and your users' daily work. A clear checklist keeps the project predictable. Here is the one we follow.</p>
<h2>1. Audit what you have</h2>
<ul>
<li>List every installed module and mark each one as <em>standard</em>, <em>third-party</em> (Odoo Apps Store / OCA) or <em>custom</em>.</li>
<li>Uninstall modules nobody uses — every module you drop is one less to migrate.</li>
<li>Check whether each third-party module is available for the target version.</li>
</ul>
<h2>2. Upgrade the database on a copy</h2>
<p>Never upgrade production first. For Enterprise databases, Odoo's upgrade service converts the standard data; Community databases are usually upgraded with OpenUpgrade scripts. Either way, work on a recent copy of production.</p>
<h2>3. Port custom modules</h2>
<p>Custom code must be updated for the new framework. Typical changes in recent versions include:</p>
<ul>
<li><code>tree</code> views renamed to <code>list</code> (Odoo 18).</li>
<li><code>attrs</code> and <code>states</code> replaced by direct <code>invisible</code> / <code>readonly</code> expressions (Odoo 17).</li>
<li>Renamed fields, for example <code>product_uom</code> → <code>product_uom_id</code> and <code>tax_id</code> → <code>tax_ids</code> on sale order lines (Odoo 19).</li>
<li>Access rights moving to the new <code>ir.access</code> model (Odoo 20).</li>
</ul>
<p>Run each module's automated tests on the new version — they catch most porting mistakes early.</p>
<h2>4. Validate the data</h2>
<ul>
<li>Compare key figures before and after: trial balance, stock valuation, open receivables and payables.</li>
<li>Spot-check documents: a few invoices, deliveries and manufacturing orders of each type.</li>
<li>Check reports and email templates render correctly.</li>
</ul>
<h2>5. User acceptance testing</h2>
<p>Ask key users to run their daily tasks on the test database with a written checklist. Fix issues, then repeat the test upgrade from a fresh production copy.</p>
<h2>6. Plan the cutover</h2>
<ul>
<li>Agree a time window and freeze changes in the old system.</li>
<li>Take a full backup (database and filestore) and keep a rollback plan.</li>
<li>Run the final upgrade, smoke-test, then open the system to users.</li>
<li>Plan a few days of hypercare for questions and small fixes.</li>
</ul>
<blockquote>Planning an upgrade? We migrate databases and port custom modules from Odoo 12 onwards. <a href="../../contact/">Talk to us</a> about your project.</blockquote>
''',
    },
    {
        'slug': 'odoo-server-performance-tuning',
        'title': 'Odoo Performance Tuning: Workers, PostgreSQL and Nginx Basics',
        'description': 'Speed up a slow Odoo server: how to size Odoo workers and memory limits, tune PostgreSQL, and configure Nginx as a reverse proxy.',
        'thumb': 'Odoo Performance Tuning',
        'date': '2026-11-10',
        'tags': ['Odoo Hosting'],
        'body': '''
<p>A slow Odoo is rarely caused by one thing. Most of the gain comes from three places: the Odoo worker configuration, PostgreSQL settings and the reverse proxy. These are the basics we check on every server.</p>
<h2>1. Run Odoo in multi-worker mode</h2>
<p>By default Odoo runs in a single process. In production, set <code>workers</code> in the config file so requests are handled in parallel. A common starting point is <strong>(CPU cores × 2) + 1</strong>, then adjust to the available RAM.</p>
<ul>
<li><code>max_cron_threads</code>: usually 1–2, so scheduled jobs don't starve user requests.</li>
<li><code>limit_memory_soft</code> / <code>limit_memory_hard</code>: recycle a worker that grows too large instead of letting the server swap.</li>
<li><code>limit_time_cpu</code> / <code>limit_time_real</code>: stop runaway requests; raise them only for known heavy reports.</li>
<li><code>proxy_mode = True</code> when Odoo runs behind Nginx.</li>
</ul>
<h2>2. Tune PostgreSQL</h2>
<p>PostgreSQL's default settings are very conservative. Typical starting values on a dedicated server:</p>
<ul>
<li><code>shared_buffers</code> ≈ 25% of RAM.</li>
<li><code>effective_cache_size</code> ≈ 50–75% of RAM.</li>
<li><code>work_mem</code>: modest (for example 16–64 MB), because it applies per sort operation.</li>
<li><code>max_connections</code>: enough for all Odoo workers plus cron and maintenance — Odoo's <code>db_maxconn</code> should stay below it.</li>
</ul>
<p>Also make sure autovacuum is running and look at slow-query logs to find missing indexes in custom modules.</p>
<h2>3. Put Nginx in front of Odoo</h2>
<ul>
<li>Terminate SSL in Nginx and redirect HTTP to HTTPS.</li>
<li>Enable gzip for text assets and set long cache headers for static files.</li>
<li>Route <code>/websocket</code> (Odoo 16 and later) to the gevent port (8072 by default) with WebSocket upgrade headers.</li>
<li>Raise <code>client_max_body_size</code> if users upload large attachments.</li>
</ul>
<h2>4. Measure before and after</h2>
<p>Change one thing at a time and measure page load times, CPU, RAM and database load. Good tuning is about matching settings to your real usage, not copying numbers.</p>
<blockquote>Is your Odoo slow? We audit and tune Odoo, PostgreSQL and Nginx without disrupting your users. <a href="../../contact/">Request a server review</a>.</blockquote>
''',
    },
]

# ── Extra content (added in content pass) ───────────────────────────────────
SERVICE_DETAIL = {
    'odoo-implementation': ('Businesses moving to Odoo from spreadsheets, Tally, QuickBooks or another ERP.',
                            'One system for sales, stock, accounts and people — live in weeks, not years, with your team trained to use it.'),
    'odoo-customization': ('Companies whose processes go beyond what standard Odoo offers.',
                           'Odoo that fits the way you work, with code that stays easy to maintain and upgrade.'),
    'odoo-migration': ('Teams on an older Odoo version, or on Community and ready for Enterprise.',
                       'The latest Odoo features and security fixes, with your history and customizations carried over.'),
    'odoo-integration': ('Businesses that use Odoo next to online stores, payment providers, couriers or in-house software.',
                         'Data flows automatically between systems — no copy-paste, fewer errors, faster month-end.'),
    'odoo-consulting': ('Decision-makers planning a new Odoo project or rescuing one that has stalled.',
                        'A clear, realistic plan before you invest in development or licences.'),
    'odoo-support': ('Companies already live on Odoo that want a reliable team on call.',
                     'Issues fixed quickly, small changes handled, and Odoo kept healthy year after year.'),
    'odoo-hosting': ('Anyone running Odoo who wants it faster, safer and properly backed up.',
                     'Pages that load quickly, a hardened server and backups you can actually restore.'),
    'odoo-reports': ('Managers who need numbers and documents Odoo does not produce out of the box.',
                     'Branded documents and reports that answer your questions in one click.'),
    'odoo-localization': ('Companies that must comply with local tax and invoicing rules.',
                          'Correct taxes, compliant invoices and tax reports ready for filing.'),
    'odoo-website-ecommerce': ('Businesses that want their website and online shop connected to stock and accounting.',
                               'Online orders flow straight into Odoo — stock, invoicing and delivery stay in sync.'),
    'odoo-training': ('Teams going live on Odoo, new joiners, and admins who manage the system.',
                      'Confident users, fewer support questions and better use of what you paid for.'),
    'odoo-apps': ('Odoo users who need a specific feature quickly and affordably.',
                  'A tested, maintained app in minutes instead of a custom project.'),
}

ODOO_APPS = [
    ('sales', 'Sales', 'Quotations, orders and pricelists'), ('crm', 'CRM', 'Leads, pipeline and follow-ups'),
    ('purchase', 'Purchase', 'RFQs, vendor bills and approvals'), ('inventory', 'Inventory', 'Warehouses, barcode, routes and valuation'),
    ('accounting', 'Accounting', 'Invoicing, payments, bank and tax reports'), ('manufacturing', 'Manufacturing', 'BoMs, work orders, quality and maintenance'),
    ('pos', 'Point of Sale', 'Shops, restaurants and offline POS'), ('employees', 'Employees & HR', 'Employees, attendance and leave'),
    ('payroll', 'Payroll', 'Salary structures and payslips'), ('project', 'Project', 'Tasks, timesheets and billing'),
    ('website', 'Website', 'Drag-and-drop website builder'), ('ecommerce', 'eCommerce', 'Online shop connected to stock'),
    ('helpdesk', 'Helpdesk', 'Tickets, SLAs and customer support'), ('field-service', 'Field Service', 'On-site jobs, routes and worksheets'),
    ('fleet', 'Fleet', 'Vehicles, contracts and costs'),
]

INDUSTRY_DESC = {
    'Trading & Distribution': 'Multi-warehouse stock, pricelists, van sales and fast invoicing.',
    'Manufacturing': 'Bills of materials, work orders, MRP planning and costing.',
    'Retail & POS': 'Connected shops, POS, loyalty and central stock control.',
    'Healthcare & Clinics': 'Appointments, patient records, pharmacy stock and billing.',
    'Construction & Projects': 'Project costing, subcontracting, materials and progress billing.',
    'Professional Services': 'Timesheets, project billing, contracts and resource planning.',
    'Education': 'Admissions, fees, courses and staff management.',
    'Logistics': 'Fleet, deliveries, routes and proof of delivery.',
}

ENGAGEMENT = [
    ('target', 'Fixed-scope project', 'Best for implementations, migrations and defined features. Agreed scope, timeline and price up front.'),
    ('users', 'Dedicated developer', 'Best for ongoing development. A developer works on your roadmap by the hour, week or month.'),
    ('support', 'Support plan (AMC)', 'Best after go-live. A monthly or yearly plan for fixes, small changes and updates.'),
]

TECH = [('odoo', 'Odoo 12 → 20'), ('python', 'Python'), ('postgresql', 'PostgreSQL'), ('javascript', 'JavaScript / OWL'),
        ('flutter', 'Flutter'), ('dart', 'Dart'), ('docker', 'Docker'), ('nginx', 'Nginx'), ('ubuntu', 'Ubuntu Linux'),
        ('digitalocean', 'Cloud servers'), ('git', 'Git'), ('githubactions', 'CI / CD')]
MOBILE_TECH = [('flutter', 'Flutter'), ('dart', 'Dart'), ('odoo', 'Odoo JSON-2 API'), ('sqlite', 'SQLite offline storage'),
               ('firebase', 'Firebase push notifications'), ('android', 'Android'), ('apple', 'iOS'),
               ('googleplay', 'Google Play'), ('appstore', 'App Store')]

HOME_FAQ += [
    ('Should we choose Odoo Community or Enterprise?',
     'Community is free and covers core apps such as Sales, Inventory, Invoicing and Manufacturing. Enterprise adds apps like full Accounting, Studio, Helpdesk and Field Service, plus the official upgrade service. We help you choose based on the apps you actually need.'),
    ('Can you take over an Odoo system built by another partner?',
     'Yes. We review the existing setup and custom modules, fix what is broken, document it and continue development and support from there.'),
    ('Do you provide support after go-live?',
     'Yes. Every project includes a hypercare period after go-live, and you can continue with a monthly or yearly support plan.'),
]

SERVICES_FAQ = [
    ('How long does an Odoo implementation take?',
     'It depends on the number of apps, users, integrations and custom features. A focused rollout of a few core apps can go live in weeks; larger multi-company projects run in phases. We give you a timeline after the discovery step.'),
    ('How much does Odoo customization cost?',
     'Customization is estimated per requirement. After a short discussion we share a written estimate with scope and effort, so you know the cost before any work starts.'),
    ('Will customizations break when we upgrade Odoo?',
     'We build custom modules as separate add-ons that follow Odoo and OCA standards, without changing Odoo core. That keeps upgrades manageable — and we port the modules for you when you upgrade.'),
    ('Can you work on our Odoo.sh or on-premise server?',
     'Yes. We work on Odoo.sh, Odoo Online (configuration only), cloud servers and on-premise installations.'),
]

MOBILE_FAQ = [
    ('Do you build separate apps for Android and iOS?',
     'No — we use Flutter, so one codebase produces both the Android and iOS app. That keeps cost and maintenance lower while the apps still feel native.'),
    ('How does the app connect to Odoo?',
     "Through Odoo's external APIs over HTTPS, using the user's own Odoo access rights. For Odoo 19 and later we use the new JSON-2 API with API keys."),
    ('Will the app work without internet?',
     'Yes, if needed. Data is stored securely on the device, the user keeps working, and changes sync to Odoo automatically when the connection returns.'),
    ('Can you publish the app to Google Play and the App Store?',
     'Yes. We prepare the store listings and handle submission, or set up private distribution if the app is only for your staff.'),
]

APP_FAQ = [
    ('Which Odoo versions does Sale Order Split support?',
     'Odoo 18, 19 and 20, on both Community and Enterprise editions.'),
    ('Can I split a confirmed sales order?',
     'The app splits quotations (Quotation and Quotation Sent) so deliveries and invoices stay consistent. We can extend it for confirmed orders as a customization.'),
    ('Do you help with installation?',
     f'Yes. If you need help installing or configuring the app, email {EMAIL}.'),
]

POSTS += [
    {
        'slug': 'odoo-community-vs-enterprise',
        'title': 'Odoo Community vs Enterprise: Which Edition Is Right for You?',
        'description': 'Compare Odoo Community and Enterprise: which apps each includes, hosting and upgrade differences, and how to choose the right edition for your business.',
        'thumb': 'Community vs Enterprise',
        'date': '2026-11-10',
        'tags': ['Odoo Basics'],
        'body': '''
<p>Odoo comes in two editions: <strong>Community</strong>, which is open source and free to use, and <strong>Enterprise</strong>, which is licensed per user and adds more apps and services. Both share the same core, so you can start with one and move to the other later. Here is how to decide.</p>
<h2>What both editions include</h2>
<p>Community already covers a lot of day-to-day business: Sales and CRM, Purchase, Inventory, Invoicing, Manufacturing, Point of Sale, Project, Website and eCommerce, Employees and more. Many small and mid-sized companies run entirely on Community, extended with custom modules or apps from the Odoo Apps Store.</p>
<h2>What Enterprise adds</h2>
<ul>
<li><strong>Full Accounting</strong> — bank synchronization, reconciliation tools and financial reports, beyond Community's invoicing.</li>
<li><strong>Extra apps</strong> such as Studio (no-code customization), Helpdesk, Field Service, Planning, Sign, Documents and Knowledge.</li>
<li><strong>Official upgrade service</strong> for moving your database to new versions.</li>
<li><strong>Odoo.sh and Odoo Online</strong> hosting options, plus Odoo's official mobile app and support.</li>
</ul>
<h2>Hosting and upgrades</h2>
<p>Community can be hosted anywhere — your own server or any cloud — and upgraded with community tools such as OpenUpgrade. Enterprise can also be hosted on-premise, or on Odoo's own platforms (Odoo Online and Odoo.sh), and its upgrades are handled by Odoo's upgrade service.</p>
<h2>How to choose</h2>
<ul>
<li><strong>Choose Community</strong> if the core apps cover your needs, you want to avoid per-user licences, and you are comfortable owning hosting and upgrades with a partner.</li>
<li><strong>Choose Enterprise</strong> if you need full accounting, Studio or the Enterprise-only apps, or you prefer Odoo to handle hosting and upgrades.</li>
</ul>
<p>The best approach is to list the processes you need to run, map each to an Odoo app, and see which edition covers them. Custom development can sometimes fill a gap more cheaply than licences — and sometimes the opposite is true.</p>
<blockquote>Not sure which edition fits? We map your processes to Odoo apps and recommend the right edition before you buy. <a href="../../contact/">Ask us</a>.</blockquote>
''',
    },
    {
        'slug': 'odoo-mobile-app-flutter',
        'title': 'Planning a Mobile App for Odoo: A Practical Guide',
        'description': 'What to plan before building a mobile app for Odoo: users and use cases, Odoo APIs (including the JSON-2 API), offline sync, security and app store publishing.',
        'thumb': 'Mobile Apps for Odoo',
        'date': '2026-11-10',
        'tags': ['Mobile Apps', 'Odoo Integration'],
        'body': '''
<p>Odoo works in any mobile browser, but staff in the field — sales reps, drivers, technicians, warehouse pickers — often need something faster and simpler: big buttons, barcode scanning, offline mode. A dedicated mobile app connected to Odoo gives them exactly that. Here is what to plan before you build one.</p>
<h2>1. Start with the user and the job</h2>
<p>A good business app does a few jobs very well. Write down who will use it, where (in a van, a shop, a warehouse), and the three to five tasks they do most — for example "take an order", "collect a payment", "confirm a delivery". Everything else can stay in Odoo's web interface.</p>
<h2>2. Decide how the app talks to Odoo</h2>
<p>Mobile apps connect to Odoo through its external API over HTTPS. Odoo 19 introduced a new <strong>JSON-2 API</strong> (<code>/json/2/&lt;model&gt;/&lt;method&gt;</code>) authenticated with API keys. The older XML-RPC and JSON-RPC endpoints are deprecated in Odoo 19 and scheduled for removal in Odoo 22, so new apps for recent versions should use JSON-2. For heavier workflows, a small custom Odoo module with dedicated endpoints keeps the app fast and the business logic on the server.</p>
<h2>3. Plan for offline use</h2>
<p>If users work where signal is weak, the app should store data on the device, queue changes, and sync when the connection returns. Decide early what happens when two people edit the same record — usually the server wins and the user is told.</p>
<h2>4. Respect Odoo security</h2>
<ul>
<li>Each user signs in with their own Odoo account, so Odoo's access rights and record rules still apply.</li>
<li>Use HTTPS only, and store tokens in the phone's secure storage.</li>
<li>Give each device its own API key so a lost phone can be revoked without affecting others.</li>
</ul>
<h2>5. Choose the technology</h2>
<p>Cross-platform frameworks like <strong>Flutter</strong> build Android and iOS apps from one codebase, which keeps development and maintenance costs down. Native features such as camera, barcode scanning, GPS and push notifications are all available.</p>
<h2>6. Publishing and maintenance</h2>
<p>Public apps go through Google Play and Apple App Store review; internal apps can be distributed privately. Budget for updates: new phone OS versions and new Odoo versions both need small adjustments over time.</p>
<blockquote>Planning an app for your Odoo users? We design, build and publish Flutter apps connected to Odoo. <a href="../../mobile-app-development/">See our mobile app services</a>.</blockquote>
''',
    },
]


def faq_block(items):
    return '<div class="faq">' + ''.join(f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'


def faq_ld(items):
    return ld({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]})


def engagement_html():
    return ''.join(f'<article class="card reveal d{i % 3}" data-tilt><div class="icon {"navy" if i == 1 else ""}">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></article>'
                   for i, (ic, t, d) in enumerate(ENGAGEMENT))


def tech_html(items=None, r=''):
    return '<div class="logos reveal">' + ''.join(
        f'<span class="logo-pill"><img src="{r}img/tech/{slug}.svg" alt="{name} logo" width="28" height="28" loading="lazy">{name}</span>'
        for slug, name in (items or TECH)) + '</div>'


def odoo_apps_html():
    return ''.join(f'<div class="app-tile reveal d{i % 3}"><img src="img/odoo/{ic}.svg" alt="Odoo {n} app icon" width="48" height="48" loading="lazy"><div><b>{n}</b><span>{d}</span></div></div>'
                   for i, (ic, n, d) in enumerate(ODOO_APPS))


# ── Templates ───────────────────────────────────────────────────────────────
NAV = [('', 'Home'), ('odoo-services/', 'Odoo Services'), ('mobile-app-development/', 'Mobile Apps'),
       ('odoo-apps/', 'Odoo Apps'), ('about/', 'About'), ('blog/', 'Blog')]


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


ORG = {
    '@context': 'https://schema.org', '@type': 'Organization', '@id': f'{SITE_URL}/#organization',
    'name': BRAND, 'legalName': LEGAL, 'url': f'{SITE_URL}/', 'email': EMAIL,
    'logo': f'{SITE_URL}/img/logo/01_primary.png', 'description': f'{BRAND} is an {TAGLINE.lower()}.',
    'contactPoint': [{'@type': 'ContactPoint', 'email': EMAIL, 'contactType': 'customer support', 'availableLanguage': ['English']}],
    'knowsAbout': ['Odoo ERP', 'Odoo implementation', 'Odoo customization', 'Odoo migration', 'Flutter mobile app development'],
}


def breadcrumb(items):
    return ld({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': f'{SITE_URL}/{p}'} for i, (p, n) in enumerate(items)]})


def page(path, title, description, body, *, schema='', current='', og_image='img/og-image.png', three=False, og_type='website'):
    depth = path.count('/')
    r = '../' * depth                       # relative prefix back to site root
    url = f'{SITE_URL}/{path}'
    cur = ' aria-current="page"'
    nav = ''.join(f'<a href="{r}{p}"{cur if p == current else ""}>{n}</a>' for p, n in NAV)
    full_title = title if (BRAND in title or len(title) + len(BRAND) + 3 > 65) else f'{title} | {BRAND}'
    scripts = ''
    if three:
        scripts += '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js" defer></script>\n'
        scripts += f'<script src="{r}js/hero3d.js" defer></script>\n'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="{BRAND}">
<meta name="theme-color" content="#0E1B33">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/{og_image}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(full_title)}">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="{SITE_URL}/{og_image}">
<link rel="icon" href="{r}img/favicon/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{r}img/favicon/favicon-32.png">
<link rel="apple-touch-icon" href="{r}img/favicon/favicon-180.png">
<link rel="manifest" href="{r}manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Anitha">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/style.css">
{ld(ORG)}
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container bar">
    <a class="brand" href="{r}" aria-label="{BRAND} home">
      <img class="logo-light" src="{r}img/logo/logo-reversed.svg" alt="{BRAND}" width="226" height="100">
      <img class="logo-dark" src="{r}img/logo/logo-primary.svg" alt="{BRAND}" width="226" height="100">
    </a>
    <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">{icon('menu')}</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {nav}
      <a class="btn" href="{r}contact/">Get a Quote</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container">
    <div class="cols">
      <div>
        <img class="logo" src="{r}img/logo/logo-reversed.svg" alt="{BRAND}" width="226" height="100" loading="lazy">
        <p>{TAGLINE}. We implement, customize, migrate and support Odoo, and build mobile apps that connect to it.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h4>Odoo Services</h4>
        <ul>
          <li><a href="{r}odoo-services/#odoo-implementation">Implementation</a></li>
          <li><a href="{r}odoo-services/#odoo-customization">Customization</a></li>
          <li><a href="{r}odoo-services/#odoo-migration">Migration &amp; Upgrade</a></li>
          <li><a href="{r}odoo-services/#odoo-integration">Integration</a></li>
          <li><a href="{r}odoo-services/#odoo-hosting">Hosting &amp; Tuning</a></li>
          <li><a href="{r}odoo-services/#odoo-support">Support &amp; AMC</a></li>
        </ul>
      </div>
      <div>
        <h4>Solutions</h4>
        <ul>
          <li><a href="{r}mobile-app-development/">Odoo Mobile Apps</a></li>
          <li><a href="{r}odoo-apps/">Odoo Apps Store Modules</a></li>
          <li><a href="{r}odoo-services/#odoo-website-ecommerce">Website &amp; eCommerce</a></li>
          <li><a href="{r}odoo-services/#odoo-reports">Reports &amp; Dashboards</a></li>
          <li><a href="{r}odoo-services/#odoo-training">Training</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="{r}about/">About Us</a></li>
          <li><a href="{r}blog/">Blog</a></li>
          <li><a href="{r}contact/">Contact</a></li>
          <li><a href="{r}sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
    </div>
    <div class="bottom">
      <span>&copy; <span data-year>{date.today().year}</span> {LEGAL} All rights reserved.</span>
      <span>Odoo is a trademark of Odoo S.A. {BRAND} is an independent service provider.</span>
    </div>
  </div>
</footer>
<div class="install" id="install-bar" hidden role="dialog" aria-label="Install app">
  <img src="{r}img/favicon/favicon-192.png" alt="" width="44" height="44">
  <div><b>Install the {BRAND} app</b><small>Quick access from your home screen</small></div>
  <button class="btn" type="button">Install</button>
  <button class="x" type="button" aria-label="Dismiss">&times;</button>
</div>
<script src="{r}js/main.js" defer></script>
{scripts}</body>
</html>
'''


def page_hero(crumbs, title, text, r):
    trail = ' / '.join([f'<a href="{r}">Home</a>'] + [escape(c) for c in crumbs])
    return f'''<section class="page-hero"><div class="container">
  <div class="crumbs">{trail}</div>
  <h1>{title}</h1>
  <p>{text}</p>
</div></section>'''


def cta(r, title='Ready to get more out of Odoo?', text='Tell us what you need — implementation, customization, migration or a mobile app. We reply within one business day.'):
    return f'''<section><div class="container"><div class="cta reveal">
  <img class="mark" src="{r}img/logo/09_mark_white_knockout.svg" alt="" loading="lazy">
  <div><h2>{title}</h2><p>{text}</p></div>
  <a class="btn" href="{r}contact/">Start your project {icon('arrow')}</a>
</div></div></section>'''


def service_cards(r, limit=None):
    out = []
    for i, (sid, ic, title, short, _) in enumerate(SERVICES[:limit] if limit else SERVICES):
        cls = 'navy' if i % 3 == 1 else ('gold' if sid == 'odoo-apps' else '')
        out.append(f'''<article class="card reveal d{i % 3}" data-tilt>
  <div class="icon {cls}">{icon(ic)}</div>
  <h3>{title}</h3><p>{short}</p>
  <a class="more" href="{r}odoo-services/#{sid}">Learn more &rarr;</a>
</article>''')
    return '\n'.join(out)


def phones():
    return '''<div class="phone-stage" aria-hidden="true">
  <div class="phone back"><div class="screen"><div class="notch"></div>
    <div class="top"><small>Today</small><b>Deliveries</b></div>
    <div class="rows" style="padding-top:14px">
      <div class="row">WH/OUT/0142 <em class="ok">Done</em></div>
      <div class="row">WH/OUT/0143 <em>Ready</em></div>
      <div class="row">WH/OUT/0144 <em>Ready</em></div>
      <div class="row">WH/OUT/0145 <em>Waiting</em></div>
      <div class="row">WH/OUT/0146 <em>Waiting</em></div>
    </div><div class="fab">&#9638;</div></div></div>
  <div class="phone"><div class="screen"><div class="notch"></div>
    <div class="top"><small>Good morning</small><b>Field Sales</b></div>
    <div class="kpis"><div class="kpi">Orders<b>18</b></div><div class="kpi">Collected<b>4.2k</b></div>
      <div class="kpi">Visits<b>9/12</b></div><div class="kpi">Van stock<b>86%</b></div></div>
    <div class="rows">
      <div class="row">S00231 · Retail Mart <em class="ok">Paid</em></div>
      <div class="row">S00232 · City Foods <em>Draft</em></div>
      <div class="row">S00233 · Green Store <em class="ok">Paid</em></div>
    </div><div class="fab">+</div></div></div>
</div>
<p class="illustrative">Illustrative app screens</p>'''


# ── Pages ───────────────────────────────────────────────────────────────────
def build_home():
    r = ''
    newcls = ' class="new"'
    hero_apps = json.dumps([{'src': f'img/odoo/{ic}.svg', 'label': lab} for ic, lab in [
        ('sales', 'Sales'), ('crm', 'CRM'), ('inventory', 'Inventory'), ('accounting', 'Accounting'), ('manufacturing', 'Manufacturing'),
        ('pos', 'POS'), ('employees', 'Employees'), ('website', 'Website')]] + [{'src': 'img/logo/10_app_icon.svg', 'label': 'Mobile App'}])
    versions_html = ''.join(f'<span{newcls if v >= 19 else ""}>Odoo {v}</span>' for v in range(12, 21))
    body = f'''
<section class="hero">
  <canvas id="hero3d" aria-hidden="true" data-apps='{hero_apps}'></canvas>
  <div class="container">
    <div>
      <div class="eyebrow">Odoo ERP &amp; Mobile Apps</div>
      <h1><span class="line">Many systems.</span> <span class="line accent">One platform.</span></h1>
      <p class="typed-line">Built for your <span class="typed" data-words="sales team|warehouse|finance team|field staff|managers|customers">sales team</span></p>
      <p class="lead">Sales, inventory, accounting, manufacturing, HR and your field teams — connected on Odoo. {BRAND} implements, customizes, migrates and supports Odoo ERP, and builds the Android and iOS apps that take it on the road.</p>
      <div class="actions">
        <a class="btn" href="contact/">Get a free consultation {icon('arrow')}</a>
        <a class="btn btn-ghost" href="odoo-services/">Explore services</a>
      </div>
      <div class="hero-badges"><span>Odoo 12 → 20</span><span>Community &amp; Enterprise</span><span>Android &amp; iOS apps</span></div>
    </div>
    <div class="hero-orbit" aria-hidden="true">
    </div>
  </div>
  <div class="scroll-hint">Scroll</div>
</section>

<section class="alt">
  <div class="container">
    <div class="section-head reveal"><div class="eyebrow">What we do</div>
      <h2>Complete Odoo services under one roof</h2>
      <p>Whether you are new to Odoo, outgrowing your current setup or stuck on an old version, we cover every step — from the first workshop to years of support.</p></div>
    <div class="grid g3">{service_cards(r, 9)}</div>
    <p style="text-align:center;margin-top:36px"><a class="btn btn-outline" href="odoo-services/">View all Odoo services {icon('arrow')}</a></p>
  </div>
</section>

<section>
  <div class="container split">
    <div class="reveal">
      <div class="eyebrow">Mobile App Development</div>
      <h2>Your Odoo, in your team's pocket</h2>
      <p>We build Android and iOS apps with Flutter that work directly with your Odoo — so sales reps, drivers, warehouse staff and employees can work from anywhere, even offline.</p>
      <ul class="ticks">
        <li>Van sales, field sales and delivery apps</li>
        <li>Warehouse and barcode scanning apps</li>
        <li>Employee self-service: attendance, leave, payslips</li>
        <li>Offline sync, push notifications and GPS</li>
      </ul>
      <a class="btn" href="mobile-app-development/">Mobile app services {icon('arrow')}</a>
    </div>
    <div class="reveal d1">{phones()}</div>
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="section-head reveal"><div class="eyebrow">Odoo apps</div><h2>The Odoo apps we implement</h2>
      <p>Start with the apps you need today and add more as you grow — they all share one database, so information is entered once and used everywhere.</p></div>
    <div class="app-tiles">{odoo_apps_html()}</div>
  </div>
</section>

<section class="dark">
  <div class="container">
    <div class="section-head reveal"><div class="eyebrow">How we work</div><h2>A clear, proven process</h2>
      <p>Every project follows the same five steps, so you always know what happens next.</p></div>
    <div class="steps">{''.join(f'<div class="step reveal d{i % 3}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PROCESS))}</div>
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="section-head reveal"><div class="eyebrow">Versions</div><h2>Every Odoo version, Community &amp; Enterprise</h2>
      <p>New implementation or a system that has been running for years — we work with the version you have.</p></div>
    <div class="versions reveal">{versions_html}</div>
    <div class="section-head reveal" style="margin:64px auto 28px"><div class="eyebrow">Technology</div><h2 style="font-size:1.6rem">Our technology stack</h2></div>
    {tech_html()}
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head reveal"><div class="eyebrow">Why {BRAND}</div><h2>A partner that stays with you</h2></div>
    <div class="grid g3">{''.join(f'<article class="card reveal d{i % 3}" data-tilt><div class="icon {"navy" if i % 2 else ""}">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate(WHY))}</div>
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="section-head reveal"><div class="eyebrow">Industries</div><h2>Odoo solutions for your industry</h2>
      <p>Odoo adapts to almost any business. These are some of the industries we configure it for.</p></div>
    <div class="grid g4">{''.join(f'<div class="card reveal d{i % 3}" data-tilt style="text-align:center;padding:26px"><div class="icon" style="margin:0 auto">{icon(ic)}</div><h3 style="font-size:1.02rem">{t}</h3><p style="font-size:.9rem">{INDUSTRY_DESC[t]}</p></div>' for i, (ic, t) in enumerate(INDUSTRIES))}</div>
  </div>
</section>

<section class="dark">
  <div class="container">
    <div class="section-head reveal"><div class="eyebrow">Engagement models</div><h2>Work with us the way that suits you</h2>
      <p>Choose a model for each stage of your project — and switch as your needs change.</p></div>
    <div class="grid g3">{engagement_html()}</div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head reveal"><div class="eyebrow">Our Odoo Apps</div><h2>Ready-made apps for the Odoo Apps Store</h2></div>
    <article class="card app-card reveal" data-tilt>
      <div class="media"><img src="img/apps/sale-order-split-banner.gif" alt="Sale Order Split app for Odoo: enter quantities, create a new quotation, keep the rest on the original" loading="lazy" width="1200" height="600"></div>
      <div class="body">
        <span class="badge">Odoo 18</span><span class="badge">Odoo 19</span><span class="badge">Odoo 20</span><span class="badge gold">Community &amp; Enterprise</span>
        <h3 style="font-size:1.5rem">Sale Order Split</h3>
        <p>Split a quotation into two orders by product quantity. Prices, discounts and taxes are kept, and both orders stay linked.</p>
        <div class="price">$9 <small>one-time</small></div>
        <p style="margin-top:18px"><a class="btn" href="odoo-apps/">See app details {icon('arrow')}</a></p>
      </div>
    </article>
  </div>
</section>

<section class="alt">
  <div class="container">
    <div class="section-head reveal"><div class="eyebrow">FAQ</div><h2>Frequently asked questions</h2></div>
    {faq_block(HOME_FAQ)}
  </div>
</section>
{cta(r)}
'''
    schema = ld({'@context': 'https://schema.org', '@type': 'WebSite', 'name': BRAND, 'url': f'{SITE_URL}/', 'publisher': {'@id': f'{SITE_URL}/#organization'}})
    schema += faq_ld(HOME_FAQ)
    return page('', f'Odoo ERP & Mobile App Development Company | {BRAND}',
                'Odoo implementation, customization, migration, integration, hosting and support for Odoo 12 to 20 — plus Android & iOS mobile apps connected to Odoo.',
                body, schema=schema, current='', three=True)


def build_services():
    r = '../'
    nav = ''.join(f'<a href="#{sid}">{t.replace("Odoo ", "", 1) if t.startswith("Odoo ") else t}</a>' for sid, _, t, _, _ in SERVICES)
    blocks = ''.join(f'''<div class="service-block" id="{sid}">
  <div class="reveal"><div class="icon {"navy" if i % 2 else ""}">{icon(ic)}</div>
    <div class="tag" style="margin-top:18px">Service {i + 1:02d}</div><h2 style="font-size:1.7rem">{t}</h2><p>{short}</p>
    <p class="who"><b>Who it's for:</b> {SERVICE_DETAIL[sid][0]}</p>
    <a class="btn btn-outline" href="{r}contact/">Discuss this service</a></div>
  <div class="reveal d1"><h3>What's included</h3><ul class="ticks">{''.join(f"<li>{x}</li>" for x in items)}</ul>
    <div class="outcome"><b>The result</b>{SERVICE_DETAIL[sid][1]}</div></div>
</div>''' for i, (sid, ic, t, short, items) in enumerate(SERVICES))
    body = page_hero(['Odoo Services'], 'Odoo services for every stage of your ERP journey',
                     'Implementation, customization, migration, integration, hosting, reports, localization, training and support — for Odoo 12 to 20, Community and Enterprise.', r) + f'''
<section style="padding-bottom:20px"><div class="container"><div class="service-nav reveal">{nav}<a href="{r}mobile-app-development/">Mobile Apps</a></div></div></section>
<section style="padding-top:20px"><div class="container">{blocks}</div></section>
<section class="dark"><div class="container">
  <div class="section-head reveal"><div class="eyebrow">Engagement models</div><h2>Flexible ways to work together</h2>
    <p>Start with a fixed-scope project, add a dedicated developer when you need more capacity, and keep a support plan after go-live.</p></div>
  <div class="grid g3">{engagement_html()}</div>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head reveal"><div class="eyebrow">FAQ</div><h2>Questions about our Odoo services</h2></div>
  {faq_block(SERVICES_FAQ)}
</div></section>
{cta(r)}'''
    schema = breadcrumb([('', 'Home'), ('odoo-services/', 'Odoo Services')])
    schema += faq_ld(SERVICES_FAQ)
    schema += ld({'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'Service', 'name': t, 'description': short, 'serviceType': t,
                                                         'url': f'{SITE_URL}/odoo-services/#{sid}', 'provider': {'@id': f'{SITE_URL}/#organization'}}}
        for i, (sid, _, t, short, _) in enumerate(SERVICES)]})
    return page('odoo-services/', 'Odoo Services: Implementation, Migration & Support',
                'Full-cycle Odoo services: implementation, custom modules, migration to Odoo 19/20, integrations, hosting, tuning, reports, training and AMC support.',
                body, schema=schema, current='odoo-services/')


def build_mobile():
    r = '../'
    body = page_hero(['Mobile Apps'], 'Mobile app development connected to Odoo',
                     'Android and iOS apps built with Flutter that work directly with your Odoo — for sales, delivery, warehouse, employees and customers.', r) + f'''
<section><div class="container split">
  <div class="reveal"><div class="eyebrow">Odoo Mobile Apps</div><h2>Take Odoo wherever your team works</h2>
    <p>Odoo's web interface is great at a desk. In a van, a warehouse aisle or a customer's shop, your team needs something faster and simpler. We design focused mobile apps for those jobs and connect them securely to your Odoo, so every order, delivery and payment lands in the ERP instantly.</p>
    <ul class="ticks"><li>Native-feeling apps for Android and iOS from one Flutter codebase</li><li>Works with Odoo 12 to 20, Community and Enterprise</li>
      <li>Published to Google Play and the App Store — or distributed privately</li><li>Maintenance and updates for new OS and Odoo versions</li></ul>
    <a class="btn" href="{r}contact/">Discuss your app {icon('arrow')}</a></div>
  <div class="reveal d1">{phones()}</div>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head reveal"><div class="eyebrow">Use cases</div><h2>Apps we build for Odoo users</h2></div>
  <div class="grid g3">{''.join(f'<article class="card reveal d{i % 3}" data-tilt><div class="icon {"navy" if i % 2 else ""}">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate(MOBILE_USECASES))}</div>
</div></section>
<section class="dark"><div class="container">
  <div class="section-head reveal"><div class="eyebrow">Features</div><h2>Built for real field conditions</h2></div>
  <div class="grid g3">{''.join(f'<article class="card reveal d{i % 3}"><div class="icon">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate(MOBILE_FEATURES))}</div>
</div></section>
<section><div class="container">
  <div class="section-head reveal"><div class="eyebrow">Process</div><h2>From idea to app store</h2></div>
  <div class="grid g4">{''.join(f'<article class="card reveal d{i % 3}"><div class="icon {"navy" if i % 2 else ""}">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate([
        ('compass', 'Discovery', 'Who uses the app, where, and which Odoo data they need.'),
        ('layers', 'UX design', 'Simple screens designed for one-handed, on-the-go use.'),
        ('code', 'Development', 'Flutter app, Odoo API endpoints and offline sync.'),
        ('rocket', 'Launch & support', 'Store publishing, rollout to users and ongoing updates.')]))}</div>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head reveal"><div class="eyebrow">Technology</div><h2>How we build Odoo mobile apps</h2>
    <p>Flutter for the app, Odoo's secure APIs for the data, and a small Odoo module when a workflow needs its own endpoints.</p></div>
  {tech_html(MOBILE_TECH, r)}
</div></section>
<section><div class="container">
  <div class="section-head reveal"><div class="eyebrow">FAQ</div><h2>Mobile app questions</h2></div>
  {faq_block(MOBILE_FAQ)}
</div></section>
{cta(r, 'Have an app idea for your Odoo?', 'Tell us who will use it and what they need to do. We will suggest the simplest app that gets the job done.')}'''
    schema = breadcrumb([('', 'Home'), ('mobile-app-development/', 'Mobile Apps')])
    schema += ld({'@context': 'https://schema.org', '@type': 'Service', 'name': 'Odoo Mobile App Development', 'serviceType': 'Mobile application development',
                  'description': 'Android and iOS apps built with Flutter and connected to Odoo ERP.', 'provider': {'@id': f'{SITE_URL}/#organization'},
                  'url': f'{SITE_URL}/mobile-app-development/'})
    schema += faq_ld(MOBILE_FAQ)
    return page('mobile-app-development/', 'Odoo Mobile App Development for Android & iOS',
                'Android and iOS apps connected to Odoo: van sales, delivery, warehouse barcode and employee self-service apps with offline mode and push notifications.',
                body, schema=schema, current='mobile-app-development/')


def build_apps():
    r = '../'
    buy = (f'<a class="btn" href="{APP_STORE_URL}" rel="noopener">View on Odoo Apps Store {icon("arrow")}</a>' if APP_STORE_URL
           else f'<a class="btn" href="mailto:{EMAIL}?subject=Sale%20Order%20Split%20app">Ask about this app {icon("arrow")}</a>')
    body = page_hero(['Odoo Apps'], 'Odoo Apps Store modules by ' + BRAND,
                     'Small, focused Odoo apps that close common gaps quickly — maintained for the latest Odoo versions.', r) + f'''
<section><div class="container">
  <article class="card app-card reveal">
    <div class="media"><img src="{r}img/apps/sale-order-split-banner.gif" alt="Sale Order Split for Odoo animated preview" loading="lazy" width="1200" height="600"></div>
    <div class="body">
      <span class="badge">Odoo 18</span><span class="badge">Odoo 19</span><span class="badge">Odoo 20</span><span class="badge gold">Community &amp; Enterprise</span>
      <h2 style="font-size:1.8rem;margin-top:10px">Sale Order Split</h2>
      <p>Split a quotation into two orders by product quantity. Choose how much of each product moves to a new quotation; the original is reduced automatically and both orders stay linked.</p>
      <ul class="ticks"><li>Full or partial quantity per product</li><li>Prices, discounts and taxes kept on both orders</li>
        <li>Split Orders smart button, Split From link and chatter log</li><li>Validation against over-splitting and empty orders</li></ul>
      <div class="price">$9 <small>one-time · technical name ats_sale_order_split</small></div>
      <p style="margin-top:18px">{buy}</p>
    </div>
  </article>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head reveal"><div class="eyebrow">Screenshots</div><h2>See it in action</h2><p>Read the step-by-step guide: <a href="{r}blog/split-sale-order-odoo/">How to split a sale order in Odoo</a>.</p></div>
  <div class="grid g2">
    <img class="reveal" src="{r}img/apps/split_wizard.png" alt="Split Order window with quantity to split per product" loading="lazy" width="1600" height="950" style="border-radius:14px;box-shadow:var(--shadow-lg)">
    <img class="reveal d1" src="{r}img/apps/split_original_order.png" alt="Original quotation after splitting with Split Orders smart button" loading="lazy" width="1600" height="950" style="border-radius:14px;box-shadow:var(--shadow-lg)">
  </div>
</div></section>
<section><div class="container">
  <div class="section-head reveal"><div class="eyebrow">Special offer</div><h2>Buy an app, get customization at a special rate</h2>
    <p>Purchase any of our Odoo apps and get up to 60 hours of customization for just $3/hr instead of $20/hr. <a href="mailto:{EMAIL}?subject=App%20customization%20offer">Email us</a> with your order details to claim it.</p></div>
  <img class="reveal" src="{r}img/apps/special-offer.gif" alt="Special offer: purchase our app and get 60 hours of customization for just $3 per hour instead of $20" loading="lazy" width="1000" height="167" style="margin:0 auto;border-radius:14px;box-shadow:var(--shadow-lg)">
</div></section>
<section class="alt"><div class="container">
  <div class="section-head reveal"><div class="eyebrow">FAQ</div><h2>App questions</h2></div>
  {faq_block(APP_FAQ)}
</div></section>
{cta(r, 'Need a custom Odoo app?', 'We build apps for your own workflow, or publish them on the Odoo Apps Store for you.')}'''
    schema = breadcrumb([('', 'Home'), ('odoo-apps/', 'Odoo Apps')])
    schema += faq_ld(APP_FAQ)
    schema += ld({'@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'Sale Order Split for Odoo', 'applicationCategory': 'BusinessApplication',
                  'operatingSystem': 'Odoo 18, Odoo 19, Odoo 20', 'description': 'Split an Odoo quotation into two sale orders by product quantity.',
                  'image': f'{SITE_URL}/img/apps/sale-order-split-banner.gif', 'author': {'@id': f'{SITE_URL}/#organization'},
                  'offers': {'@type': 'Offer', 'price': '9.00', 'priceCurrency': 'USD'}})
    return page('odoo-apps/', 'Sale Order Split App for Odoo 18, 19 & 20',
                'Sale Order Split for Odoo 18, 19 and 20: split a quotation into two orders by product quantity while keeping prices and taxes. $9 one-time.',
                body, schema=schema, current='odoo-apps/', og_image='img/apps/split_wizard.png')


def build_about():
    r = '../'
    body = page_hero(['About'], f'About {BRAND}',
                     'An Odoo ERP and mobile app development company that helps businesses run on one connected platform.', r) + f'''
<section><div class="container split">
  <div class="reveal"><div class="eyebrow">Who we are</div><h2>Many systems, integrating into one platform</h2>
    <p>{LEGAL} helps businesses replace scattered spreadsheets and disconnected software with Odoo — one platform for sales, inventory, accounting, manufacturing, HR and more — and extends it to the field with mobile apps.</p>
    <p>Our logo says it best: two planes meeting at the apex. Many systems integrating into one platform, with an upward interior for growth. Deep navy for trust; signal blue for technology.</p></div>
  <div class="reveal d1" style="text-align:center"><img src="{r}img/logo/01_primary.svg" alt="{BRAND} logo" width="519" height="300" loading="lazy" style="margin:0 auto;width:100%;max-width:440px"></div>
</div></section>
<section class="dark"><div class="container">
  <div class="grid g2">
    <article class="card reveal"><div class="icon">{icon('target')}</div><h3>Our mission</h3><p>Help growing businesses run on one connected platform — so every team works from the same accurate data, in the office and in the field.</p></article>
    <article class="card reveal d1"><div class="icon gold">{icon('rocket')}</div><h3>Our vision</h3><p>To be the partner companies trust for Odoo and the mobile apps around it: simple to work with, honest about cost, and there for the long run.</p></article>
  </div>
</div></section>
<section><div class="container split">
  <div class="reveal"><div class="eyebrow">Our approach</div><h2>Standard first, custom only where it counts</h2>
    <p>Odoo already does a great deal out of the box. We start by configuring standard features, then add apps from the Odoo ecosystem, and write custom code only for what truly makes your business different.</p>
    <p>That keeps projects faster and cheaper, and it keeps your Odoo easy to upgrade for years to come.</p></div>
  <div class="reveal d1"><ul class="ticks">
    <li><b>Configure</b> — use standard Odoo features wherever they fit</li>
    <li><b>Extend</b> — add proven apps from the Odoo Apps Store and OCA</li>
    <li><b>Customize</b> — build clean custom modules for the real gaps</li>
    <li><b>Connect</b> — integrate other systems and add mobile apps</li>
    <li><b>Support</b> — stay with you after go-live</li></ul></div>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head reveal"><div class="eyebrow">What we stand for</div><h2>Our values</h2></div>
  <div class="grid g3">{''.join(f'<article class="card reveal d{i % 3}" data-tilt><div class="icon {"navy" if i % 2 else ""}">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate([
        ('target', 'Business first', 'We start from your processes and goals, not from features.'),
        ('code', 'Quality you can upgrade', 'Standard, tested code that keeps your Odoo easy to upgrade.'),
        ('users', 'Honest partnership', 'Clear estimates, open communication and no surprises.'),
        ('shield', 'Long-term thinking', 'Decisions that still make sense after your next upgrade.'),
        ('layers', 'Simplicity', 'The simplest solution that works — for users and for maintenance.'),
        ('support', 'Responsiveness', 'Quick, clear answers when you need help.')]))}</div>
</div></section>
<section><div class="container">
  <div class="section-head reveal"><div class="eyebrow">Capabilities</div><h2>What we bring to your project</h2></div>
  <div class="grid g2">
    <div class="card reveal"><h3 style="margin-top:0">Odoo ERP</h3><ul class="ticks"><li>Implementation and configuration</li><li>Custom module development</li><li>Migration from Odoo 12 to 20</li><li>Integrations and APIs</li><li>Hosting, tuning and support</li></ul></div>
    <div class="card reveal d1"><h3 style="margin-top:0">Mobile apps</h3><ul class="ticks"><li>Flutter apps for Android and iOS</li><li>Real-time Odoo connection</li><li>Offline sync and push notifications</li><li>Barcode, camera and GPS features</li><li>Store publishing and maintenance</li></ul></div>
  </div>
</div></section>
{cta(r)}'''
    schema = breadcrumb([('', 'Home'), ('about/', 'About')])
    schema += ld({'@context': 'https://schema.org', '@type': 'AboutPage', 'name': f'About {BRAND}', 'url': f'{SITE_URL}/about/', 'mainEntity': {'@id': f'{SITE_URL}/#organization'}})
    return page('about/', f'About Us | {BRAND}',
                f'{LEGAL} is an Odoo ERP and mobile app development company helping businesses run on one connected platform.',
                body, schema=schema, current='about/')


def build_blog_index():
    r = '../'
    cards = ''.join(f'''<article class="card post-card reveal d{i % 3}" data-tilt>
  <a class="thumb" href="{p["slug"]}/" tabindex="-1" aria-hidden="true"><span>{p["thumb"]}</span></a>
  <div class="content"><div class="meta">{date.fromisoformat(p["date"]).strftime("%d %b %Y")} · {", ".join(p["tags"])}</div>
    <h3><a href="{p["slug"]}/">{p["title"]}</a></h3><p>{p["description"]}</p>
    <a class="more" href="{p["slug"]}/">Read article &rarr;</a></div>
</article>''' for i, p in enumerate(POSTS))
    body = page_hero(['Blog'], 'Odoo insights &amp; guides', 'Practical articles on Odoo implementation, migration, hosting, apps and mobile.', r) + f'''
<section><div class="container"><div class="grid g3">{cards}</div></div></section>{cta(r)}'''
    schema = breadcrumb([('', 'Home'), ('blog/', 'Blog')])
    schema += ld({'@context': 'https://schema.org', '@type': 'Blog', 'name': f'{BRAND} Blog', 'url': f'{SITE_URL}/blog/',
                  'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': f'{SITE_URL}/blog/{p["slug"]}/', 'datePublished': p['date']} for p in POSTS]})
    return page('blog/', 'Odoo Blog: Guides & Insights',
                'Odoo guides and insights from Anitha Techsolutions: sale order split, migration checklist for Odoo 19/20, server performance tuning and more.',
                body, schema=schema, current='blog/')


def build_post(p):
    r = '../../'
    others = ''.join(f'<li><a href="../{o["slug"]}/">{o["title"]}</a></li>' for o in POSTS if o is not p)
    body = f'''<section class="page-hero"><div class="container">
  <div class="crumbs"><a href="{r}">Home</a> / <a href="../">Blog</a> / {escape(p["title"])}</div>
  <h1>{p["title"]}</h1>
  <p>{date.fromisoformat(p["date"]).strftime("%d %B %Y")} · {BRAND} Team · {", ".join(p["tags"])}</p>
</div></section>
<section><div class="container"><article class="article">{p["body"]}
  <hr style="border:0;border-top:1px solid var(--line);margin:48px 0 24px"><h3>More articles</h3><ul>{others}</ul>
</article></div></section>{cta(r)}'''
    schema = breadcrumb([('', 'Home'), ('blog/', 'Blog'), (f'blog/{p["slug"]}/', p['title'])])
    schema += ld({'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'description': p['description'],
                  'datePublished': p['date'], 'dateModified': UPDATED, 'author': {'@type': 'Organization', 'name': BRAND},
                  'publisher': {'@id': f'{SITE_URL}/#organization'}, 'mainEntityOfPage': f'{SITE_URL}/blog/{p["slug"]}/',
                  'image': f'{SITE_URL}/img/og-image.png', 'keywords': ', '.join(p['tags'])})
    return page(f'blog/{p["slug"]}/', p['title'], p['description'], body, schema=schema, current='blog/', og_type='article')


def build_contact():
    r = '../'
    opts = ''.join(f'<option>{t}</option>' for _, _, t, _, _ in SERVICES) + '<option>Mobile App Development</option><option>Something else</option>'
    body = page_hero(['Contact'], "Let's talk about your project",
                     'Tell us about your business and what you need. We reply within one business day.', r) + f'''
<section><div class="container contact-grid">
  <div class="reveal">
    <h2 style="font-size:1.8rem">Get in touch</h2>
    <p>Whether it is a new Odoo implementation, a migration, a custom module or a mobile app — we are happy to help.</p>
    <div class="contact-item"><div class="icon">{icon('mail')}</div><div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
    <div class="contact-item"><div class="icon navy">{icon('clock')}</div><div><b>Response time</b>Within one business day</div></div>
    <div class="contact-item"><div class="icon">{icon('globe')}</div><div><b>Working with clients</b>Remote projects worldwide</div></div>
    <h3 style="margin-top:32px">Helpful to include</h3>
    <ul class="ticks"><li>Your industry and number of users</li><li>Current system or Odoo version and edition</li>
      <li>The processes or features you need</li><li>Your preferred timeline</li></ul>
  </div>
  <div class="card reveal d1">
    <form class="form" id="contact-form" data-to="{EMAIL}">
      <div class="two"><label>Name<input name="name" required autocomplete="name"></label><label>Email<input name="email" type="email" required autocomplete="email"></label></div>
      <div class="two"><label>Company<input name="company" autocomplete="organization"></label><label>Phone<input name="phone" type="tel" autocomplete="tel"></label></div>
      <label>Service<select name="service">{opts}</select></label>
      <label>Message<textarea name="message" required placeholder="Tell us about your project, Odoo version and timeline"></textarea></label>
      <button class="btn" type="submit" style="justify-self:start">Send message {icon('arrow')}</button>
      <p class="note">Sending opens your email app with the message filled in, addressed to {EMAIL}.</p>
      <p class="note" id="form-done" hidden>Your email app should now be open. If it isn't, email us directly at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </form>
  </div>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head reveal"><div class="eyebrow">What happens next</div><h2>From first message to project start</h2></div>
  <div class="grid g3">{''.join(f'<article class="card reveal d{i % 3}"><div class="icon {"navy" if i == 1 else ""}">{icon(ic)}</div><h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate([
        ('mail', '1. We reply', 'Within one business day, with any questions we need answered.'),
        ('users', '2. Discovery call', 'A short call to understand your processes, systems and goals.'),
        ('target', '3. Proposal', 'A written scope, timeline and estimate — so you can decide with confidence.')]))}</div>
</div></section>'''
    schema = breadcrumb([('', 'Home'), ('contact/', 'Contact')])
    schema += ld({'@context': 'https://schema.org', '@type': 'ContactPage', 'name': f'Contact {BRAND}', 'url': f'{SITE_URL}/contact/'})
    return page('contact/', f'Contact Us | {BRAND}',
                f'Contact {BRAND} for Odoo implementation, customization, migration, support or mobile app development. Email {EMAIL}.',
                body, schema=schema, current='contact/')


def build_404():
    body = f'''<section class="page-hero" style="min-height:70vh;display:flex;align-items:center"><div class="container">
  <h1>Page not found</h1><p>The page you are looking for has moved or does not exist.</p>
  <p style="margin-top:24px"><a class="btn" href="/">Back to home</a></p></div></section>'''
    return page('404.html', 'Page not found', 'This page could not be found.', body).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')


# ── Build ───────────────────────────────────────────────────────────────────
def write(path, html):
    target = OUT / (path if path.endswith('.html') else path + 'index.html')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding='utf-8')
    return target


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)
    pages = {
        '': build_home(), 'odoo-services/': build_services(), 'mobile-app-development/': build_mobile(),
        'odoo-apps/': build_apps(), 'about/': build_about(), 'blog/': build_blog_index(), 'contact/': build_contact(),
    }
    for p in POSTS:
        pages[f'blog/{p["slug"]}/'] = build_post(p)
    for path, html in pages.items():
        write(path, html)
    write('404.html', build_404())

    prio = {'': '1.0', 'odoo-services/': '0.9', 'mobile-app-development/': '0.9', 'odoo-apps/': '0.8', 'contact/': '0.8'}
    urls = ''.join(f'  <url><loc>{SITE_URL}/{p}</loc><lastmod>{UPDATED}</lastmod><priority>{prio.get(p, "0.7")}</priority></url>\n' for p in pages)
    (OUT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    (OUT / 'manifest.webmanifest').write_text(json.dumps({
        'name': BRAND, 'short_name': 'Anitha', 'description': TAGLINE, 'start_url': '/', 'scope': '/', 'display': 'standalone',
        'background_color': '#0E1B33', 'theme_color': '#0E1B33',
        'icons': [{'src': '/img/favicon/favicon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                  {'src': '/img/favicon/favicon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                  {'src': '/img/favicon/favicon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}],
    }, indent=2))
    core = ['/', '/css/style.css', '/js/main.js', '/img/logo/logo-reversed.svg', '/img/logo/logo-primary.svg', '/offline.html']
    (OUT / 'sw.js').write_text(f'''// Service worker: makes the site installable and readable offline.
const CACHE = 'anitha-{UPDATED}';
const CORE = {json.dumps(core)};
self.addEventListener('install', e => {{ e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); }});
self.addEventListener('activate', e => {{ e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); }});
self.addEventListener('fetch', e => {{
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  if (req.mode === 'navigate') {{
    e.respondWith(fetch(req).then(res => {{ const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res; }})
      .catch(() => caches.match(req).then(r => r || caches.match('/offline.html'))));
    return;
  }}
  e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => {{ const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res; }})));
}});
''')
    offline = page('offline.html', 'Offline', 'You are offline.', '''<section class="page-hero" style="min-height:70vh;display:flex;align-items:center"><div class="container">
  <h1>You're offline</h1><p>Check your connection and try again. Pages you visited before are still available.</p></div></section>''')
    write('offline.html', offline.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">'))
    (OUT / '.nojekyll').write_text('')   # GitHub Pages: serve files as-is, skip Jekyll
    print(f'Built {len(pages) + 2} pages into {OUT}')
    if 'your-domain.com' in SITE_URL:
        print('NOTE: SITE_URL is still a placeholder — set your real domain in build.py before publishing.')


if __name__ == '__main__':
    main()
