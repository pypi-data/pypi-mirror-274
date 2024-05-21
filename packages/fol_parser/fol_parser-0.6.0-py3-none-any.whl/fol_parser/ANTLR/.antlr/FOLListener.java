// Generated from /Users/emrekuru/Downloads/Bologna/ANTLR/FOL.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link FOLParser}.
 */
public interface FOLListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link FOLParser#p_text}.
	 * @param ctx the parse tree
	 */
	void enterP_text(FOLParser.P_textContext ctx);
	/**
	 * Exit a parse tree produced by {@link FOLParser#p_text}.
	 * @param ctx the parse tree
	 */
	void exitP_text(FOLParser.P_textContext ctx);
	/**
	 * Enter a parse tree produced by {@link FOLParser#directive}.
	 * @param ctx the parse tree
	 */
	void enterDirective(FOLParser.DirectiveContext ctx);
	/**
	 * Exit a parse tree produced by {@link FOLParser#directive}.
	 * @param ctx the parse tree
	 */
	void exitDirective(FOLParser.DirectiveContext ctx);
	/**
	 * Enter a parse tree produced by {@link FOLParser#clause}.
	 * @param ctx the parse tree
	 */
	void enterClause(FOLParser.ClauseContext ctx);
	/**
	 * Exit a parse tree produced by {@link FOLParser#clause}.
	 * @param ctx the parse tree
	 */
	void exitClause(FOLParser.ClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link FOLParser#termlist}.
	 * @param ctx the parse tree
	 */
	void enterTermlist(FOLParser.TermlistContext ctx);
	/**
	 * Exit a parse tree produced by {@link FOLParser#termlist}.
	 * @param ctx the parse tree
	 */
	void exitTermlist(FOLParser.TermlistContext ctx);
	/**
	 * Enter a parse tree produced by the {@code atom_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void enterAtom_term(FOLParser.Atom_termContext ctx);
	/**
	 * Exit a parse tree produced by the {@code atom_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void exitAtom_term(FOLParser.Atom_termContext ctx);
	/**
	 * Enter a parse tree produced by the {@code binary_operator}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void enterBinary_operator(FOLParser.Binary_operatorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code binary_operator}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void exitBinary_operator(FOLParser.Binary_operatorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unary_operator}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void enterUnary_operator(FOLParser.Unary_operatorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unary_operator}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void exitUnary_operator(FOLParser.Unary_operatorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code braced_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void enterBraced_term(FOLParser.Braced_termContext ctx);
	/**
	 * Exit a parse tree produced by the {@code braced_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void exitBraced_term(FOLParser.Braced_termContext ctx);
	/**
	 * Enter a parse tree produced by the {@code list_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void enterList_term(FOLParser.List_termContext ctx);
	/**
	 * Exit a parse tree produced by the {@code list_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void exitList_term(FOLParser.List_termContext ctx);
	/**
	 * Enter a parse tree produced by the {@code variable}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void enterVariable(FOLParser.VariableContext ctx);
	/**
	 * Exit a parse tree produced by the {@code variable}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void exitVariable(FOLParser.VariableContext ctx);
	/**
	 * Enter a parse tree produced by the {@code float}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void enterFloat(FOLParser.FloatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code float}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void exitFloat(FOLParser.FloatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code compound_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void enterCompound_term(FOLParser.Compound_termContext ctx);
	/**
	 * Exit a parse tree produced by the {@code compound_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void exitCompound_term(FOLParser.Compound_termContext ctx);
	/**
	 * Enter a parse tree produced by the {@code integer_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void enterInteger_term(FOLParser.Integer_termContext ctx);
	/**
	 * Exit a parse tree produced by the {@code integer_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void exitInteger_term(FOLParser.Integer_termContext ctx);
	/**
	 * Enter a parse tree produced by the {@code curly_bracketed_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void enterCurly_bracketed_term(FOLParser.Curly_bracketed_termContext ctx);
	/**
	 * Exit a parse tree produced by the {@code curly_bracketed_term}
	 * labeled alternative in {@link FOLParser#term}.
	 * @param ctx the parse tree
	 */
	void exitCurly_bracketed_term(FOLParser.Curly_bracketed_termContext ctx);
	/**
	 * Enter a parse tree produced by {@link FOLParser#operator_}.
	 * @param ctx the parse tree
	 */
	void enterOperator_(FOLParser.Operator_Context ctx);
	/**
	 * Exit a parse tree produced by {@link FOLParser#operator_}.
	 * @param ctx the parse tree
	 */
	void exitOperator_(FOLParser.Operator_Context ctx);
	/**
	 * Enter a parse tree produced by the {@code empty_list}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterEmpty_list(FOLParser.Empty_listContext ctx);
	/**
	 * Exit a parse tree produced by the {@code empty_list}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitEmpty_list(FOLParser.Empty_listContext ctx);
	/**
	 * Enter a parse tree produced by the {@code empty_braces}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterEmpty_braces(FOLParser.Empty_bracesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code empty_braces}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitEmpty_braces(FOLParser.Empty_bracesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code name}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterName(FOLParser.NameContext ctx);
	/**
	 * Exit a parse tree produced by the {@code name}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitName(FOLParser.NameContext ctx);
	/**
	 * Enter a parse tree produced by the {@code graphic}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterGraphic(FOLParser.GraphicContext ctx);
	/**
	 * Exit a parse tree produced by the {@code graphic}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitGraphic(FOLParser.GraphicContext ctx);
	/**
	 * Enter a parse tree produced by the {@code quoted_string}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterQuoted_string(FOLParser.Quoted_stringContext ctx);
	/**
	 * Exit a parse tree produced by the {@code quoted_string}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitQuoted_string(FOLParser.Quoted_stringContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dq_string}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterDq_string(FOLParser.Dq_stringContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dq_string}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitDq_string(FOLParser.Dq_stringContext ctx);
	/**
	 * Enter a parse tree produced by the {@code backq_string}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterBackq_string(FOLParser.Backq_stringContext ctx);
	/**
	 * Exit a parse tree produced by the {@code backq_string}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitBackq_string(FOLParser.Backq_stringContext ctx);
	/**
	 * Enter a parse tree produced by the {@code semicolon}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterSemicolon(FOLParser.SemicolonContext ctx);
	/**
	 * Exit a parse tree produced by the {@code semicolon}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitSemicolon(FOLParser.SemicolonContext ctx);
	/**
	 * Enter a parse tree produced by the {@code cut}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterCut(FOLParser.CutContext ctx);
	/**
	 * Exit a parse tree produced by the {@code cut}
	 * labeled alternative in {@link FOLParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitCut(FOLParser.CutContext ctx);
	/**
	 * Enter a parse tree produced by {@link FOLParser#integer}.
	 * @param ctx the parse tree
	 */
	void enterInteger(FOLParser.IntegerContext ctx);
	/**
	 * Exit a parse tree produced by {@link FOLParser#integer}.
	 * @param ctx the parse tree
	 */
	void exitInteger(FOLParser.IntegerContext ctx);
}