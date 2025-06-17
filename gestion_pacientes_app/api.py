from .models import Paciente,Medico,GrupoSanguineo,PlanMedico,Vacuna,ContactoUrgencia
from django.db import connection
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from .serializers import DaoPacientes,RegistroMedicoSerializer
from rest_framework.pagination import PageNumberPagination

class PacientePagination(PageNumberPagination):
    page_size = 20  # o la cantidad que quieras por página
    page_size_query_param = 'page_size'
    max_page_size = 100

class DaoViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by('id_pac')
    serializer_class = DaoPacientes
    permission_classes = [permissions.AllowAny]
    pagination_class = PacientePagination

    def destroy(self, request, *args, **kwargs):
        try:
            paciente = self.get_object()
            id_pac = paciente.id_pac
            id_med = paciente.medico.id_med

            print(f"Eliminando paciente {id_pac} y sus relaciones")

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM CALIFICACION_CITA WHERE PACIENTE_id_pac = :1 AND PACIENTE_MEDICO_id_med = :2", [id_pac, id_med])
                cursor.execute("DELETE FROM VACUNAS WHERE PACIENTE_id_pac = :1 AND PACIENTE_MEDICO_id_med = :2", [id_pac, id_med])
                cursor.execute("DELETE FROM CONTACTO_URGENCIA WHERE PACIENTE_id_pac = :1 AND PACIENTE_MEDICO_id_med = :2", [id_pac, id_med])
                cursor.execute("DELETE FROM HISTORIAL_CITA WHERE PACIENTE_id_pac = :1 AND PACIENTE_MEDICO_id_med = :2", [id_pac, id_med])
                cursor.execute("DELETE FROM FICHA_PACIENTE WHERE PACIENTE_id_pac = :1 AND PACIENTE_MEDICO_id_med = :2", [id_pac, id_med])
                cursor.execute("DELETE FROM PLAN_MEDICO WHERE PACIENTE_id_pac = :1 AND PACIENTE_MEDICO_id_med = :2", [id_pac, id_med])
                cursor.execute("DELETE FROM PACI_ESPECIALES WHERE PACIENTE_id_pac = :1 AND PACIENTE_MEDICO_id_med = :2", [id_pac, id_med])
                cursor.execute("DELETE FROM DERIVAC_PACIENTE WHERE PACIENTE_id_pac = :1 AND PACIENTE_MEDICO_id_med = :2", [id_pac, id_med])
                cursor.execute("DELETE FROM HIST_MEDICO WHERE PACIENTE_id_pac = :1 AND PACIENTE_MEDICO_id_med = :2", [id_pac, id_med])
                cursor.execute("DELETE FROM DOCUMENTO WHERE id_paciente = :1", [id_pac])
                # Agrega más tablas si encuentras más relacionadas
                cursor.execute("DELETE FROM PACIENTE WHERE id_pac = :1", [id_pac])

            print("Paciente eliminado con éxito")
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            print(f"Error eliminando paciente: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class RegistroMedicoView(APIView):
    def post(self, request):
        serializer = RegistroMedicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Registro guardado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def lista_medicos(request):
    medicos = Medico.objects.all().values('id_med', 'nombre', 'apellido')
    data = [
        {
            'id': m['id_med'],
            'nombre_completo': f"{m['nombre']} {m['apellido']}"
        }
        for m in medicos
    ]
    return Response(data)

@api_view(['GET'])
def lista_grupos_sanguineos(request):
    grupos = GrupoSanguineo.objects.all().values('id_grupo', 'grupo_sang', 'factor_rh')
    data = [
        {'id': g['id_grupo'], 'nombre': f"{g['grupo_sang']} {g['factor_rh']}"}
        for g in grupos
    ]
    return Response(data)