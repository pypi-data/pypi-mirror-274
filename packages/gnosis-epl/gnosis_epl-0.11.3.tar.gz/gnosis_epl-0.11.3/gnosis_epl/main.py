from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from .grammar.GnosisEPLLexer import GnosisEPLLexer
from .grammar.GnosisEPLParser import GnosisEPLParser
from .grammar.epl_listener import ToDictionaryEPLListener


class QueryParser():

    def parse(self, query_text):
        lexer = GnosisEPLLexer(InputStream(query_text))
        stream = CommonTokenStream(lexer)
        parser = GnosisEPLParser(stream)
        tree = parser.query()

        listener = ToDictionaryEPLListener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener.query
