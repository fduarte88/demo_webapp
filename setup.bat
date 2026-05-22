@echo off
echo ================================================
echo  AgendaPro - Setup inicial
echo ================================================

echo.
echo [1] Creando entorno virtual...
python -m venv venv

echo [2] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [3] Instalando dependencias...
pip install -r requirements.txt

echo [4] Copiando archivo de configuracion...
if not exist .env (
    copy .env.example .env
    echo     Edita el archivo .env con tus credenciales de PostgreSQL
)

echo.
echo ================================================
echo  IMPORTANTE: Edita .env antes de continuar
echo  Configura DB_NAME, DB_USER, DB_PASSWORD
echo ================================================
echo.
pause

echo [5] Ejecutando migraciones...
python manage.py migrate

echo [6] Creando usuario administrador...
python manage.py create_admin

echo [7] Recolectando archivos estaticos...
python manage.py collectstatic --noinput

echo.
echo ================================================
echo  Setup completo!
echo  Ejecuta: python manage.py runserver 8001
echo  Abre: http://localhost:8001
echo  Usuario: admin  /  Contrasena: admin88++
echo ================================================
pause
