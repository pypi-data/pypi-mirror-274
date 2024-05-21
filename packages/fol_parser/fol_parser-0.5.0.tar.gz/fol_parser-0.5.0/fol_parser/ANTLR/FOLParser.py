# Generated from ANTLR/FOL.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,66,104,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,1,0,5,0,19,8,0,10,0,12,0,22,9,0,1,0,1,0,1,1,1,1,1,
        1,1,1,1,2,1,2,1,2,1,3,1,3,1,3,5,3,36,8,3,10,3,12,3,39,9,3,1,4,1,
        4,1,4,1,4,1,4,1,4,1,4,3,4,48,8,4,1,4,1,4,3,4,52,8,4,1,4,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,3,4,67,8,4,1,4,1,4,1,4,1,
        4,1,4,1,4,1,4,3,4,76,8,4,1,4,1,4,1,4,1,4,5,4,82,8,4,10,4,12,4,85,
        9,4,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,100,
        8,6,1,7,1,7,1,7,0,1,8,8,0,2,4,6,8,10,12,14,0,2,4,0,1,1,3,3,6,6,12,
        50,1,0,54,58,118,0,20,1,0,0,0,2,25,1,0,0,0,4,29,1,0,0,0,6,32,1,0,
        0,0,8,75,1,0,0,0,10,86,1,0,0,0,12,99,1,0,0,0,14,101,1,0,0,0,16,19,
        3,2,1,0,17,19,3,4,2,0,18,16,1,0,0,0,18,17,1,0,0,0,19,22,1,0,0,0,
        20,18,1,0,0,0,20,21,1,0,0,0,21,23,1,0,0,0,22,20,1,0,0,0,23,24,5,
        0,0,1,24,1,1,0,0,0,25,26,5,1,0,0,26,27,3,8,4,0,27,28,5,2,0,0,28,
        3,1,0,0,0,29,30,3,8,4,0,30,31,5,2,0,0,31,5,1,0,0,0,32,37,3,8,4,0,
        33,34,5,3,0,0,34,36,3,8,4,0,35,33,1,0,0,0,36,39,1,0,0,0,37,35,1,
        0,0,0,37,38,1,0,0,0,38,7,1,0,0,0,39,37,1,0,0,0,40,41,6,4,-1,0,41,
        76,5,53,0,0,42,43,5,4,0,0,43,44,3,8,4,0,44,45,5,5,0,0,45,76,1,0,
        0,0,46,48,5,6,0,0,47,46,1,0,0,0,47,48,1,0,0,0,48,49,1,0,0,0,49,76,
        3,14,7,0,50,52,5,6,0,0,51,50,1,0,0,0,51,52,1,0,0,0,52,53,1,0,0,0,
        53,76,5,59,0,0,54,55,3,12,6,0,55,56,5,4,0,0,56,57,3,6,3,0,57,58,
        5,5,0,0,58,76,1,0,0,0,59,60,3,10,5,0,60,61,3,8,4,4,61,76,1,0,0,0,
        62,63,5,7,0,0,63,66,3,6,3,0,64,65,5,8,0,0,65,67,3,8,4,0,66,64,1,
        0,0,0,66,67,1,0,0,0,67,68,1,0,0,0,68,69,5,9,0,0,69,76,1,0,0,0,70,
        71,5,10,0,0,71,72,3,6,3,0,72,73,5,11,0,0,73,76,1,0,0,0,74,76,3,12,
        6,0,75,40,1,0,0,0,75,42,1,0,0,0,75,47,1,0,0,0,75,51,1,0,0,0,75,54,
        1,0,0,0,75,59,1,0,0,0,75,62,1,0,0,0,75,70,1,0,0,0,75,74,1,0,0,0,
        76,83,1,0,0,0,77,78,10,5,0,0,78,79,3,10,5,0,79,80,3,8,4,5,80,82,
        1,0,0,0,81,77,1,0,0,0,82,85,1,0,0,0,83,81,1,0,0,0,83,84,1,0,0,0,
        84,9,1,0,0,0,85,83,1,0,0,0,86,87,7,0,0,0,87,11,1,0,0,0,88,89,5,7,
        0,0,89,100,5,9,0,0,90,91,5,10,0,0,91,100,5,11,0,0,92,100,5,52,0,
        0,93,100,5,60,0,0,94,100,5,61,0,0,95,100,5,62,0,0,96,100,5,63,0,
        0,97,100,5,18,0,0,98,100,5,51,0,0,99,88,1,0,0,0,99,90,1,0,0,0,99,
        92,1,0,0,0,99,93,1,0,0,0,99,94,1,0,0,0,99,95,1,0,0,0,99,96,1,0,0,
        0,99,97,1,0,0,0,99,98,1,0,0,0,100,13,1,0,0,0,101,102,7,1,0,0,102,
        15,1,0,0,0,9,18,20,37,47,51,66,75,83,99
    ]

class FOLParser ( Parser ):

    grammarFileName = "FOL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "':-'", "'.'", "','", "'('", "')'", "'-'", 
                     "'['", "'|'", "']'", "'{'", "'}'", "'-->'", "'?-'", 
                     "'dynamic'", "'multifile'", "'discontiguous'", "'public'", 
                     "';'", "'->'", "'\\+'", "'='", "'\\='", "'=='", "'\\=='", 
                     "'@<'", "'@=<'", "'@>'", "'@>='", "'=..'", "'is'", 
                     "'=:='", "'=\\='", "'<'", "'=<'", "'>'", "'>='", "':'", 
                     "'+'", "'/\\'", "'\\/'", "'*'", "'/'", "'//'", "'rem'", 
                     "'mod'", "'<<'", "'>>'", "'**'", "'^'", "'\\'", "'!'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "LETTER_DIGIT", "VARIABLE", "DECIMAL", "BINARY", "OCTAL", 
                      "HEX", "CHARACTER_CODE_CONSTANT", "FLOAT", "GRAPHIC_TOKEN", 
                      "QUOTED", "DOUBLE_QUOTED_LIST", "BACK_QUOTED_STRING", 
                      "WS", "COMMENT", "MULTILINE_COMMENT" ]

    RULE_p_text = 0
    RULE_directive = 1
    RULE_clause = 2
    RULE_termlist = 3
    RULE_term = 4
    RULE_operator_ = 5
    RULE_atom = 6
    RULE_integer = 7

    ruleNames =  [ "p_text", "directive", "clause", "termlist", "term", 
                   "operator_", "atom", "integer" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    T__37=38
    T__38=39
    T__39=40
    T__40=41
    T__41=42
    T__42=43
    T__43=44
    T__44=45
    T__45=46
    T__46=47
    T__47=48
    T__48=49
    T__49=50
    T__50=51
    LETTER_DIGIT=52
    VARIABLE=53
    DECIMAL=54
    BINARY=55
    OCTAL=56
    HEX=57
    CHARACTER_CODE_CONSTANT=58
    FLOAT=59
    GRAPHIC_TOKEN=60
    QUOTED=61
    DOUBLE_QUOTED_LIST=62
    BACK_QUOTED_STRING=63
    WS=64
    COMMENT=65
    MULTILINE_COMMENT=66

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class P_textContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(FOLParser.EOF, 0)

        def directive(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FOLParser.DirectiveContext)
            else:
                return self.getTypedRuleContext(FOLParser.DirectiveContext,i)


        def clause(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FOLParser.ClauseContext)
            else:
                return self.getTypedRuleContext(FOLParser.ClauseContext,i)


        def getRuleIndex(self):
            return FOLParser.RULE_p_text

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterP_text" ):
                listener.enterP_text(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitP_text" ):
                listener.exitP_text(self)




    def p_text(self):

        localctx = FOLParser.P_textContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_p_text)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & -2854) != 0):
                self.state = 18
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 16
                    self.directive()
                    pass

                elif la_ == 2:
                    self.state = 17
                    self.clause()
                    pass


                self.state = 22
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 23
            self.match(FOLParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DirectiveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self):
            return self.getTypedRuleContext(FOLParser.TermContext,0)


        def getRuleIndex(self):
            return FOLParser.RULE_directive

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirective" ):
                listener.enterDirective(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirective" ):
                listener.exitDirective(self)




    def directive(self):

        localctx = FOLParser.DirectiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_directive)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25
            self.match(FOLParser.T__0)
            self.state = 26
            self.term(0)
            self.state = 27
            self.match(FOLParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClauseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self):
            return self.getTypedRuleContext(FOLParser.TermContext,0)


        def getRuleIndex(self):
            return FOLParser.RULE_clause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClause" ):
                listener.enterClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClause" ):
                listener.exitClause(self)




    def clause(self):

        localctx = FOLParser.ClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_clause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self.term(0)
            self.state = 30
            self.match(FOLParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermlistContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FOLParser.TermContext)
            else:
                return self.getTypedRuleContext(FOLParser.TermContext,i)


        def getRuleIndex(self):
            return FOLParser.RULE_termlist

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTermlist" ):
                listener.enterTermlist(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTermlist" ):
                listener.exitTermlist(self)




    def termlist(self):

        localctx = FOLParser.TermlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_termlist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.term(0)
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3:
                self.state = 33
                self.match(FOLParser.T__2)
                self.state = 34
                self.term(0)
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FOLParser.RULE_term

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class Atom_termContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(FOLParser.AtomContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom_term" ):
                listener.enterAtom_term(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom_term" ):
                listener.exitAtom_term(self)


    class Binary_operatorContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FOLParser.TermContext)
            else:
                return self.getTypedRuleContext(FOLParser.TermContext,i)

        def operator_(self):
            return self.getTypedRuleContext(FOLParser.Operator_Context,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinary_operator" ):
                listener.enterBinary_operator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinary_operator" ):
                listener.exitBinary_operator(self)


    class Unary_operatorContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def operator_(self):
            return self.getTypedRuleContext(FOLParser.Operator_Context,0)

        def term(self):
            return self.getTypedRuleContext(FOLParser.TermContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnary_operator" ):
                listener.enterUnary_operator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnary_operator" ):
                listener.exitUnary_operator(self)


    class Braced_termContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self):
            return self.getTypedRuleContext(FOLParser.TermContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBraced_term" ):
                listener.enterBraced_term(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBraced_term" ):
                listener.exitBraced_term(self)


    class List_termContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def termlist(self):
            return self.getTypedRuleContext(FOLParser.TermlistContext,0)

        def term(self):
            return self.getTypedRuleContext(FOLParser.TermContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterList_term" ):
                listener.enterList_term(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitList_term" ):
                listener.exitList_term(self)


    class VariableContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VARIABLE(self):
            return self.getToken(FOLParser.VARIABLE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariable" ):
                listener.enterVariable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariable" ):
                listener.exitVariable(self)


    class FloatContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(FOLParser.FLOAT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFloat" ):
                listener.enterFloat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFloat" ):
                listener.exitFloat(self)


    class Compound_termContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(FOLParser.AtomContext,0)

        def termlist(self):
            return self.getTypedRuleContext(FOLParser.TermlistContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompound_term" ):
                listener.enterCompound_term(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompound_term" ):
                listener.exitCompound_term(self)


    class Integer_termContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def integer(self):
            return self.getTypedRuleContext(FOLParser.IntegerContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInteger_term" ):
                listener.enterInteger_term(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInteger_term" ):
                listener.exitInteger_term(self)


    class Curly_bracketed_termContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def termlist(self):
            return self.getTypedRuleContext(FOLParser.TermlistContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCurly_bracketed_term" ):
                listener.enterCurly_bracketed_term(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCurly_bracketed_term" ):
                listener.exitCurly_bracketed_term(self)



    def term(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = FOLParser.TermContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_term, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                localctx = FOLParser.VariableContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 41
                self.match(FOLParser.VARIABLE)
                pass

            elif la_ == 2:
                localctx = FOLParser.Braced_termContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 42
                self.match(FOLParser.T__3)
                self.state = 43
                self.term(0)
                self.state = 44
                self.match(FOLParser.T__4)
                pass

            elif la_ == 3:
                localctx = FOLParser.Integer_termContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 47
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 46
                    self.match(FOLParser.T__5)


                self.state = 49
                self.integer()
                pass

            elif la_ == 4:
                localctx = FOLParser.FloatContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 51
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 50
                    self.match(FOLParser.T__5)


                self.state = 53
                self.match(FOLParser.FLOAT)
                pass

            elif la_ == 5:
                localctx = FOLParser.Compound_termContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 54
                self.atom()
                self.state = 55
                self.match(FOLParser.T__3)
                self.state = 56
                self.termlist()
                self.state = 57
                self.match(FOLParser.T__4)
                pass

            elif la_ == 6:
                localctx = FOLParser.Unary_operatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 59
                self.operator_()
                self.state = 60
                self.term(4)
                pass

            elif la_ == 7:
                localctx = FOLParser.List_termContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 62
                self.match(FOLParser.T__6)
                self.state = 63
                self.termlist()
                self.state = 66
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==8:
                    self.state = 64
                    self.match(FOLParser.T__7)
                    self.state = 65
                    self.term(0)


                self.state = 68
                self.match(FOLParser.T__8)
                pass

            elif la_ == 8:
                localctx = FOLParser.Curly_bracketed_termContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 70
                self.match(FOLParser.T__9)
                self.state = 71
                self.termlist()
                self.state = 72
                self.match(FOLParser.T__10)
                pass

            elif la_ == 9:
                localctx = FOLParser.Atom_termContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 74
                self.atom()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 83
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = FOLParser.Binary_operatorContext(self, FOLParser.TermContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                    self.state = 77
                    if not self.precpred(self._ctx, 5):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                    self.state = 78
                    self.operator_()
                    self.state = 79
                    self.term(5) 
                self.state = 85
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Operator_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FOLParser.RULE_operator_

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperator_" ):
                listener.enterOperator_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperator_" ):
                listener.exitOperator_(self)




    def operator_(self):

        localctx = FOLParser.Operator_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_operator_)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2251799813681226) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FOLParser.RULE_atom

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Backq_stringContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BACK_QUOTED_STRING(self):
            return self.getToken(FOLParser.BACK_QUOTED_STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBackq_string" ):
                listener.enterBackq_string(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBackq_string" ):
                listener.exitBackq_string(self)


    class CutContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCut" ):
                listener.enterCut(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCut" ):
                listener.exitCut(self)


    class Empty_bracesContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEmpty_braces" ):
                listener.enterEmpty_braces(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEmpty_braces" ):
                listener.exitEmpty_braces(self)


    class Dq_stringContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DOUBLE_QUOTED_LIST(self):
            return self.getToken(FOLParser.DOUBLE_QUOTED_LIST, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDq_string" ):
                listener.enterDq_string(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDq_string" ):
                listener.exitDq_string(self)


    class NameContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LETTER_DIGIT(self):
            return self.getToken(FOLParser.LETTER_DIGIT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterName" ):
                listener.enterName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitName" ):
                listener.exitName(self)


    class Quoted_stringContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def QUOTED(self):
            return self.getToken(FOLParser.QUOTED, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuoted_string" ):
                listener.enterQuoted_string(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuoted_string" ):
                listener.exitQuoted_string(self)


    class Empty_listContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEmpty_list" ):
                listener.enterEmpty_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEmpty_list" ):
                listener.exitEmpty_list(self)


    class GraphicContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def GRAPHIC_TOKEN(self):
            return self.getToken(FOLParser.GRAPHIC_TOKEN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGraphic" ):
                listener.enterGraphic(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGraphic" ):
                listener.exitGraphic(self)


    class SemicolonContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FOLParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSemicolon" ):
                listener.enterSemicolon(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSemicolon" ):
                listener.exitSemicolon(self)



    def atom(self):

        localctx = FOLParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_atom)
        try:
            self.state = 99
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7]:
                localctx = FOLParser.Empty_listContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 88
                self.match(FOLParser.T__6)
                self.state = 89
                self.match(FOLParser.T__8)
                pass
            elif token in [10]:
                localctx = FOLParser.Empty_bracesContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 90
                self.match(FOLParser.T__9)
                self.state = 91
                self.match(FOLParser.T__10)
                pass
            elif token in [52]:
                localctx = FOLParser.NameContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 92
                self.match(FOLParser.LETTER_DIGIT)
                pass
            elif token in [60]:
                localctx = FOLParser.GraphicContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 93
                self.match(FOLParser.GRAPHIC_TOKEN)
                pass
            elif token in [61]:
                localctx = FOLParser.Quoted_stringContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 94
                self.match(FOLParser.QUOTED)
                pass
            elif token in [62]:
                localctx = FOLParser.Dq_stringContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 95
                self.match(FOLParser.DOUBLE_QUOTED_LIST)
                pass
            elif token in [63]:
                localctx = FOLParser.Backq_stringContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 96
                self.match(FOLParser.BACK_QUOTED_STRING)
                pass
            elif token in [18]:
                localctx = FOLParser.SemicolonContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 97
                self.match(FOLParser.T__17)
                pass
            elif token in [51]:
                localctx = FOLParser.CutContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 98
                self.match(FOLParser.T__50)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntegerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DECIMAL(self):
            return self.getToken(FOLParser.DECIMAL, 0)

        def CHARACTER_CODE_CONSTANT(self):
            return self.getToken(FOLParser.CHARACTER_CODE_CONSTANT, 0)

        def BINARY(self):
            return self.getToken(FOLParser.BINARY, 0)

        def OCTAL(self):
            return self.getToken(FOLParser.OCTAL, 0)

        def HEX(self):
            return self.getToken(FOLParser.HEX, 0)

        def getRuleIndex(self):
            return FOLParser.RULE_integer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInteger" ):
                listener.enterInteger(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInteger" ):
                listener.exitInteger(self)




    def integer(self):

        localctx = FOLParser.IntegerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_integer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 558446353793941504) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[4] = self.term_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def term_sempred(self, localctx:TermContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 5)
         




