class Customer:

    def __init__(self, id, name, address, phone, custom_num):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.custom_num = custom_num

    def get_customer_info(self):
        info = [0, self.id, self.name, self.address, self.phone, self.custom_num]
        return info

    def set_cutomer_info(self, id, name, address, phone, custom_num):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.custom_num = custom_num
