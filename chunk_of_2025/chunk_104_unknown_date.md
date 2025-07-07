

以抗性基因为例，抗性基因可能位于染色体和一些移动遗传元件上，如质粒、转座子或整合子，在环境中作为细胞内抗性基

因(iracellular antibiotic resistance genes, iARGs)和细胞外抗性基因(eracellular antibiotic resistance genes, eARGs)存在。

iARGs可通过自我复制传递给后代，也能够通过水平基因转移等方式传递给其他物种；细胞外抗性基因(eARGs)则可能通过

自然转化被细菌吸收。环境中存在的高浓度抗生素，加速了生物膜中ARGs的产生及传播；eARG占总ARGs 60%以上，并

且与游离态eDNA相比，吸附态eDNA更容易与感受态细胞耦合。

来自iMeta

CARD-PLM映射表

CARD Drug Class，39个类

PLM drug class，29个类

映射关系，映射后30个，相比PLM新增4个类，缺少3个类。合并后33类

['alkaloids with antibiotic activity',
'aminocoumarin',
'aminoglycoside',
'antibacterial free fatty acids',
'antibiotic without defined
classification',
'beta-lactam',
'diaminopyrimidine',
'disinfecting agents and
antiseptics',
'elfamycin',
'fluoroquinolone',
'glycopeptide',
'ionophore with antibiotic activity',
'lincosamide',
'macrolide',
'multi-drug',
'nitrofuran',
'nitroimidazole',
'nucleoside',
'oxazolidinone',
'peptide',
'phenicol',
'pleuromutilin',
'polyamine',
'rifamycin',
'streptogramin',
'sulfonamide',
'sulfone',
'tetracenomycin',

'tetracycline']四环素

{   'aminocoumarin antibiotic': 'aminocoumarin',
    'aminoglycoside antibiotic': 'aminoglycoside',
    'antibacterial free fatty acids': 'antibacterial free fatty acids',
    'bicyclomycin-like antibiotic': 'bicyclomycin-like antibiotic',
    'carbapenem': 'beta-lactam',
    'cephalosporin': 'beta-lactam',
    'cephamycin': 'beta-lactam',
    'diaminopyrimidine antibiotic': 'diaminopyrimidine',
    'disinfecting agents and antiseptics': 'disinfecting agents and
antiseptics',
    'elfamycin antibiotic': 'elfamycin',
    'fluoroquinolone antibiotic': 'fluoroquinolone',
    'fusidane antibiotic': 'multi-drug',
    'glycopeptide antibiotic': 'glycopeptide',
    'glycylcycline': 'tetracycline',
    'isoniazid-like antibiotic': 'isoniazid-like antibiotic',
    'lincosamide antibiotic': 'lincosamide',
    'macrolide antibiotic': 'macrolide',
    'monobactam': 'beta-lactam',
    'mupirocin-like antibiotic': 'mupirocin-like antibiotic',
    'nitrofuran antibiotic': 'nitrofuran',
    'nitroimidazole antibiotic': 'nitroimidazole',
    'nucleoside antibiotic': 'nucleoside',
    'orthosomycin antibiotic': 'alkaloids with antibiotic activity',
    'oxacephem': 'beta-lactam',
    'oxazolidinone antibiotic': 'oxazolidinone',
    'penam': 'beta-lactam',
    'penem': 'beta-lactam',
    'peptide antibiotic': 'peptide',
    'phenicol antibiotic': 'phenicol',
    'phosphonic acid antibiotic': 'phosphonic acid antibiotic',
    'pleuromutilin antibiotic': 'pleuromutilin',
    'polyamine antibiotic': 'polyamine',
    'rifamycin antibiotic': 'rifamycin',
    'streptogramin A antibiotic': 'streptogramin',
    'streptogramin B antibiotic': 'streptogramin',
    'streptogramin antibiotic': 'streptogramin',
    'sulfonamide antibiotic': 'sulfonamide',
    'sulfone antibiotic': 'sulfone',
    'tetracycline antibiotic': 'tetracycline'
}

['aminocoumarin antibiotic',
'aminoglycoside antibiotic',
'antibacterial free fatty
acids',
'bicyclomycin-like
antibiotic',
'carbapenem',
'cephalosporin',
'cephamycin',
'diaminopyrimidine
antibiotic',
'disinfecting agents and
antiseptics',
'elfamycin antibiotic',
'fluoroquinolone antibiotic',
'fusidane antibiotic',
'glycopeptide antibiotic',
'glycylcycline',甘氨酰环素
'isoniazid-like antibiotic',
'lincosamide antibiotic',
'macrolide antibiotic',
'monobactam',
'mupirocin-like antibiotic',
'nitrofuran antibiotic',
'nitroimidazole antibiotic',
'nucleoside antibiotic',
'orthosomycin antibiotic',
'oxacephem',
'oxazolidinone antibiotic',
'penam',
'penem',
'peptide antibiotic',
'phenicol antibiotic',
'phosphonic acid antibiotic',
磷霉素 'pleuromutilin
antibiotic',
'polyamine antibiotic',多胺
'rifamycin antibiotic',
'streptogramin A antibiotic',
'streptogramin B antibiotic',
'streptogramin antibiotic',
'sulfonamide antibiotic',
'sulfone antibiotic',
'tetracycline antibiotic']

MIBGC注释整理

耐药类别信息

规则

映射关系（CARD检索）

'bcr':  'export'

mapping = {
    'macrolide': 'macrolide',

有transport的

都是外排机制

有multidrug

的都归为耐多

药

    'gentamicin': 'aminoglycoside',

    'multidrug' : 'multidrug'
'emrb': 'fluoroquinolone',
'teicoplanin':  'glycopeptide',
'bleomycin': 'glycopeptide',
'acriflavin': 'disinfecting agents and antiseptics',
'monensin'    :'ionophore with antibiotic activity',
'16s_rrna_methyltransferase': 'aminoglycoside',
'tetracenomycin' : 'tetracenomycin',
'clorobiocin': 'aminocoumarin',
'sisomicin': 'aminoglycoside'

}

# 耐药机制, 都是自抗性机制
'emrb' : 'antibiotic efflux',
'macrolide_glycosyltransferase': 'antibiotic inactivation',
'16s_rrna_methyltransferase': 'antibiotic target alteration'

'abc_transporter': 'general',
'bicyclomycin',独特的分类系统，
'metal-dependent',

什么是multi-drug

array(['16s_rrna_methyltransferase;_fortimicin_resistance',
       'acriflavin_resistance_protein',
       'antibiotic_resistance_macrolide_glycosyltransferase',
       'antibiotic_resistance_protein',
'bicyclomycin_resistant_protein',

       博来霉素'bleomycin_resisance_protein',
'bleomycin_resistance',
       'bleomycin_resistance_protein',
'cfla_family_protein_putative',
       'cfla_subfamily', 'clorobiocin-resistant_gyrase_b',
'daunorubicin',
      多柔比星 ？？？'daunorubicin_resistance_abc_transporter',
       'daunorubicin_resistance_abc_transporter_atpase_subunit',
       'daunorubicin_resistance_atp-binding_protein_drra',

'daunorubicin_resistance_protein_drra_family_abc_transporter_atp
-binding_protein',
       'daunorubicin_resistance_protein_drrc',
       'daunorubicin_resistance_transmembrane_protein',
     'dioxygenase', 'dioxygenase_superfamily',
      阿霉素？？？ 'doxorubicin_resistance_abc_transporter',

'doxorubicin_resistance_abc_transporter_permease_protein_drrb',
       'doxorubicin_resistance_atp-binding_protein_drra',
       'drug-resistance_pump',
'drug_resistance_related_regulator',
       'drug_resistance_transporter',
'drug_resistance_transporter_bcr',
       'drug_resistance_transporter_emrb',
       'efflux_pump_antibiotic_resistance_protein_putative',
'emrb',
       'enediyne_self-sacrifice_resistance_protein', 'exporter',
       'gentamicin_resistance_ribosomal_methyl_transferase',
'glyoxalase',乙
二醛酶
'major_facilitator_superfamily_transporter_multidrug_resistance_
protein',
       'metal-dependent_hydrolase_(resistance)',

       ？？？'methylenomycin_a_resistance_protein_mmr',
       'mfs_multidrug_resistance_transporter_putative',
       'multidrug_resistance_abc_transporter_atp-
binding_and_permease_protein',
       'multidrug_resistance_protein',
       'multidrug_resistance_protein_mdtg',
       'multidrug_resistance_protein_stp',
       'putative_abc_multidrug_resistance_transporter',
       'putative_drug_resistance_transporter',
'putative_glyoxalase',
       'putative_monensin_resistance_protein',
       'putative_multidrug_resistance_efflux_protein',
       'putative_multidrug_resistance_pump',
       ？？？'putative_netropsin_resistance_protein_subunit_1',
       'putative_netropsin_resistance_protein_subunit_2',
       'putative_resistance_protein',
       'putative_resistance_protein_transporter',

