class MobberManager(object):
    def __init__(self):
        self.driver_index = 0
        self.navigator_index = 1
        self.mobber_list = []
        self.mobber_list_change_callbacks = []

    def mobber_count(self):
        return self.mobber_list.__len__()

    def add_mobber(self, mobber_name):
        self.mobber_list.append(mobber_name)
        self.fire_time_change_callbacks()

    def get_mobbers(self):
        return self.mobber_list

    def remove_mobber(self, remove_mobber_index):
        if self.mobber_count() == 0: return
        del self.mobber_list[remove_mobber_index]
        self.fire_time_change_callbacks()

    def move_mobber_up(self, swap_index):
        if self.mobber_count() == 0: return
        destination_index = swap_index - 1
        self.mobber_list[swap_index], self.mobber_list[destination_index] = self.mobber_list[destination_index], \
                                                                            self.mobber_list[swap_index]
        self.fire_time_change_callbacks()

    def move_mobber_down(self, swap_index):
        if self.mobber_count() == 0: return
        destination_index = (swap_index + 1) % self.mobber_list.__len__()
        self.mobber_list[swap_index], self.mobber_list[destination_index] = self.mobber_list[destination_index], \
                                                                            self.mobber_list[swap_index]
        self.fire_time_change_callbacks()

    def subscribe_to_mobber_list_change(self, mobber_list_change_callback):
        self.mobber_list_change_callbacks.append(mobber_list_change_callback)
        self.fire_time_change_callbacks()

    def fire_time_change_callbacks(self):
        self.update_navigator_driver_index()
        for mobber_list_change_callback in self.mobber_list_change_callbacks:
            if mobber_list_change_callback:
                mobber_list_change_callback(self.mobber_list, self.driver_index, self.navigator_index)

    def clear(self):
        self.mobber_list = []
        self.fire_time_change_callbacks()

    def switch_navigator_driver(self):
        mobber_count = self.mobber_list.__len__()
        if mobber_count > 0:
            self.driver_index = (self.driver_index + 1) % mobber_count
        self.update_navigator_driver_index()
        self.fire_time_change_callbacks()

    def update_navigator_driver_index(self):
        mobber_count = self.mobber_list.__len__()
        if mobber_count > 0:
            self.driver_index = self.driver_index % mobber_count
            self.navigator_index = (self.driver_index + 1) % mobber_count
        else:
            self.driver_index = 0
            self.navigator_index = 1

    def rewind_driver(self):
        mobber_count = self.mobber_list.__len__()
        if mobber_count > 0:
            self.driver_index = (self.driver_index - 1)
            if self.driver_index < 0:
                self.driver_index = mobber_count - 1
        self.update_navigator_driver_index()
        self.fire_time_change_callbacks()