from polygons import ConvexPolygon


if __name__ is not None and "." in __name__:
    from .gramaticaParser import gramaticaParser
    from .gramaticaVisitor import gramaticaVisitor
else:
    from gramaticaParser import gramaticaParser
    from gramaticaVisitor import gramaticaVisitor


class EvalVisitor(gramaticaVisitor):
    '''
    Aquesta classe s'encarrega d'implementar el visitor de la gràmatica
    '''
    def __init__(self):
        '''
        Inicialitza el diccionari (única variable de la classe)
        '''
        self.diccionari = {}

    def visitRoot(self, ctx: gramaticaParser.RootContext):
        '''
        Visita el fill de root
        '''
        n = next(ctx.getChildren())
        self.visit(n)

    def visitExpressions(self, ctx: gramaticaParser.ExpressionsContext):
        '''
        Visita els fills de expressions
        '''
        l = [n for n in ctx.getChildren()]
        for i in l:
            self.visit(i)

    def visitExpr(self, ctx: gramaticaParser.ExprContext):
        '''
        Visita el fill de Expr
        '''
        n = next(ctx.getChildren())
        self.visit(n)

    def visitIde(self, ctx: gramaticaParser.IdeContext):
        '''
        Si l'identificador donat es correspon amb una clau del diccionari
        retorna el polígon associat. En cas contrari, retorna un None. En
        les funcions següents en cas de rebre un None ignoraran la petició
        '''
        return self.diccionari.get(ctx.getText())

    def visitOp(self, ctx: gramaticaParser.OpContext):
        '''
        Si té un fill:
        - Es visita el fill (Es pot tractar d'un identificador o una llista)
        Si té dos fills:
        - Si comença per # es retorna el bounding box del polígon obtingut
        després de visitar el segon fill
        - Si comença per ! i va seguit per un natural n es retorna un polígon
        generat de forma aleatòria amb n vèrtexs
        Si té tres fills:
        - Si el segon fill es correspon al símbol '*' es retorna la intersecció
        entre els polígons obtinguts després de vistar el primer i el tercer
        fill
        - Si el segon fill es correspon al símbol '+' es retorna la unió
        entre els polígons obtinguts després de vistar el primer i el tercer
        fill
        - Si el primer fill és '(' i el tercer ')' es retorna el polígon
        obtingut després de visitar el segon fill
        '''
        l = [n for n in ctx.getChildren()]
        le = len(l)
        if le == 1:
            return self.visit(l[0])
        elif le == 2:
            if '#' == l[0].getText():
                c = self.visit(l[1])
                if c is None:
                    return None
                else:
                    return c.bounding_box()
            else:
                c = ConvexPolygon()
                return c.random_polygon(int(l[1].getText()))
        else:
            if '*' == ctx.getChild(1).getText():
                c1 = self.visit(l[0])
                c2 = self.visit(l[2])
                if c1 is None or c2 is None:
                    return None
                else:
                    return c1.intersection(c2)
            elif '+' == ctx.getChild(1).getText():
                c1 = self.visit(l[0])
                c2 = self.visit(l[2])
                if c1 is None or c2 is None:
                    return None
                else:
                    return c1.union(c2)
            else:
                return self.visit(l[1])

    def visitPoint(self, ctx: gramaticaParser.PointContext):
        '''
        Retorna: Un punt (x, y) on x, y són reals
        '''
        l = [n for n in ctx.getChildren()]
        return (float(l[0].getText()), float(l[1].getText()))

    def visitLlista(self, ctx: gramaticaParser.LlistaContext):
        '''
        Retorna: Un polígon creat a partir de la llista de punts
        passada com a entrada
        '''
        l = [n for n in ctx.getChildren()]
        res = []
        for i in l:
            x = self.visit(i)
            if x is not None:
                res.append(x)
        c = ConvexPolygon(res)
        return c

    def visitAssign(self, ctx: gramaticaParser.AssignContext):
        '''
        Guarda al diccionari un nou element amb clau = identificador
        del polígon i diccionari[clau] = al polígon obtingut de
        la segona part
        '''
        l = [n for n in ctx.getChildren()]
        c1 = self.visit(l[2])
        if c1 is not None:
            res = c1.get_points()
            c2 = ConvexPolygon(res)
            self.diccionari[l[0].getText()] = c2

    def visitPrinti(self, ctx: gramaticaParser.PrintiContext):
        '''
        Imprimeix els punts del polígon resultants del Convex Hull.
        Format: 3 digits després del punt.
        '''
        l = [n for n in ctx.getChildren()]
        c = self.visit(l[1])
        if c is not None:
            points = c.get_points()
            for x, y in points:
                print("{:.3f}".format(x), "{:.3f}".format(y), end=" ")
            print()

    def visitPrintx(self, ctx: gramaticaParser.PrintxContext):
        '''
        Imprimeix el string passat com a entrada.
        '''
        l = [n for n in ctx.getChildren()]
        x = l[1].getText()
        fi = len(x)-1
        print(x[1:fi])

    def visitArea(self, ctx: gramaticaParser.AreaContext):
        '''
        Imprimeix l'àrea del polígon. Format: 3 digits després del punt.
        '''
        l = [n for n in ctx.getChildren()]
        c = self.visit(l[1])
        if c is not None:
            print("{:.3f}".format(c.get_area()))

    def visitPerimeter(self, ctx: gramaticaParser.PerimeterContext):
        '''
        Imprimeix el perímetre del polígon. Format: 3 digits després del punt.
        '''
        l = [n for n in ctx.getChildren()]
        c = self.visit(l[1])
        if c is not None:
            print("{:.3f}".format(c.get_perimeter()))

    def visitVertices(self, ctx: gramaticaParser.VerticesContext):
        '''
        Imprimeix el nombre de vèrtexs del polígon.
        '''
        l = [n for n in ctx.getChildren()]
        c = self.visit(l[1])
        if c is not None:
            print(c.get_n_vertices())

    def visitCentroid(self, ctx: gramaticaParser.CentroidContext):
        '''
        Imprimeix el centroide del polígon. Format: 3 digits després del punt.
        '''
        l = [n for n in ctx.getChildren()]
        c = self.visit(l[1])
        if c is not None:
            cx, cy = c.get_centroid()
            print("{:.3f}".format(cx), "{:.3f}".format(cy))

    def visitColor(self, ctx: gramaticaParser.ColorContext):
        '''
        Canvia el color del polígon al color passat com a entrada
        '''
        l = [n for n in ctx.getChildren()]
        ide = l[1].getText()
        c = self.diccionari.get(ide)
        if c is not None:
            r = float(l[4].getText())
            g = float(l[5].getText())
            b = float(l[6].getText())
            c.set_color((r, g, b))
            self.diccionari[ide] = c

    def visitInside(self, ctx: gramaticaParser.InsideContext):
        '''
        Imprimeix 'yes' si elprimer polígon es troba dins del
        segon i 'no' en cas contrari.
        '''
        l = [n for n in ctx.getChildren()]
        c1 = self.visit(l[1])
        c2 = self.visit(l[3])
        if c1 is not None and c2 is not None:
            if c2.polygon_inside(c1):
                print('yes')
            else:
                print('no')

    def visitEqual(self, ctx: gramaticaParser.EqualContext):
        '''
        Imprimeix 'yes' si els dos polígons són iguals i 'no'
        en cas contrari.
        '''
        l = [n for n in ctx.getChildren()]
        c1 = self.visit(l[1])
        c2 = self.visit(l[3])
        if c1 is not None and c2 is not None:
            if c2.polygon_equal(c1):
                print('yes')
            else:
                print('no')

    def visitRegular(self, ctx: gramaticaParser.RegularContext):
        '''
        Imprimeix 'yes' si el polígon és regular i 'no'
        en cas contrari.
        '''
        l = [n for n in ctx.getChildren()]
        c = self.visit(l[1])
        if c is not None:
            if c.is_regular():
                print('yes')
            else:
                print('no')

    def visitDraw(self, ctx: gramaticaParser.DrawContext):
        '''
        Recopilem els polígons passats com a entrada en un llistat.
        Dibuixem els polígons en una imatge amb el nom indicat
        per la entrada.
        '''
        l = [n for n in ctx.getChildren()]
        x = l[1].getText()
        fi = len(x)-1
        nom = x[1:fi]
        v = []
        le = len(l)
        for i in range(3, le, 2):
            c = self.visit(l[i])
            if c is not None:
                v.append(c)
        o = ConvexPolygon()
        o.draw(nom, v)

    def visitCondicio(self, ctx: gramaticaParser.CondicioContext):
        '''
        Si té un fill:
        - Si es 'True', es retorna un booleà True
        - Si és 'False', es retorna un booleà False
        Si té tres fills:
        - Es compara el primer fill amb el tercer fent servir el
        símbol indicat pel segon fill
        '''
        l = [n for n in ctx.getChildren()]
        le = len(l)
        if le == 1:
            if l[0].getText() == 'True':
                return True
            else:
                return False
        elif le == 3:
            a = float(l[0].getText())
            b = float(l[2].getText())
            if l[1].getText() == '>':
                return a > b
            elif l[1].getText() == '<':
                return a < b
            elif l[1].getText() == '==':
                return a == b
            elif l[1].getText() == '!=':
                return a != b
            elif l[1].getText() == '>=':
                return a >= b
            else:
                return a <= b

    def visitCondicional(self, ctx: gramaticaParser.CondicionalContext):
        '''
        Farem un recorregut per les clausules if/elif/else
        - Si la clàusula es compleix, visitarem les expressions
        associades i acabarem.
        - En cas contrari, passarem a la següent clàusula
        '''
        l = [n for n in ctx.getChildren()]
        if self.visit(l[1]):
            self.visit(l[2])
        else:
            le = len(l)-1
            i = 3
            while i < le:
                if l[i].getText() == 'elif':
                    if self.visit(l[i+1]):
                        self.visit(l[i+2])
                        break
                    else:
                        i += 3
                else:
                    self.visit(l[i+1])
                    break
