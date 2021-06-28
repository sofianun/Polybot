# Generated from gramatica.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .gramaticaParser import gramaticaParser
else:
    from gramaticaParser import gramaticaParser

# This class defines a complete generic visitor for a parse tree produced by gramaticaParser.

class gramaticaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by gramaticaParser#root.
    def visitRoot(self, ctx:gramaticaParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#expressions.
    def visitExpressions(self, ctx:gramaticaParser.ExpressionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#expr.
    def visitExpr(self, ctx:gramaticaParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#op.
    def visitOp(self, ctx:gramaticaParser.OpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#assign.
    def visitAssign(self, ctx:gramaticaParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#printi.
    def visitPrinti(self, ctx:gramaticaParser.PrintiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#printx.
    def visitPrintx(self, ctx:gramaticaParser.PrintxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#area.
    def visitArea(self, ctx:gramaticaParser.AreaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#perimeter.
    def visitPerimeter(self, ctx:gramaticaParser.PerimeterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#vertices.
    def visitVertices(self, ctx:gramaticaParser.VerticesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#centroid.
    def visitCentroid(self, ctx:gramaticaParser.CentroidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#color.
    def visitColor(self, ctx:gramaticaParser.ColorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#inside.
    def visitInside(self, ctx:gramaticaParser.InsideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#equal.
    def visitEqual(self, ctx:gramaticaParser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#regular.
    def visitRegular(self, ctx:gramaticaParser.RegularContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#draw.
    def visitDraw(self, ctx:gramaticaParser.DrawContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#condicio.
    def visitCondicio(self, ctx:gramaticaParser.CondicioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#condicional.
    def visitCondicional(self, ctx:gramaticaParser.CondicionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#llista.
    def visitLlista(self, ctx:gramaticaParser.LlistaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#point.
    def visitPoint(self, ctx:gramaticaParser.PointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gramaticaParser#ide.
    def visitIde(self, ctx:gramaticaParser.IdeContext):
        return self.visitChildren(ctx)



del gramaticaParser