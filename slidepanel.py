import customtkinter as ctk

class SlidePanel(ctk.CTkFrame):
    def __init__(self,parent, start_pos, end_pos):
        super().__init__(master = parent, fg_color = '#36393e')

        self.start_pos = start_pos + 0.004
        self.end_pos = end_pos 
        self.width = abs(start_pos - end_pos)

        self.pos = self.start_pos
        self.in_start_pos = True

        self.place(relx = self.start_pos, rely = 0, relwidth = self.width, relheight = 1)
    
    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.004
            self.place(relx = self.pos, rely = 0, relwidth = self.width, relheight = 0.9)
            self.after(1, self.animate_forward)
        else: 
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.004
            self.place(relx = self.pos, rely = 0, relwidth = self.width, relheight = 0.9)
            self.after(1, self.animate_backwards)
        else: 
            self.in_start_pos = True

'''def move_btn():
    global button_x
    button_x += 0.001
    button.place(relx = button_x, rely=0.5, anchor = 'center')

    return None'''

'''
window = ctk.CTk()
window.title('Animated Widgets')
window.geometry('600x400')'''

#animated_panel = SlidePanel(root, 1, 0.7)

'''
button_x = 0.5
button = ctk.CTkButton(window, text = 'toggle sidebar', command= animated_panel.animate)
button.place(relx = button_x, rely = 0.5, anchor = 'center')

window.mainloop()'''

