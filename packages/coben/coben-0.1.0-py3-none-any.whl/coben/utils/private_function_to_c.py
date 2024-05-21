import re

def parse_plantuml(content):
    """ Einfaches Parsen des PlantUML-Inhalts zu C++-Code """
    code = ""
    # Finden der Partition "super_function"
    partition_match = re.search(r'partition "([^"]+)" \{([^}]+)\}', content, re.DOTALL)
    if partition_match:
        function_name = partition_match.group(1)
        actions = partition_match.group(2).strip().split('\n')
        code += f"void {function_name}() {{\n"
        for action in actions:
            # Einfaches Parsen der Aktionen innerhalb der Funktion
            action_match = re.search(r':([^;]+);', action.strip())
            if action_match:
                code += f"    {action_match.group(1).strip()};\n"
        code += "}\n"
    return code

# PlantUML Inhalt
plantuml_content = """
@startuml "a_private_function"
|#LightYellow|Data|
partition "super_function" {
    :int some_variable = 10;
    |#Pink|Processing|
    :some_variable++;
    |#LightYellow|Data|
}
:some_variable;
@enduml
"""

# C++-Code generieren
cpp_code = parse_plantuml(plantuml_content)
print(cpp_code)
