from cortexquest.core.sheet_loader import SheetLoader


class DataManager:
    def __init__(self, sheet_loader: SheetLoader):
        self.sheet_loader = sheet_loader
        self.data = self.sheet_loader.load_data()

    def get_participant_data(self, participant_id: str):
        # Implement logic to get participant data
        pass

    def update_response(self, participant_id: str, response: dict):
        # Implement logic to update a response
        pass
