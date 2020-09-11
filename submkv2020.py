from os import path,listdir,system,mkdir,popen
from colorama import init,Fore,Style
header=r"""
    ___       ___       ___       ___       ___       ___        
   /\  \     /\__\     /\  \     /\__\     /\__\     /\__\       
  /::\  \   /:/ _/_   /::\  \   /::L_L_   /:/ _/_   /:/ _/_      
 /\:\:\__\ /:/_/\__\ /::\:\__\ /:/L:\__\ /::-"\__\ |::L/\__\     
 \:\:\/__/ \:\/:/  / \:\::/  / \/_/:/  / \;:;-",-" |::::/  /     
  \::/  / 2 \::/  / 0 \::/  /SUB /:/  / 2 |:|  | 0  L;;/__/      
   \/__/     \/__/     \/__/ MKV \/__/     \|__|             

 Script para subtitular archivos de video
 Este script esta basado en comando de ffmpeg

 ADVENTENCIA:
 Esto puede generar efectos destructivos
 Asegurece de que los subtitulos tengan exactamente el mismo nombre que los archivos de video\n"""
menu="""\n
    [1] Añadir subs (mp4)

    [0] Salir
"""
init(autoreset=True)
print(header+menu)
menu_opc = input(">>> ")
while True:
    if menu_opc == '1':
        while True:
            directorio = input("Directorio ["+Style.BRIGHT+"current"+Style.RESET_ALL+"]:")
            if not directorio: 
                directorio='.'
                break
            break
        while True:
            sub_ext = input("Extension subs ["+Style.BRIGHT+"srt"+Style.RESET_ALL+"/ssa/ass]:")
            if not sub_ext:
                sub_ext='srt'
                break
            elif sub_ext != 'srt' or sub_ext != 'ssa' or sub_ext != 'ass':
                print(Fore.RED+"Error:",Fore.RESET+"No se ha especificado una extensión correcta.")
                continue
        while True:
            sub_len = input("Lenguaje subs ["+Style.BRIGHT+"spa"+Style.RESET_ALL+"/eng/fre/ger/ita]:")
            if not sub_len:
                sub_len = 'spa'
                break
            elif sub_len != 'spa' or sub_len != 'eng' or sub_len != 'fre' or sub_len != 'ger' or sub_len != 'ita':
                continue
        break
    elif menu_opc == 0:
        exit(0)
    else:
        print(Fore.RED+"Error:",Fore.RESET+"Seleccione una opción correcta.")
        continue
print("Leyendo archivos... ")
try:
    archivos = sorted(listdir(directorio))
except:
    print(Fore.RED+"Error:",Fore.RESET+"No se puede leer el contenido en",directorio)
    exit(1)
try:
    print("Creando carpeta de respaldo... ")
    if not path.isdir(path.join(directorio,"backup")):
      mkdir(path.join(directorio,"backup"))
except:
    print(Fore.RED+"Error:",Fore.RESET+"No se ha podido crear la carpeta de respaldo.")
    exit(1)
print("Procesando archivos...")
archivos_filt = list()
for archivo in archivos:
    if archivo.endswith('.mp4'):
        archivos_filt.append(archivo)
if len(archivos_filt)<1:
    print(Fore.RED+"Error:",Fore.RESET+"No se han encontrado archivos.")
    exit(1)
for archivo in sorted(archivos_filt):
    if archivo.endswith(".mp4"):
        nom_archivo = archivo[:-4]
        print("Buscando subtitulos para:",archivo)
        sub = nom_archivo+'.'+sub_ext
        if not path.exists(path.join(directorio,sub)):
            print(Fore.RED+"Error:",Fore.RESET+"No se han encontrado subtitulos para",archivo+". Omitiendo...")
            continue
        codcar=popen("file --mime-encoding -b '"+path.join(directorio,sub)+"'").read().strip()
        print("Codificación:",codcar)
        print("Subtitulando... (esto puede tardar)")
        if system("""
        ffmpeg -y -i "{}" \
            -sub_charenc {} \
                -i "{}" -map 0:v -map 0:a -c copy \
                    -map 1 -c:s:0 {} -metadata:s:s:0 languaje={} -disposition:s:0 default \
                        "{}_submkv.mkv" > /dev/null 2>&1
                        """.format(path.join(directorio,archivo),codcar,path.join(directorio,sub),sub_ext,sub_len,path.join(directorio,nom_archivo))) != 0:
            print(Fore.RED+"Error:",Fore.RESET+"Ha ocurrido un error subtitulando "+archivo+". Omitiendo...")
            continue
        print("Respaldando archivos originales... ")
        if system("""mv "{}" "{}" "{}" """.format(path.join(directorio,archivo),path.join(directorio,sub),path.join(directorio,'backup'))) != 0:
            print(Fore.RED+"Error:",Fore.RESET+"Ha ocurrido un error respaldando "+archivo+". Omitiendo...")
        print("Done! :)")