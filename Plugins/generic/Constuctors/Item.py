import json


class ItemConstructor:
    @staticmethod
    def getJavaCode(package: str, data: dict):
        result = {}
        for name, entry in data.items():
            changed = entry.get("data", {})
            class_name = name
            content_type = entry.get("content", "unknown")
            path = entry.get("path", "")
            end = entry.get("end", ".java")

            java_lines = []
            print(changed)
            for key, value in changed.items():
                print(key)
                if key.startswith("_"):
                    continue
                java_value = ItemConstructor._convert_to_java(value)
                print(java_value)
                if key == "package": continue
                elif key == "color":
                    java_lines.append(f"        {key} = Color.valueOf({java_value});")
                    continue
                java_lines.append(f"        {key} = {java_value};")

            pk = '.'.join(path.split('.'))
            if len(pk) > 0:
                pk = "."+pk
            java_code = (
                f"package {package}.content{pk};\n"
                f"\nimport mindustry.type.Item;\n"
                f"import arc.graphics.Color;\n"

                f"\npublic class {class_name} extends Item {{\n"
                f"    public {class_name}() {{\n"
                f'        super("{class_name}");\n'
                f'        alwaysUnlocked = false;\n'
                f"{ItemConstructor._format_params(java_lines)}\n"
                f"    }}\n"
                f"}}"
            )

            result[name] = {
                "code": java_code,
                "path": path,
                "filename": name + end,
                "init": [
                    f"import {package}.content{pk}.{name};",
                    f"new {name}();"
                ]
            }

        return result

    @staticmethod
    def _convert_to_java(value):
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, float):
            return str(value)+"f"
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            return str(value)
        elif isinstance(value, dict):
            return json.dumps(value, indent=2)
        elif value is None:
            return "null"
        else:
            return str(value)

    @staticmethod
    def _format_params(params):
        return "\n".join(params)