from IPython.display import display
import pymbc as mbc
my_dir_path = "pymbc"

from pathlib import Path

def test_mbc():
    csvfile = Path(r'tests\_20230626_PTS__A.csv')
    mb = mbc.MbcLog()
    mb.ReadMbCsv(csvfile)
    fnotes = csvfile.parent / (csvfile.stem + '_notes' + csvfile.suffix)
    mb.ReadNotes(fnotes)
    mb.CreateRunLog()
    plotdef = [mbc.PlotDefinition('Timedelta', 'Depth', 'slategray', '-', False),
               mbc.PlotDefinition('Timedelta', 'Pressure', 'royalblue', '-', False),
               mbc.PlotDefinition('Timedelta', 'Frequency', 'darkorange', '-', False),
               mbc.PlotDefinition('Timedelta', 'Temperature', 'indianred', '--', True)]
    st,figt = mbc.PlotLog(mb, plotdef, title=mb.name, depthaxis=False)
    
    plotdef = [mbc.PlotDefinition('Depth', 'Timedelta', 'black', '-', False),
               mbc.PlotDefinition('Depth', 'Speed', 'forestgreen', '--', True),
               mbc.PlotDefinition('Depth', 'Pressure', 'maroon', '-', False),
               mbc.PlotDefinition('Depth', 'Temperature', 'royalblue', '-', True)]
    sd,figd = mbc.PlotLog(mb, plotdef, title=mb.name, depthaxis=True)  
    pts = mb.PtsWellTestAnalysis()

    assert 'Depth' in mb.logDf.columns