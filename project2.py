from comprpg_classes import Game, Player
from comprpg_data import all_characters, all_items

def play_comprpg(player, turn, active_opponents, history):
    """
    Creates strategy for the actions for the current turn of the game
    """
    if turn == 0:
        # 1st turn: choose two characters to be active
        # Picking characters with the most health to maximise initial strength
        if len(player.characters) >= 2:
            characters = sorted(
                player.characters, key=lambda c: c.get("max_health", 0), 
                reverse=True
            )
            active_characters = [characters[0]["name"], characters[1]["name"]]
        else:
            active_characters = [char["name"] for char in player.characters]
            while len(active_characters) < 2:
                active_characters.append("Default Character")

        # Decide which items to buy
        # Prioritise buying items that are affordable and beneficial
        items_to_buy = []
        total_money = player.money
        for item in all_items:
            if ("cost" in item 
                and item["cost"] <= total_money 
                and item["cost"] > 0):
                items_to_buy.append(item["name"])
                total_money -= item["cost"]

        # Save money for later: Buy only 3 items at max
        items_to_buy = items_to_buy[:3]

        return [active_characters, items_to_buy]

    # If not the 1st turn, decide actions for active characters
    actions = []
    active_characters = player.active_characters
    available_electricity = player.electricity

    for character in active_characters:
        # Try to find an attack move for the character
        character_data = next(
            (char for char in all_characters if char["name"] == character), 
            None)
        if character_data:
            attack_moves = character_data.get("attack_moves", [])
            if attack_moves:
                for move in attack_moves:
                    if (move.get("cost", 0) <= available_electricity 
                        and move.get("damage", 0) > 0):
                        num_targets = move.get("target", 0)
                        if len(active_opponents) >= num_targets:
                            target_list = active_opponents[:num_targets]
                        else:
                            target_list = active_opponents

                        if len(target_list) == num_targets:
                            actions.append(
                                (character, "attack", move["name"], 
                                 move["damage"], num_targets, move["cost"], 
                                 target_list))
                            available_electricity -= move["cost"]
                            break

        # If no attack is possible, try to find a defend move
        if not actions:
            defend_moves = character_data.get("defend_moves", [])
            if defend_moves:
                for move in defend_moves:
                    if (move["cost"] <= available_electricity 
                        and move["protect"] > 0):
                        actions.append((
                            character, "defend", move["name"], 
                            move["protect"], move["cost"]
                        ))
                        available_electricity -= move["cost"]
                        break

    # If no actions were found, try swapping or doing something else
    if not actions:
        # Try swapping to another character if possible
        # Potentially fail if all characters are defeated
        for character in player.characters:
            if (character["name"] not in active_characters 
                and not character.get("defeated", False)):
                actions.append(
                    (active_characters[0], "swap", character["name"])
                )
                break

    # Add a fallback action to ensure 1 action is performed at least
    if not actions:
        actions.append((
            active_characters[0], "defend", "default defence", 1, 0
        ))

    return actions
    