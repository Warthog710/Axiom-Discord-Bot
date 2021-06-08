import json
import random

class markovNameGenerator:
    def __init__(self, order):
        self.__order = order
        self.__name_starts = []
        self.__markov_map = {}
        name_starts_found = self.__loadNameStarts()
        map_found = self.__loadMarkovMap()

        # If the files didn't exist, or were not loaded, generate a new map from the name bank
        if not name_starts_found or not map_found:
            print('No markov_map found, attempting to generate a new map...')
            self.__generateMarkovMap()

    def __dumpMap(self):
        json_out = open('./Config/markov_map.json', 'w')
        json.dump(self.__markov_map, json_out, indent=4)
        json_out.close()

    def __dumpNameStarts(self):
        name_out = open('./Config/name_starts.txt', 'w')
        for start in self.__name_starts:
            name_out.write(start + '\n')

        name_out.close()

    def __loadNameStarts(self):
        try:
            nameBank = open('./Config/name_starts.txt', 'r')
            for line in nameBank:
                self.__name_starts.append(line.strip())
            nameBank.close()
        except Exception as e:
            print(e)
            return False

        return True

    def __loadMarkovMap(self):
        try:
            markov_json = open('./Config/markov_map.json', 'r')
            self.__markov_map = json.load(markov_json)
            markov_json.close()
        except Exception as e:
            print(e)
            return False

        return True

    def __generateMarkovMap(self):
        nameBank = open('./Config/name_bank.txt')
        nameList = []

        # Read the names from the bank
        for line in nameBank:
            nameList.append(line.strip())

        nameBank.close()

        # Generate the markov map
        for name in nameList:
            for x in range(0, len(name) - self.__order):
                ngram = name[x : x + self.__order]

                # Save the name starts
                if ngram[0].isupper() and ngram not in self.__name_starts:
                    self.__name_starts.append(ngram)

                # If the ngram is not in the map, create a new list
                if ngram not in self.__markov_map:
                    self.__markov_map[ngram] = []

                # Save the ngram
                self.__markov_map[ngram].append(name[x + self.__order])

        # Dump map and starts for later use
        self.__dumpMap()
        self.__dumpNameStarts()

    async def generateName(self, length):
        #Grab a random start
        result = random.choice(self.__name_starts)

        # Determine length
        if length == None:
            length = random.randint(3, 10)

        # Generate name
        for x in range(length - self.__order):
            currentGram = result[x : x + self.__order]
            if currentGram not in self.__markov_map:
                break
            else:
                result += random.choice(self.__markov_map[currentGram])

        return result