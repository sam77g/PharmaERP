import os
import platform

sistema = platform.system()
base = os.path.dirname(os.path.abspath(__file__))

# Deteta se o Dockerfile está na pasta atual ou dentro de /src
pasta_app = os.path.join(base, "src") if os.path.exists(os.path.join(base, "src", "Dockerfile")) else base

os.system(f'docker build -t meu-app-tk "{pasta_app}"')

if sistema == "Darwin":  # macOS
    os.system("open -a XQuartz && /opt/X11/bin/xhost +localhost")
    os.system(f'docker run --rm -it -e DISPLAY=host.docker.internal:0 -v "{pasta_app}:/src" meu-app-tk')

elif sistema == "Linux":  # Linux
    os.system("xhost +local:docker")
    os.system(f'docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v "{pasta_app}:/src" meu-app-tk')

else:  # Windows
    os.system(f'docker run --rm -it -e DISPLAY=:0 -v /run/desktop/mnt/host/wslg/.X11-unix:/tmp/.X11-unix -v /run/desktop/mnt/host/wslg:/mnt/wslg -v "{pasta_app}:/src" meu-app-tk')