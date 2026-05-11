import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *

generator = cms.EDFilter("Pythia8PtGun",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(True),
        
    PGunParameters = cms.PSet(
        ParticleID = cms.vint32(9120443),  # X(3872) PDG ID
        AddAntiParticle = cms.bool(False),  # No antiparticles needed
        MinPt = cms.double(0.0),            # Zero pT for UPC
        MaxPt = cms.double(0.02),          # Essentially zero
        MinEta = cms.double(-2.5),
        MaxEta = cms.double(2.5),
        MinPhi = cms.double(-3.14159265359),
        MaxPhi = cms.double(3.14159265359)
    ),

    # Decay settings - let X(3872) decay to J/psi rho
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            use_default_decay = cms.untracked.bool(False),            
            decay_table = cms.string('GeneratorInterface/ExternalDecays/data/incl_UPC_X3872_Jpsipipi.dec'),
            particle_property_file = cms.FileInPath(
                "GeneratorInterface/ExternalDecays/data/evt.pdl"
            ),
            list_forced_decays = cms.vstring('myX(3872)','MyJ/psi','Myrho0'),            
            operates_on_particles = cms.vint32(9120443),
            convertPythiaCodes = cms.untracked.bool(True)
        ),
        parameterSets = cms.vstring("EvtGen130")
    ),

    Verbosity = cms.untracked.int32(1),     # Set to 1 for debug output
    psethack = cms.string('X(3872) UPC gun'),
    firstRun = cms.untracked.uint32(1),

    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        processParameters = cms.vstring(
            'ParticleDecays:allowPhotonRadiation = on',
            '9120443:all = myX(3872) myX(3872) 3 0 0 3.87169 0.0008 3.870 3.873 0',
            '9120443:mayDecay = on'            
        ),        
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'processParameters'
        )
    )
)

# Filter on muons from X(3872) -> J/psi(->mu mu) rho(->pi pi)
# Require muons in |eta| < 2.5
mumugenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(0.5, 0.5),
    MinP = cms.untracked.vdouble(0.0, 0.0),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13)
)

# Filter on pions from X(3872) -> J/psi rho(->pi pi)
# Require pions in |eta| < 3.0
pipiGenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(0.1, 0.1),
    MaxEta = cms.untracked.vdouble(3.0, 3.0),
    MinEta = cms.untracked.vdouble(-3.0, -3.0),
    ParticleCharge = cms.untracked.int32(-1),  # Opposite charges
    ParticleID1 = cms.untracked.vint32(211),   # pi+
    ParticleID2 = cms.untracked.vint32(211)   # pi-
)

ProductionFilterSequence = cms.Sequence(generator * mumugenfilter * pipiGenfilter)
