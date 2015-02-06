#!/usr/bin/env python
import subprocess
import shutil
from graftm.HouseKeeping import HouseKeeping

class Pplacer:
    
    def __init__(self, refpkg):
        self.refpkg = refpkg
        self.HK = HouseKeeping()
    
    # run pplacer
    def pplacer(self, ts_file, threads, base_list):
        cmd = "pplacer -j %s --verbosity 0 -c %s %s" % (threads, self.refpkg, ts_file)
        # log
        subprocess.check_call(cmd, shell=True)
        
        for src, dest in zip([x+'_hits.aln.jplace' for x in base_list], [x+'/'+x+'_placements.jplace' for x in base_list]):
            shutil.move(src, dest)
        
    
    # run guppy classify
    def guppy_class(self, guppy_path, base_list, GM_temp):
    
        guppy_main = GM_temp + 'Graftm' + guppy_path
        jplace_list = [x+'/'+x+'_placements.jplace' for x in base_list]
    
        cmd = 'guppy classify -c %s %s > %s' % (self.refpkg, ' '.join(jplace_list), guppy_main)
        # log
    
        subprocess.check_call(cmd, shell=True)
        
        
        # Split the guppy and distribute into ouput files
        guppy = []
        report = {}
    
        for line in open(guppy_main, 'r'):
    
            if 'name' in line:
                if len(guppy) == 0:
                    guppy.append(line)
    
                else:
                    out =  guppy[1].split()[5].replace('_placements', '')
                    r_num = 0
                    seen = []
                    for l in guppy:
                        if not l.startswith('name'):
    
                            seq_id = l.rstrip().split()[0]
                            if seq_id not in seen:
                                seen.append(seq_id)
                                r_num += 1
    
                    report[out] = r_num
                    out = out+'/'+out+'_placements.guppy'
    
                    with open(out, 'w') as out_guppy:
                        for l in guppy:
                            out_guppy.write(l)
    
                    guppy = []
    
                    guppy.append(line)
    
            else:
                guppy.append(line)
    
    
        # Write the last guppy file
    
        out =  guppy[1].split()[5].replace('_placements', '')
    
        r_num = 0
        seen = []
        for line in guppy:
            if not line.startswith('name'):
    
                seq_id = line.rstrip().split()[0]
                if seq_id not in seen:
                    seen.append(seq_id)
                    r_num += 1
    
        report[out] = r_num
    
        out = out+'/'+out+'_placements.guppy'
    
        with open(out, 'w') as out_guppy:
            for line in guppy:
                out_guppy.write(line)
    
        self.HK.delete(['GraftM.guppy'])
    
        return report