
  const tabla = new Tabulator("#motorcycle-table", {
        locale: "es_BO",
        langs: {
            "es_BO": {
            "pagination": {
                "first": "Primero",
                "last": "Último",
                "prev": "Anterior",
                "next": "Siguiente",
            },
            "headerFilters": {
                "default": "filtrar columna...",
            },
            "group": {
                "item": "elemento",
                "items": "elementos",
            },
            "ajax": {
                "loading": "Cargando datos...",
                "error": "Error al cargar datos",
            },
            "dataTree": {
                "loading": "Cargando...",
                "error": "Error en datos de árbol",
            },
            "validation": {
                "required": "Campo requerido",
                "min": "Valor mínimo: ",
                "max": "Valor máximo: ",
            }
            // más traducciones si quieres
            }
        },
        ajaxURL: "http://127.0.0.1:8000/motorcycles/api/motorcycle/tabulator",
        ajaxResponse: function(url, params, response) {
            // Solo retornamos el array de datos
            return response.data;
        },
        layout: "fitColumns",
        pagination: "remote",
        paginationSize: 10,
        columns: [
            { title: "ID", field: "id" },
            { title: "Código DIM", field: "code_dim" },
            { title: "Código FVR", field: "code_fvr" },
            { title: "Modelo", field: "model_year" },
            { title: "Fabricación", field: "manufacturing_year" },
            { title: "Chasis", field: "code_chasis" },
        ],
  });
// ✅ Elimina el paginador luego de renderizar los datos
tabla.on("renderComplete", function () {
  const footer = document.querySelector("#motorcycle-table .tabulator-footer");
  if (footer) footer.remove();
})
document.getElementById("btn-return").addEventListener("click", async () => {
    const page = await tabla.getPage();
    if (page > 1) tabla.setPage(page - 1);
});

document.getElementById("btn-next").addEventListener("click", async () => {
    const page = await tabla.getPage();
    const max = await tabla.getPageMax();
    if (page < max) tabla.setPage(page + 1);
});