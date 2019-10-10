#!/usr/bin/env python3

"""The scripts takes a table of drug resistance characteristics in tydy format and an edge list, and then output a table
 with edges and shared drug resistance
"""

import argparse
import csv

__author__ = "Sergey Knyazev"
__credits__ = ["Sergey Knyazev, Ellsworth Campbell"]
__email__ = "sergey.n.knyazev@gmail.com"


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-n', '--nodes', required=True, type=str, dest='node_csv',
                            help='list of drug resistant mutation associated to a patient id in csv tidy format.'
                            'The first column should be a patient id')
    arg_parser.add_argument('-e', '--edges', required=True, type=str, dest='edge_csv',
                            help='list of edges in csv format. The first two columns should be source and target names,'
                                 'the third one should be the distance')
    arg_parser.add_argument('-o', '--out_csv', required=True, type=str, dest='out_csv',
                            help='name of output csv file')
    return arg_parser.parse_args()


def parse_nodes(node_csv):
    nodes = dict()
    drms = set()
    with open(node_csv) as csvfile:
        node_reader = csv.DictReader(csvfile)
        n = next(node_reader)
        attrs = list(n.keys())
        for n in node_reader:
            node_name = n[attrs[0]]
            drm = n[attrs[1]]
            drms.add(drm)
            if node_name not in nodes:
                nodes[node_name] = set()
            nodes[node_name].add(drm)
    return nodes, drms


def parse_edges(edge_csv):
    edges = list()
    with open(edge_csv) as csvfile:
        edge_reader = csv.DictReader(csvfile)
        n = next(edge_reader)
        attrs = list(n.keys())
        col_names = attrs[:3]
        for n in edge_reader:
            source_name = n[attrs[0]]
            target_name = n[attrs[1]]
            dist = n[attrs[2]]
            edges.append((source_name, target_name, dist))
    return edges, col_names


if __name__ == "__main__":
    args = parse_args()
    node_attributes, drms = parse_nodes(args.node_csv)
    drms = sorted(drms)
    edges, col_names = parse_edges(args.edge_csv)
    with open(args.out_csv, 'w') as f:
        f.write(','.join(col_names + drms)+'\n')
        for s, t, d in edges:
            f.write(",".join([s, t, d] +
                             ["0" if s not in node_attributes or
                                     t not in node_attributes or
                                     m not in node_attributes[s] or
                                     m not in node_attributes[t]
                              else "1" for m in drms])+'\n')
