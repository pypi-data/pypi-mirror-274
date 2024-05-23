from .GnosisEPLListener import GnosisEPLListener


class GnosisEPLParserException(RuntimeError):
    """
    Exception raised by any error during the parse of the query
    """

    def __init__(self, node):
        payload = node.getPayload()
        symbol = node.getText()
        message = "Error parsing query. '{}' is not valid in the line {}:{}".format(
            symbol,
            payload.line,
            payload.column,
            payload
        )
        self.message = message
        self.node = node
        super(GnosisEPLParserException, self).__init__(message)


class ToDictionaryEPLListener(GnosisEPLListener):

    def __init__(self):
        self.query = {}

    def int_or_str_cast(self, value):
        try:
            return int(value)
        except ValueError:
            return value

    def enterWindow(self, ctx):
        args = [self.int_or_str_cast(arg.getText()) for arg in ctx.window_arg_list().window_arg()]
        window = {
            'window_type': ctx.window_type().getText(),
            'args': args
        }
        self.query['window'] = window

    def enterQuery_name(self, ctx):
        self.query['name'] = ctx.getText()

    def enterOutput_list(self, ctx):
        self.query['output'] = [p.getText() for p in ctx.output()]

    def enterContent(self, ctx):
        self.query['content'] = [c.getText() for c in ctx.content_service()]

    def enterPublisher_list(self, ctx):
        self.query['from'] = [p.getText() for p in ctx.publisher()]

    def enterMatch_clause(self, ctx):
        match = f'MATCH {ctx.getText()}'
        is_optional = 'match' in self.query.keys()
        key = 'match'
        if is_optional:
            match = f'OPTIONAL {match}'
            key = 'optional_match'
        self.query[key] = match

    def enterWhere_clause(self, ctx):
        self.query['where'] = f'WHERE {ctx.getText()}'

    def enterQos_metric_list(self, ctx):
        self.query['qos_policies'] = {}

    def enterQos_metric(self, ctx):
        name = ctx.qos_metric_name().getText()
        attr_value_ctx = ctx.qos_metric_value().attribute_value()

        num_val = attr_value_ctx.attribute_value_num()
        if num_val:
            val = float(num_val.getText())
        else:
            str_val_list = attr_value_ctx.attribute_value_str().attribute_value_str_inner()
            val = ''.join([v.getText() for v in str_val_list])
        self.query['qos_policies'][name] = val

    def enterNode_list(self, ctx):
        self.query['ret'] = f'RETURN {ctx.getText()}'

    def visitErrorNode(self, node):
        raise GnosisEPLParserException(node)
