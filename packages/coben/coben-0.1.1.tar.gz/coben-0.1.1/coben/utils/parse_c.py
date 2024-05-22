from pycparser import c_parser, c_ast, parse_file

# Dummy C-Code
code = """

int tns_storage_mmc_init(void)
{
    if (disk_access_init(mount.storage_dev) != 0) {
        LOG_ERR("Storage init ERROR!");
        return -ENODATA;
    }

    int block_count;
    if (disk_access_ioctl(mount.storage_dev, DISK_IOCTL_GET_SECTOR_COUNT, &block_count)) {
        LOG_ERR("Unable to get sector count");
        return -ENODATA;
    }

    int block_size;
    if (disk_access_ioctl(mount.storage_dev, DISK_IOCTL_GET_SECTOR_SIZE, &block_size)) {
        LOG_ERR("Unable to get sector size");
        return -ENODATA;
    }

    const int memory_size_mb = ((int)block_count * block_size) >> 20;
    LOG_INF("MMC Disk initialized. Block count: %u, block size: %u -> Memory Size %llu MB",
            block_count, block_size, memory_size_mb);

    LOG_DBG("Mounting filesystem");
    const int rc = fs_mount(&mount);
    if (rc < 0) {
        LOG_ERR("Failed to mount %s, rc: %d", mount.mnt_point, rc);
        return rc;
    }

    LOG_INF("Mounted %s", mount.mnt_point);
    return rc;
}
"""

# Parser initialisieren
parser = c_parser.CParser()
ast = parser.parse(code)  # Parsing des Dummy-Codes

class PlantUMLActivityGenerator(c_ast.NodeVisitor):
    def __init__(self):
        self.activities = []
    def _expr_to_string(self, expr):
        """Hilfsfunktion, um den Ausdruck rekursiv in einen String umzuwandeln."""
        if isinstance(expr, c_ast.BinaryOp):
            left = self._expr_to_string(expr.left)
            right = self._expr_to_string(expr.right)
            return f"{left} {expr.op} {right}"
        elif isinstance(expr, c_ast.Constant):
            return expr.value
        elif isinstance(expr, c_ast.ID):
            return expr.name
        elif isinstance(expr, c_ast.FuncCall):
            return self._expr_to_string(expr.name) + "(" + ", ".join(self._expr_to_string(a) for a in expr.args.exprs) + ")"
        elif isinstance(expr, c_ast.UnaryOp):
            return expr.op + self._expr_to_string(expr.expr)
        # Erweitern Sie dies für andere Ausdruckstypen nach Bedarf
        return ""
    def visit_FuncDef(self, node):
        self.activities.append(f'partition \"{node.decl.name}\" ')
        self.generic_visit(node)

    def visit_If(self, node):
        condition = self._expr_to_string(node.cond)
        self.activities.append(f"if ({condition}) then (yes)")
        self.generic_visit(node.iftrue)
        self.activities.append("else (no)")
        self.generic_visit(node.iffalse)
        self.activities.append("endif")

    def visit_For(self, node):
        self.activities.append("repeat")
        self.generic_visit(node.stmt)
        self.activities.append("repeat while()")

    def visit_FuncCall(self, node):
        self.activities.append(f":{node.name.name}();")

    def generic_visit(self, node):
        if node is not None:
            super().generic_visit(node)

generator = PlantUMLActivityGenerator()
generator.visit(ast)

# Ausgabe des PlantUML-Aktivitätsdiagramms
print("@startuml\n|#LightYellow|Data|")
print("\n".join(generator.activities))
print("}\nend\n@enduml")
