import os
import argparse
import re
from pathlib import Path

def parse_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}
    
    metadata = {}
    for line in match.group(1).splitlines():
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            metadata[key] = val
    return metadata

def get_search_globs(config_path):
    """
    Parses task_config.yaml to determine precisely where to look for tasks and bugs.
    Returns a list of glob patterns relative to the project root.
    """
    globs = []
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)
            
        levels = cfg.get("levels", {})
        
        # Master path
        master = levels.get("master", {})
        if master:
            base_path = master.get("path", "")
            folders = master.get("folders", {})
            if folders.get("tasks"): globs.append(base_path + folders.get("tasks") + "*.md")
            if folders.get("bugs"): globs.append(base_path + folders.get("bugs") + "*.md")
            
        # Component paths
        for comp in levels.get("components", []):
            base_path = comp.get("path", "").replace("{name}", "*")
            folders = comp.get("folders", {})
            if folders.get("tasks"): globs.append(base_path + folders.get("tasks") + "*.md")
            if folders.get("bugs"): globs.append(base_path + folders.get("bugs") + "*.md")
            
    except ImportError:
        print("⚠️ Advertencia: No se encontró la librería 'yaml' instalada. Se procederá usando búsqueda heurística (fallback).")
        print("Para un mejor rendimiento y precisión, ejecuta: pip install pyyaml")
        # Fallback manual de búsqueda en base a convenciones conocidas del task_config
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # simple heuristic via regex
        paths = re.findall(r'path:\s*(.*?)\n', content)
        for p in paths:
            p = p.strip().strip('"\'').replace("{name}", "*")
            globs.append(p + "tasks/*.md")
            globs.append(p + "bugs/*.md")

    return list(set(globs))

def main():
    parser = argparse.ArgumentParser(description="Verifica que todas las tareas y bugs de una release estén cerradas.")
    parser.add_argument("--version", required=True, help="Versión target a comprobar (ej. v1.2.0)")
    parser.add_argument("--dir", default=".", help="Directorio raíz del proyecto")
    args = parser.parse_args()

    root_dir = Path(args.dir)
    config_path = root_dir / "task_config.yaml"
    
    if not config_path.exists():
        print(f"❌ ERROR: No se encontró {config_path}. Asegúrate de ejecutar el script desde la raíz del proyecto.")
        exit(1)
        
    search_globs = get_search_globs(config_path)
    incomplete = []
    verified_files = 0
    
    # Buscar solo en las rutas específicas según task_config.yaml
    for glob_pattern in search_globs:
        for path in root_dir.glob(glob_pattern):
            if not path.is_file():
                continue
                
            if not re.match(r'^(T|B)-', path.name):
                continue
                
            verified_files += 1
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read(4096) 
                fm = parse_frontmatter(content)
            except Exception:
                continue
                
            task_ver = fm.get("version", "")
            
            if task_ver == args.version:
                status = fm.get("status", "").lower()
                if status not in ["completed", "cancelled", "superseded", "rejected"]:
                    incomplete.append({
                        "id": fm.get("id", path.stem),
                        "status": status,
                        "path": str(path.relative_to(root_dir))
                    })

    if incomplete:
        print(f"ERROR: Encontradas tareas/bugs asignadas a {args.version} que no estan completadas:")
        for t in incomplete:
            print(f"  - [{t['id']}] (Estado: {t['status']}) -> {t['path']}")
        exit(1)
    else:
        print(f"OK: Todas las anotaciones para la version {args.version} estan completadas (verificados {verified_files} archivos).")
        exit(0)

if __name__ == "__main__":
    main()
