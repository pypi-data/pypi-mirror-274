// Generated from /Users/emrekuru/Downloads/Bologna/ANTLR/FOL.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class FOLParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, T__21=22, T__22=23, T__23=24, 
		T__24=25, T__25=26, T__26=27, T__27=28, T__28=29, T__29=30, T__30=31, 
		T__31=32, T__32=33, T__33=34, T__34=35, T__35=36, T__36=37, T__37=38, 
		T__38=39, T__39=40, T__40=41, T__41=42, T__42=43, T__43=44, T__44=45, 
		T__45=46, T__46=47, T__47=48, T__48=49, T__49=50, T__50=51, LETTER_DIGIT=52, 
		VARIABLE=53, DECIMAL=54, BINARY=55, OCTAL=56, HEX=57, CHARACTER_CODE_CONSTANT=58, 
		FLOAT=59, GRAPHIC_TOKEN=60, QUOTED=61, DOUBLE_QUOTED_LIST=62, BACK_QUOTED_STRING=63, 
		WS=64, COMMENT=65, MULTILINE_COMMENT=66;
	public static final int
		RULE_p_text = 0, RULE_directive = 1, RULE_clause = 2, RULE_termlist = 3, 
		RULE_term = 4, RULE_operator_ = 5, RULE_atom = 6, RULE_integer = 7;
	private static String[] makeRuleNames() {
		return new String[] {
			"p_text", "directive", "clause", "termlist", "term", "operator_", "atom", 
			"integer"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "':-'", "'.'", "','", "'('", "')'", "'-'", "'['", "'|'", "']'", 
			"'{'", "'}'", "'-->'", "'?-'", "'dynamic'", "'multifile'", "'discontiguous'", 
			"'public'", "';'", "'->'", "'\\+'", "'='", "'\\='", "'=='", "'\\=='", 
			"'@<'", "'@=<'", "'@>'", "'@>='", "'=..'", "'is'", "'=:='", "'=\\='", 
			"'<'", "'=<'", "'>'", "'>='", "':'", "'+'", "'/\\'", "'\\/'", "'*'", 
			"'/'", "'//'", "'rem'", "'mod'", "'<<'", "'>>'", "'**'", "'^'", "'\\'", 
			"'!'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, "LETTER_DIGIT", "VARIABLE", "DECIMAL", "BINARY", 
			"OCTAL", "HEX", "CHARACTER_CODE_CONSTANT", "FLOAT", "GRAPHIC_TOKEN", 
			"QUOTED", "DOUBLE_QUOTED_LIST", "BACK_QUOTED_STRING", "WS", "COMMENT", 
			"MULTILINE_COMMENT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "FOL.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public FOLParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class P_textContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(FOLParser.EOF, 0); }
		public List<DirectiveContext> directive() {
			return getRuleContexts(DirectiveContext.class);
		}
		public DirectiveContext directive(int i) {
			return getRuleContext(DirectiveContext.class,i);
		}
		public List<ClauseContext> clause() {
			return getRuleContexts(ClauseContext.class);
		}
		public ClauseContext clause(int i) {
			return getRuleContext(ClauseContext.class,i);
		}
		public P_textContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_p_text; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterP_text(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitP_text(this);
		}
	}

	public final P_textContext p_text() throws RecognitionException {
		P_textContext _localctx = new P_textContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_p_text);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(20);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & -2854L) != 0)) {
				{
				setState(18);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
				case 1:
					{
					setState(16);
					directive();
					}
					break;
				case 2:
					{
					setState(17);
					clause();
					}
					break;
				}
				}
				setState(22);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(23);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DirectiveContext extends ParserRuleContext {
		public TermContext term() {
			return getRuleContext(TermContext.class,0);
		}
		public DirectiveContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_directive; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterDirective(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitDirective(this);
		}
	}

	public final DirectiveContext directive() throws RecognitionException {
		DirectiveContext _localctx = new DirectiveContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_directive);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(25);
			match(T__0);
			setState(26);
			term(0);
			setState(27);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ClauseContext extends ParserRuleContext {
		public TermContext term() {
			return getRuleContext(TermContext.class,0);
		}
		public ClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_clause; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterClause(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitClause(this);
		}
	}

	public final ClauseContext clause() throws RecognitionException {
		ClauseContext _localctx = new ClauseContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_clause);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(29);
			term(0);
			setState(30);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TermlistContext extends ParserRuleContext {
		public List<TermContext> term() {
			return getRuleContexts(TermContext.class);
		}
		public TermContext term(int i) {
			return getRuleContext(TermContext.class,i);
		}
		public TermlistContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_termlist; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterTermlist(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitTermlist(this);
		}
	}

	public final TermlistContext termlist() throws RecognitionException {
		TermlistContext _localctx = new TermlistContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_termlist);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(32);
			term(0);
			setState(37);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__2) {
				{
				{
				setState(33);
				match(T__2);
				setState(34);
				term(0);
				}
				}
				setState(39);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TermContext extends ParserRuleContext {
		public TermContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_term; }
	 
		public TermContext() { }
		public void copyFrom(TermContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Atom_termContext extends TermContext {
		public AtomContext atom() {
			return getRuleContext(AtomContext.class,0);
		}
		public Atom_termContext(TermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterAtom_term(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitAtom_term(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Binary_operatorContext extends TermContext {
		public List<TermContext> term() {
			return getRuleContexts(TermContext.class);
		}
		public TermContext term(int i) {
			return getRuleContext(TermContext.class,i);
		}
		public Operator_Context operator_() {
			return getRuleContext(Operator_Context.class,0);
		}
		public Binary_operatorContext(TermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterBinary_operator(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitBinary_operator(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Unary_operatorContext extends TermContext {
		public Operator_Context operator_() {
			return getRuleContext(Operator_Context.class,0);
		}
		public TermContext term() {
			return getRuleContext(TermContext.class,0);
		}
		public Unary_operatorContext(TermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterUnary_operator(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitUnary_operator(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Braced_termContext extends TermContext {
		public TermContext term() {
			return getRuleContext(TermContext.class,0);
		}
		public Braced_termContext(TermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterBraced_term(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitBraced_term(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class List_termContext extends TermContext {
		public TermlistContext termlist() {
			return getRuleContext(TermlistContext.class,0);
		}
		public TermContext term() {
			return getRuleContext(TermContext.class,0);
		}
		public List_termContext(TermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterList_term(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitList_term(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class VariableContext extends TermContext {
		public TerminalNode VARIABLE() { return getToken(FOLParser.VARIABLE, 0); }
		public VariableContext(TermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterVariable(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitVariable(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FloatContext extends TermContext {
		public TerminalNode FLOAT() { return getToken(FOLParser.FLOAT, 0); }
		public FloatContext(TermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterFloat(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitFloat(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Compound_termContext extends TermContext {
		public AtomContext atom() {
			return getRuleContext(AtomContext.class,0);
		}
		public TermlistContext termlist() {
			return getRuleContext(TermlistContext.class,0);
		}
		public Compound_termContext(TermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterCompound_term(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitCompound_term(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Integer_termContext extends TermContext {
		public IntegerContext integer() {
			return getRuleContext(IntegerContext.class,0);
		}
		public Integer_termContext(TermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterInteger_term(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitInteger_term(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Curly_bracketed_termContext extends TermContext {
		public TermlistContext termlist() {
			return getRuleContext(TermlistContext.class,0);
		}
		public Curly_bracketed_termContext(TermContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterCurly_bracketed_term(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitCurly_bracketed_term(this);
		}
	}

	public final TermContext term() throws RecognitionException {
		return term(0);
	}

	private TermContext term(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		TermContext _localctx = new TermContext(_ctx, _parentState);
		TermContext _prevctx = _localctx;
		int _startState = 8;
		enterRecursionRule(_localctx, 8, RULE_term, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(75);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,6,_ctx) ) {
			case 1:
				{
				_localctx = new VariableContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(41);
				match(VARIABLE);
				}
				break;
			case 2:
				{
				_localctx = new Braced_termContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(42);
				match(T__3);
				setState(43);
				term(0);
				setState(44);
				match(T__4);
				}
				break;
			case 3:
				{
				_localctx = new Integer_termContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(47);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__5) {
					{
					setState(46);
					match(T__5);
					}
				}

				setState(49);
				integer();
				}
				break;
			case 4:
				{
				_localctx = new FloatContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(51);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__5) {
					{
					setState(50);
					match(T__5);
					}
				}

				setState(53);
				match(FLOAT);
				}
				break;
			case 5:
				{
				_localctx = new Compound_termContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(54);
				atom();
				setState(55);
				match(T__3);
				setState(56);
				termlist();
				setState(57);
				match(T__4);
				}
				break;
			case 6:
				{
				_localctx = new Unary_operatorContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(59);
				operator_();
				setState(60);
				term(4);
				}
				break;
			case 7:
				{
				_localctx = new List_termContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(62);
				match(T__6);
				setState(63);
				termlist();
				setState(66);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__7) {
					{
					setState(64);
					match(T__7);
					setState(65);
					term(0);
					}
				}

				setState(68);
				match(T__8);
				}
				break;
			case 8:
				{
				_localctx = new Curly_bracketed_termContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(70);
				match(T__9);
				setState(71);
				termlist();
				setState(72);
				match(T__10);
				}
				break;
			case 9:
				{
				_localctx = new Atom_termContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(74);
				atom();
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(83);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,7,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new Binary_operatorContext(new TermContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_term);
					setState(77);
					if (!(precpred(_ctx, 5))) throw new FailedPredicateException(this, "precpred(_ctx, 5)");
					setState(78);
					operator_();
					setState(79);
					term(5);
					}
					} 
				}
				setState(85);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,7,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Operator_Context extends ParserRuleContext {
		public Operator_Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_operator_; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterOperator_(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitOperator_(this);
		}
	}

	public final Operator_Context operator_() throws RecognitionException {
		Operator_Context _localctx = new Operator_Context(_ctx, getState());
		enterRule(_localctx, 10, RULE_operator_);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(86);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 2251799813681226L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AtomContext extends ParserRuleContext {
		public AtomContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_atom; }
	 
		public AtomContext() { }
		public void copyFrom(AtomContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Backq_stringContext extends AtomContext {
		public TerminalNode BACK_QUOTED_STRING() { return getToken(FOLParser.BACK_QUOTED_STRING, 0); }
		public Backq_stringContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterBackq_string(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitBackq_string(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CutContext extends AtomContext {
		public CutContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterCut(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitCut(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Empty_bracesContext extends AtomContext {
		public Empty_bracesContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterEmpty_braces(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitEmpty_braces(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Dq_stringContext extends AtomContext {
		public TerminalNode DOUBLE_QUOTED_LIST() { return getToken(FOLParser.DOUBLE_QUOTED_LIST, 0); }
		public Dq_stringContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterDq_string(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitDq_string(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NameContext extends AtomContext {
		public TerminalNode LETTER_DIGIT() { return getToken(FOLParser.LETTER_DIGIT, 0); }
		public NameContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterName(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitName(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Quoted_stringContext extends AtomContext {
		public TerminalNode QUOTED() { return getToken(FOLParser.QUOTED, 0); }
		public Quoted_stringContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterQuoted_string(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitQuoted_string(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class Empty_listContext extends AtomContext {
		public Empty_listContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterEmpty_list(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitEmpty_list(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class GraphicContext extends AtomContext {
		public TerminalNode GRAPHIC_TOKEN() { return getToken(FOLParser.GRAPHIC_TOKEN, 0); }
		public GraphicContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterGraphic(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitGraphic(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SemicolonContext extends AtomContext {
		public SemicolonContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterSemicolon(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitSemicolon(this);
		}
	}

	public final AtomContext atom() throws RecognitionException {
		AtomContext _localctx = new AtomContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_atom);
		try {
			setState(99);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__6:
				_localctx = new Empty_listContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(88);
				match(T__6);
				setState(89);
				match(T__8);
				}
				break;
			case T__9:
				_localctx = new Empty_bracesContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(90);
				match(T__9);
				setState(91);
				match(T__10);
				}
				break;
			case LETTER_DIGIT:
				_localctx = new NameContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(92);
				match(LETTER_DIGIT);
				}
				break;
			case GRAPHIC_TOKEN:
				_localctx = new GraphicContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(93);
				match(GRAPHIC_TOKEN);
				}
				break;
			case QUOTED:
				_localctx = new Quoted_stringContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(94);
				match(QUOTED);
				}
				break;
			case DOUBLE_QUOTED_LIST:
				_localctx = new Dq_stringContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(95);
				match(DOUBLE_QUOTED_LIST);
				}
				break;
			case BACK_QUOTED_STRING:
				_localctx = new Backq_stringContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(96);
				match(BACK_QUOTED_STRING);
				}
				break;
			case T__17:
				_localctx = new SemicolonContext(_localctx);
				enterOuterAlt(_localctx, 8);
				{
				setState(97);
				match(T__17);
				}
				break;
			case T__50:
				_localctx = new CutContext(_localctx);
				enterOuterAlt(_localctx, 9);
				{
				setState(98);
				match(T__50);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class IntegerContext extends ParserRuleContext {
		public TerminalNode DECIMAL() { return getToken(FOLParser.DECIMAL, 0); }
		public TerminalNode CHARACTER_CODE_CONSTANT() { return getToken(FOLParser.CHARACTER_CODE_CONSTANT, 0); }
		public TerminalNode BINARY() { return getToken(FOLParser.BINARY, 0); }
		public TerminalNode OCTAL() { return getToken(FOLParser.OCTAL, 0); }
		public TerminalNode HEX() { return getToken(FOLParser.HEX, 0); }
		public IntegerContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_integer; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).enterInteger(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof FOLListener ) ((FOLListener)listener).exitInteger(this);
		}
	}

	public final IntegerContext integer() throws RecognitionException {
		IntegerContext _localctx = new IntegerContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_integer);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(101);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 558446353793941504L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 4:
			return term_sempred((TermContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean term_sempred(TermContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 5);
		}
		return true;
	}

	public static final String _serializedATN =
		"\u0004\u0001Bh\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002\u0002"+
		"\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002\u0005"+
		"\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0001\u0000"+
		"\u0001\u0000\u0005\u0000\u0013\b\u0000\n\u0000\f\u0000\u0016\t\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0002\u0001\u0002\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0005"+
		"\u0003$\b\u0003\n\u0003\f\u0003\'\t\u0003\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0003\u00040\b"+
		"\u0004\u0001\u0004\u0001\u0004\u0003\u00044\b\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0003"+
		"\u0004C\b\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0003\u0004L\b\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0005\u0004R\b\u0004\n\u0004\f\u0004U\t"+
		"\u0004\u0001\u0005\u0001\u0005\u0001\u0006\u0001\u0006\u0001\u0006\u0001"+
		"\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001"+
		"\u0006\u0001\u0006\u0003\u0006d\b\u0006\u0001\u0007\u0001\u0007\u0001"+
		"\u0007\u0000\u0001\b\b\u0000\u0002\u0004\u0006\b\n\f\u000e\u0000\u0002"+
		"\u0004\u0000\u0001\u0001\u0003\u0003\u0006\u0006\f2\u0001\u00006:v\u0000"+
		"\u0014\u0001\u0000\u0000\u0000\u0002\u0019\u0001\u0000\u0000\u0000\u0004"+
		"\u001d\u0001\u0000\u0000\u0000\u0006 \u0001\u0000\u0000\u0000\bK\u0001"+
		"\u0000\u0000\u0000\nV\u0001\u0000\u0000\u0000\fc\u0001\u0000\u0000\u0000"+
		"\u000ee\u0001\u0000\u0000\u0000\u0010\u0013\u0003\u0002\u0001\u0000\u0011"+
		"\u0013\u0003\u0004\u0002\u0000\u0012\u0010\u0001\u0000\u0000\u0000\u0012"+
		"\u0011\u0001\u0000\u0000\u0000\u0013\u0016\u0001\u0000\u0000\u0000\u0014"+
		"\u0012\u0001\u0000\u0000\u0000\u0014\u0015\u0001\u0000\u0000\u0000\u0015"+
		"\u0017\u0001\u0000\u0000\u0000\u0016\u0014\u0001\u0000\u0000\u0000\u0017"+
		"\u0018\u0005\u0000\u0000\u0001\u0018\u0001\u0001\u0000\u0000\u0000\u0019"+
		"\u001a\u0005\u0001\u0000\u0000\u001a\u001b\u0003\b\u0004\u0000\u001b\u001c"+
		"\u0005\u0002\u0000\u0000\u001c\u0003\u0001\u0000\u0000\u0000\u001d\u001e"+
		"\u0003\b\u0004\u0000\u001e\u001f\u0005\u0002\u0000\u0000\u001f\u0005\u0001"+
		"\u0000\u0000\u0000 %\u0003\b\u0004\u0000!\"\u0005\u0003\u0000\u0000\""+
		"$\u0003\b\u0004\u0000#!\u0001\u0000\u0000\u0000$\'\u0001\u0000\u0000\u0000"+
		"%#\u0001\u0000\u0000\u0000%&\u0001\u0000\u0000\u0000&\u0007\u0001\u0000"+
		"\u0000\u0000\'%\u0001\u0000\u0000\u0000()\u0006\u0004\uffff\uffff\u0000"+
		")L\u00055\u0000\u0000*+\u0005\u0004\u0000\u0000+,\u0003\b\u0004\u0000"+
		",-\u0005\u0005\u0000\u0000-L\u0001\u0000\u0000\u0000.0\u0005\u0006\u0000"+
		"\u0000/.\u0001\u0000\u0000\u0000/0\u0001\u0000\u0000\u000001\u0001\u0000"+
		"\u0000\u00001L\u0003\u000e\u0007\u000024\u0005\u0006\u0000\u000032\u0001"+
		"\u0000\u0000\u000034\u0001\u0000\u0000\u000045\u0001\u0000\u0000\u0000"+
		"5L\u0005;\u0000\u000067\u0003\f\u0006\u000078\u0005\u0004\u0000\u0000"+
		"89\u0003\u0006\u0003\u00009:\u0005\u0005\u0000\u0000:L\u0001\u0000\u0000"+
		"\u0000;<\u0003\n\u0005\u0000<=\u0003\b\u0004\u0004=L\u0001\u0000\u0000"+
		"\u0000>?\u0005\u0007\u0000\u0000?B\u0003\u0006\u0003\u0000@A\u0005\b\u0000"+
		"\u0000AC\u0003\b\u0004\u0000B@\u0001\u0000\u0000\u0000BC\u0001\u0000\u0000"+
		"\u0000CD\u0001\u0000\u0000\u0000DE\u0005\t\u0000\u0000EL\u0001\u0000\u0000"+
		"\u0000FG\u0005\n\u0000\u0000GH\u0003\u0006\u0003\u0000HI\u0005\u000b\u0000"+
		"\u0000IL\u0001\u0000\u0000\u0000JL\u0003\f\u0006\u0000K(\u0001\u0000\u0000"+
		"\u0000K*\u0001\u0000\u0000\u0000K/\u0001\u0000\u0000\u0000K3\u0001\u0000"+
		"\u0000\u0000K6\u0001\u0000\u0000\u0000K;\u0001\u0000\u0000\u0000K>\u0001"+
		"\u0000\u0000\u0000KF\u0001\u0000\u0000\u0000KJ\u0001\u0000\u0000\u0000"+
		"LS\u0001\u0000\u0000\u0000MN\n\u0005\u0000\u0000NO\u0003\n\u0005\u0000"+
		"OP\u0003\b\u0004\u0005PR\u0001\u0000\u0000\u0000QM\u0001\u0000\u0000\u0000"+
		"RU\u0001\u0000\u0000\u0000SQ\u0001\u0000\u0000\u0000ST\u0001\u0000\u0000"+
		"\u0000T\t\u0001\u0000\u0000\u0000US\u0001\u0000\u0000\u0000VW\u0007\u0000"+
		"\u0000\u0000W\u000b\u0001\u0000\u0000\u0000XY\u0005\u0007\u0000\u0000"+
		"Yd\u0005\t\u0000\u0000Z[\u0005\n\u0000\u0000[d\u0005\u000b\u0000\u0000"+
		"\\d\u00054\u0000\u0000]d\u0005<\u0000\u0000^d\u0005=\u0000\u0000_d\u0005"+
		">\u0000\u0000`d\u0005?\u0000\u0000ad\u0005\u0012\u0000\u0000bd\u00053"+
		"\u0000\u0000cX\u0001\u0000\u0000\u0000cZ\u0001\u0000\u0000\u0000c\\\u0001"+
		"\u0000\u0000\u0000c]\u0001\u0000\u0000\u0000c^\u0001\u0000\u0000\u0000"+
		"c_\u0001\u0000\u0000\u0000c`\u0001\u0000\u0000\u0000ca\u0001\u0000\u0000"+
		"\u0000cb\u0001\u0000\u0000\u0000d\r\u0001\u0000\u0000\u0000ef\u0007\u0001"+
		"\u0000\u0000f\u000f\u0001\u0000\u0000\u0000\t\u0012\u0014%/3BKSc";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}