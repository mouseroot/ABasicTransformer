import random
""" 
Train("Who are you","I am an AI Assistant")
Train("What is your name","My name is Jenna")




 """
class ABasicTransformer:
    def __init__(self):
        self.nodes = {}
        self.weight_incr = 0.01


    def train(self, input_str, keys,triggers=[]):
        # Used to generate nodes
        # they contain the following 
        # 'weight' - a value associated with the node
        # 'keys,  - the keywords used to select the node
        # 'text' - the full response
        # 'triggers' - words that act as command arguments
        # Example: Triggers=['command']
        # would select the words after command
        # run the command ffmpeh.exe --silent
        # the response would be populated with the trigger
        scrub_str = input_str.lower().strip()

        self.nodes[scrub_str] = {
            'value': 0,
            'keys': keys.split(","),
            'text': scrub_str,
            'triggers': triggers,
            'triggers_arg': []
        }
        
        
    def generate(self, phrase,threshold=3):
        print(f"--- Generating from phrase: '{phrase}' ---")
        phrase_tokens = phrase.lower().replace("?","").strip().split(" ")
        results = []
        

        for node in self.nodes:
            #set match counter to 0
            counter = 0
            #Get keys from node
            _keys = self.nodes[node]['keys']
            _triggers = self.nodes[node]['triggers']

            #Check if we have triggers in this node
            if len(_triggers) > 0:
                print(f"Triggers Found")
                #Look through all the triggers and the phrase tokens for a match
                for trigger in _triggers:
                    print(f"Searching for {trigger}")
                    if trigger in phrase_tokens:
                        trigger_index = phrase_tokens.index(trigger)
                        command_phrase = " ".join(phrase_tokens[trigger_index+1:])
                        print(f"!!!FOUND {command_phrase}")
                        self.nodes[node]['trigger_arg'] = command_phrase
            print(f"Searching node: {node}")
            for key in _keys:
                for phrase in phrase_tokens:
                    if key == phrase:
                        print(f"Match {key} == {phrase}")
                        counter += 1
            print(f"Node Match Counter: {counter}")
            if counter >= threshold:
                results.append(node)
        return results

            
                    


aTransform = ABasicTransformer()

aTransform.train("I am an assistant","who,you")
aTransform.train("OKaY im ExecUTING the COMMAND {0}","execute,command",triggers=["command"])
aTransform.train("name is jenna","your,name")
aTransform.train("My favorite color is Black","favorite,color")

while 1:
    try:
        inp = input("?")
        results = aTransform.generate(inp,threshold=2)
        if results:
            first_res = results[0]
            nn_trigger_args = aTransform.nodes[first_res]['trigger_arg']
            if nn_trigger_args:
                print(f"Response Command: {nn_trigger_args}")
                print(f"First Response: {first_res.replace('{0}',nn_trigger_args)}")
            else:
                print(f"Response: {first_res}")
        else:
            print(f"NO Response")
    except KeyboardInterrupt:
        break

print("End!")