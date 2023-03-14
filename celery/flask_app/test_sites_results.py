
# take the second element for sort
def take_second(elem):
    return elem[0]

arr = []
nsitio = []
sites = []
with open("status1.csv") as archivo:
    for linea in archivo:
        linea=linea.replace("\n","")
        array = linea.split(",")

        #print(array)
        s=int(array[0].split("mc")[1].split(".")[0])
        arr.append((s,array[0],array[1]))
        #arr.append()
        #arr.append(array[1])

    arr = sorted(arr, key=take_second)
    #print(arr)

    for i,el in enumerate(arr):
        #if = 1
        sites.append(arr[1])
        print(i,el)
        #print(el)
    #for site in sites:
    #    print(sites)
    file = open('status_result.csv','w')   
    for site in arr: 
        file.write("\n")
        file.write(f"{site[1]},{site[2]}")
    file.close()

    file = open('status_result_offline.py','w')   
    for site in arr: 
        if site[2]!='1':
            file.write(f"'{site[1]}'\n")
    file.close()
