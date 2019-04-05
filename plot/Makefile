.PHONY:  all clean

FIGS_DIR =../figs

DIRS = $(sort $(dir $(wildcard ../data/*/*/)))

DATAConfigs = $(wildcard ../data/configs/*.delta)
FIGSConfigs = $(addprefix ${FIGS_DIR}/, $(notdir $(DATAConfigs:.delta=.png)))
PATTERNConfigs = $(subst MTBF,%,${FIGSConfigs})
SCRIPTConfigs = ./correctable_bar.py

DATA5HZ = $(wildcard ../data/bursty-5Hz/*.scale)
FIGS5HZ = $(addprefix ${FIGS_DIR}/, $(notdir $(DATA5HZ:.scale=-apps-scale.pdf)))
PATTERN5HZ = $(subst 5Hz,%,${FIGS5HZ})
SCRIPT5HZ = ./scale.py

DATAFreq = $(wildcard ../data/bursty-775us/*.freq)
FIGSFreq = $(addprefix ${FIGS_DIR}/, $(notdir $(DATAFreq:.freq=-apps-freq.pdf)))
PATTERNFreq = $(subst nodes,%,${FIGSFreq})
SCRIPTFreq = ./freq.py

DATADelta5HZ = $(wildcard ../data/bursty-5Hz/*.delta)
FIGSDelta5HZ = $(addprefix ${FIGS_DIR}/, $(notdir $(DATADelta5HZ:.delta=-apps-delta.pdf)))
PATTERNDelta5HZ = $(subst nodes,%,${FIGSDelta5HZ})
SCRIPTDelta5HZ = ./delta5hz.py

DATAdetour = $(wildcard ../data/DRAM-correctable-einj/*/*.data)
FIGSdetour = $(addprefix ${FIGS_DIR}/, $(notdir $(DATAdetour:.data=_dtr.eps)))
PATTERNdetour = $(subst selfish,%,${FIGSdetour})
SCRIPTdetour = ./detour.py 

SCALING_DIRS = $(sort $(dir $(wildcard ../data/correctables/scaling/*/)))
DATAscaling = ${wildcard ../data/correctables/scaling/*/*.data}
FIGSscaling = $(addprefix ${FIGS_DIR}/, $(SCALING_DIRS:../data/correctables/scaling/%/=%.eps))
PATTERNscaling = $(subst Hz,%,${FIGSscaling})
SCRIPTscaling = ./scaling.py

DATAdelta = $(wildcard ../data/correctables/delta/*.delta)
FIGSdelta = $(addprefix ${FIGS_DIR}/,$(DATAdelta:../data/correctables/delta/%.delta=%-apps-delta.pdf)) \
            $(addprefix ${FIGS_DIR}/,$(DATAdelta:../data/correctables/delta/%.delta=%-micros-delta.pdf))
PATTERNdelta = $(subst delta,%,${FIGSdelta})
SCRIPTdelta  = ./delta.py

all: ${FIGSdetour} ${FIGSscaling} ${FIGSdelta} ${FIGS5HZ} ${FIGSFreq} ${FIGSDelta5HZ} ${FIGSConfigs}

print-%  : ; @echo $* = $($*)

${PATTERNConfigs}: ${DATAConfigs} ${SCRIPTConfigs}
	${SCRIPTConfigs}

${PATTERN5HZ}: ${DATA5HZ} ${SCRIPT5HZ}
	${SCRIPT5HZ}

${PATTERNFreq}: ${DATAFreq} ${SCRIPTFreq}
	${SCRIPTFreq}

${PATTERNDelta5HZ}: ${DATADelta5HZ} ${SCRIPTDelta5HZ}
	${SCRIPTDelta5HZ}

${PATTERNdelta}: ${DATAdelta} ${SCRIPTdelta}
	${SCRIPTdelta}

${PATTERNscaling}: ${DATAscaling} ${SCRIPTscaling}
	${SCRIPTscaling}

${PATTERNdetour}: ${DATAdetour} ${SCRIPTdetour}
	${SCRIPTdetour}

print-%  : ; @echo $* = $($*)

clean:
	-rm -f ${FIGSdetour} ${FIGSscaling} ${FIGSdelta} ${FIGS5HZ} ${FIGSFreq} ${FIGSDelta5HZ} ${FIGSConfigs}
	-rm -f ${FIGS_DIR}/*.pdf
