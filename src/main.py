from InfoSimulator import *
import sys
import getopt

def get_interval():
    broad_interval = [-0.5, 0.5]
    tight_interval = [-0.9, 0.1]

    while True:
        option = input("Choose Uncertainty Intervals")
        try:
            if option.isdigit():
                if int(option) > 6:
                    raise ValueError

            elif option == "quit":
                raise Exception
            break
        except ValueError:
            print("This is not a number. Please enter a valid number or type 'quit' to close the game")
        except Exception:
            print("Gracefully quiting game")
            exit(0)

    return int(option)


def usage(prog):
    print(f"Usage: {prog} [OPTIONS]")
    print("Description")
    print("\tThe purpose of this program is to simulate a Red vs. Blue scenerio where information is the main weapon")
    print("Option")
    print("\tIf no options are used default intervals, grey proportion and connection probablities will be applied will be applied\n")
    print("\t-h\tdisplay this help and exit\n")
    print("\t-s\twill run simulations and save any outputs to the logs and graphs folder\n")


if __name__ == "__main__":

    # Example of current acceptable inputs
    # May change as we learn more and program evolves
    num_green = 10
    percent_will_vote = 0.5
    broad_interval = [-0.5, 0.5]
    tight_interval = [-0.9, 0.1]
    connect_prob_1 = [1000, 0.20] # I think if I can remember probability! the probroablity of num_greens knowing each other is 50%
    connect_prob_2 = [50, 0.1] # num_greens knowing each other is 10%, again might need to confirm n and p values
    grey_proportion_high = 0.8 # 80% chance grey is working for Red team
    grey_proportion_low = 0.1 # 10% chance grey is working for Red team

    default_option = ''

    simulate = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hstb", ["help", "simulate", "tight", "broad"])
        prog = sys.argv[0]
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage(sys.argv[0])
        sys.exit(2)
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage(prog)
            sys.exit()
        elif o in ("-s", "--simulate"):
            simulate = True
        elif o in ("-t", '--tight'):
            default_option = 'tight'
        elif o in ("-b", '--broad'):
            default_option = 'broad'
        else:
            assert False, "unhandled option"


    if simulate:
        # Redirecting the print function to the void
        sys.stdout = open(os.devnull, 'w')

        if default_option == 'tight':
            sim = InfoSimulator(tight_interval, connect_prob_1[0], connect_prob_1[1], grey_proportion_low, simulate=simulate)
            sim.run()
        elif default_option == 'broad':
            sim = InfoSimulator(broad_interval, connect_prob_1[0], connect_prob_1[1], grey_proportion_low, simulate=simulate)
            sim.run()
    else:
        sim = InfoSimulator(broad_interval, connect_prob_1[0], connect_prob_1[1], grey_proportion_low)
        sim.run()
    #sim.print_distrubution_graph(display="distribution")
    #sim.print_distrubution_graph(display="graph")

    #sim.print_green_adjlist()

