# Django
from django.db.models import Manager

# Manager para el modelo persona natural
class NaturalPersonManager(Manager):
    
    # Función para crear u obtener
    def get_or_create_natural_person(self,**person_fields):
        natural_person, created = self.get_or_create(
            document_code=person_fields['document_code'], 
            document_complement=person_fields['document_complement'],
            defaults=person_fields
        )
        return natural_person, created