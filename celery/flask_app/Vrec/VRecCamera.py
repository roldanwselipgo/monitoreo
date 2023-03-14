import logging
from   datetime import datetime

#
# Procesa la lista de videos disponibles para determinar:
# - Primer video disponible
# - Ultimo video disponible
# - Video faltantes
#
def ProcessVideoList(videoList):
    logging.info(f"ProcessVideoList( )")

    first  = 0
    last   = 0
    prev   = 0
    lost   = []

    for videoStr in videoList:
        video = int(videoStr)
        if not first:
            first = video

        #print(video)
        # Busca los segmentos faltantes (de entrada asumiendo que son segmentos de 1 hora)
        prev = last

        if (prev):
            delta = video - prev

            videoDt = datetime.strptime(str(video), "%Y%m%d%H")
            prevDt  = datetime.strptime(str(prev), "%Y%m%d%H")

            # Obtiene la diferencia de los horarios, en Minutos
            delta = (videoDt-prevDt).total_seconds() / 60 
            
            #print(f"Dates: '{prevDt}' '{videoDt}' ", delta)

            if (delta > 60):
                lostDate = [str(prevDt), str(videoDt)]
                lost.append(lostDate)
                #print(f">> {prevDt} {videoDt} {delta}")
            
        last = video    
        #logging.info(f"Lost videos: ( {lost} )")
   

    #print("\n\r", datetime.strptime(str(first), "%Y%m%d%H"), datetime.strptime(str(last), "%Y%m%d%H"))
    #print(loosen)

    #print("fll:",datetime.strptime(str(first), "%Y%m%d%H"), datetime.strptime(str(last), "%Y%m%d%H"), lost)
    #print(">>first last:",first,last)
    return datetime.strptime(str(first), "%Y%m%d%H"), datetime.strptime(str(last), "%Y%m%d%H"), lost
