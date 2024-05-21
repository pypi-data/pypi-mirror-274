import logging
import toml
import uvicorn
from threading import Thread
from cv_smart_house_camera.cam_capture import cam_capture
from twirp.asgi import TwirpASGIApp
from  cv_smart_house_camera.proto_services.camera_service_twirp import CameraServiceServer
import  cv_smart_house_camera.proto_services.camera_service_pb2 as camera_service
from cv_smart_house_camera.data.frames import modules_result
from cv_smart_house_camera.modules.modules_list import modules as modules_list
from starlette.middleware.cors import CORSMiddleware

from cv_smart_house_camera.helpers.poetry_install import poetry_install
from cv_smart_house_camera.generate_code import generate_code
from google.protobuf.empty_pb2 import Empty
from cv_smart_house_camera.constants import PORT
from cv_smart_house_camera.utils.get_local_ip import get_local_ip

class CameraService(object):
    def IsCameraAlive(self, ctx, request):
        return camera_service.IsCameraAliveResponse(is_alive=True)
        

    def InstallModules(self, ctx, request):
        # Add packages from array to the project.
        with open('pyproject.toml', 'r') as file:
            pyproject_data = toml.load(file)

        for package in request.modules:
            pyproject_data['tool']['poetry']['dependencies'][package.name] = package.version

        with open('pyproject.toml', 'w') as file:
            toml.dump(pyproject_data, file)

        generate_code()

        return Empty()
    
    def UninstallModules(self, ctx, request):
        # Remove packages from array from the project.
        original_names = []

        #find original_name of the package
        for module in request.modules:
            for installed_module in modules_list:
                if installed_module.get("name") == module:
                    original_names.append(installed_module.get("package_name"))

        with open('pyproject.toml', 'r') as file:
            pyproject_data = toml.load(file)

        for package in original_names:
            del pyproject_data['tool']['poetry']['dependencies'][package]

        with open('pyproject.toml', 'w') as file:
            toml.dump(pyproject_data, file)

        generate_code()

        return Empty()
    
    def GetInstalledModules(self, ctx, request):
        formatted_modules = []

        for module in modules_list:
            formatted_modules.append(camera_service.InstalledModule(name = module.get("name"), options = module.get("options")))

        return camera_service.InstalledModules(modules=formatted_modules)

    def GetLastFrame(self, ctx, request):
        module_result = modules_result.get(request.module)
        if module_result is None or module_result.get("ok") == False:
            raise Exception(f"Module {request.module} failed processing")
        
        frame = module_result.get("frame")

        return camera_service.Frame(frame=frame)

app = TwirpASGIApp()
service = CameraServiceServer(service=CameraService())
app.add_service(service)

# Wrap the app with CORSMiddleware
app = CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_server():
    uvicorn.run(app=app, host=get_local_ip(), port=PORT)

def configure_camera_server(services: list = [], 
                            modules: list = [],
                            allow_origins=[],
                            allow_methods=[],
                            allow_headers=[]):
    logging.basicConfig()

    # Install packages.
    poetry_install()

    # Add modules to the list
    for module in modules:
        modules_list.append(module)

    app = TwirpASGIApp()
    services.append(CameraServiceServer(service=CameraService()))

    for service in services:
        app.add_service(service)



    # Wrap the app with CORSMiddleware
    app = CORSMiddleware(
    app,
    allow_origins=allow_origins,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
    )

    thread = Thread(target = run_server, args = ())
    thread.start()
    cam_capture()
