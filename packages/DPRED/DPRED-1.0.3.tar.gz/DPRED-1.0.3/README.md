
===============================================================================
   This is an implementation for automatic HMM-based domain prediction and k-fold cross-validation, in Python. The program still needs some optimization, and it will require more or less 7 minutes to finish. It uses mTM-align and HMMER packages, for which you can find the references here.

   REQUIREMENTS:
     HMMER and BioPython have to be installed. Also, check for your Python built-in modules availability in the distribution depository.

   DISCLAIMER:
     Permission is granted to use, copy, modify, and distribute this program for any purpose, with or without fee, provided that the notices in the header, reference information, and this copyright notice are included in all copies or substantial portions of the software. The software is provided "as is," without any express or implied warranty.

===============================================================================

=========================
 How to install DPRED
=========================
pip install DPRED

You can find further informations at: https://pypi.org/project/DPRED/

=====================
 How to use DPRED
=====================
 Usage: dpred --pfam <PFAM ID> -k <k fold> -l <domain length range> [Options]
 Options:
   --pfam PFAM                      The protein family domain PFAM identifier, e.g. PF00014

   -k K                             The number of folds to on which to base the cross-validation procedure

   -l range                         The domain lenght range. Has to be specified with a ":", e.g. 50:80

   -n name                          The domain's name. It will be written in the .hmm and .txt valdidation files. Default is "domain"

   --res resolution                 The maximum resolution of PDB structures on which to base the HMM generation

   --mut mutation count             The mutation count per pdb structure. Default is 0

   --iden identity                  The percentage of sequence identity used for grouping pdb entities. Default is 50

   --bid blast identity             The percentage of sequence identity used for positives blast selection. Default is 95.

   --mtm msa directory              Keep the MSA directory. Default is False.
   
   --msa msa file                   Keep the MSA directory. Default is False.
   
   --pdb PDB directory              Keep the PDB structures directory. Default is False.
   
   --chunks chunks directory        Keep the chunks directory generated during the cross-validation procedure. Default is False.
   
   --sets sets directory            Keep the sets directory generated during the cross-validation procedure. Default is False.
   
   --db blast database directory    Keep the blast database directory. Default is False.