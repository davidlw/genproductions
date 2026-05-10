import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *

source = cms.Source("EmptySource")

generator = cms.EDFilter(
    "Pythia8PtGun",
    PGunParameters = cms.PSet(
        ParticleID = cms.vint32(9120443),  # X(3872) PDG ID
        AddAntiParticle = cms.bool(False),  # No antiparticles needed
        MinPt = cms.double(0.0),            # Zero pT for UPC
        MaxPt = cms.double(0.001),          # Essentially zero
        MinEta = cms.double(-2.5),
        MaxEta = cms.double(2.5),
        MinPhi = cms.double(-3.14159265359),
        MaxPhi = cms.double(3.14159265359)
    ),
    # Decay settings - let X(3872) decay to J/psi rho
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.FileInPath(
                "GeneratorInterface/ExternalDecays/data/incl_UPC_X3872_Jpsipipi.dec"
            ),
            particle_property_file = cms.FileInPath(
                "GeneratorInterface/ExternalDecays/data/evt.pdl"
            ),
            user_decay_embedded = cms.vstring(),
            list_forced_decays = cms.vstring('myX(3872)'),
            operates_on_particles = cms.vint32()
        ),
        parameterSet = cms.string("EvtGen130")
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        parameterSets = cms.vstring('pythia8CommonSettings')
    )    
    Verbosity = cms.untracked.int32(1),     # Set to 1 for debug output
    psethack = cms.string('X(3872) UPC gun'),
    firstRun = cms.untracked.uint32(1),
)

ProductionFilterSequence = cms.Sequence(generator)
