# Generated from ANTLR/FOL.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .FOLParser import FOLParser
else:
    from FOLParser import FOLParser

# This class defines a complete listener for a parse tree produced by FOLParser.
class FOLListener(ParseTreeListener):

    # Enter a parse tree produced by FOLParser#p_text.
    def enterP_text(self, ctx:FOLParser.P_textContext):
        pass

    # Exit a parse tree produced by FOLParser#p_text.
    def exitP_text(self, ctx:FOLParser.P_textContext):
        pass


    # Enter a parse tree produced by FOLParser#directive.
    def enterDirective(self, ctx:FOLParser.DirectiveContext):
        pass

    # Exit a parse tree produced by FOLParser#directive.
    def exitDirective(self, ctx:FOLParser.DirectiveContext):
        pass


    # Enter a parse tree produced by FOLParser#clause.
    def enterClause(self, ctx:FOLParser.ClauseContext):
        pass

    # Exit a parse tree produced by FOLParser#clause.
    def exitClause(self, ctx:FOLParser.ClauseContext):
        pass


    # Enter a parse tree produced by FOLParser#termlist.
    def enterTermlist(self, ctx:FOLParser.TermlistContext):
        pass

    # Exit a parse tree produced by FOLParser#termlist.
    def exitTermlist(self, ctx:FOLParser.TermlistContext):
        pass


    # Enter a parse tree produced by FOLParser#atom_term.
    def enterAtom_term(self, ctx:FOLParser.Atom_termContext):
        pass

    # Exit a parse tree produced by FOLParser#atom_term.
    def exitAtom_term(self, ctx:FOLParser.Atom_termContext):
        pass


    # Enter a parse tree produced by FOLParser#binary_operator.
    def enterBinary_operator(self, ctx:FOLParser.Binary_operatorContext):
        pass

    # Exit a parse tree produced by FOLParser#binary_operator.
    def exitBinary_operator(self, ctx:FOLParser.Binary_operatorContext):
        pass


    # Enter a parse tree produced by FOLParser#unary_operator.
    def enterUnary_operator(self, ctx:FOLParser.Unary_operatorContext):
        pass

    # Exit a parse tree produced by FOLParser#unary_operator.
    def exitUnary_operator(self, ctx:FOLParser.Unary_operatorContext):
        pass


    # Enter a parse tree produced by FOLParser#braced_term.
    def enterBraced_term(self, ctx:FOLParser.Braced_termContext):
        pass

    # Exit a parse tree produced by FOLParser#braced_term.
    def exitBraced_term(self, ctx:FOLParser.Braced_termContext):
        pass


    # Enter a parse tree produced by FOLParser#list_term.
    def enterList_term(self, ctx:FOLParser.List_termContext):
        pass

    # Exit a parse tree produced by FOLParser#list_term.
    def exitList_term(self, ctx:FOLParser.List_termContext):
        pass


    # Enter a parse tree produced by FOLParser#variable.
    def enterVariable(self, ctx:FOLParser.VariableContext):
        pass

    # Exit a parse tree produced by FOLParser#variable.
    def exitVariable(self, ctx:FOLParser.VariableContext):
        pass


    # Enter a parse tree produced by FOLParser#float.
    def enterFloat(self, ctx:FOLParser.FloatContext):
        pass

    # Exit a parse tree produced by FOLParser#float.
    def exitFloat(self, ctx:FOLParser.FloatContext):
        pass


    # Enter a parse tree produced by FOLParser#compound_term.
    def enterCompound_term(self, ctx:FOLParser.Compound_termContext):
        pass

    # Exit a parse tree produced by FOLParser#compound_term.
    def exitCompound_term(self, ctx:FOLParser.Compound_termContext):
        pass


    # Enter a parse tree produced by FOLParser#integer_term.
    def enterInteger_term(self, ctx:FOLParser.Integer_termContext):
        pass

    # Exit a parse tree produced by FOLParser#integer_term.
    def exitInteger_term(self, ctx:FOLParser.Integer_termContext):
        pass


    # Enter a parse tree produced by FOLParser#curly_bracketed_term.
    def enterCurly_bracketed_term(self, ctx:FOLParser.Curly_bracketed_termContext):
        pass

    # Exit a parse tree produced by FOLParser#curly_bracketed_term.
    def exitCurly_bracketed_term(self, ctx:FOLParser.Curly_bracketed_termContext):
        pass


    # Enter a parse tree produced by FOLParser#operator_.
    def enterOperator_(self, ctx:FOLParser.Operator_Context):
        pass

    # Exit a parse tree produced by FOLParser#operator_.
    def exitOperator_(self, ctx:FOLParser.Operator_Context):
        pass


    # Enter a parse tree produced by FOLParser#empty_list.
    def enterEmpty_list(self, ctx:FOLParser.Empty_listContext):
        pass

    # Exit a parse tree produced by FOLParser#empty_list.
    def exitEmpty_list(self, ctx:FOLParser.Empty_listContext):
        pass


    # Enter a parse tree produced by FOLParser#empty_braces.
    def enterEmpty_braces(self, ctx:FOLParser.Empty_bracesContext):
        pass

    # Exit a parse tree produced by FOLParser#empty_braces.
    def exitEmpty_braces(self, ctx:FOLParser.Empty_bracesContext):
        pass


    # Enter a parse tree produced by FOLParser#name.
    def enterName(self, ctx:FOLParser.NameContext):
        pass

    # Exit a parse tree produced by FOLParser#name.
    def exitName(self, ctx:FOLParser.NameContext):
        pass


    # Enter a parse tree produced by FOLParser#graphic.
    def enterGraphic(self, ctx:FOLParser.GraphicContext):
        pass

    # Exit a parse tree produced by FOLParser#graphic.
    def exitGraphic(self, ctx:FOLParser.GraphicContext):
        pass


    # Enter a parse tree produced by FOLParser#quoted_string.
    def enterQuoted_string(self, ctx:FOLParser.Quoted_stringContext):
        pass

    # Exit a parse tree produced by FOLParser#quoted_string.
    def exitQuoted_string(self, ctx:FOLParser.Quoted_stringContext):
        pass


    # Enter a parse tree produced by FOLParser#dq_string.
    def enterDq_string(self, ctx:FOLParser.Dq_stringContext):
        pass

    # Exit a parse tree produced by FOLParser#dq_string.
    def exitDq_string(self, ctx:FOLParser.Dq_stringContext):
        pass


    # Enter a parse tree produced by FOLParser#backq_string.
    def enterBackq_string(self, ctx:FOLParser.Backq_stringContext):
        pass

    # Exit a parse tree produced by FOLParser#backq_string.
    def exitBackq_string(self, ctx:FOLParser.Backq_stringContext):
        pass


    # Enter a parse tree produced by FOLParser#semicolon.
    def enterSemicolon(self, ctx:FOLParser.SemicolonContext):
        pass

    # Exit a parse tree produced by FOLParser#semicolon.
    def exitSemicolon(self, ctx:FOLParser.SemicolonContext):
        pass


    # Enter a parse tree produced by FOLParser#cut.
    def enterCut(self, ctx:FOLParser.CutContext):
        pass

    # Exit a parse tree produced by FOLParser#cut.
    def exitCut(self, ctx:FOLParser.CutContext):
        pass


    # Enter a parse tree produced by FOLParser#integer.
    def enterInteger(self, ctx:FOLParser.IntegerContext):
        pass

    # Exit a parse tree produced by FOLParser#integer.
    def exitInteger(self, ctx:FOLParser.IntegerContext):
        pass



del FOLParser