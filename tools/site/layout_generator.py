#!/usr/bin/env python3
"""Generate varied layout configurations for site rendering."""

import random
from dataclasses import dataclass
from typing import Dict, List


LAYOUT_TYPES = [
    "classic-grid",
    "split-hero",
    "magazine",
    "timeline",
    "feature-stack",
    "dual-column",
    "masonry",
]

SIDEBAR_POSITIONS = ["left", "right", "none"]


@dataclass
class LayoutConfig:
    layout_type: str
    sidebar_position: str
    footer_columns: int
    grid_columns: int
    hero_variant: str
    sidebar_widgets: int

    def to_dict(self) -> Dict:
        return {
            "layout_type": self.layout_type,
            "sidebar_position": self.sidebar_position,
            "footer_columns": self.footer_columns,
            "grid_columns": self.grid_columns,
            "hero_variant": self.hero_variant,
            "sidebar_widgets": self.sidebar_widgets,
        }


class LayoutGenerator:
    def generar_configuracion_layout(self, seed: int | None = None) -> Dict:
        rng = random.Random(seed)
        layout = rng.choice(LAYOUT_TYPES)
        sidebar = rng.choice(SIDEBAR_POSITIONS)
        footer_columns = rng.choice([3, 4])
        grid_columns = rng.choice([2, 3])
        hero_variant = rng.choice(["image-left", "image-right", "full-bleed"])
        sidebar_widgets = rng.choice([2, 3, 4])
        return LayoutConfig(
            layout_type=layout,
            sidebar_position=sidebar,
            footer_columns=footer_columns,
            grid_columns=grid_columns,
            hero_variant=hero_variant,
            sidebar_widgets=sidebar_widgets,
        ).to_dict()

    def generar_distribucion_noticias(self, total: int, seed: int | None = None) -> Dict:
        rng = random.Random(seed)
        featured = 1
        main = rng.choice([4, 5, 6])
        sidebar = rng.choice([3, 4]) if total > 6 else 2
        return {"featured": featured, "main": main, "sidebar": sidebar}

    def randomizar_categorias(self, categorias: List[str], seed: int | None = None) -> List[str]:
        rng = random.Random(seed)
        categorias = list(categorias)
        rng.shuffle(categorias)
        return categorias

    def generar_clases_css_dinamicas(self, layout_config: Dict) -> Dict:
        """
        Genera clases CSS dinámicas basadas en la configuración del layout.

        Args:
            layout_config: Diccionario con configuración del layout

        Returns:
            Dict con las clases CSS para container, main, footer, etc.
        """
        layout_type = layout_config.get("layout_type", "classic-grid")
        sidebar_pos = layout_config.get("sidebar_position", "right")
        
        # Clases base
        container_class = "container"
        main_class = "main-content"
        footer_class = "footer"
        
        # Modificadores según layout
        if layout_type == "magazine":
            container_class += " layout-magazine"
        elif layout_type == "timeline":
            container_class += " layout-timeline"
        elif layout_type == "masonry":
            container_class += " layout-masonry"
        elif layout_type == "dual-column":
            container_class += " layout-dual-column"
        elif layout_type == "feature-stack":
            container_class += " layout-feature-stack"
        elif layout_type == "split-hero":
            container_class += " layout-split-hero"
        
        # Modificadores de sidebar
        if sidebar_pos == "left":
            main_class += " sidebar-left"
        elif sidebar_pos == "right":
            main_class += " sidebar-right"
        else:
            main_class += " no-sidebar"
        
        return {
            "container": container_class,
            "main": main_class,
            "footer": footer_class,
            "sidebar": "sidebar sidebar-" + sidebar_pos if sidebar_pos != "none" else "sidebar-hidden"
        }

    def generar_estilos_widget_sidebar(self) -> List[Dict]:
        """
        Genera configuraciones de widgets para el sidebar.

        Returns:
            List of widget configurations
        """
        widgets = [
            {"type": "popular", "title": "Más leídas", "count": 5},
            {"type": "categories", "title": "Categorías", "count": 8},
            {"type": "newsletter", "title": "Boletín", "description": "Suscríbete para recibir noticias"},
            {"type": "social", "title": "Síguenos", "networks": ["facebook", "twitter", "instagram"]}
        ]
        return widgets


class HTMLLayoutBuilder:
    def __init__(self, layout_config: Dict):
        self.layout = layout_config

    def build_header(self, site_config: Dict, categorias: List[str]) -> str:
        title = site_config.get("title", "Noticias")
        tagline = site_config.get("tagline", "")
        logo_path = site_config.get("logo_path")
        if logo_path:
            logo_block = (
                f"<div class=\"logo-image\">"
                f"<img src=\"{logo_path}\" alt=\"Logo {title}\" class=\"logo-img\">"
                f"<div class=\"logo-text\"><h1>{title}</h1><p class=\"tagline\">{tagline}</p></div>"
                f"</div>"
            )
        else:
            logo_block = f"<div class=\"logo\"><h1>{title}</h1><p class=\"tagline\">{tagline}</p></div>"

        links = []
        for cat in categorias:
            # Slug sin tildes
            slug = cat.lower()
            slug = slug.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            slug = slug.replace(" ", "-")
            links.append(f"<a href=\"categoria-{slug}.html\" class=\"nav-link\">{cat}</a>")

        return (
            "<header class=\"header\">"
            "<div class=\"container\">"
            f"{logo_block}"
            "<nav class=\"nav\">"
            f"{''.join(links)}"
            "</nav>"
            "<div class=\"header-actions\">"
            "<input type=\"search\" placeholder=\"Buscar noticias...\" class=\"search-input\">"
            "<button class=\"btn-subscribe\">Suscribirse</button>"
            "</div>"
            "</div>"
            "</header>\n"
        )

    def build_featured_section(self, featured_news):
        if not featured_news:
            return ""
        hero_class = f"hero hero-{self.layout['hero_variant']}"
        items = []
        for item in featured_news:
            title = item.get("title", "")
            description = item.get("description", "")
            image = item.get("ai_image_path") or item.get("image") or "assets/images/fallback-1.svg"
            items.append(
                f"<article class=\"featured-item\">"
                f"<img src=\"{image}\" alt=\"{title}\">"
                f"<div class=\"featured-content\"><h2>{title}</h2><p>{description}</p></div>"
                f"</article>"
            )
        return f"<section class=\"{hero_class}\">{''.join(items)}</section>\n"

    def build_news_grid(self, main_news, distribucion):
        cols = self.layout["grid_columns"]
        items = []
        for item in main_news:
            title = item.get("title", "")
            description = item.get("description", "")
            image = item.get("ai_image_path") or item.get("image") or "assets/images/fallback-2.svg"
            items.append(
                f"<article class=\"news-card\">"
                f"<img src=\"{image}\" alt=\"{title}\">"
                f"<div class=\"news-card-content\"><h3>{title}</h3><p>{description}</p></div>"
                f"</article>"
            )
        return (
            f"<section class=\"news-grid columns-{cols}\">"
            f"{''.join(items)}"
            f"</section>\n"
        )

    def build_sidebar(self, sidebar_news, widgets):
        if self.layout["sidebar_position"] == "none":
            return ""
        items = []
        for item in sidebar_news:
            title = item.get("title", "")
            items.append(f"<li><a href=\"#\">{title}</a></li>")
        return (
            "<aside class=\"sidebar\">"
            f"<section class=\"sidebar-widget\"><h4>Más leídas</h4><ul>{''.join(items)}</ul></section>"
            "</aside>\n"
        )
