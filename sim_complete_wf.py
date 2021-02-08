import msprime
import tskit
import sys
from argparse import ArgumentParser
import json

parser = ArgumentParser("sim_complete")

parser.add_argument("input_ts", help="input incomplete tree sequence")
parser.add_argument("output_ts", help="output tree sequence file")
parser.add_argument(
    "-N", "--population-size", help="Effective population size", type=int, default=1_000
)

args = parser.parse_args()
ts = tskit.load(args.input_ts)

# read the recombination map from the provenance
provenance = json.loads(ts.provenance(0).record)
ts_recomb_rate = provenance["parameters"]["recombination_rate"]

sim = msprime.simulate(
    from_ts=ts, model="dtwf", Ne=args.population_size, recombination_rate=ts_recomb_rate
)

sim.dump(args.output_ts)