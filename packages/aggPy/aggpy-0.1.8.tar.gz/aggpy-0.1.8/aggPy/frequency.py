from MDAnalysis.analysis.base import (AnalysisBase, AnalysisFromFunction, analysis_class)
import json
import aggPy.initial_analysis 
import aggPy.workup
import aggPy.timeCorr 

class Analysis:
    def __init__(self, json_file, key):
        with open(json_file) as f:
            args = json.load(f)
            initial = args['init'][0]
            args = args[key][0]
        self.__dict__.update(**initial)
        self.__dict__.update(**args)

    #def atom_mapping(self):
    #    return atom_mapping(self)

    def hCoordination(self):
        aggPy.initial_analysis.init_analysis(self)
        self.atom_map = aggPy.atom_map.atom_mapping(self.universe.atoms)
        self.XYZ = [x for x in self.XYZ.split(',')]
        self.HbondParm = [float(x) for x in self.HbondParm.split(',')]
        
        hbonds =  AnalysisFromFunction(aggPy.MDHbondMain.hbond,self.universe.trajectory,
            topology = self.topology,
            donors = self.donors,
            hydrogens = self.hydrogens,
            acceptors = self.acceptors,
            HbondParm = self.HbondParm,
            box = self.box,
            pre_allo = self.pre_allo,
            XYZ = [eval(self.XYZ[0]), self.atom_map, f'{self.XYZ[1].strip()}.xyz']
        )
        
        if self.run_length == 'n':
            self.length = int((self.end_frame - self.start_frame / self.frame_dt))
            hbonds.run(start=self.start_frame, stop=self.end_frame, step=self.frame_dt)
        else:
            self.length = int(len(self.universe.trajectory))
            hbonds.run()

        results = hbonds.results.timeseries
        output = {}
        for i in range(0,len(results)):
            output[f'result{i}'] = results[i]
        self.__dict__.update(**output)

    def vibSpectra(self):
        return self.bond

    @staticmethod
    def aggregate(data, variable):
        return aggPy.workup.aggregate(data, variable)

    @staticmethod
    def average(data, variable):
        return aggPy.workup.average(data, variable)

    @staticmethod
    def std_dev(data, variable, bin_width=1):
        return aggPy.workup.std_dev(data, variable, bin_width)
    
    @staticmethod
    def timeCorr(data, min_dt=1, max_dt=10, skip_dt=1, t_prop=1, num_mols=1):
        return aggPy.timeCorr(data, min_dt, max_dt, skip_dt, t_prop, num_mols)

    def graphing(data):
        return None

