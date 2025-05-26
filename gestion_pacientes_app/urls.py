from rest_framework import routers
from django.urls import path
from .api import DaoViewSet
from .api import lista_medicos, lista_grupos_sanguineos, RegistroMedicoView

router = routers.DefaultRouter()
router.register('api/gestion_pacientes_app', DaoViewSet, 'DAO_Pacientes')

urlpatterns = router.urls + [
    path('api/medicos/', lista_medicos, name='lista_medicos'),
    path('api/grupos_sanguineos/', lista_grupos_sanguineos, name='lista_grupos_sanguineos'),
    path('api/registro-medico/', RegistroMedicoView.as_view(), name='registro_medico'),
]

