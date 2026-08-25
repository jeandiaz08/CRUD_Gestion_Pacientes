# Backend de Gestión de Pacientes - API REST

Este proyecto corresponde al módulo backend centralizado para la **Gestión de Pacientes**, desarrollado como parte de un sistema distribuido de integración de plataformas de salud. 

En la arquitectura del sistema, las responsabilidades se dividieron entre diferentes equipos de trabajo (gestión de citas/horas, administración médica, etc.). Este módulo actúa como el **proveedor principal de datos de pacientes**, sirviendo información tanto al frontend del módulo como a las plataformas de los demás equipos integrados.

---

## 🚀 Características Principales

* **API RESTful Completa:** Operaciones CRUD (GET, POST, PUT/PATCH, DELETE) para la administración completa de fichas de pacientes.
* **Integración Base de Datos Oracle:** Almacenamiento persistente mediante conexión con Oracle Database a través del ORM de Django.
* **Manejo de Serializadores:** Transformación eficiente y segura de datos mediante Django REST Framework (DRF).
* **Control de Orígenes (CORS / Allowed Hosts):** Configuración estricta en `settings.py` para permitir la comunicación cruzada únicamente a los dominios y clientes autorizados.

---

## 🛠️ Tecnologías Utilizadas

* **Python**
* **Django & Django REST Framework (DRF)**
* **Oracle Database**
* **HTML5 & JavaScript (Fetch API)** *(Frontend básico para consumo interno)*

---

## 📐 Arquitectura de Integración

```text
[ Frontend JS / Cliente ] ──────┐
                                ├──► [ API REST Backend ] ──► [ Serializers ] ──► [ Modelos Django ] ──► [ Base de Datos Oracle ]
[ Módulos Externos / Equipos ] ─┘   (Django REST Framework)
