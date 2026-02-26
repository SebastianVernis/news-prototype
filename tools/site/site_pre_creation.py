#!/usr/bin/env python3
"""
SitePreCreation - Module for creating site metadata before HTML generation.
Handles batch creation of site configurations with varied properties.
"""

import json
import random
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# Site name patterns for generating varied sites
SITE_PREFIXES = [
    "El Diario", "Noticias", "El Informador", "Crónica", "Reporte",
    "El Observador", "Noticias Express", "El Noticiero", "Diario Digital",
    "La Prensa", "El Universal", "El Heraldo", "La Gaceta", "El Periódico"
]

SITE_SUFFIXES = [
    "Nacional", "al Momento", "Actual", "Directo", "Hoy",
    "24/7", "En Línea", "Digital", "MX", "Latino",
    "Global", "Regional", "Local", "Urbano", "Metropolitano"
]

# Taglines
TAGLINES = [
    "La Verdad en Cada Historia",
    "Tu Fuente de Información Confiable",
    "Noticias que Importan",
    "Mantente Informado",
    "Las Noticias más Recientes",
    "Periodismo de Calidad",
    "Rápido, Preciso, Confiable",
    "Información al Instante",
    "Noticias 24/7",
    "Tu Conexión con el Mundo",
    "Comprometidos con la Verdad",
    "El Pulso de la Nación"
]

# Domain patterns
DOMAIN_TLDS = ["com", "com.mx", "mx", "news", "media", "info"]


class SitePreCreation:
    """
    Handles pre-creation of site metadata for batch site generation.
    """

    def __init__(self, output_dir: Optional[Path | str] = None):
        """
        Initialize the SitePreCreation module.

        Args:
            output_dir: Directory to store metadata files. Defaults to NEWS_METADATA_DIR env var or ./data/sites_metadata
        """
        if output_dir is None:
            self.output_dir = Path("./data/sites_metadata")
        elif isinstance(output_dir, str):
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = output_dir

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rng = random.Random()

    def _slugify(self, value: str) -> str:
        """Convert a string to a URL-friendly slug."""
        value = (value or "").strip().lower()
        value = re.sub(r"[^a-z0-9]+", "-", value)
        value = value.strip("-")
        return value or "site"

    def _generate_domain(self, name: str) -> str:
        """Generate a domain name based on the site name."""
        slug = self._slugify(name).replace("-", "")
        tld = self.rng.choice(DOMAIN_TLDS)
        return f"www.{slug}.{tld}"

    def generar_configuracion_sitio(self, seed: Optional[int] = None) -> Dict:
        """
        Generate a random site configuration.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Dict with site configuration
        """
        if seed is not None:
            self.rng = random.Random(seed)

        prefix = self.rng.choice(SITE_PREFIXES)
        suffix = self.rng.choice(SITE_SUFFIXES)
        name = f"{prefix} {suffix}"

        return {
            "nombre": name,
            "name": name,
            "title": name,
            "tagline": self.rng.choice(TAGLINES),
            "dominio": self._generate_domain(name),
            "domain": self._generate_domain(name),
            "created_at": datetime.now().isoformat(),
            "template_id": self.rng.randint(1, 20),
            "categories": self._generate_categories(),
            "layout_config": self._generate_layout_config()
        }

    def _generate_categories(self) -> List[str]:
        """Generate a list of categories for the site."""
        all_categories = [
            "Inicio", "Política", "Tecnología", "Deportes",
            "Entretenimiento", "Mundial", "Negocios", "Cultura",
            "Economía", "Salud", "Ciencia", "Opinión"
        ]
        num_categories = self.rng.randint(5, 8)
        return self.rng.sample(all_categories, num_categories)

    def _generate_layout_config(self) -> Dict:
        """Generate layout configuration for the site."""
        return {
            "layout_type": self.rng.choice([
                "classic-grid", "split-hero", "magazine",
                "timeline", "feature-stack", "dual-column", "masonry"
            ]),
            "sidebar_position": self.rng.choice(["left", "right", "none"]),
            "footer_columns": self.rng.choice([3, 4]),
            "grid_columns": self.rng.choice([2, 3]),
            "hero_variant": self.rng.choice(["image-left", "image-right", "full-bleed"]),
            "sidebar_widgets": self.rng.choice([2, 3, 4])
        }

    def crear_sitio(self, seed: Optional[int] = None,
                    verificar_dominios: bool = False) -> Dict:
        """
        Create a single site configuration.

        Args:
            seed: Optional random seed
            verificar_dominios: Whether to check domain uniqueness

        Returns:
            Dict with complete site configuration
        """
        config = self.generar_configuracion_sitio(seed)
        config["id"] = self._slugify(config["nombre"])
        config["output_dir"] = config["id"]
        config["logo_path"] = "logo.png"
        return config

    def crear_batch_sitios(self, cantidad: int = 10,
                           verificar_dominios: bool = False,
                           guardar_archivo: bool = True,
                           seed: Optional[int] = None) -> List[Dict]:
        """
        Create a batch of site configurations.

        Args:
            cantidad: Number of sites to create
            verificar_dominios: Whether to verify domain uniqueness
            guardar_archivo: Whether to save to a JSON file
            seed: Optional random seed for reproducibility

        Returns:
            List of site configuration dicts
        """
        if seed is not None:
            self.rng = random.Random(seed)

        sitios = []
        dominios_usados = set()

        for i in range(cantidad):
            intentos = 0
            max_intentos = 10

            while intentos < max_intentos:
                config = self.crear_sitio(seed=i)

                # Check domain uniqueness if requested
                if verificar_dominios:
                    if config["domain"] not in dominios_usados:
                        dominios_usados.add(config["domain"])
                        break
                    intentos += 1
                else:
                    # Add small variation to ensure uniqueness
                    if i > 0:
                        config["id"] = f"{config['id']}-{i}"
                        config["output_dir"] = config["id"]
                    sitios.append(config)
                    break

            if intentos >= max_intentos:
                # Force uniqueness
                config["id"] = f"{config['id']}-{i + 1}"
                config["output_dir"] = config["id"]
                config["dominio"] = f"site{i + 1}.{self.rng.choice(DOMAIN_TLDS)}"
                config["domain"] = config["dominio"]

            sitios.append(config)

        # Save to file if requested
        if guardar_archivo:
            self._guardar_metadatos(sitios)

        return sitios

    def _guardar_metadatos(self, sitios: List[Dict]) -> Path:
        """
        Save site metadata to a JSON file.

        Args:
            sitios: List of site configurations

        Returns:
            Path to the saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sites_metadata_{timestamp}.json"
        filepath = self.output_dir / filename

        data = {
            "created_at": datetime.now().isoformat(),
            "total_sites": len(sitios),
            "sites": sitios
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"   📄 Metadatos guardados en: {filepath}")
        return filepath

    def cargar_metadatos(self, archivo: Optional[str] = None) -> List[Dict]:
        """
        Load site metadata from a JSON file.

        Args:
            archivo: Optional filename to load. If None, loads the most recent.

        Returns:
            List of site configurations
        """
        if archivo:
            filepath = self.output_dir / archivo
        else:
            # Load most recent file
            files = sorted(self.output_dir.glob("sites_metadata_*.json"), reverse=True)
            if not files:
                return []
            filepath = files[0]

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("sites", [])


def main():
    """Test the SitePreCreation module."""
    print("Testing SitePreCreation module...")
    print("=" * 60)

    protocolo = SitePreCreation()
    sitios = protocolo.crear_batch_sitios(cantidad=5, guardar_archivo=True)

    print(f"\n✅ Created {len(sitios)} site configurations:")
    for sitio in sitios:
        print(f"   - {sitio['title']} ({sitio['domain']})")

    print("\nDone!")


if __name__ == "__main__":
    main()
