from util.ensemble import ensemble_depths
from model.marigold_pipeline import MarigoldPipeline

def func():
    print("一个神奇的包")
    
def add(a:int,b:int) -> int:
    return a+b

def get_marigold_pipeline():
    # from model.marigold_pipeline import MarigoldPipeline
    return MarigoldPipeline

def get_ensemble_depths():
    # from util.ensemble import ensemble_depths
    return ensemble_depths