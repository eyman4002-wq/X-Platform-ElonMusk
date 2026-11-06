from pathlib import Path
import html
import json
import subprocess
import sys

root = Path(".")
index = root / "index.html"

if not index.exists():
    sys.exit("ERROR: index.html غير موجود")

source = index.read_text(encoding="utf-8")

apps = {
    "cyber": ("00e5ff", "CYBER", "shield"),
    "netcore": ("00ff9d", "NETCORE", "network"),
    "rescue": ("ff9b42", "PHONE RESCUE", "phone"),
    "wificore": ("9d75ff", "NETWORK BRAIN", "wifi"),
    "noc": ("00c8ff", "NETWORK NOC", "monitor"),
    "netmgmt": ("45e0a5", "NETWORK MGMT", "server"),
    "wifixv2": ("42bfff", "WIFI CONTROL", "wifi"),
    "globalrescue": ("ff6b83", "GLOBAL RESCUE", "lifebuoy"),
    "guardian": ("65e0ff", "MOBILE GUARDIAN", "shield"),
    "lifelink": ("d18cff", "LIFE LINK", "link"),
    "nexus": ("ffbd59", "SAMI NEXUS", "network"),
    "gwifi": ("55e6c1", "G WIFI", "wifi"),
    "stylematch": ("ff82c5", "STYLE MATCH", "style"),
    "viruses": ("b7e36a", "PHONE VIRUSES", "security"),
    "printer": ("a4b5ff", "UNIVERSAL PRINT", "printer"),
    "guard": ("4de0b5", "PHONE GUARD", "shield"),
    "magicwall": ("d18aff", "MAGIC WALL", "magic"),
    "clockwall": ("ffc66d", "CLOCK WALL", "clock"),
}

icons = {
    "shield": '<path d="M100 35 L145 53 V91 Q140 128 100 151 Q60 128 55 91 V53 Z" fill="none" stroke="url(#g)" stroke-width="9"/><path d="M77 91 L94 108 L126 73" fill="none" stroke="url(#g)" stroke-width="9" stroke-linecap="round"/>',
    "network": '<g fill="none" stroke="url(#g)" stroke-width="7"><circle cx="100" cy="65" r="18"/><circle cx="58" cy="130" r="15"/><circle cx="142" cy="130" r="15"/><path d="M90 82 L67 115 M110 82 L133 115 M73 130 H127"/></g>',
    "phone": '<rect x="69" y="32" width="62" height="125" rx="13" fill="none" stroke="url(#g)" stroke-width="8"/><path d="M84 48 H116 M94 140 H106" stroke="url(#g)" stroke-width="5" stroke-linecap="round"/><path d="M100 76 L88 99 H101 L94 120 L117 91 H103 Z" fill="url(#g)"/>',
    "wifi": '<g fill="none" stroke="url(#g)" stroke-width="9" stroke-linecap="round"><path d="M42 77 Q100 22 158 77"/><path d="M60 99 Q100 62 140 99"/><path d="M79 120 Q100 102 121 120"/></g><circle cx="100" cy="145" r="8" fill="url(#g)"/>',
    "monitor": '<rect x="37" y="42" width="126" height="87" rx="9" fill="none" stroke="url(#g)" stroke-width="8"/><path d="M100 129 V151 M73 151 H127 M57 105 L82 84 L101 99 L143 65" fill="none" stroke="url(#g)" stroke-width="7" stroke-linecap="round"/>',
    "server": '<g fill="none" stroke="url(#g)" stroke-width="7"><rect x="48" y="35" width="104" height="42" rx="8"/><rect x="48" y="91" width="104" height="42" rx="8"/><path d="M66 55 H68 M66 111 H68 M84 55 H133 M84 111 H133"/></g>',
    "lifebuoy": '<circle cx="100" cy="96" r="57" fill="none" stroke="url(#g)" stroke-width="18"/><path d="M60 56 L79 75 M121 117 L140 136 M140 56 L121 75 M79 117 L60 136" stroke="#fff" stroke-width="13"/>',
    "link": '<g fill="none" stroke="url(#g)" stroke-width="12" stroke-linecap="round"><path d="M83 113 L65 131 Q44 148 28 131 Q11 113 29 95 L61 63 Q78 46 95 63"/><path d="M117 79 L135 61 Q156 44 173 61 Q190 79 172 97 L140 129 Q123 146 106 129"/><path d="M71 102 L129 84"/></g>',
    "security": '<circle cx="100" cy="96" r="58" fill="none" stroke="url(#g)" stroke-width="8"/><path d="M100 55 V137 M59 96 H141 M71 67 L129 125 M129 67 L71 125" stroke="url(#g)" stroke-width="6"/>',
    "style": '<path d="M69 48 L100 34 L131 48 L153 74 L133 89 L121 75 V150 H79 V75 L67 89 L47 74 Z" fill="none" stroke="url(#g)" stroke-width="8" stroke-linejoin="round"/><path d="M88 41 L100 58 L112 41" fill="none" stroke="url(#g)" stroke-width="5"/>',
    "printer": '<g fill="none" stroke="url(#g)" stroke-width="8"><path d="M63 64 V37 H137 V64"/><rect x="39" y="65" width="122" height="62" rx="10"/><path d="M63 108 H137 V154 H63 Z"/><circle cx="139" cy="84" r="5" fill="url(#g)"/></g>',
    "magic": '<path d="M100 29 L112 76 L158 94 L112 109 L100 157 L87 109 L42 94 L87 76 Z" fill="none" stroke="url(#g)" stroke-width="8"/><path d="M151 28 L157 48 L177 54 L157 60 L151 80 L145 60 L125 54 L145 48 Z" fill="url(#g)"/>',
    "clock": '<circle cx="100" cy="96" r="61" fill="none" stroke="url(#g)" stroke-width="8"/><path d="M100 51 V96 L132 115" fill="none" stroke="url(#g)" stroke-width="9" stroke-linecap="round"/>'
}

folder = root / "assets" / "app-images"
folder.mkdir(parents=True, exist_ok=True)

for app_id, (color, title, icon) in apps.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#101d35"/>
  <stop offset="1" stop-color="#080b15"/>
 </linearGradient>
 <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#{color}"/>
  <stop offset="1" stop-color="#ffffff"/>
 </linearGradient>
 <filter id="glow">
  <feGaussianBlur stdDeviation="5" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
 </filter>
</defs>
<rect width="200" height="200" rx="25" fill="url(#bg)"/>
<circle cx="100" cy="88" r="70" fill="#{color}" opacity=".09"/>
<circle cx="100" cy="88" r="59" fill="none" stroke="#{color}" opacity=".20" stroke-width="1.5"/>
<g filter="url(#glow)">{icons[icon]}</g>
<path d="M25 166 H175" stroke="#{color}" opacity=".35"/>
<text x="100" y="185" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="#ffffff">{html.escape(title)}</text>
</svg>'''
    (folder / f"{app_id}.svg").write_text(svg, encoding="utf-8")

# Add image styles once
css = """
        .app-art {
            display:block;
            width:100%;
            height:190px;
            object-fit:contain;
            border-radius:13px;
            margin:0 auto 18px;
            background:linear-gradient(135deg,#101b2d,#090d17);
            border:1px solid #2f4054;
            transition:transform .25s ease, border-color .25s ease;
        }
        .card:hover .app-art {
            transform:scale(1.025);
            border-color:#00ba7c;
        }
        @media(max-width:480px) {
            .app-art { height:170px; }
            .card { padding:1rem; }
        }
"""

if ".app-art" not in source:
    source = source.replace("    </style>", css + "\n    </style>", 1)

old = '''                card.innerHTML = `
                    <div class="card-header">'''

new = '''                card.innerHTML = `
                    <img class="app-art"
                         src="assets/app-images/${item.id}.svg"
                         alt="${data.name}"
                         loading="lazy"
                         onerror="this.style.display='none'">
                    <div class="card-header">'''

if old in source:
    source = source.replace(old, new, 1)
elif 'assets/app-images/${item.id}.svg' not in source:
    sys.exit("لم أستطع تحديد مكان بطاقات التطبيقات. لم يتم تعديل الصفحة.")

index.write_text(source, encoding="utf-8")

print("تم إنشاء صور التطبيقات:")
print("عدد الصور:", len(apps))
print("المجلد:", folder)
print("تم تحديث index.html")
