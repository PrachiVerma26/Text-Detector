import customtkinter as ctk
import tkinter
import os
import cv2
import pytesseract
from PIL import Image,UnidentifiedImageError
import webbrowser

file = ""
image = ""
previous = ""

#class for webcam frame
class openwebcam(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        def tesseract():
            path_to_tesseract=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            Imagepath='test1.jpg'
            pytesseract.tesseract_cmd=path_to_tesseract
            text=pytesseract.image_to_string(Image.open(Imagepath))
            return text
        tesseract()

        def convert():
            # do the conversion
            
            if not tesseract():
                return
            try:
                result = tesseract()
            except:
                tkinter.messagebox.showerror("Missing Tesseract-OCR!",
                                     "Tesseract is not installed or it's not in your PATH")
                return

            text_box.delete(1.0, tkinter.END)
            text_box.insert(tkinter.END, result)

        frame_1 = ctk.CTkFrame(self)
        frame_1.grid(row=0, column=0, sticky="nsew", padx=15, pady=20)
        #frame_1.rowconfigure(0, weight=0)
        #frame_1.columnconfigure(0, weight=1)

        frame_2 = ctk.CTkFrame(self)
        frame_2.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)
        #frame_2.rowconfigure(1, weight=1)
        #frame_2.columnconfigure(0, weight=1)
    
        label_header = ctk.CTkButton(frame_1, text="TEXTIMAGE", 
                             height=30,hover=False, corner_radius=30)
        label_header.grid(row=2,column=0,padx=10, pady=10)
        label_header.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
        

        openwebcam_button = ctk.CTkButton(frame_1, text="OPEN WEBCAM", command=self.open_webcam_button_event, anchor="center", corner_radius=30)
        openwebcam_button.grid(row=3, column=0, padx=20, pady=20)
        openwebcam_button.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        convert_button = ctk.CTkButton(frame_1, text="EXTRACT", command=convert, corner_radius=30)
        convert_button.grid(row=15, column =2,padx=10, pady=10, sticky="we")
        convert_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        label_2 = ctk.CTkLabel(frame_2, text="Converted text will be shown here")
        label_2.grid(padx=20, pady=20)

        text_box = ctk.CTkTextbox(frame_2,width=750,height=450)
        text_box.grid(sticky="news", padx=20, pady=20)
        
        
        #text_box._textbox.configure(selectbackground=))
    def webcam1(self):

        camera=cv2.VideoCapture(0)
        while True:

            _,image=camera.read()
            cv2.imshow('text detection',image)
            if cv2.waitKey(1)& 0xFF==ord('s'):
                cv2.imwrite('test1.jpg',image)
                break
        camera.release()
        cv2.destroyAllWindows()

    def open_webcam_button_event(self):
        self.webcam1()
#class for opening an image frame    
class openimage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        def open_image():
            # open image file
            global file, image, img, previous
            file = tkinter.filedialog.askopenfilename(filetypes =[('Images', ['*.png','*.jpg','*.jpeg','*.bmp','*webp'])
                                                          ,('All Files', '*.*')])
            if file:
                previous = file
                if len(os.path.basename(file))>=30:
                    open_button.configure(text=os.path.basename(file)[:30]+"..."+os.path.basename(file)[-3:])
                else:
                    open_button.configure(text=os.path.basename(file))

                try:
                    Image.open(file)
                except UnidentifiedImageError:
                    tkinter.messagebox.showerror("Oops!", "Not a valid image file!")
                    return

                img = Image.open(file)   
                image = ctk.CTkImage(img)
                label_image.configure(text="", image=image)
                image.configure(size=(label_image.winfo_height(),label_image.winfo_height()*img.size[1]/img.size[0]))
            else:
                if previous!="":
                    file = previous
            
        '''def resize_event(event):
            # dynamic resize of the image with UI
            global image
            if image!="":
                image.configure(size=(event.height,event.height*img.size[1]/img.size[0]))'''

        def convert():
            # do the conversion
            if not file:
                return
            try:
                result = pytesseract.image_to_string(img)
            except:
                tkinter.messagebox.showerror("Missing Tesseract-OCR!",
                                     "Tesseract is not installed or it's not in your PATH")
                return

            text_box.delete(1.0, tkinter.END)
            text_box.insert(tkinter.END, result)

        if ctk.get_appearance_mode()=="Dark":
            o = 1
        else:
            o = 0
    
        def new_window():
            # About window 
            label_header.configure(state="disabled")
        
            def web(link):
                webbrowser.open_new_tab(link)
            
            try:
                version = str(pytesseract.get_tesseract_version())[:5]
            except:
                version = "Unknown"
        
        DIRPATH = os.getcwd()

        with open(os.path.join(DIRPATH,"tesseract_path.txt"), 'r') as tfile:
            patht = tfile.read() # read the path from the path file
            pytesseract.pytesseract.tesseract_cmd = patht
            tfile.close()

        frame_1 = ctk.CTkFrame(self,width=800, height=400)
        frame_1.grid(row=0, column=0, sticky="news", padx=20, pady=20)
        frame_1.rowconfigure(2, weight=1)
        frame_1.columnconfigure(0, weight=1)

        frame_2 = ctk.CTkFrame(self,width=200,height=400)
        frame_2.grid(row=0, column=1, sticky="news", padx=(0,20), pady=20)
        frame_2.rowconfigure(1, weight=1)
        frame_2.columnconfigure(0, weight=1)

        label_header = ctk.CTkButton(frame_1, text="TEXTEMAGE", 
                             height=30, command=new_window, hover=True, corner_radius=30)
        label_header.grid(padx=10, pady=10)

        open_button = ctk.CTkButton(frame_1, text="OPEN SOURCE IMAGE", command=open_image, corner_radius=30)
        open_button.grid(padx=10, pady=10, sticky="nsew")

        image_frame = ctk.CTkFrame(frame_1, corner_radius=20)
        image_frame.grid(padx=10, pady=10, sticky="nsew")
        image_frame.rowconfigure(0, weight=1)
        image_frame.columnconfigure(0, weight=1)

        label_image = ctk.CTkLabel(image_frame, text="➕", corner_radius=10)
        label_image.grid(padx=10, pady=10, sticky="nsew")

        #image_frame.bind("<Configure>", resize_event)

        convert_button = ctk.CTkButton(frame_1, text="EXTRACT", command=convert, corner_radius=30)
        convert_button.grid(padx=10, pady=10, sticky="we")

        label_2 = ctk.CTkLabel(frame_2, text="Converted text will be shown here")
        label_2.grid(padx=10, pady=10)

        text_box = ctk.CTkTextbox(frame_2,width=800, height=450)
        text_box.grid(sticky="nsew", padx=10, pady=10)
        text_box._textbox.configure(selectbackground=open_button._apply_appearance_mode(open_button._fg_color))
        

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image to Txt Converter.py")
        self.geometry("700x500")
        #ctk.set_default_color_theme("dark-blue")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        
        #create navigation or side frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  TEXT DETECTOR", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), font=ctk.CTkFont(size=15), hover_color=("gray70", "gray30"),
                                                   anchor="c",command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.webcamframe_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Webcam Mode",
                                                      fg_color="red", text_color=("gray10", "gray90"), font=ctk.CTkFont(size=15), hover_color=("gray70", "gray30"),
                                                       anchor="c", command=self.webcamframe_2_button_event)
        self.webcamframe_2_button.grid(row=2, column=0, sticky="ew")

        self.imageframe_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Image Mode",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), font=ctk.CTkFont(size=15), hover_color=("gray70", "gray30"),
                                                       anchor="c", command=self.imageframe_3_button_event)
        self.imageframe_3_button.grid(row=3, column=0, sticky="ew")

        #appearance mode
        self.appearance_mode_label = ctk.CTkLabel(self.navigation_frame, text="Appearance Mode:", font=ctk.CTkFont(size=15), anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(10,0), sticky="s")

        #scaling mode
        self.scaling_label = ctk.CTkLabel(self.navigation_frame, text="UI Scaling:", font=ctk.CTkFont(size=15), anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.navigation_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        #create textbox in home frame
        self.home_frame_textbox = ctk.CTkTextbox(self.home_frame, width=250, height=300)
        self.home_frame_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.home_frame_textbox.insert("0.0", "TEXT DETECTOR" + "\n\nGeneral Instructions for use of the app: \n\n1.Two modes of operation i.e webcam and input image \n\n2.Webcam captures the image and displays results on terminal \n\n3.Input image mode opens up a window and detects individual characters \n\n4.Images other than webcam input can also be added by either specifying path or input image filename \n\n5. Press 's' to capture images using Webcam Mode")

        #create webcam frame
        self.webcam_frame = openwebcam(master=self)
        self.webcam_frame.grid_columnconfigure(0, weight=1)
        
        # create image frame
        self.image_frame = openimage(master=self)
        self.webcam_frame.grid_columnconfigure(0, weight=1)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.webcamframe_2_button.configure(fg_color=("gray75", "gray25") if name == "webcam_mode" else "transparent")
        self.imageframe_3_button.configure(fg_color=("gray75", "gray25") if name == "image_mode" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "webcam_mode":
            self.webcam_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.webcam_frame.grid_forget()
        if name == "image_mode":
            self.image_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.image_frame.grid_forget()
        
    
    def home_button_event(self):
        self.select_frame_by_name("home")

    def webcamframe_2_button_event(self):
        self.select_frame_by_name("webcam_mode")

    def imageframe_3_button_event(self):
        self.select_frame_by_name("image_mode")

    def change_appearance_mode_event(self, new_appearance_mode):
            ctk.set_appearance_mode(new_appearance_mode)
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
