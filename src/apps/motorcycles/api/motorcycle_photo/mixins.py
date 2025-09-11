class PublicListPrivateRetrieveMixin:
    def initial(self, request, *args, **kwargs):
        # Determinar nombre del lookup usado por el viewset (por defecto 'pk')
        lookup_kw = getattr(self, "lookup_url_kwarg", None) or getattr(self, "lookup_field", "pk")
        # Consideramos 'list' cuando es GET y no hay lookup en kwargs
        is_list = request.method.upper() == "GET" and lookup_kw not in kwargs
        if is_list:
            # Guardar y deshabilitar autenticadores SOLO para esta instancia/solicitud
            self._saved_authentication_classes = getattr(self, "authentication_classes", None)
            # Asignar vacio a nivel de instancia; así DRF no intentará autenticar
            self.authentication_classes = []
        try:
            return super().initial(request, *args, **kwargs)
        finally:
            # Restaurar autenticadores para no afectar otras llamadas
            if is_list:
                if self._saved_authentication_classes is None:
                    try:
                        delattr(self, "authentication_classes")
                    except Exception:
                        pass
                else:
                    self.authentication_classes = self._saved_authentication_classes
                del self._saved_authentication_classes