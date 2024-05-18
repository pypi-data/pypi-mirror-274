
from .Data import RVData, PHOTdata, GAIAData, ETData
from .RVmodel import RVmodel
from .GPmodel import GPmodel

from .RVFWHMmodel import RVFWHMmodel
from .TRANSITmodel import TRANSITmodel
from .RVFWHMRHKmodel import RVFWHMRHKmodel

from .OutlierRVmodel import OutlierRVmodel
from .BINARIESmodel import BINARIESmodel
from .GAIAmodel import GAIAmodel
from .RVGAIAmodel import RVGAIAmodel
from .ETmodel import ETmodel

__models__ = (
    RVmodel,
    GPmodel,
    RVFWHMmodel,
    RVFWHMRHKmodel,
    TRANSITmodel,
    OutlierRVmodel,
    BINARIESmodel,
    GAIAmodel,
    RVGAIAmodel,
    ETmodel,
)

# add plot method to data classes
from .pykima.display import plot_RVData
RVData.plot = plot_RVData


# kima.run
from .Sampler import run
# kima.load_results
from .pykima.results import load_results #, KimaResults
# kima.cleanup
from .pykima.cli import cli_clean as cleanup

# sub-packages
from .kepler import keplerian
#from . import spleaf
from . import distributions

# examples
from . import examples
