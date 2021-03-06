import tableau

class TableauBuilder(object):
    def build(self, signedFormulas):
        """ Vytvori a vrati uzavrete alebo uplne tablo pre zoznam oznacenych formul. """

        # vyplnime prve vrcholy podla zoznamu vstupnych formul
        tabl = tableau.Tableau()
        lastNode = None
        for sf in signedFormulas:
            newNode = tableau.Node(sf)
            tabl.append(lastNode, newNode)
            lastNode = newNode

        # TODO vytvorit tablo

        return tabl

# vim: set sw=4 ts=8 sts=4 et :
