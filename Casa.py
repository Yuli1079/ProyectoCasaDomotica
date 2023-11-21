from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import auth as firebase_auth

# Inicializar Firebase
cred = credentials.Certificate('E:\\Universidad\\semestre 8\\programacion 2\\Proyecto (1)\\Proyecto\\casa-domotica-da5dd-firebase-adminsdk-uypxw-9c202520db.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://casa-domotica-da5dd-default-rtdb.firebaseio.com/'
})

class LoginRegistroApp:
    def __init__(self, master):
        self.master = master
        master.title('Monitoreo y Control de su casa')
        master.config(width=500, height=450, bg='sky blue')
        master.resizable(1, 1)
        master.iconbitmap('Casa_Domotica.ico')
        

        Label(master, text='Correo:').pack(pady=10)
        self.correo_entry = Entry(master)
        self.correo_entry.pack()

        Label(master, text='Contraseña:').pack(pady=10)
        self.clave_entry = Entry(master, show='*')
        self.clave_entry.pack()

        Label(master, text='Contraseña de Administrador:').pack(pady=10)
        self.clave_admin_entry = Entry(master, show='*')
        self.clave_admin_entry.pack()

        Button(master, text='Iniciar Sesión', command=self.iniciar_sesion).pack(pady=10)  # Espaciado vertical
        Button(master, text='Registrarse', command=self.registrarse).pack(pady=5)  # Espaciado vertical
        
         # Establecer el tamaño de la ventana
        master.geometry('250x260')

    def iniciar_sesion(self):
        correo = self.correo_entry.get()
        clave = self.clave_entry.get()

        try:
            usuario = firebase_auth.get_user_by_email(correo)
            firebase_auth.update_user(usuario.uid, password=clave)
            self.master.destroy()  # Cerrar la ventana de inicio de sesión
            root = Tk()
            app = CasaDomoticaApp(root, usuario.uid)
            root.mainloop()
        except firebase_auth.AuthError as e:
            messagebox.showerror('Error de autenticación', f'Error: {e}')


    def registrarse(self):
        correo = self.correo_entry.get()
        clave = self.clave_entry.get()
        clave_admin = self.clave_admin_entry.get()  # Nueva línea para obtener la clave de administrador

        try:
            # Verificar la clave de administrador
            if clave_admin == '123456':  # Reemplaza 'tu_clave_de_administrador' con tu propia clave
                usuario = firebase_auth.create_user(email=correo, password=clave)
                messagebox.showinfo('Registro exitoso', 'Usuario registrado correctamente')
            else:
                messagebox.showerror('Error de registro', 'Clave de administrador incorrecta')
        except ValueError as e:
            messagebox.showerror('Error de registro', f'Error: {e}')
        except firebase_auth.FirebaseError as e:
            error_code, error_message = e.error_info
            messagebox.showerror('Error de registro', f'Error ({error_code}): {error_message}')


class CasaDomoticaApp:
    def __init__(self, master, uid):
        self.master = master
        master.title('Monitoreo y Control de su casa')
        master.config(width=500, height=350, bg='sky blue')
        master.resizable(1, 1)
        master.iconbitmap('Casa_Domotica.ico')
        master.config(cursor='heart')

        self.temperatura = StringVar()
        self.alarma = StringVar()

        self.update_data_from_firebase()

        etiqueta_temperatura = Label(master, textvariable=self.temperatura)
        etiqueta_temperatura.pack()
        etiqueta_temperatura.place(x=350, y=50)


        etiqueta_Alarma = Label(master, textvariable=self.alarma)
        etiqueta_Alarma.pack()
        etiqueta_Alarma.place(x=350, y=170)
        
        # Botones de control para luces
        btn_luces_on = Button(self.master, text="On", command=self.encender_luces)
        btn_luces_on.pack()
        btn_luces_on.place(x=200, y=20)

        btn_luces_off = Button(self.master, text="Off", command=self.apagar_luces)
        btn_luces_off.pack()
        btn_luces_off.place(x=250, y=20)

        # Botones de control para puertas
        btn_puerta_abrir = Button(self.master, text="Abrir", command=self.abrir_puerta)
        btn_puerta_abrir.pack()
        btn_puerta_abrir.place(x=200, y=195)

        btn_puerta_cerrar = Button(self.master, text="Cerrar", command=self.cerrar_puerta)
        btn_puerta_cerrar.pack()
        btn_puerta_cerrar.place(x=250, y=195)

        # Botones de control para alarma
        btn_puerta_abrir = Button(self.master, text="Activar", command=self.activar_alarma)
        btn_puerta_abrir.pack()
        btn_puerta_abrir.place(x=350, y=200)

        btn_puerta_cerrar = Button(self.master, text="Desactivar", command=self.desactivar_alarma)
        btn_puerta_cerrar.pack()
        btn_puerta_cerrar.place(x=400, y=200)

        self.led()
        self.Puerta()

        self.start_update_task()  # Iniciar la tarea de actualización

    def update_data_from_firebase(self):
        lecturas_ref = db.reference('/lecturas')
        temperatura = lecturas_ref.child('temperatura').get()
        alarma = lecturas_ref.child('alarma').get()

        self.temperatura.set(f'Temperatura: {temperatura} °C')
        self.alarma.set(f'Alarma: {alarma}')

    def start_update_task(self):
        self.master.after(1000, self.update_data_and_reschedule)

    def update_data_and_reschedule(self):
        self.update_data_from_firebase()
        self.start_update_task()

    def led(self):
        etiqueta_led = Label(self.master, text="Luces: ")
        etiqueta_led.pack()
        etiqueta_led.place(x=50, y=20)

        imagen_pillow = Image.open('led1.jpg')
        self.imagen_led = ImageTk.PhotoImage(imagen_pillow)

        etiqueta_imagen_led = Label(self.master, image=self.imagen_led)
        etiqueta_imagen_led.pack()
        etiqueta_imagen_led.place(x=100, y=55)

    def Puerta(self):
        etiqueta_Puerta = Label(self.master, text="Puertas: ")
        etiqueta_Puerta.pack()
        etiqueta_Puerta.place(x=50, y=195)

        imagen_pillow = Image.open('puerta1.jpg')
        self.imagen_puerta = ImageTk.PhotoImage(imagen_pillow)

        etiqueta_puerta = Label(self.master, image=self.imagen_puerta)
        etiqueta_puerta.pack()
        etiqueta_puerta.place(x=100, y=230)
        
        
    def encender_luces(self):
        # Lógica para cambiar el estado de las luces en Firebase
        lecturas_ref = db.reference('/lecturas')
        lecturas_ref.update({'luz': 1})  # Cambiar el estado de las luces a encendido

    def apagar_luces(self):
        # Lógica para cambiar el estado de las luces en Firebase
        lecturas_ref = db.reference('/lecturas')
        lecturas_ref.update({'luz': 0})  # Cambiar el estado de las luces a apagado

    def abrir_puerta(self):
        # Lógica para cambiar el estado de la puerta en Firebase
        lecturas_ref = db.reference('/lecturas')
        lecturas_ref.update({'puerta': 1})  # Cambiar el estado de la puerta a abierta

    def cerrar_puerta(self):
        # Lógica para cambiar el estado de la puerta en Firebase
        lecturas_ref = db.reference('/lecturas')
        lecturas_ref.update({'puerta': 0})  # Cambiar el estado de la puerta a cerrada

    def activar_alarma(self):
        # Lógica para cambiar el estado de la alarma en Firebase
        lecturas_ref = db.reference('/lecturas')
        lecturas_ref.update({'alarma': 'activada'})  # Cambiar el estado de la alarma a activada

    def desactivar_alarma(self):
        # Lógica para cambiar el estado de la alarma en Firebase
        lecturas_ref = db.reference('/lecturas')
        lecturas_ref.update({'alarma': 'desactivada'})  # Cambiar el estado de la alarma a desactivada



if __name__ == "__main__":
    root_login = Tk()
    app_login = LoginRegistroApp(root_login)
    root_login.mainloop()
