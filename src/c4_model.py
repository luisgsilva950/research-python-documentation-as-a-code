import graphviz


class C4DiagramBuilder:
    def __init__(self):
        self.graph = graphviz.Digraph()

    def add_system(self, system_name):
        self.graph.node(system_name, shape='box', style='rounded, filled', fillcolor='#1168bd', fontcolor='white')

    def add_container(self, container_name, system_name):
        self.graph.node(container_name, shape='component', style='rounded, filled', fillcolor='#4392f1',
                        fontcolor='white')
        self.graph.edge(system_name, container_name)

    def add_component(self, component_name, container_name):
        self.graph.node(component_name, shape='box', style='rounded, filled', fillcolor='#7fa8d4', fontcolor='white')
        self.graph.edge(container_name, component_name)

    def render(self, filename, format='svg'):
        self.graph.format = format
        self.graph.render(filename, cleanup=True)


if __name__ == '__main__':
    builder = C4DiagramBuilder()

    builder.add_system("System A")
    builder.add_container("Container A1", "System A")
    builder.add_container("Container A2", "System A")
    builder.add_component("Component A1.1", "Container A1")
    builder.add_component("Component A1.2", "Container A1")
    builder.add_component("Component A2.1", "Container A2")

    builder.render("c4_diagram")
