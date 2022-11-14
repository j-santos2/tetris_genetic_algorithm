from population import Population



def main(weights):
    SIZE = 1
    p = Population(SIZE, play_weights=weights)
    p.play()


if __name__ == '__main__':
    # Trained weights
    # GEN 0 20pop (untrained) fitness=164
    # weights = [-0.28042501, 0.4366274, 0.24890294, 0.26809393, 0.41633996, 0.43888306, 0.06801367]
    # GEN 0 20pop (untrained best) fitness=4706
    # weights = [-0.24283289,  0.31357166, -0.27310741, 0.46267076, -0.39385909, -0.20031742, -0.16421708]
    # GEN 4 20pop (best) fitness=18108
    # weights = [-0.3096281749397588, 0.3135716572680667, -0.2731074119584489, 0.4626707600431673, -0.39385908676727044, -0.20031741876909237, -0.16421708328625317]
    # GEN 8 20pop (best) fitness=21540
    # weights = [-0.500666578231783, 0.3135716572680667, -0.24029962470543792, 0.4626707600431673, -0.37819247132962164, -0.1529320456424909, -0.16870519845682644]
    # GEN 13 20pop (best) fitness=614355
    # weights = [-0.500666578231783, 0.3135716572680667, -0.05722215021970961, 0.4626707600431673, -0.37819247132962164, -0.1529320456424909, -0.16870519845682644]
    # GEN 15 20pop (best) fitness=1064070
    # weights = [-0.500666578231783, 0.3135716572680667, -0.07187762204485185, 0.4626707600431673, -0.37819247132962164, -0.1529320456424909, -0.16870519845682644]
    weights = [-0.2946477618668636, -0.4993783661544299, -0.066506647939826, 0.18804909470556155, -0.05780594883244905, -0.049325553536466595, 0.05592647788841032]
    main(weights)
