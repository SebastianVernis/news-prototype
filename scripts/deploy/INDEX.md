# Deploy Scripts

- `deploy-full.sh`: **NUEVO** - Despliegue completo: Worker API → CMS → Todos los sitios.
- `deploy-menu.sh`: Menú interactivo de despliegue.
- `deploy-10-sites.sh`: Despliega cada sitio como proyecto Pages separado.
- `deploy-complete-sites.sh`: Despliega paquetes de sitios multipágina.
- `deploy-final-10-sites.sh`: Despliegue específico para 10 sitios.
- `deploy-all-sites-mime-fix.sh`: Despliegue con correcciones MIME.
- `create-and-deploy-10-sites.sh`: Genera y despliega en un solo flujo.
- `full-deploy.sh`, `deploy.sh`, `deploy-updated.sh`, `deploy-interactive.sh`: Flujos heredados.
- `redeploy-with-css.sh`: Redeploy con CSS actualizado.

La mayoría de scripts usan por defecto `sites/` y `assets/`. Override con `SITES_DIR` y `NEWS_ASSETS_DIR`.
