from ..data_managers.semantic_header import SemanticHeader
from graphviz import Digraph


class Visualize:
    def __init__(self, semantic_header: SemanticHeader):
        self.semantic_header = semantic_header
        self.dot = Digraph('round-table', comment='The Round Table')

        self.dot.format = 'svg'

    def create_record_layer(self):
        records = self.semantic_header.records
        for record in records:
            print(record)

    def create_round_table(self):
        self.dot.node('A', 'King Arthur')
        self.dot.node('B', 'Sir Bedevere the Wise')
        self.dot.node('L', 'Sir Lancelot the Brave')

        self.dot.edges(['AB', 'AL'])
        self.dot.edge('B', 'L', constraint='false')
        print(self.dot.source)

        self.dot.render(directory='doctest-output', view=True)
