
from app.services.router_service import router_service


print("\n========== ROUTER TEST ==========\n")


subjects = [
    "web_developement",
    "mathematics",
    "physics",
]


for subject in subjects:

    route = router_service.route_subject(subject)

    print(
        f"Subject: {subject}"
    )

    print(
        f"Route:   {route}"
    )

    print("-" * 40)

