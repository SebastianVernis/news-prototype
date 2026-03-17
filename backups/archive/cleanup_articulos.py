#!/usr/bin/env python3
"""
Script de respaldo y limpieza de ARTICULOS_ORIGINALES
Elimina duplicados conservando los que tienen imagen válida
"""

import sqlite3
import json
from datetime import datetime

def backup_and_cleanup(db_path):
    """Hacer backup y limpiar duplicados"""
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = OFF")
    cursor = conn.cursor()
    
    backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        print("=" * 60)
        print("RESPALDO Y LIMPIEZA DE ARTICULOS_ORIGINALES")
        print("=" * 60)
        
        # PASO 1: Contar registros actuales
        cursor.execute("SELECT COUNT(*) FROM ARTICULOS_ORIGINALES")
        original_count = cursor.fetchone()[0]
        print(f"\n✓ Total artículos originales: {original_count}")
        
        # PASO 2: Crear backup completo
        print(f"\n📦 Creando backup...")
        backup_table = f"ARTICULOS_ORIGINALES_BACKUP_{backup_time}"
        cursor.execute(f"""
            CREATE TABLE {backup_table} AS 
            SELECT * FROM ARTICULOS_ORIGINALES
        """)
        print(f"✓ Backup creado: {backup_table}")
        
        # PASO 3: Obtener todos los artículos
        cursor.execute("""
            SELECT ID, TITULO, URL_IMAGEN, FECHA 
            FROM ARTICULOS_ORIGINALES 
            ORDER BY TITULO, FECHA DESC
        """)
        articles = cursor.fetchall()
        
        # PASO 4: Agrupar por título y seleccionar cuáles mantener
        by_title = {}
        for id, titulo, url_imagen, fecha in articles:
            if titulo not in by_title:
                by_title[titulo] = []
            by_title[titulo].append({
                'id': id,
                'url_imagen': url_imagen,
                'fecha': fecha,
                'has_valid_image': url_imagen and url_imagen != '' and '/logo.png' not in str(url_imagen)
            })
        
        # PASO 5: Identificar qué conservar y qué eliminar
        ids_to_keep = []
        ids_to_delete = []
        duplicates_count = 0
        
        for titulo, items in by_title.items():
            if len(items) > 1:
                duplicates_count += 1
                # Ordenar: primero con imagen válida, luego por fecha (más reciente primero)
                items_sorted = sorted(items, 
                    key=lambda x: (not x['has_valid_image'], x['fecha']),
                    reverse=(False, True)  # hasValidImage DESC, fecha DESC
                )
                items_sorted.sort(key=lambda x: not x['has_valid_image'])  # Primero con imagen
                items_sorted.sort(key=lambda x: x['fecha'], reverse=True)  # Luego por fecha
                
                # Mantener el primero
                ids_to_keep.append(items_sorted[0]['id'])
                
                # Eliminar el resto
                for item in items_sorted[1:]:
                    ids_to_delete.append(item['id'])
            else:
                ids_to_keep.append(items[0]['id'])
        
        print(f"\n📊 Estadísticas:")
        print(f"   - Títulos únicos: {len(by_title)}")
        print(f"   - Títulos duplicados: {duplicates_count}")
        print(f"   - IDs a conservar: {len(ids_to_keep)}")
        print(f"   - IDs a eliminar: {len(ids_to_delete)}")
        
        if not ids_to_delete:
            print("\n✓ No hay duplicados que eliminar")
            return
        
        # PASO 6: Guardar IDs eliminados en archivo JSON
        backup_data = {
            'backup_time': backup_time,
            'original_count': original_count,
            'deleted_count': len(ids_to_delete),
            'deleted_ids': ids_to_delete,
            'articles': []
        }
        
        # Obtener detalles de los artículos eliminados
        placeholders = ','.join('?' * len(ids_to_delete))
        cursor.execute(f"""
            SELECT ID, TITULO, URL_IMAGEN, FECHA 
            FROM {backup_table}
            WHERE ID IN ({placeholders})
        """, ids_to_delete)
        
        for row in cursor.fetchall():
            backup_data['articles'].append({
                'id': row[0],
                'titulo': row[1],
                'url_imagen': row[2],
                'fecha': row[3]
            })
        
        backup_file = f"backup_articulos_eliminar_{backup_time}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Backup JSON creado: {backup_file}")
        
        # PASO 7: Eliminar referencias en REVISION_CONTENIDO
        print(f"\n🗑️  Eliminando referencias en REVISION_CONTENIDO...")
        cursor.execute(f"""
            DELETE FROM REVISION_CONTENIDO 
            WHERE ID_ORIGEN IN ({placeholders})
        """, ids_to_delete)
        deleted_refs = cursor.rowcount
        print(f"   - Referencias eliminadas: {deleted_refs}")
        
        # PASO 8: Eliminar duplicados en ARTICULOS_ORIGINALES
        print(f"\n🗑️  Eliminando artículos duplicados...")
        cursor.execute(f"""
            DELETE FROM ARTICULOS_ORIGINALES 
            WHERE ID IN ({placeholders})
        """, ids_to_delete)
        deleted_articles = cursor.rowcount
        print(f"   - Artículos eliminados: {deleted_articles}")
        
        # PASO 9: Verificar resultado
        cursor.execute("SELECT COUNT(*) FROM ARTICULOS_ORIGINALES")
        final_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT TITULO FROM ARTICULOS_ORIGINALES 
                GROUP BY TITULO HAVING COUNT(*) > 1
            )
        """)
        remaining_duplicates = cursor.fetchone()[0]
        
        print(f"\n✅ RESULTADO FINAL:")
        print(f"   - Artículos antes: {original_count}")
        print(f"   - Artículos después: {final_count}")
        print(f"   - Eliminados: {deleted_articles}")
        print(f"   - Duplicados restantes: {remaining_duplicates}")
        
        conn.commit()
        print(f"\n✓ Operación completada exitosamente")
        print(f"✓ Cambios guardados en la base de datos")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ ERROR: {e}")
        print("✓ Se hizo rollback, no hay cambios")
        raise
    finally:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python cleanup_articulos.py <ruta_db.sqlite>")
        sys.exit(1)
    
    db_path = sys.argv[1]
    backup_and_cleanup(db_path)
