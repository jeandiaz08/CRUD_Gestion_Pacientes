from rest_framework import serializers
from .models import Paciente,Medico,GrupoSanguineo,PlanMedico,Vacuna,ContactoUrgencia
from django.db.models import Max


class DaoContactoUrgencia(serializers.ModelSerializer):
    class Meta:
        model = ContactoUrgencia
        fields = '__all__'
        id_doc = serializers.IntegerField(required=True)

class DaoPacientes(serializers.ModelSerializer):
    contacto_emergencia = DaoContactoUrgencia(write_only = True)
    medico = serializers.PrimaryKeyRelatedField(queryset=Medico.objects.all())
    grupo_sanguineo = serializers.PrimaryKeyRelatedField(queryset=GrupoSanguineo.objects.all())
    class Meta:
        model = Paciente
        fields = '__all__'
        

    def create(self, validated_data):
        contacto_data = validated_data.pop('contacto_emergencia')
        medico = validated_data['medico']

        paciente = Paciente.objects.create(**validated_data)  

        max_id = ContactoUrgencia.objects.aggregate(max_id=Max('id_doc'))['max_id'] or 0
        new_id = max_id + 1

        ContactoUrgencia.objects.create(
            id_doc=new_id,
            contacto=contacto_data['contacto'],
            parentesco=contacto_data['parentesco'],
            paciente=paciente,
            medico=medico
        )

        return paciente

    def update(self, instance, validated_data):
        contacto_data = validated_data.pop('contacto_emergencia', None)

        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.fecha_nac  = validated_data.get('fechaNacimiento', instance.fecha_nac )
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.alergias = validated_data.get('alergias', instance.alergias)
        instance.seguro_medico = validated_data.get('seguro', instance.seguro_medico)
        instance.obser_clinica = validated_data.get('observacion', instance.obser_clinica)

        instance.save()

        return instance


class PlanMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanMedico
        fields = '__all__'

    def create(self, validated_data):
        max_id = PlanMedico.objects.aggregate(max_id=Max('id_plan'))['max_id'] or 0
        validated_data['id_plan'] = max_id + 1
        return super().create(validated_data)


class RegistroMedicoSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=200)
    descripcion_plan = serializers.CharField(max_length=200)
    vacunas = serializers.ListField(child=serializers.CharField(max_length=100))
    paciente = serializers.IntegerField()
    medico = serializers.IntegerField()

    def create(self, validated_data):
        nombre = validated_data['nombre']
        descripcion = validated_data['descripcion_plan']
        paciente_id = validated_data['paciente']
        medico_id = validated_data['medico']
        vacunas = validated_data['vacunas']

        paciente = Paciente.objects.get(pk=paciente_id)
        medico = Medico.objects.get(pk=medico_id)

        max_plan = PlanMedico.objects.aggregate(max_id=Max('id_plan'))['max_id'] or 0
        plan = PlanMedico.objects.create(
            id_plan=max_plan + 1,
            nombre=nombre,
            descripcion_plan=descripcion,
            paciente=paciente,
            medico=medico
        )

        max_vac = Vacuna.objects.aggregate(max_id=Max('id_vancuna'))['max_id'] or 0
        for i, vacuna_nombre in enumerate(vacunas):
            Vacuna.objects.create(
                id_vancuna=max_vac + i + 1,
                nom_vacuna=vacuna_nombre,
                descrip_vacuna="",
                paciente=paciente,
                medico=medico
            )

        return {"mensaje": "Plan médico y vacunas guardados correctamente"}

class DaoGrupoSanguineo(serializers.ModelSerializer):
    class Meta:
        model = GrupoSanguineo
        fields = '__all__'