from .models import Paciente,Medico,GrupoSanguineo,PlanMedico,Vacuna,ContactoUrgencia
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from .serializers import DaoPacientes,RegistroMedicoSerializer

class DaoViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DaoPacientes

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