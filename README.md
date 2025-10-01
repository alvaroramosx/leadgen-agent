## Leadgen Agent (MVP)

Estructura de carpetas mínima, modular y sin tests para un flujo: buscar negocios (Google Places) → extraer datos útiles → scrapear web para email → enviar email.

### Árbol de directorios
```
leadgen-agent/
├─ src/
│  ├─ config/          # Configuración y carga de variables (.env)
│  ├─ types/           # Tipos/Interfaces compartidas (p.ej., Business, Lead)
│  ├─ utils/           # Utilidades genéricas (logging, rate limit, etc.)
│  ├─ modules/
│  │  ├─ places/       # Integración Google Maps Places (búsqueda y parseo)
│  │  ├─ scraper/      # Scraper para extraer email desde sitios web
│  │  └─ email/        # Envío de correos (SMTP/API)
│  └─ pipeline/        # Orquestación del flujo end-to-end (entrada → salida)
├─ data/
│  ├─ outputs/         # Resultados/exportaciones (CSV/JSON)
│  └─ logs/            # Logs del proceso (opcional)
├─ scripts/            # Scripts de conveniencia (ejecución/cron)
├─ .env.example        # Variables de entorno de ejemplo
└─ README.md
```

### Guía rápida
- src/config: carga y validación de variables de entorno.
- src/types: define entidades como `Business`, `Lead`, etc.
- src/utils: helpers (formateo, reintentos, throttling, http simple, etc.).
- src/modules/places: cliente y funciones para consultar Google Places y normalizar resultados.
- src/modules/scraper: lógica para visitar dominios y buscar emails.
- src/modules/email: proveedor de envío (SMTP o API) y plantillas básicas.
- src/pipeline: una función/CLI que recibe sector, provincia, municipio y coordina el flujo completo.
- data/outputs: guarda leads encontrados; data/logs: trazas del proceso.

### Variables de entorno
Replica `.env.example` a `.env` y completa los valores.

### Próximos pasos sugeridos
1) Implementar `src/pipeline/leadgen` con la orquestación del flujo.
2) Añadir en `src/modules/places` el cliente a Google Places.
3) Implementar `src/modules/scraper` para extraer emails desde la web.
4) Implementar `src/modules/email` para envío de correos.

### Requisitos
- Python 3.10+
- pip
- Cuenta de Google Cloud con facturación activa
- API habilitada: Places API (New)

### Instalación
```
pip install -r requirements.txt
```

### Configuración
- Copia `config_ejemplo.yaml` a `config.yaml` y rellena tu `apiKey`.
- Opcionalmente puedes pasar valores por argumentos para sobrescribir lo del archivo.

### Uso (Python)
Pipeline en Python que realiza: búsqueda en Google Places por sector/provincia/municipio, obtiene detalles, intenta scrapear email desde la web y exporta a CSV. Soporta archivo de configuración (YAML) con override por argumentos.

Ejemplos:
```
# Usando solo argumentos (módulo)
python -m src.pipeline.main --sector "restaurantes" --provincia "Madrid" --municipio "Alcobendas" --apiKey "TU_API_KEY" --max 50

# Usando archivo de configuración (config.yaml) y sobrescribiendo algunos valores por argumentos (módulo)
python -m src.pipeline.main --config config.yaml --max 100
```

Formato recomendado de `config.yaml`:
```yaml
sector: restaurantes
provincia: Madrid
municipio: Alcobendas
apiKey: TU_API_KEY
max: 50
timeoutMs: 15000
outputDir: data
```

Salida:
- CSV en `data/` con columnas: Nombre, Direccion, Telefono, Web, Email.

### Notas de API (Places API New)
- Usamos `places:searchText` (v1) con `X-Goog-FieldMask` para pedir sólo: nombre, dirección, teléfono internacional y web.
- Debes habilitar "Places API (New)" en tu proyecto y usar la `apiKey` con permisos.
- Si ves `REQUEST_DENIED`, revisa: facturación, API habilitada, restricciones de la clave, y que no uses la versión legacy.


