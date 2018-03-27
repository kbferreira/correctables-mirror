.PHONY:  all clean

FIGS_DIR =../figs

DIRS = $(sort $(dir $(wildcard ../data/*/*/)))

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

print-%  : ; @echo $* = $($*)

all: ${FIGSdetour} ${FIGSscaling} ${FIGSdelta}

${PATTERNdelta}: ${DATAdelta} ${SCRIPTdelta}
	${SCRIPTdelta}

${PATTERNscaling}: ${DATAscaling} ${SCRIPTscaling}
	${SCRIPTscaling}

${PATTERNdetour}: ${DATAdetour} ${SCRIPTdetour}
	${SCRIPTdetour}

print-%  : ; @echo $* = $($*)

clean:
	-rm -f ${FIGSdetour} ${FIGSscaling} ${FIGSdelta}
	-rm -f ${FIGS_DIR}/*.pdf
