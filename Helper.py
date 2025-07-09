import pandas as pd
import numpy  as np

def ParsePercent(pct: str) -> float:
    try:
        args = pct.strip().split("%")
        return float(args[0]) / 100
    except:
        return 0.0

def ParseRatios(ratio: str) -> float:
    try:
        args = ratio.strip().split("of")

        if args[1] == 0:
            return 0.0
        return float(args[0]) / float(args[1])
    except:
        return 0.0

def ParseTime(time: str) -> int:
    try:
        args = time.strip().split(":")
        return 60 * float(args[0]) + float(args[1])
    except:
        return 0.0



def ParseCntrlTime(df: pd.DataFrame) -> None:
    for mod in ['A', 'B']:
        df[f'{mod}_Ctrl'] = df[f'{mod}_Ctrl'].apply(ParseTime)

    denom = df['A_Ctrl'] + df['B_Ctrl']
    df['A_Ctrl_%'] = np.where(denom == 0, 0, df['A_Ctrl'] / denom)
    df['B_Ctrl_%'] = np.where(denom == 0, 0, df['B_Ctrl'] / denom)
    
def ParseTds(df: pd.DataFrame) -> None:
    for mod in ['A', 'B']:
        df[f'{mod}_Td_%'] = df[f'{mod}_Td'].apply(ParseRatios)

def ParseSignificantStrikes(df: pd.DataFrame) -> None:
    for mod in ['A', 'B']:
        df[f'{mod}_Sig._str._%'] = df[f'{mod}_Sig._str._%'].apply(ParsePercent)