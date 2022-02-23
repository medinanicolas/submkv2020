import os, sys
from os import path, system, mkdir, popen
from colorama import init,Fore,Style
from argparse import ArgumentParser
header=r"""
    ___       ___       ___       ___       ___       ___        
   /\  \     /\__\     /\  \     /\__\     /\__\     /\__\       
  /::\  \   /:/ _/_   /::\  \   /::L_L_   /:/ _/_   /:/ _/_      
 /\:\:\__\ /:/_/\__\ /::\:\__\ /:/L:\__\ /::-"\__\ |::L/\__\     
 \:\:\/__/ \:\/:/  / \:\::/  / \/_/:/  / \;:;-",-" |::::/  /     
  \::/  / 2 \::/  / 0 \::/  /SUB /:/  / 2 |:|  | 0  L;;/__/      
   \/__/     \/__/     \/__/ MKV \/__/     \|__|             

        Script para subtitular archivos de video
                Este script utiliza ffmpeg
"""

def get_realpath(arg_path):
    return path.realpath(path.join(path.dirname(arg_path), path.basename(arg_path)))

init(autoreset=True)

print(header)

argparser = ArgumentParser(description="SubMKV20")
argparser.add_argument("-m", "--mov", help="Input movie file", metavar="MOVIE", required=True, type=str)
argparser.add_argument("-s", "--sub", help="Input Subtitule file", metavar="SUB", required=True, type=str)
argparser.add_argument("-l", "--lan", help="Subtitle language", metavar="LANG", default="spa", choices=["spa", "eng", "fre", "ita", "ger"], type=str)
argparser.add_argument("-o", "--out", help="Output movie subtituled directory", metavar="OUT", type=str)
args = argparser.parse_args()

movie = get_realpath(args.mov)
sub = get_realpath(args.sub)
out = path.realpath(path.dirname(movie))

if args.out:
    if not path.isdir(args.out):
        print(Fore.RED + "Error:", args.out, "no existe. Configurado ->", out)
    else:
        out = args.out
else:
    print(Fore.YELLOW + "Advertencia:", "directorio de salida no configurado. Configurado ->", out)

if not path.isfile(movie) & path.isfile(sub):
    print(Fore.RED + "Error:", "No se ha podido encontrar los archivos de entrada", path.basename(movie), path.basename(sub))

if movie.lower().endswith(".mp4"):
    filename = path.basename(movie)[:-4]

    sub_enc = popen("file --mime-encoding -b '"+sub+"'").read().strip()

    print(Fore.CYAN + "Codificación:", sub_enc)
    print(Fore.CYAN + "Subtitulando...", "(esto puede tardar)")
    if system("""
        ffmpeg -y -i "{}" \
            -sub_charenc {} \
                -i "{}" -map 0:v -map 0:a -c copy \
                    -map 1 -c:s:0 copy -metadata:s:s:0 language={} -disposition:s:0 default \
                        "{}_submkv.mkv" > /dev/null 2>&1
                        """.format(movie, sub_enc , sub, args.lan, path.join(out, filename))) != 0:
        print(Fore.RED+"Error:", "Ha ocurrido un error subtitulando")
    else:
        print(Fore.MAGENTA + "Done! :)")
else:
    print(Fore.RED + "Error:", "WowOwow, a donde vas camarada? Aquí solo aceptamos mp4's")