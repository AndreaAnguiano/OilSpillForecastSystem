from mainF import main
namePosition = ['P1', 'P2', 'P3', 'P4', 'P5','P6']
coords = [[-95.01622889, 25.97096444],[-95.25811667, 25.36115583], [-96.56495556, 24.75155556],[- 96.82528583, 23.51224639],[-96.71577028, 20.97098889],[-94.76735833, 20.04058889]]
latbox = [18.2, 31]
lonbox = [-98, -83]

for indx in range(0,len(namePosition)):
        print 'running ', namePosition[indx], ' position', coords[indx]
        main(coords[indx], namePosition[indx], latbox,lonbox)


