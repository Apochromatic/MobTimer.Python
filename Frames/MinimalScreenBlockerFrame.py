from tkinter import ttk, N, E, W, S
from datetime import datetime


from Infrastructure.ImageUtility import ImageUtility


class MinimalScreenBlockerFrame(ttk.Frame):
    def __init__(self, master, controller, time_options_manager, mobber_manager, countdown_manager, settings_manager,
                 tips_manager, theme_manager,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.controller = controller
        self.countdown_manager = countdown_manager
        self.time_options_manager = time_options_manager
        self.mobber_manager = mobber_manager
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager
        self.tips_manager = tips_manager
        self.build_window_content()
        self.mobber_manager.subscribe_to_mobber_list_change(self.mobber_list_change_callback)
        if self.settings_manager.get_continue_screen_blocker_show_current_time():
            self.countdown_manager.subscribe_to_time_changes(self.update_current_time)

    def update_current_time(self, days, minutes, seconds):
        self.current_time_label["text"] = datetime.now().strftime('%Y-%m-%d     %I:%M %p')

    def build_window_content(self):
        center_frame = ttk.Frame(self)
        center_frame.grid()

        row_index = 0


        image_utility = ImageUtility(self.theme_manager)



        self.invisible_icon = image_utility.load('images\\invisible.png')
        self.fade_label = ttk.Label(center_frame, image=self.invisible_icon)
        self.fade_label.grid(row=0, column=0, sticky=(N,W))
        self.fade_label.bind("<Enter>", lambda event: self.controller.fade_app())
        self.fade_label.bind("<Leave>", lambda event: self.controller.unfade_app())

        if self.settings_manager.get_general_use_logo_image():
            self.image_utility = ImageUtility(self.theme_manager)
            self.background_image = self.image_utility.load(self.settings_manager.get_general_logo_image_name(),800,200,self.settings_manager.get_general_auto_theme_logo())
            title = ttk.Label(center_frame, image=self.background_image)
        else:
            title = ttk.Label(center_frame, text="Mobbing Timer", font="Helvetica 60 bold italic")
        title.grid(row=row_index,  column = 0, columnspan=6 ,padx=150, pady=10)
        row_index += 1

        self.keyboard_icon = image_utility.load('images\\keyboard.png',75,75)
        self.keyboard_label = ttk.Label(center_frame, image=self.keyboard_icon)
        self.keyboard_label.grid(row=row_index, column=1, sticky=(N,E))

        self.current_mobber_label = ttk.Label(center_frame, text="", font="Helvetica 50 bold italic",
                                              style="Highlight.TLabel")
        self.current_mobber_label.grid(row=row_index, column=2, columnspan=1,  sticky=(N,W))



        self.minions_icon = image_utility.load('images\\minions.png',75,75)
        self.minions_label = ttk.Label(center_frame, image=self.minions_icon)
        self.minions_label.grid(row=row_index, column=3, sticky=(N,E))

        self.next_mobber_label = ttk.Label(center_frame, text="", font="Helvetica 50")
        self.next_mobber_label.grid(row=row_index, column=4, columnspan=1,sticky=(N,W))
        row_index += 1

        start_button = ttk.Button(center_frame, text="Continue Mobbing!", style="StartButton.TButton", )
        start_button.grid(row=row_index, column=1, columnspan=4, sticky=N + E + W, padx=10, pady=10)
        start_button.bind("<Button-1>", lambda event: self.controller.show_transparent_countdown_frame())
        row_index += 1

        if self.settings_manager.get_general_enable_tips():
            self.tip_text = ttk.Label(center_frame, text="", font="Helvetica 15 bold", wraplength=500)
            self.tip_text.grid(row=row_index, column=1, columnspan=4, padx=30, pady=10, sticky=(N))
            row_index += 1

        if self.settings_manager.get_continue_screen_blocker_show_current_time():
            self.current_time_label = ttk.Label(center_frame, text="current time",font="Helvetica 15")
            self.current_time_label.grid(row=row_index, column=1, columnspan=4, padx=30, pady=10, sticky=(N))
            row_index += 1


        start_button = ttk.Button(center_frame, text="Mob Setup & Time")
        start_button.grid(row=row_index, column=1, columnspan=4, sticky=N + E + W, padx=90, pady=10)
        start_button.bind("<Button-1>", lambda event: self.controller.show_screen_blocker_frame())
        row_index += 1

        start_button = ttk.Button(center_frame, text="Quit Mobbing")
        start_button.grid(row=row_index, column=1, columnspan=4, sticky=N + E + W, padx=90, pady=10)
        start_button.bind("<Button-1>", lambda event: self.controller.quit_and_destroy_session())
        row_index += 1
    def mobber_list_change_callback(self, mobber_list, driver_index, navigator_index):
        self.current_mobber_label['text'] = ""
        self.next_mobber_label['text'] = ""
        for index in range(0, mobber_list.__len__()):
            name = mobber_list[index]
            if index == driver_index:
                self.current_mobber_label['text'] = "{} ".format(name)
            if index == navigator_index:
                self.next_mobber_label['text'] = "{}".format(name)
        if self.settings_manager.get_general_enable_tips():
            self.tip_text['text'] = self.tips_manager.get_random_tip()