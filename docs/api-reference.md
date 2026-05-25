---
# Questo frontmatter attiva il template custom di Stoplight Elements
template: api-reference.html

# URL della spec OpenAPI — può essere:
#   - un percorso relativo alla root del sito (inizia con /)
#   - un URL esterno (https://...)
api_spec_url: /openapi.yaml

# Layout di Elements: sidebar | stacked | responsive
api_layout: sidebar

# Router: hash | memory | history
# "hash" è il più compatibile (funziona anche con file://)
api_router: hash

# Metti true per nascondere il pannello "Try it"
api_hide_try_it: false

# Metadati SEO standard di MkDocs
title: API Reference
description: LanguageCheck API reference
---

<!--
  Il contenuto di questo file .md NON viene renderizzato:
  il template api-reference.html sovrascrive completamente
  il blocco {% block container %} con <elements-api>.

  Puoi però usare questo spazio per note interne o come
  fallback di testo per i crawler SEO (vedi tecnica sotto).
-->
