import random
import requests
from config import API_TIMEOUT

# Mock One Piece lore data (fallback if API unavailable)
MOCK_LORE = [
    {
        "category": "Devil Fruit",
        "name": "Gomu Gomu no Mi",
        "description": "A Paramecia-type Devil Fruit that allows the user to stretch their body like rubber. Eaten by Monkey D. Luffy, it grants him immunity to most blunt attacks and electricity."
    },
    {
        "category": "Character",
        "name": "Roronoa Zoro",
        "description": "The swordsman of the Straw Hat Pirates and one of their two combatants alongside Sanji. He aims to become the world's greatest swordsman and wields three swords in his unique Santoryu style."
    },
    {
        "category": "Location",
        "name": "Raftel",
        "description": "The final island of the Grand Line where One Piece is said to be located. Only the Pirate King Gol D. Roger and his crew have ever reached it. The island can only be found by piecing together four Road Poneglyphs."
    },
    {
        "category": "Organization",
        "name": "Shichibukai",
        "description": "Also known as the Seven Warlords of the Sea, these are seven powerful pirates who work for the World Government in exchange for having their bounties suspended and immunity from prosecution."
    },
    {
        "category": "Weapon",
        "name": "Meito",
        "description": "A classification of exceptional swords in the One Piece world. These blades are renowned for their quality and are wielded by the most skilled swordsmen. They are divided into graded and ungraded categories."
    },
    {
        "category": "Concept",
        "name": "Haki",
        "description": "A form of spiritual energy that exists within all living beings in the One Piece world. It manifests in three types: Observation Haki, Armament Haki, and Conqueror's Haki, each with unique applications."
    },
    {
        "category": "Ship",
        "name": "Thousand Sunny",
        "description": "The second ship of the Straw Hat Pirates, built by the shipwright Franky using the legendary Adam Wood. It features various vehicles and gadgets, including the Mini Merry II and the Shark Submerge III."
    },
    {
        "category": "Event",
        "name": "Marineford War",
        "description": "A massive battle between the World Government and the Whitebeard Pirates over the execution of Portgas D. Ace. It marked the end of the era of Gol D. Roger and the beginning of a new age of piracy."
    },
    {
        "category": "Treasure",
        "name": "Poneglyph",
        "description": "Indestructible stone tablets scattered throughout the world, written in an ancient language that only a few can read. They reveal the lost history of the Void Century and the location of Raftel."
    },
    {
        "category": "Faction",
        "name": "Revolutionary Army",
        "description": "A military organization led by Monkey D. Dragon, aiming to overthrow the World Government. They operate in secret across the world, recruiting allies and challenging the Celestial Dragons' rule."
    }
]

def get_random_logpose():
    """
    Fetch a random piece of One Piece lore.
    
    Returns a dict with:
      - success (bool)
      - data (dict with category, name, description) - only on success
      - message (str) - only on failure
    """
    # Try to fetch from external API (optional - can be implemented later)
    # For now, use mock data to ensure the bot always works
    
    try:
        # Simulate API call delay
        import time
        time.sleep(0.3)
        
        # Randomly select a lore entry
        lore = random.choice(MOCK_LORE)
        
        return {
            "success": True,
            "data": lore
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Navigation failed: {str(e)}"
        }

# Optional: Real API integration (uncomment and configure if you have an API key)
# def get_random_logpose_from_api():
#     """
#     Fetch from a real One Piece API if available.
#     """
#     API_URL = "https://api.onepiece.com/v1/lore/random"
#     API_KEY = os.getenv("ONE_PIECE_API_KEY")
#     
#     if not API_KEY:
#         return get_random_logpose()  # Fallback to mock
#     
#     try:
#         headers = {"Authorization": f"Bearer {API_KEY}"}
#         response = requests.get(API_URL, headers=headers, timeout=API_TIMEOUT)
#         
#         if response.status_code == 200:
#             data = response.json()
#             return {
#                 "success": True,
#                 "data": {
#                     "category": data.get("type", "Unknown"),
#                     "name": data.get("name", "Unknown"),
#                     "description": data.get("description", "No description available.")
#                 }
#             }
#         else:
#             return get_random_logpose()  # Fallback to mock
#             
#     except requests.RequestException:
#         return get_random_logpose()  # Fallback to mock