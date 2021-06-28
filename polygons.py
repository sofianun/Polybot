import math
import random
from PIL import Image, ImageDraw


class ConvexPolygon:
    '''
    Aquesta classe serveix per treballar amb polígons convexos.
    Un polígon és convex quan és un polígon simple i tots els seus
    angles interiors són estrictament menors a 180º
    '''
    def __init__(self, L=[]):
        '''
        Inicialització d'un polígon convex
        Paràmetres: un llistat de punts seguint el format
        [(x0, y0),(x1, y1),...]. Per defecte es crea un polígon buit
        Descripció:
        - El color es posa a negre
        - Es considera que és regular en un primer moment
        - Es calculen els punts del polígon cridant a la funció convex_hull
        - Es crida a la funció privada __calcula__ encarregada de determinar
        el perímetre, l'àrea, el centroide i si realment és regular
        '''
        self.__color__ = (0, 0, 0)
        self.__regular__ = True
        self.__points__ = self.convex_hull(L)
        self.__calcula__()

    def get_points(self):
        '''
        Paràmetres: cap
        Retorna: el llistat de punts obtinguts del Convex Hull. Els punts estan
        ordenats en sentit horari i començant pel punt amb menor x (i menor y
        en cas d'empat).
        El format és [(x0, y0),(x1, y1),...] on x0, y0, x1, y1, ... són reals
        '''
        return self.__points__.copy()

    def get_n_vertices(self):
        '''
        Paràmetres: cap
        Retorna: un enter corresponent al nombre de vèrtexs del propi polígon
        '''
        return len(self.__points__)

    def get_n_edges(self):
        '''
        Paràmetres: cap
        Retorna: un enter corresponent al nombre d'aristes del propi polígon
        '''
        return len(self.__points__)

    def get_perimeter(self):
        '''
        Paràmetres: cap
        Retorna: un real corresponent al perímetre del propi polígon
        '''
        return self.__perimeter__

    def get_area(self):
        '''
        Paràmetres: cap
        Retorna: un real corresponent a l'àrea del propi polígon
        '''
        return self.__area__

    def get_centroid(self):
        '''
        Paràmetres: cap
        Retorna: les coordenades del centroide del propi polígon en format
        (x, y) on x, y són reals
        '''
        return self.__centroid__

    def get_xmin(self):
        '''
        Paràmetres: cap
        Retorna: la x mínima del propi polígon
        '''
        return self.__xmin__

    def get_ymin(self):
        '''
        Paràmetres: cap
        Retorna: la y mínima del propi polígon
        '''
        return self.__ymin__

    def get_xmax(self):
        '''
        Paràmetres: cap
        Retorna: la x màxima del propi polígon
        '''
        return self.__xmax__

    def get_ymax(self):
        '''
        Paràmetres: cap
        Retorna: la y màxima del propi polígon
        '''
        return self.__ymax__

    def get_color(self):
        '''
        Paràmetres: cap
        Retorna: el color del propi polígon en format (r, g, b) on r, g, b són
        reals entre el 0 i l'1
        '''
        return self.__color__

    def set_color(self, c):
        '''
        Paràmetres: un color en format (r, g, b) on r, g, b són reals
        entre el 0 i l'1
        Retorna: res
        Descripció:
        Es comprova que el color passat com a entrada és vàlid.
        En cas afirmatiu, passa a ser el color del propi polígon
        '''
        r, g, b = c
        if 0 <= r and r <= 1 and 0 <= g and g <= 1 and 0 <= b and b <= 1:
            self.__color__ = c

    def is_regular(self):
        '''
        Paràmetres: cap
        Retorna: un booleà que indica
            True si el propi polígon és regular
            False en cas contrari
        '''
        return self.__regular__

    def merge(self, L1, L2, x0, y0):
        '''
        Paràmetres:
        - una llista de punts L1,
        - una llista de punts L2
        - un punt amb coordenades x0, y0
        Retorna: una llista amb els elements de L1 i L2 en ordre i sense
        repetits
        Descripció:
        S'ordenen segons l'angle que formi amb el punt (x0, y0) i la
        vertical que passa per x0 (de menor a major). En cas d'empat,
        ens quedem únicament amb el punt més llunyà. Si els dos punts
        tornessin a empatar, ens quedaríem amb el segon (podríem
        quedar-nos amb qualsevol dels dos). Si el punt es troba
        en (x0, y0) es descarta.
        '''
        if L1 == []:
            return L2
        elif L2 == []:
            return L1
        else:
            res = []
            x1, y1 = L1[0]
            x2, y2 = L2[0]
            d1 = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            d2 = math.sqrt((x2-x0)**2 + (y2-y0)**2)
            if d1 > 0 and d2 > 0:
                a1 = math.acos((y1-y0)/d1)
                a2 = math.acos((y2-y0)/d2)
                if a1 < a2:
                    res = [L1[0]]
                    res.extend(self.merge(L1[1:], L2, x0, y0))
                elif a1 == a2:
                    if d1 > d2:
                        res = [L1[0]]
                        res.extend(self.merge(L1[1:], L2[1:], x0, y0))
                    else:
                        res = [L2[0]]
                        res.extend(self.merge(L1[1:], L2[1:], x0, y0))
                else:
                    res = [L2[0]]
                    res.extend(self.merge(L1, L2[1:], x0, y0))
            else:
                if d1 > 0:
                    res = [L1[0]]
                    res.extend(self.merge(L1[1:], L2[1:], x0, y0))
                elif d2 > 0:
                    res = [L2[0]]
                    res.extend(self.merge(L1[1:], L2[1:], x0, y0))
            return res

    def msort(self, L, x0, y0):
        '''
        Paràmetres:
        - una llista de punts L,
        - un punt amb coordenades x0, y0
        Retorna: una llista que conté els punts de L en ordre i sense repetits
        Descripció:
        S'ordenen les meitats de la llista L per separat i després es combinen
        fent servir la funció merge.
        '''
        long = len(L)
        if long <= 1:
            return L
        else:
            m = math.floor(long/2)
            L1 = self.msort(L[0:m], x0, y0)
            L2 = self.msort(L[m:], x0, y0)
            res = self.merge(L1, L2, x0, y0)
            return res

    def convex_hull(self, L, sorted=False):
        '''
        Paràmetres:
        - una llista de punts L,
        - (opcional) un booleà que indica que la llista L ja està ordenada i no
        té repetits, és a dir, la llista comença pel punt amb menor x (i menor
        y en cas d'empat) i la resta de punts estan ordenats en funció de
        l'angle que forman amb aquest i la seva vertical (i en cas d'empat,
        es descarta el més proper). Per defecte es considera que la llista
        ve desordenada.
        Descripció:
        - Es troba el punt amb menor x i en cas que hagi més d'un s'escull
        el que tingui menor y, les coordenades del qual anomenarem x0, y0
        - S'ordenen segons l'angle que formi amb el punt (x0, y0) i la vertical
        que passa per x0 (de menor a major). En cas d'empat, ens quedem
        únicament amb el punt més llunyà. Si els dos punts tornessin a empatar,
        ens quedaríem amb el segon (podríem quedar-nos amb qualsevol dels dos).
        Si el punt es troba en (x0, y0) es descarta.
        - Fem un recorregut per la llista i comprovem que els últims dos punts
        de la llista i el nou afegit continuen es troben en sentit horari i
        els punts apilats fins al moment formen part d'un polígon convex.
        En cas contrari, es desapilen els punts que donen problemes i es
        continua llegint.
        '''
        n_points = len(L)
        points = L.copy()
        if n_points < 2:
            return points
        else:
            x0, y0 = points[0]
            if sorted:
                points.pop(0)
            else:
                for i in range(1, n_points):
                    x, y = points[i]
                    if x < x0 or (x == x0 and y < y0):
                        x0 = x
                        y0 = y
                points.remove((x0, y0))
                points = self.msort(points, x0, y0)
            stack = [(x0, y0)]
            for p in points:
                le = len(stack)
                while le > 1:
                    x0, y0 = stack[le-2]
                    x1, y1 = stack[le-1]
                    x2, y2 = p
                    clockwise = (x1-x0)*(y2-y1) - (y1-y0)*(x2-x1)
                    if clockwise < 0:
                        break
                    else:
                        stack.pop()
                        le = len(stack)
                stack.append(p)
            return stack

    def __calcula__(self):
        '''
        Paràmetres: cap
        Retorna: res
        Descripció:
        Es calcula l'àrea, el perímetre, el centroide, la x mínima,
        la y mínima, la x màxima, la y màxima i en cas que sigui irregular,
        s'actualitza la variable __regular__ a False.
        Si té 0 punts:
        - L'àrea és 0
        - El perímetre és 0
        - El centroide és (0, 0)
        - És regular
        Si té 1 punt:
        - L'àrea és 0
        - El perímetre és 0
        - El centroide és el propi punt
        - És regular
        Si té 2 punts:
        - L'àrea és 0
        - El perímetre és la distància entre els dos punts
        - El centroide és el punt mig
        - És regular
        Si té 3 punts o més:
        - L'àrea és la meitat del sumatori x0*y1-x1*y0 + x1*y2-x2*y1 + ... +
        xn*y0-x0*yn amb el signe canviat (dona negatiu perquè els punts estan
        en sentit horari per això hem de canviar el signe al final)
        - El perímetre és el sumatori de les distàncies entre x0-x1,
        x1-x2,...,xn-x0, on la distància es calcula així:
        math.sqrt((x2-x1)**2 + (y2-y1)**2)
        - La coordenada x del centroide és el sumatori (x0+x1)*(x0*y1-x1*y0) +
        (x1+x2)*(x1*y2-x2*y1) + ... + (xn+x0)*(xn*y0-x0*yn) dividit per 6*àrea
        amb el signe canviat. De la mateixa manera, la coordenada y del
        centroide és el sumatori (y0+y1)*(x0*y1-x1*y0) + (y1+y2)*(x1*y2-x2*y1)
        + ... + (yn+y0)*(xn*y0-x0*yn) dividit per 6*àrea amb el signe canviat
        (Els punts estan en sentit horari per això hem de canviar els signes al
        final)
        - Si tots els costats fan la mateixa mida es crida a la funció
        __angles_iguals__ per estudiar si els angles són iguals (regular) o no
        (irregular). En cas contrari, el polígon passa a ser irregular i no
        es fan més comprovacions.
        '''
        n_points = len(self.__points__)
        if n_points <= 2:
            self.__area__ = 0
            if n_points <= 1:
                self.__perimeter__ = 0
                if n_points == 0:
                    self.__centroid__ = (0, 0)
                    self.__xmin__ = 0
                    self.__ymin__ = 0
                    self.__xmax__ = 0
                    self.__ymax__ = 0
                else:
                    self.__centroid__ = self.__points__[0]
                    x, y = self.__points__[0]
                    self.__xmin__ = x
                    self.__ymin__ = y
                    self.__xmax__ = x
                    self.__ymax__ = y
            elif n_points == 2:
                x1, y1 = self.__points__[0]
                x2, y2 = self.__points__[1]
                self.__xmin__ = x1
                self.__xmax__ = x2
                if y1 < y2:
                    self.__ymin__ = y1
                    self.__ymax__ = y2
                else:
                    self.__ymin__ = y2
                    self.__ymax__ = y1
                self.__perimeter__ = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                self.__centroid__ = ((x1 + x2)/2, (y1 + y2)/2)
        else:
            x1, y1 = self.__points__[0]
            p = 0
            a = 0
            sum_cx = 0
            sum_cy = 0
            digual = 0
            xmin, ymin = self.__points__[0]
            xmax, ymax = self.__points__[0]
            for i in range(1, n_points+1):
                if i == n_points:
                    x2, y2 = self.__points__[0]
                else:
                    x2, y2 = self.__points__[i]
                if x2 < xmin:
                    xmin = x2
                if x2 > xmax:
                    xmax = x2
                if y2 < ymin:
                    ymin = y2
                if y2 > ymax:
                    ymax = y2
                d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                if i == 1:
                    digual = d
                elif self.__regular__ and digual != d:
                    self.__regular__ = False
                p += d
                a += x1*y2-x2*y1
                sum_cx += (x1+x2)*(x1*y2-x2*y1)
                sum_cy += (y1+y2)*(x1*y2-x2*y1)
                x1, y1 = x2, y2
            self.__xmin__ = xmin
            self.__ymin__ = ymin
            self.__xmax__ = xmax
            self.__ymax__ = ymax
            self.__perimeter__ = p
            self.__area__ = -a/2
            sum_cx = -sum_cx / (6*self.__area__)
            sum_cy = -sum_cy / (6*self.__area__)
            self.__centroid__ = (sum_cx, sum_cy)
            if self.__regular__:
                self.__angles_iguals__()

    def __angles_iguals__(self):
        '''
        Paràmetres: cap
        Retorna: res
        Descripció:
        Comparem els angles que formen p1-p2 i p1-centroide on p1-p2 són els
        punts p0-p1,p1-p2...pn-p0. Si tots són iguals, el polígon és regular i
        en cas contrari, irregular.
        '''
        n_points = len(self.__points__)
        cx, cy = self.__centroid__
        x0, y0 = self.__points__[0]
        for i in range(1, n_points+1):
            if i == n_points:
                x1, y1 = self.__points__[0]
            else:
                x1, y1 = self.__points__[i]
            p = (x1-x0)*(cx-x0) + (y1-y0)*(cy-y0)
            dc = math.sqrt((cx-x0)**2 + (cy-y0)**2)
            d1 = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            angle_aux = math.acos(p/(dc*d1))
            if i == 1:
                angle = angle_aux
            else:
                if angle != angle_aux:
                    self.__regular__ = False
                    break
            x0, y0 = x1, y1

    def point_inside(self, x, y):
        '''
        Paràmetres: un punt amb coordenades (x, y)
        Retorna: un booleà indicant que si el punt es troba dins del propi
        polígon (True) o no (False)
        Descripció:
        Si el propi polígon és buit, es retorna False
        Si el propi polígon té un punt, es comprova si el punt del polígon i
        (x, y) són iguals
        Si el propi polígon té dos punts o més:
        - Si el punt es troba fora del bounding box del polígon es retorna
        False directament
        - Altrament, fem un recorregut per les arestes del polígon. Si el
        polígon es troba sobre una aresta es retorna True directament. Si
        la vertical que passa per x, intersecta una vegada amb les arestes
        del polígon per sobre de y o per sota de y, es retorna True.
        Si la vertical intersecta amb dues arestes per sobre i dues per sota
        (intersecta amb dos vèrtexs) també es retorna True. En cas contrari,
        es retorna False
        '''
        n_points = len(self.__points__)
        if n_points == 0:
            return False
        elif n_points == 1:
            x1, y1 = self.__points__[0]
            return x == x1 and y == y1
        else:
            xmin = self.__xmin__
            ymin = self.__ymin__
            xmax = self.__xmax__
            ymax = self.__ymax__
            if x < xmin or y < ymin or x > xmax or y > ymax:
                return False
            x1, y1 = self.__points__[0]
            c = 0
            c2 = 0
            for i in range(1, n_points+1):
                if i == n_points:
                    x2, y2 = self.__points__[0]
                else:
                    x2, y2 = self.__points__[i]
                if x2-x1 != 0:
                    m = (y2-y1)/(x2-x1)
                    auxy = y1 + m*(x-x1)
                    if x1 <= x <= x2 or x2 <= x <= x1:
                        if y == auxy:
                            return True
                        if auxy < y:
                            c += 1
                        else:
                            c2 += 1
                elif x == x1:
                    if y1 <= y <= y2 or y2 <= y <= y1:
                        return True
                    else:
                        return False
                x1, y1 = x2, y2
            if c == 1 or c2 == 1 or (c == 2 and c2 == 2):
                return True
            else:
                return False

    def polygon_inside(self, c):
        '''
        Paràmetres: un polígon convex
        Retorna: True si el polígon passat com a entrada es troba dins del
        propi polígon, False en cas contrari
        Descripció:
        Si tots els punts del polígon passat com a entrada són interiors,
        el polígon és interior.
        '''
        for x, y in c.get_points():
            if not self.point_inside(x, y):
                return False
        return True

    def polygon_equal(self, c):
        '''
        Paràmetres: un polígon convex
        Retorna: True si les llistes de punts del polígon passat com a entrada
        i el propi polígon són iguals, False en cas contrari.
        Descripció:
        Es comparen les llistes, com que estan ordenades si els polígons són
        iguals les llistes han de ser iguals per força.
        '''
        return self.__points__ == c.get_points()

    def intersection(self, c):
        '''
        Paràmetres: un polígon convex
        Retorna: el polígon convex producte de la intersecció entre el polígon
        passat com a entrada i el propi polígon
        Descripció:
        - Si algún dels polígons és buit, es retorna ún polígon buit
        - Si les seves bounding box no es solapen, es retorna
        un polígon buit directament
        - Si algún dels dos està format per un únic punt, es comprova
        si aquest punt és interior a l'altre. En cas afirmatiu, es
        retorna el punt. Altrament, es retorna un polígon buit
        - Si tots dos tenen més d'un punt, recompilem els següents
        punts en una llista: els que vèrtexs del propi polígon que
        són interiors al segon polígon, els vèrtexs del segon polígon
        que són interiors al propi polígon i les interseccions entre
        costats del propi polígon i el segon polígon. Utilitzem la
        llista per crear el polígon intersecció i el retornem.
        NOTA: per calcular les interseccions es té en compte que
        un costat pot ser paral·lel a l'eix x, a l'eix y o no
        '''
        n_points1 = len(self.__points__)
        points2 = c.get_points()
        n_points2 = len(points2)
        i = ConvexPolygon()
        if n_points1 == 0 or n_points2 == 0:
            return i
        le1 = self.__xmin__
        le2 = c.get_xmin()
        ri1 = self.__xmax__
        ri2 = c.get_xmax()
        cond1 = (le1 < le2 and ri1 < le2) or (le2 < le1 and ri2 < le1)
        down1 = self.__ymin__
        down2 = c.get_ymin()
        up1 = self.__ymax__
        up2 = c.get_ymax()
        cond2 = (up1 > up2 and down1 > up2) or (up2 > up1 and down2 > up1)
        if cond1 or cond2:
            return i
        if n_points1 == 1:
            x, y = self.__points__[0]
            if c.point_inside(x, y):
                i = ConvexPolygon([(x, y)])
        elif n_points2 == 1:
            x, y = c.get_points()[0]
            if self.point_inside(x, y):
                i = ConvexPolygon([(x, y)])
        else:
            L = []
            for x, y in self.__points__:
                if c.point_inside(x, y):
                    L.append((x, y))
            for x, y in points2:
                if self.point_inside(x, y):
                    L.append((x, y))
            x1, y1 = self.__points__[0]
            for i in range(1, n_points1+1):
                if i == n_points1:
                    x2, y2 = self.__points__[0]
                else:
                    x2, y2 = self.__points__[i]
                dx1 = x2-x1
                dy1 = y2-y1
                x3, y3 = points2[0]
                for j in range(1, n_points2+1):
                    if j == n_points2:
                        x4, y4 = points2[0]
                    else:
                        x4, y4 = points2[j]
                    dx3 = x4-x3
                    dy3 = y4-y3
                    if dx1 == 0:
                        cond3 = (x3 <= x1 <= x4) or (x4 <= x1 <= x3)
                        if dx3 != 0 and cond3:
                            if dy3 == 0:
                                if (y1 <= y3 <= y2) or (y2 <= y3 <= y1):
                                    L.append((x1, y3))
                            else:
                                m3 = dy3 / dx3
                                auxy = y3 + m3*(x1-x3)
                                if (y1 <= auxy <= y2) or (y2 <= auxy <= y1):
                                    L.append((x1, auxy))
                    elif dy1 == 0:
                        if dy3 != 0 and ((y3 <= y1 <= y4) or (y4 <= y1 <= y3)):
                            if dx3 == 0:
                                if (x1 <= x3 <= x2) or (x2 <= x3 <= x1):
                                    L.append((x3, y1))
                            else:
                                m3 = dy3 / dx3
                                auxx = (y1-y3+m3*x3)/m3
                                if (x1 <= auxx <= x2) or (x2 <= auxx <= x1):
                                    L.append((auxx, y1))
                    else:
                        m1 = dy1 / dx1
                        if dx3 == 0:
                            auxy = y1 + m1*(x3-x1)
                            if (y3 <= auxy <= y4) or (y4 <= auxy <= y3):
                                L.append((x3, auxy))
                        elif dy3 == 0:
                            auxx = (y3-y1+m1*x1)/m1
                            if (x3 <= auxx <= x4) or (x4 <= auxx <= x3):
                                L.append((auxx, y3))
                        else:
                            m3 = dy3 / dx3
                            if m1 != m3:
                                auxx = (y3 - m3*x3-y1 + m1*x1) / (m1-m3)
                                auxy = y1 + m1*(auxx-x1)
                                b3 = (x1 <= auxx <= x2) or (x2 <= auxx <= x1)
                                b4 = (x3 <= auxx <= x4) or (x4 <= auxx <= x3)
                                if b3 and b4:
                                    L.append((auxx, auxy))
                    x3, y3 = x4, y4
                x1, y1 = x2, y2
            i = ConvexPolygon(L)
        return i

    def union(self, c):
        '''
        Paràmetres: un polígon convex
        Retorna: el polígon convex que engloba el polígon passat com a
        entrada i el propi polígon
        Descripció:
        Si un dels dos és el polígon buit, la unió és directament l'altre
        polígon. Altrament, retornem el polígon resultant del Convex Hull
        de tots dos polígons
        '''
        L1 = self.__points__
        L2 = c.get_points()
        if L1 == []:
            u = ConvexPolygon(L2)
        elif L2 == []:
            u = ConvexPolygon(L1)
        else:
            x1, y1 = L1[0]
            x2, y2 = L2[0]
            if x1 < x2 or (x1 == x2 and y1 < y2):
                L2_ordered = self.msort(L2, x1, y1)
                Lmerge = [(x1, y1)]
                Lmerge.extend(self.merge(L1[1:], L2_ordered, x1, y1))
            else:
                L1_ordered = self.msort(L1, x2, y2)
                Lmerge = [(x2, y2)]
                Lmerge.extend(self.merge(L1_ordered, L2[1:], x2, y2))
            L = self.convex_hull(Lmerge, True)
            u = ConvexPolygon(L)
        return u

    def bounding_box(self):
        '''
        Paràmetres: cap
        Retorna: un rectangle amb els costats paral·lels als eixos que
        engloba el propi polígon
        Descripció:
        Si és el polígon buit, es retorna un altre polígon buit
        Altrament es retorna el rectangle delimitat per ls x mínima,
        la y mínima, la x màxima i la y màxima
        '''
        n_points = len(self.__points__)
        if n_points == 0:
            b = ConvexPolygon()
        else:
            xmin = self.__xmin__
            ymin = self.__ymin__
            xmax = self.__xmax__
            ymax = self.__ymax__
            p1 = (xmin, ymin)
            p2 = (xmin, ymax)
            p3 = (xmax, ymax)
            p4 = (xmax, ymin)
            b = ConvexPolygon([p1, p2, p3, p4])
        return b

    def random_polygon(self, n):
        '''
        Paràmetres: un natural n
        Retorna: un polígon convex generat a partir de n punts aleatoris
        en unitats quadrades ([0,1],^2)
        Descripció:
        Generem una llista sense repetits de n punts aleatoris en unitats
        quadrades ([0,1],^2) i retornem el polígon convex que s'obté a
        partir d'aquesta.
        '''
        L = []
        if isinstance(n, int) and n > 0:
            for i in range(n):
                x = random.uniform(0, 1)
                y = random.uniform(0, 1)
                if (x, y) not in L:
                    L.append((x, y))
        r = ConvexPolygon(L)
        return r

    def draw(self, name='draw.png', l=[]):
        '''
        Paràmetres: un polígon convex
        Retorna: el nom de l'arxiu amb l'extensió i la llista de polígons
        que es vol dibuixar. Per defecte, el nom és draw.png i la llista
        és la llista buida
        Descripció:
        -En primer lloc, fem una búsqueda dels valors xmin, ymin, xmax, ymax
        entre tots els polígons.
        -Seguidament calculem els factors fx, fy que utilitzarem per reescalar
        els valors x, y respectivament.
        Si les distàncies entre xmax-xmin i entre ymax-ymin són 0, fx = fy = 1
        Si la distància entre xmax-xmin és 0 i entre ymax-ymin > 0, fx = 1 i
        fy = 397/dy
        Si la distància entre xmax-xmin és > 0 i entre ymax-ymin = 0, fy = 1 i
        fx = 397/dx
        Si les distàncies entre xmax-xmin i entre ymax-ymin són
        majors que 0, calcularem fx, fy a partir de la distància
        més gran fx = fy = 397/d_més_gran
        -Calculem el vector que va de xmin, ymin a 0, 0 i l'apliquem a tots els
        punts dels polígons per a que es trobin en la regió de x i y positives
        -Seguidament els multipliquem pels factors de reescala per que ocupin
        398x398 i la imatge estigui centrada.
        -Girem les y per a que el polígon no estigui cap per avall
        -Pintem els polígons amb els nous punts i del seu color
        '''
        img = Image.new('RGB', (400, 400), color='white')
        img1 = ImageDraw.Draw(img)
        xmin = None
        xmax = None
        ymin = None
        ymax = None
        first = False
        for i in l:
            xminima = i.get_xmin()
            yminima = i.get_ymin()
            xmaxima = i.get_xmax()
            ymaxima = i.get_ymax()
            if i.get_n_vertices() > 0:
                if not first:
                    xmin = xminima
                    xmax = xmaxima
                    ymin = yminima
                    ymax = ymaxima
                    first = True
                else:
                    if xminima < xmin:
                        xmin = xminima
                    if xmaxima > xmax:
                        xmax = xmaxima
                    if yminima < ymin:
                        ymin = yminima
                    if ymaxima > ymax:
                        ymax = ymaxima
        if xmin is not None and ymin is not None:
            dx = xmax - xmin
            dy = ymax - ymin
            for i in l:
                n = i.get_n_vertices()
                r, g, b = i.get_color()
                r = round(r*255)
                g = round(g*255)
                b = round(b*255)
                if dx == 0 and dy == 0:
                    points = [(199, 199) for x, y in i.get_points()]
                elif dx == 0:
                    fy = 397/dy
                    p = i.get_points()
                    points = [(199, 399-(y-ymin)*fy-1) for x, y in p]
                elif dy == 0:
                    fx = 397/dx
                    points = [((x-xmin)*fx+1, 199) for x, y in i.get_points()]
                elif dx > dy:
                    fx = 397/dx
                    m = (dy*fx)/2
                    a = 1+199-int(m)
                    p = i.get_points()
                    points = [((x-xmin)*fx+1, 399-(y-ymin)*fx-a) for x, y in p]
                else:
                    fy = 397/dy
                    m = (dx*fy)/2
                    a = 1+199-int(m)
                    p = i.get_points()
                    points = [((x-xmin)*fy+a, 399-(y-ymin)*fy-1) for x, y in p]
                if n == 1:
                    img1.point(points, fill=(r, g, b))
                elif n > 1:
                    img1.polygon(points, outline=(r, g, b))
        img.save(name)
