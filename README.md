# wahapediaBackend
Backend que devuelve datos de warhammer 40k : kill team y en el que se pueden crear y guardar los killteam de cada usuario.
- [Requisitos](#requisitos)
- [Tecnologías](#tecnologias)
- [Instalación](#instalacion)
- [Uso](#uso)
- [Documentación](#documentacion)
- [Endpoints](#endpoints)
- [Contribuidores](#contribuidores)
## Requisitos
https://github.com/aseoanef/wahapediaBackend/blob/main/requirements.txt
## Tecnologias
Python
Django
PostgreSQL
## Instalacion
1. Clonar el repositorio:
```bash
 git clone https://github.com/aseoanef/wahapediaBackend.git
```
2. Instalar dependencias:
```bash
pip install -r requirements.txt
 ```
# Uso
Crear usuario admin
```bash
python manage.py createsuperuser
 ```
Ejecutar el servidor
```bash
python manage.py runserver
 ```
## Documentacion
https://docs.google.com/document/d/1X30G-O2FHpn8PwcZLLNacUumZr8D2-VFFNeZGpodfoA/edit?usp=drive_link

## Endpoints
Añadir y gestionar la base de datos
```
    admin/
```
GET y POST de los ejércitos
```
    army/
```
GET y PUT de ejércitos por id
```
    army/<int:armyId>/
```
GET y POST de los soldados
```
    operative/
```
GET Y PUT de los soldados por id
```
    operative/<int:operativeId>/
```
GET y POST de las armas
```
    gun/
```
GET y PUT de las armas por id
```
    gun/<int:gunId>/
```
Simulación de ataques
```
    attack/<int:gunId>/
```
GET y POST de las acciones únicas de los operativos
```
    uniqueaction/
```
GET y PUT de las acciones únicas de los operativos por id
```
    uniqueaction/<int:uniqueactionId>/
```
GET y POST de las reglas especiales de las armas
```
    specialrule/
```
GET y PUT de las reglas especiales de las armas por id
```
    specialrule/<int:specialruleId>/
```
GET y POST de las abilidades de los ejércitos
```
    ability/
```
GET y PUT de las abilidades de los ejércitos por id
```
    ability/<int:abilityId>/
```
GET y POST para los ejércitos personalizados
```
    customarmy/
```
GET, PUT y DELETE para los ejércitos personalizados por id
```
    customarmy/<int:customarmyId>/
```
GET y POST para los soldados personalizados
```
    operativegun/
```
GET, PUT y DELETE para los soldados personalizados por id
```
    operativegun/<int:operativegunId>/
```
# Contribuidores
- [Anxo Seoane Fernández](https://github.com/aseoanef)
