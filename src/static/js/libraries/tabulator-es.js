// static/js/tabulator-es.js
Tabulator.extendModule("localize", "langs", {
  "es": {
    "columns": {},
    "ajax": {
      "loading": "Cargando...",
      "error": "Error al cargar datos",
    },
    "groups": {
      "item": "ítem",
      "items": "ítems",
    },
    "pagination": {
      "page_size": "Tamaño de página",
      "first": "Primera",
      "first_title": "Primera página",
      "last": "Última",
      "last_title": "Última página",
      "prev": "Anterior",
      "prev_title": "Página anterior",
      "next": "Siguiente",
      "next_title": "Página siguiente",
      "page_title": "Página {{page}}",
      "all": "Todo",
    },
    "headerFilters": {
      "default": "filtrar columna...",
      "columns": {}
    },
    "data": {
      "loading": "Cargando...",
      "error": "Error al cargar datos",
    },
    "validation": {
      "required": "Campo requerido",
      "unique": "Valor debe ser único",
      "integer": "Debe ser un entero",
      "float": "Debe ser decimal",
      "numeric": "Debe ser numérico",
      "min": "Mínimo {{min}}",
      "max": "Máximo {{max}}",
      "minLength": "Mínimo {{minLength}} caracteres",
      "maxLength": "Máximo {{maxLength}} caracteres",
      "match": "Debe coincidir con {{pattern}}",
      "step": "Debe ser un múltiplo de {{step}}",
    }
  }
});

Tabulator.defaultOptions.locale = "es";