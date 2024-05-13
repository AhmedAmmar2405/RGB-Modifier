import numpy as np
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

# Initialiser imagemdf comme un tableau vide
imagemdf = np.empty((0,0,0), dtype=np.uint8)

def import_picture():
    global image_label, imagemdf
    filepath = filedialog.askopenfilename()
    if filepath:
        image = cv2.imread(filepath)
        if image is not None:
            # Convertir l'image OpenCV en format compatible avec Tkinter
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            # Mettre à jour l'étiquette d'image
            image_label.config(image=photo)
            image_label.image = photo
            # Initialiser imagemdf avec la même image
            imagemdf = np.array(image)

def modifier_couleur(r, g, b):
    global image_label, imagemdf
    if imagemdf.shape != (0,0,0):
        imagemdf[:, :, 0] += int(b)
        imagemdf[:, :, 1] += int(g)
        imagemdf[:, :, 2] += int(r)

        imagemdf = np.clip(imagemdf, 0, 255)

        # Convertir l'image en RGB
        imagemdf_rgb = cv2.cvtColor(imagemdf, cv2.COLOR_BGR2RGB)

        # Convertir l'image en format PhotoImage de Tkinter
        imagemdf_pil = Image.fromarray(imagemdf_rgb)
        imagefinal = ImageTk.PhotoImage(image=imagemdf_pil)

        image_modifier.config(image=imagefinal)
        image_modifier.image = imagefinal

def delete():
    global imagemdf
    imagemdf = np.empty((0,0,0), dtype=np.uint8)
    # Détruire l'objet PhotoImage associé à l'étiquette
    if image_label.image:
        image_label.image = None
        if image_modifier.image:
            image_modifier.image=None
    # Effacer l'image de l'étiquette
    else:
        image_label.config(image=None)
        image_modifier.config(image=None)
def reset():
    global image_modifier, imagemdf
    if image_modifier is not None and imagemdf is not None:
        # Réinitialiser l'image modifiée à l'image importée initiale
        image_modifier.config(image=image_label.cget("image"))
        # Réinitialiser l'array imagemdf à l'array initial
        imagemdf = np.array(Image.open(image_label.cget("image")))


def telecharger():
    global imagemdf
    if imagemdf is not None:
        filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if filepath:
                # Enregistrer l'image modifiée
                cv2.imwrite(filepath, cv2.cvtColor(imagemdf, cv2.COLOR_RGB2BGR))

fenetre = tk.Tk()
fenetre.title("RGB manipulation")

button1=tk.Button(fenetre, text="import a picture", bg="green", command=import_picture)
button1.grid(row=0, column=0, padx=5, pady=5)

image_label = tk.Label(fenetre)
image_label.grid(row=1, column=0, padx=5, pady=5)

scale_red = tk.Scale(fenetre, label="Rouge", from_=0, to=255, orient="horizontal", length=150, resolution=1,
                     command=lambda value: modifier_couleur(scale_red.get(), scale_green.get(), scale_blue.get()))
scale_red.grid(row=2, column=0, padx=5, pady=5)

scale_green = tk.Scale(fenetre, label="Vert", from_=0, to=255, orient="horizontal", length=150, resolution=1,
                       command=lambda value: modifier_couleur(scale_red.get(), scale_green.get(), scale_blue.get()))
scale_green.grid(row=2, column=1, padx=5, pady=5)

scale_blue = tk.Scale(fenetre, label="Bleu", from_=0, to=255, orient="horizontal", length=150, resolution=1,
                      command=lambda value: modifier_couleur(scale_red.get(), scale_green.get(), scale_blue.get()))
scale_blue.grid(row=2, column=2, padx=5, pady=5)

image_modifier = tk.Label(fenetre)
image_modifier.grid(row=1, column=2, columnspan=3, padx=5, pady=5)

button_supprime=tk.Button(fenetre, text="Supprimer", bg='red', command=delete)
button_supprime.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
button_reset=tk.Button(fenetre, text="Reset", bg='white', command=reset)
button_reset.grid(row=4, column=1, columnspan=3, padx=5, pady=5)
button_telecharger=tk.Button(text="Telecharger",bg="green",command=telecharger)
button_telecharger.grid(row=4, column=2, columnspan=3, padx=5, pady=5)

fenetre.mainloop()
