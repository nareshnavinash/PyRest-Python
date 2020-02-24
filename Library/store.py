class Store:

    URL = None
    global_data_path = None
    dynamic_data_path = None
    static_data_path = None
    current_response = None
    ignore_keys = []

    @staticmethod
    def reset_all_variables():
        Store.ignore_keys = []
        Store.current_response = None
