from openi import OpenIApi

api = OpenIApi(token="d4fb86b56df9b71dd78ea00b966732734f817e09")

info = api.get_model_info("FoundationModel/01-ai", "Yi-1.5-34B")

print(info)
