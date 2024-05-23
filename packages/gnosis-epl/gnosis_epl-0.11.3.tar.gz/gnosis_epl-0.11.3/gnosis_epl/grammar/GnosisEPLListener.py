# Generated from tools/antlr/GnosisEPL.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GnosisEPLParser import GnosisEPLParser
else:
    from GnosisEPLParser import GnosisEPLParser

# This class defines a complete listener for a parse tree produced by GnosisEPLParser.
class GnosisEPLListener(ParseTreeListener):

    # Enter a parse tree produced by GnosisEPLParser#alphanumeric.
    def enterAlphanumeric(self, ctx:GnosisEPLParser.AlphanumericContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#alphanumeric.
    def exitAlphanumeric(self, ctx:GnosisEPLParser.AlphanumericContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#comparison_operator.
    def enterComparison_operator(self, ctx:GnosisEPLParser.Comparison_operatorContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#comparison_operator.
    def exitComparison_operator(self, ctx:GnosisEPLParser.Comparison_operatorContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#query.
    def enterQuery(self, ctx:GnosisEPLParser.QueryContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#query.
    def exitQuery(self, ctx:GnosisEPLParser.QueryContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#subcription.
    def enterSubcription(self, ctx:GnosisEPLParser.SubcriptionContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#subcription.
    def exitSubcription(self, ctx:GnosisEPLParser.SubcriptionContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#query_name.
    def enterQuery_name(self, ctx:GnosisEPLParser.Query_nameContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#query_name.
    def exitQuery_name(self, ctx:GnosisEPLParser.Query_nameContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#output_list.
    def enterOutput_list(self, ctx:GnosisEPLParser.Output_listContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#output_list.
    def exitOutput_list(self, ctx:GnosisEPLParser.Output_listContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#output.
    def enterOutput(self, ctx:GnosisEPLParser.OutputContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#output.
    def exitOutput(self, ctx:GnosisEPLParser.OutputContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#separator.
    def enterSeparator(self, ctx:GnosisEPLParser.SeparatorContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#separator.
    def exitSeparator(self, ctx:GnosisEPLParser.SeparatorContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#content.
    def enterContent(self, ctx:GnosisEPLParser.ContentContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#content.
    def exitContent(self, ctx:GnosisEPLParser.ContentContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#content_service.
    def enterContent_service(self, ctx:GnosisEPLParser.Content_serviceContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#content_service.
    def exitContent_service(self, ctx:GnosisEPLParser.Content_serviceContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#match_clause.
    def enterMatch_clause(self, ctx:GnosisEPLParser.Match_clauseContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#match_clause.
    def exitMatch_clause(self, ctx:GnosisEPLParser.Match_clauseContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#relationship.
    def enterRelationship(self, ctx:GnosisEPLParser.RelationshipContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#relationship.
    def exitRelationship(self, ctx:GnosisEPLParser.RelationshipContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#relationship_ref_with_class.
    def enterRelationship_ref_with_class(self, ctx:GnosisEPLParser.Relationship_ref_with_classContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#relationship_ref_with_class.
    def exitRelationship_ref_with_class(self, ctx:GnosisEPLParser.Relationship_ref_with_classContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#relationship_ref_middle.
    def enterRelationship_ref_middle(self, ctx:GnosisEPLParser.Relationship_ref_middleContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#relationship_ref_middle.
    def exitRelationship_ref_middle(self, ctx:GnosisEPLParser.Relationship_ref_middleContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#relationship_type.
    def enterRelationship_type(self, ctx:GnosisEPLParser.Relationship_typeContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#relationship_type.
    def exitRelationship_type(self, ctx:GnosisEPLParser.Relationship_typeContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#left_object.
    def enterLeft_object(self, ctx:GnosisEPLParser.Left_objectContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#left_object.
    def exitLeft_object(self, ctx:GnosisEPLParser.Left_objectContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#right_object.
    def enterRight_object(self, ctx:GnosisEPLParser.Right_objectContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#right_object.
    def exitRight_object(self, ctx:GnosisEPLParser.Right_objectContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#object_ref_with_class.
    def enterObject_ref_with_class(self, ctx:GnosisEPLParser.Object_ref_with_classContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#object_ref_with_class.
    def exitObject_ref_with_class(self, ctx:GnosisEPLParser.Object_ref_with_classContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#object_class.
    def enterObject_class(self, ctx:GnosisEPLParser.Object_classContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#object_class.
    def exitObject_class(self, ctx:GnosisEPLParser.Object_classContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#object_ref.
    def enterObject_ref(self, ctx:GnosisEPLParser.Object_refContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#object_ref.
    def exitObject_ref(self, ctx:GnosisEPLParser.Object_refContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#attributes.
    def enterAttributes(self, ctx:GnosisEPLParser.AttributesContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#attributes.
    def exitAttributes(self, ctx:GnosisEPLParser.AttributesContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#attribute.
    def enterAttribute(self, ctx:GnosisEPLParser.AttributeContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#attribute.
    def exitAttribute(self, ctx:GnosisEPLParser.AttributeContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#attribute_name.
    def enterAttribute_name(self, ctx:GnosisEPLParser.Attribute_nameContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#attribute_name.
    def exitAttribute_name(self, ctx:GnosisEPLParser.Attribute_nameContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#attribute_value.
    def enterAttribute_value(self, ctx:GnosisEPLParser.Attribute_valueContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#attribute_value.
    def exitAttribute_value(self, ctx:GnosisEPLParser.Attribute_valueContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#attribute_value_str.
    def enterAttribute_value_str(self, ctx:GnosisEPLParser.Attribute_value_strContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#attribute_value_str.
    def exitAttribute_value_str(self, ctx:GnosisEPLParser.Attribute_value_strContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#attribute_value_str_inner.
    def enterAttribute_value_str_inner(self, ctx:GnosisEPLParser.Attribute_value_str_innerContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#attribute_value_str_inner.
    def exitAttribute_value_str_inner(self, ctx:GnosisEPLParser.Attribute_value_str_innerContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#attribute_value_num.
    def enterAttribute_value_num(self, ctx:GnosisEPLParser.Attribute_value_numContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#attribute_value_num.
    def exitAttribute_value_num(self, ctx:GnosisEPLParser.Attribute_value_numContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#logical_operator.
    def enterLogical_operator(self, ctx:GnosisEPLParser.Logical_operatorContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#logical_operator.
    def exitLogical_operator(self, ctx:GnosisEPLParser.Logical_operatorContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#where_clause.
    def enterWhere_clause(self, ctx:GnosisEPLParser.Where_clauseContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#where_clause.
    def exitWhere_clause(self, ctx:GnosisEPLParser.Where_clauseContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#where_logical_op_set.
    def enterWhere_logical_op_set(self, ctx:GnosisEPLParser.Where_logical_op_setContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#where_logical_op_set.
    def exitWhere_logical_op_set(self, ctx:GnosisEPLParser.Where_logical_op_setContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#where_attribute.
    def enterWhere_attribute(self, ctx:GnosisEPLParser.Where_attributeContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#where_attribute.
    def exitWhere_attribute(self, ctx:GnosisEPLParser.Where_attributeContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#where_attribute_name.
    def enterWhere_attribute_name(self, ctx:GnosisEPLParser.Where_attribute_nameContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#where_attribute_name.
    def exitWhere_attribute_name(self, ctx:GnosisEPLParser.Where_attribute_nameContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#publisher_list.
    def enterPublisher_list(self, ctx:GnosisEPLParser.Publisher_listContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#publisher_list.
    def exitPublisher_list(self, ctx:GnosisEPLParser.Publisher_listContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#publisher.
    def enterPublisher(self, ctx:GnosisEPLParser.PublisherContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#publisher.
    def exitPublisher(self, ctx:GnosisEPLParser.PublisherContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#window.
    def enterWindow(self, ctx:GnosisEPLParser.WindowContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#window.
    def exitWindow(self, ctx:GnosisEPLParser.WindowContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#window_type.
    def enterWindow_type(self, ctx:GnosisEPLParser.Window_typeContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#window_type.
    def exitWindow_type(self, ctx:GnosisEPLParser.Window_typeContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#window_arg_list.
    def enterWindow_arg_list(self, ctx:GnosisEPLParser.Window_arg_listContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#window_arg_list.
    def exitWindow_arg_list(self, ctx:GnosisEPLParser.Window_arg_listContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#window_arg.
    def enterWindow_arg(self, ctx:GnosisEPLParser.Window_argContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#window_arg.
    def exitWindow_arg(self, ctx:GnosisEPLParser.Window_argContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#qos_metric_list.
    def enterQos_metric_list(self, ctx:GnosisEPLParser.Qos_metric_listContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#qos_metric_list.
    def exitQos_metric_list(self, ctx:GnosisEPLParser.Qos_metric_listContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#qos_metric.
    def enterQos_metric(self, ctx:GnosisEPLParser.Qos_metricContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#qos_metric.
    def exitQos_metric(self, ctx:GnosisEPLParser.Qos_metricContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#qos_metric_name.
    def enterQos_metric_name(self, ctx:GnosisEPLParser.Qos_metric_nameContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#qos_metric_name.
    def exitQos_metric_name(self, ctx:GnosisEPLParser.Qos_metric_nameContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#qos_metric_value.
    def enterQos_metric_value(self, ctx:GnosisEPLParser.Qos_metric_valueContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#qos_metric_value.
    def exitQos_metric_value(self, ctx:GnosisEPLParser.Qos_metric_valueContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#return_clause.
    def enterReturn_clause(self, ctx:GnosisEPLParser.Return_clauseContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#return_clause.
    def exitReturn_clause(self, ctx:GnosisEPLParser.Return_clauseContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#node_list.
    def enterNode_list(self, ctx:GnosisEPLParser.Node_listContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#node_list.
    def exitNode_list(self, ctx:GnosisEPLParser.Node_listContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#node.
    def enterNode(self, ctx:GnosisEPLParser.NodeContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#node.
    def exitNode(self, ctx:GnosisEPLParser.NodeContext):
        pass


    # Enter a parse tree produced by GnosisEPLParser#aggregator.
    def enterAggregator(self, ctx:GnosisEPLParser.AggregatorContext):
        pass

    # Exit a parse tree produced by GnosisEPLParser#aggregator.
    def exitAggregator(self, ctx:GnosisEPLParser.AggregatorContext):
        pass



del GnosisEPLParser