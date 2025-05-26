import json


class WallConstructor:
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
            for key, value in changed.items():
                java_value = WallConstructor._convert_to_java(value)
                if key == "requirements":
                    java_lines.append(f"        {java_value}")
                elif key != "package":
                    java_lines.append(f"        {key} = {java_value};")

            pk = '.'.join(path.split('.'))
            if len(pk) > 0:
                pk = "."+pk
            java_code = (
                f"package {package}{pk};\n"
                f"\nimport mindustry.content.Items;\n"
                f"import mindustry.type.Category;\n"
                f"import mindustry.type.ItemStack;\n"
                f"import mindustry.world.blocks.defense.Wall;\n"
                f"\npublic class {class_name} extends Wall {{\n"
                f"    public {class_name}() {{\n"
                f'        super("{class_name}");\n'
                f"{WallConstructor._format_params(java_lines)}\n"
                f"    }}\n"
                f"}}"
            )

            result[name] = {
                "code": java_code,
                "path": path,
                "filename": name + end,
                "init": [
                    f"import {package}{pk}.{name};",
                    f"new {name}();"
                ]
            }

        return result

    @staticmethod
    def _convert_to_java(value):
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            items = ", ".join(f"{item[0]}, {item[1]}" for item in value)
            return f"requirements(Category.defense, ItemStack.with({items}))"
        elif isinstance(value, dict):
            return json.dumps(value, indent=2)
        elif value is None:
            return "null"
        else:
            return str(value)

    @staticmethod
    def _format_params(params):
        return "\n".join(params)