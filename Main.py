import textwrap
import openai
import random

openai.api_key = 'YOUR KEY HERE'
# imports everything and key ^

# Chooeses random character setting and item
characters = ["a brave knight", "a cunning thief", "a wise wizard", "a fearless pirate", "a mysterious sorceress", "a vampire", "a blacksmith", "a normal person", "an archer", "an assassin"]
setting = ["an ancient forest", "a bustling medieval town", "a hidden cave deep in the mountains", "a haunted mansion", "a vast desert", "an underwater kingdom in the depths of the ocean", "a magical realm beyond the clouds", "a remote space station in deep space"]
items = ["a gold sword", "a loyal animal companion", "a set of lock-picking tools", "a mysterious key", "a suit of enchanted armor", "a bag of gold coins", "a spellbook with powerful spells"]
current_character = random.choice(characters)
current_setting = random.choice(setting)
item = random.choice(items)
prompt = f"you are a narrator in a build-you-own adventure story, where you in advance choose a win condition but don't tell the user and push them forward in the story, but set them back too. The user is {current_character} in {current_setting} that starts with {item} to aid in the adventure, make the item a crucial part of the story. Make sure that the win condition is very-clear to you and hint at it to the user until the very end. Make it clear that the user won by ending with the text \"You won!\". Try and keep the story relatively short. Always give the user options of what they can do next in the form of Options: Option 1, 2 , 3. TELL THE USER WHAT THEY CAN DO. Don't predict user responses, advance the plot. Write at most two sentences at a time. Tell the user to start the game."

previous =  [
            {
                "role": "system", "content": prompt
            }
        ]

#
def next_move():
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=previous,
            temperature=.88
        )
    total_tokens_used_c = response['usage']['total_tokens']
    price = (total_tokens_used_c / 1000) * .0015
    actual_response = response['choices'][0]['message']['content']
    return actual_response





def main():
    print(f"Welcome to choose your own adventure!\n\nIn this story you are going to be {current_character} in {current_setting} that starts with {item}\nThe narrator is going to give you options to guide you but you are free to respond however you like\n")
    won = False
    # Counter here to check at what point to delete previous messages
    counter = 0
    while not won:
        counter += 1
        print("Iteration: " + str(counter))
        move = next_move()
        # Neatly prints
        print(textwrap.fill(move, width=100))
        if move[-8:] == "You won!":
            won = True
        else:
            # Get user input
            user_response = input("\nUser: ")
            # Append as part of the prompt
            previous.append({"role": "assistant", "content": move})
            previous.append({"role": "user", "content": user_response})

            # Start reseting earlier sequence
            if counter > 8:
                del previous[2:4]



main()
print("Thanks for playing!")
