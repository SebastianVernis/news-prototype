#!/usr/bin/env python3
"""
Script para eliminar duplicados de ARTICULOS_ORIGINALES
Prioriza conservar artículos con URL_IMAGEN válida
"""

import sqlite3
import sys

def cleanup_duplicates(db_path):
    """Eliminar duplicados de ARTICULOS_ORIGINALES"""
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = OFF")
    cursor = conn.cursor()
    
    try:
        # Paso 1: Obtener todos los artículos
        cursor.execute("SELECT ID, TITULO, URL_IMAGEN, FECHA FROM ARTICULOS_ORIGINALES ORDER BY TITULO, FECHA DESC")
        articles = cursor.fetchall()
        
        # Paso 2: Agrupar por título
        by_title = {}
        for id, titulo, url_imagen, fecha in articles:
            if titulo not in by_title:
                by_title[titulo] = []
            by_title[titulo].append({
                'id': id,
                'url_imagen': url_imagen,
                'fecha': fecha,
                'has_valid_image': url_imagen and url_imagen != '' and '/logo.png' not in url_imagen
            })
        
        # Paso 3: Identificar cuáles eliminar
        ids_to_delete = []
        duplicates_found = 0
        
        for titulo, items in by_title.items():
            if len(items) > 1:
                duplicates_found += 1
                # Ordenar: primero los que tienen imagen válida, luego por fecha (más reciente primero)
                items_sorted = sorted(items, 
                    key=lambda x: (not x['has_valid_image'], x['fecha']),
                    reverse=False
                )
                # Mantener el primero (mejor), eliminar el resto
                ids_to_keep = [items_sorted[0]['id']]
                for item in items_sorted[1:]:
                    ids_to_delete.append(item['id'])
        
        print(f"✓ Títulos duplicados encontrados: {duplicates_found}")
        print(f"✓ IDs a eliminar: {len(ids_to_delete)}")
        
        if not ids_to_delete:
            print("✓ No hay duplicados que eliminar")
            return
        
        # Paso 4: Eliminar referencias en REVISION_CONTENIDO
        if ids_to_delete:
            placeholders = ','.join('?' * len(ids_to_delete))
            cursor.execute(f"DELETE FROM REVISION_CONTENIDO WHERE ID_ORIGEN IN ({placeholders})", ids_to_delete)
            deleted_refs = cursor.rowcount
            print(f"✓ Referencias eliminadas en REVISION_CONTENIDO: {deleted_refs}")
        
        # Paso 5: Eliminar duplicados en ARTICULOS_ORIGINALES
        if ids_to_delete:
            placeholders = ','.join('?' * len(ids_to_delete))
            cursor.execute(f"DELETE FROM ARTICULOS_ORIGINALES WHERE ID IN ({placeholders})", ids_to_delete)
            deleted_articles = cursor.rowcount
            print(f"✓ Artículos duplicados eliminados: {deleted_articles}")
        
        # Paso 6: Verificar resultado
        cursor.execute("SELECT COUNT(*) FROM ARTICULOS_ORIGINALES")
        final_count = cursor.fetchone()[0]
        print(f"✓ Total artículos restantes: {final_count}")
        
        # Verificar si aún hay duplicados
        cursor.execute("""
            SELECT TITULO, COUNT(*) as cantidad 
            FROM ARTICULOS_ORIGINALES 
            GROUP BY TITULO 
            HAVING COUNT(*) > 1 
            LIMIT 5
        """)
        remaining = cursor.fetchall()
        if remaining:
            print(f"⚠ Aún hay {len(remaining)} títulos duplicados")
            for titulo, cantidad in remaining:
                print(f"  - '{titulo[:50]}...': {cantidad}")
        else:
            print("✓ No hay duplicados restantes")
        
        conn.commit()
        print("\n✓ Limpieza completada exitosamente")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error: {e}")
        sys.exit(1)
    finally:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python cleanup_duplicates.py <ruta_a_la_base_de_datos.sqlite>")
        sys.exit(1)
    
    db_path = sys.argv[1]
    cleanup_duplicates(db_path)
