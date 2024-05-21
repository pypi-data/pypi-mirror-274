from gitsint import *


async def profile(user, client, out,args):
    name = "aprofile"
    domain = "Github Profile"
    method="api"
    frequent_rate_limit=True
    out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
            "rateLimit": False,
            "exists": True,
            "data": user,
            "others": None})

