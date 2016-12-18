import network as net
import pickle


class IntNode(object):
    def __init__(self, line):
        """
        Parse the correct entry in the following format:
        uid @loc [+] [bb] (num_neigh) [&ext] -> <nuid-1> <nuid-2> ... {-euid} ... =name[!] rn

        Look RocketFuel documentation for the detail description.
        """

        entry = line.split()

        self.uid = int(entry[0])
        self.loc = entry[1][1:]

        index = 2
        self.is_dns_loc = (entry[index] == "+")
        index += self.is_dns_loc

        self.is_backbone = (entry[index] == "bb")
        index += self.is_backbone

        # number of neighbours
        index += 1

        # external number
        if entry[index][0] == "&":
            index += 1

        assert(entry[index] == "->")
        index += 1

        self.neighbors = set()
        while entry[index][0] == "<":
            self.neighbors.add(int(entry[index][1:-1]))
            index += 1

        self.euids = set()
        while entry[index][0] == "{":
            self.euids.add(int(entry[index][2:-1]))
            index += 1

        assert(index == len(entry) - 2)
        self.name = entry[-2][1:]
        self.distance = int(entry[-1][1:])


class ExtNode(object):
    def __init__(self, line):
        """
        Parse the correct entry in the following format:
        -euid =externaladdress rn

        Look RocketFuel documentation for the detail description.
        """
        entry = line.split()
        assert(len(entry) == 3)

        self.uid = int(entry[0][1:])
        self.address = entry[1][1:]
        self.distance = int(entry[2][1:])


def parse_rocketfuel_file(filename):
    """
    Build network graph from RocketFuel configuration file.
    IMPORTANT: it is supposed, topology has no parallel edges!
    """

    int_nodes, ext_nodes = [], []
    with open(filename) as fd:
        for line in fd:
            if line[0] == "#":
                continue
            if line[0] == "-":
                ext_nodes.append(ExtNode(line))
            else:
                int_nodes.append(IntNode(line))

    res_net = net.Network('rocketFuel ' + filename)

    shift = 0
    for x in int_nodes:
        res_net.add_node(net.OVSSwitch(ID=x.uid, name="ovs-sw{}".format(x.uid)))
        shift = max(shift, x.uid)  # changed here

    # shift ext_nodes ID
    # change shift

    for x in ext_nodes:
        res_net.add_node(net.Host(ID=x.uid + shift, name="host{}".format(x.uid)))

    for x in int_nodes:
        for yid in x.neighbors:
            # suppose there are no parallel edges
            if not res_net.has_link(x.uid, yid):
                res_net.add_link(x.uid, None, yid, None)
        for yid in x.euids:
            if not res_net.has_link(x.uid, yid + shift):
                res_net.add_link(x.uid, None, yid + shift, None)

    return res_net


if __name__ == "__main__":
    # Parses a given RocketFuel configuration file and dumps it using pickle.

    import argparse

    parser = argparse.ArgumentParser(description='Build graph from given RocketFuel configuration.')
    parser.add_argument('config', type=str, help='path to RocketFuel configuration file')
    parser.add_argument('dump', type=str, help='dump file generation path')
    parser.add_argument('-stat', action="store_true", default=False, help='print nodes and links number')
    args = parser.parse_args()

    conf_file = args.config
    network = parse_rocketfuel_file(conf_file)

    if args.stat:
        print("Number of nodes: {}".format(network.topology.number_of_nodes()))
        print("Number of links: {}".format(network.topology.number_of_edges()))

    f = open(args.dump, 'wb')
    pickle.dump(network, f)
