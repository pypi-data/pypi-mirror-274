from cv_smart_house_camera.utils.get_modules_from_toml import get_modules_from_toml

def generate_code():
    modules = get_modules_from_toml()
    import_code = []
    original_frame_processing = "def original_frame_processing(frame, frame_number):\n\treturn"
    modules_list = ['{ "name": "Original Frame", "package_name": "original", "proccessing": original_frame_processing }']



    for package, version in modules:
        import_statement = f"import {package}"
        import_code.append(import_statement)
        module_item = f"""{{ "name": {package}.name, "package_name": "{package}", "proccessing": {package}.proccessing, "options": {package}.options }}"""

        modules_list.append(module_item)

    # with open('.\\camera_service\\modules\\modules_list.py', 'w') as out_file:
    with open('.\\.venv\\Lib\\site-packages\\camera_service\\modules\\modules_list.py', 'w') as out_file:
        out_file.write('\n'.join([*import_code, "\n", original_frame_processing, "\n" "modules = [", ", ".join(modules_list), "]"]))

if __name__ == "__main__":
    generate_code()