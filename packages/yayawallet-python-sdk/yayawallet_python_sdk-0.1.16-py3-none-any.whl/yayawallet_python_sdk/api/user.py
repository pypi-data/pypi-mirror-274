from ..functions.api_request import api_request

async def get_organization():
  api_response = await api_request("GET", "/user/organization", "", None)
  return api_response

async def get_profile():
  api_response = await api_request("GET", "/user/profile", "", None)
  return api_response

async def search_user(query: str):
  api_response = await api_request("POST", "/user/search", "", { "query": query })
  return api_response