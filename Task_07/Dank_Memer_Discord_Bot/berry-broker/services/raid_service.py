import random
from datetime import datetime, timedelta

from database.connection import get_connection, close_connection
from services.economy_service import get_or_create_user
from config import (
    BASE_RAID_SUCCESS_CHANCE,
    RAID_STEAL_PERCENTAGE,
    RAID_PENALTY_PERCENTAGE,
    MIN_RAID_AMOUNT,
    RAID_COOLDOWN_MINUTES
)


def attempt_raid(raider_name, target_name):
    """
    Attempt to raid another pirate.
    
    Returns a dict with:
      - attempted (bool): False if validation failed before the raid
      - success (bool): True if raid succeeded, False if failed
      - message (str): Description of outcome
      - amount (int): Berries stolen or lost
      - raider_new_balance (int): Raider's wallet after the raid
    """
    # Can't raid yourself
    if raider_name.lower() == target_name.lower():
        return {
            "attempted": False,
            "success": False,
            "message": "You can't raid yourself, ya fool!",
            "amount": 0,
            "raider_new_balance": 0
        }
    
    # Ensure both users exist
    raider = get_or_create_user(raider_name)
    target = get_or_create_user(target_name)
    
    # Check raider has minimum berries
    if raider["wallet"] < MIN_RAID_AMOUNT:
        return {
            "attempted": False,
            "success": False,
            "message": f"You need at least {MIN_RAID_AMOUNT} 🍓 to attempt a raid.",
            "amount": 0,
            "raider_new_balance": raider["wallet"]
        }
    
    # Check cooldown
    last_raid_val = raider["last_raid"] if "last_raid" in raider.keys() else None
    if last_raid_val:
        try:
            last_raid = datetime.fromisoformat(last_raid_val)
            cooldown_end = last_raid + timedelta(minutes=RAID_COOLDOWN_MINUTES)
            if datetime.now() < cooldown_end:
                remaining = cooldown_end - datetime.now()
                minutes = max(1, (remaining.seconds // 60) + (1 if remaining.seconds % 60 > 0 else 0))
                return {
                    "attempted": False,
                    "success": False,
                    "message": f"Your crew is still recovering. Try again in {minutes} minutes.",
                    "amount": 0,
                    "raider_new_balance": raider["wallet"]
                }
        except (ValueError, TypeError):
            pass  # If last_raid is invalid, ignore cooldown
    
    # Check target has berries to steal
    if target["wallet"] < MIN_RAID_AMOUNT:
        return {
            "attempted": False,
            "success": False,
            "message": f"{target_name} doesn't have enough berries to raid! (Minimum: {MIN_RAID_AMOUNT} 🍓)",
            "amount": 0,
            "raider_new_balance": raider["wallet"]
        }
    
    # Calculate success chance
    success_chance = BASE_RAID_SUCCESS_CHANCE
    
    # Check for raid-boosting items
    conn = get_connection()
    try:
        has_compass = conn.execute(
            """SELECT inv.quantity FROM inventory inv
               JOIN items i ON inv.item_id = i.id
               WHERE inv.user_id = ? AND LOWER(i.name) = 'berry compass'""",
            (raider["id"],)
        ).fetchone()
        
        if has_compass and has_compass["quantity"] > 0:
            success_chance += 0.10  # +10% from Berry Compass
        
        # Check for Sea Stone on target (defensive item)
        has_sea_stone = conn.execute(
            """SELECT inv.quantity FROM inventory inv
               JOIN items i ON inv.item_id = i.id
               WHERE inv.user_id = ? AND LOWER(i.name) = 'sea stone'""",
            (target["id"],)
        ).fetchone()
        
        if has_sea_stone and has_sea_stone["quantity"] > 0:
            success_chance -= 0.15  # -15% if target has Sea Stone
        
        # Clamp success chance between 0.1 and 0.9
        success_chance = max(0.1, min(0.9, success_chance))
        
    finally:
        close_connection(conn)
    
    # Roll the dice
    raid_succeeded = random.random() < success_chance
    
    # Calculate amount
    if raid_succeeded:
        # Steal 20% of target's wallet
        steal_amount = int(target["wallet"] * RAID_STEAL_PERCENTAGE)
        steal_amount = max(MIN_RAID_AMOUNT, steal_amount)  # Minimum steal
        steal_amount = min(steal_amount, target["wallet"])  # Can't steal more than they have
    else:
        # Lose 10% of raider's wallet as penalty
        penalty_amount = int(raider["wallet"] * RAID_PENALTY_PERCENTAGE)
        penalty_amount = max(MIN_RAID_AMOUNT, penalty_amount)  # Minimum penalty
        penalty_amount = min(penalty_amount, raider["wallet"])  # Can't lose more than they have
    
    # Execute the raid atomically
    conn = get_connection()
    try:
        conn.execute("BEGIN")
        
        if raid_succeeded:
            # Raider steals from target
            conn.execute(
                "UPDATE users SET wallet = wallet + ? WHERE id = ?",
                (steal_amount, raider["id"])
            )
            conn.execute(
                "UPDATE users SET wallet = wallet - ? WHERE id = ?",
                (steal_amount, target["id"])
            )
            
            # Record transactions
            conn.execute(
                """INSERT INTO transactions (user_id, type, amount, target_user_id, description)
                   VALUES (?, ?, ?, ?, ?)""",
                (raider["id"], "raid_win", steal_amount, target["id"],
                 f"Raided {target_name} and stole {steal_amount:,} berries")
            )
            conn.execute(
                """INSERT INTO transactions (user_id, type, amount, target_user_id, description)
                   VALUES (?, ?, ?, ?, ?)""",
                (target["id"], "raid_loss", -steal_amount, raider["id"],
                 f"Raided by {raider_name}, lost {steal_amount:,} berries")
            )
            
            amount_changed = steal_amount
            
        else:
            # Raider pays penalty to target
            conn.execute(
                "UPDATE users SET wallet = wallet - ? WHERE id = ?",
                (penalty_amount, raider["id"])
            )
            conn.execute(
                "UPDATE users SET wallet = wallet + ? WHERE id = ?",
                (penalty_amount, target["id"])
            )
            
            # Record transactions
            conn.execute(
                """INSERT INTO transactions (user_id, type, amount, target_user_id, description)
                   VALUES (?, ?, ?, ?, ?)""",
                (raider["id"], "raid_loss", -penalty_amount, target["id"],
                 f"Failed raid on {target_name}, paid {penalty_amount:,} berries penalty")
            )
            conn.execute(
                """INSERT INTO transactions (user_id, type, amount, target_user_id, description)
                   VALUES (?, ?, ?, ?, ?)""",
                (target["id"], "raid_win", penalty_amount, raider["id"],
                 f"Defended against {raider_name}, gained {penalty_amount:,} berries")
            )
            
            amount_changed = penalty_amount
        
        # Update raider's last_raid timestamp
        conn.execute(
            "UPDATE users SET last_raid = ? WHERE id = ?",
            (datetime.now().isoformat(), raider["id"])
        )
        
        conn.commit()
        
        # Get updated balance
        updated_raider = conn.execute(
            "SELECT wallet FROM users WHERE id = ?",
            (raider["id"],)
        ).fetchone()
        
        return {
            "attempted": True,
            "success": raid_succeeded,
            "message": "Raid successful!" if raid_succeeded else "Raid failed!",
            "amount": amount_changed,
            "raider_new_balance": updated_raider["wallet"]
        }
        
    except Exception as e:
        conn.rollback()
        return {
            "attempted": True,
            "success": False,
            "message": f"Raid failed due to an error: {str(e)}",
            "amount": 0,
            "raider_new_balance": raider["wallet"]
        }
    finally:
        close_connection(conn)