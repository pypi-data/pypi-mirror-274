import os

with open(os.path.join(os.path.dirname(__file__), "version"), mode="r") as fp:
    __version__ = fp.readline().rstrip()

# We import some functions/classes for ease of reference.

# Tool for plotting CDFs with confidence intervals
from mirabolic.cdf.cdf_tools import cdf_plot
from mirabolic.rates.rate_tools import rate_comparison
