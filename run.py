from population import Population



def main(weights):
    SIZE = 1
    p = Population(SIZE, play_weights=weights)
    p.play()


if __name__ == '__main__':
    # Trained weights
    weights = [-0.49965614409808135, -0.32196528325935436, -0.4140410324419228, -0.2299787158740888, -0.20876739983437947, 0.4383595964482666, -0.6127204307375033, -0.46870807702322737, -0.4210204056839687]
    main(weights)
