from django.db import models

class GrupoSanguineo(models.Model):
    id_grupo = models.IntegerField(primary_key=True)
    grupo_sang = models.CharField(max_length=350)
    factor_rh = models.CharField(max_length=350)

    class Meta:
        db_table = 'GRUPO_SANGUINEO'
        managed = False


class Medico(models.Model):
    id_med = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=10, db_column='rut')
    nombre = models.CharField(max_length=100, db_column='nombre')
    apellido = models.CharField(max_length=100, db_column='apellido')
    email = models.CharField(max_length=200, db_column='email')
    est_med = models.CharField(max_length=1, db_column='est_med')


    class Meta:
        db_table = 'MEDICO'
        managed = False 


class Paciente(models.Model):
    id_pac = models.IntegerField(primary_key=True)
    sexo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nac = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    alergias = models.CharField(max_length=100)
    seguro_medico = models.CharField(max_length=100, blank=True, null=True)
    obser_clinica = models.CharField(max_length=350)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, db_column='MEDICO_id_med')
    grupo_sanguineo = models.ForeignKey(GrupoSanguineo, on_delete=models.CASCADE, db_column='GRUPO_SANGUINEO_id_grupo')

    class Meta:
        db_table = 'PACIENTE'
        unique_together = (('medico', 'id_pac'),)
        managed = False


class PlanMedico(models.Model):
    id_plan = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion_plan = models.CharField(max_length=200)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,
        db_column='PACIENTE_id_pac',
        related_name='planes_medicos')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE,
        db_column='PACIENTE_MEDICO_id_med',
        related_name='planes_medicos')

    class Meta:
        db_table = 'PLAN_MEDICO'
        unique_together = (('paciente', 'medico'),)
        managed = False


class Vacuna(models.Model):
    id_vancuna = models.AutoField(primary_key=True)
    nom_vacuna = models.CharField(max_length=100)
    descrip_vacuna = models.CharField(max_length=250, blank=True, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,
        db_column='PACIENTE_id_pac',
        related_name='vacunas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE,
        db_column='PACIENTE_MEDICO_id_med',
        related_name='vacunas')

    class Meta:
        db_table = 'VACUNAS'
        unique_together = (('paciente', 'medico'),)
        managed = False


class ContactoUrgencia(models.Model):
    id_doc = models.IntegerField(primary_key=True)
    contacto = models.IntegerField()
    parentesco = models.CharField(max_length=100)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,
        db_column='PACIENTE_id_pac',
        related_name='contactos_urgencia')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE,
        db_column='PACIENTE_MEDICO_id_med',
        related_name='contactos_urgencia')

    class Meta:
        db_table = 'CONTACTO_URGENCIA'
        unique_together = (('paciente', 'medico', 'id_doc'),)
        managed = True        
