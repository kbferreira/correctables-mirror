.PHONY:  all clean

FIGS_DIR =../figs

DIRS = $(sort $(dir $(wildcard ../data/*/*/)))

DATAdetour = $(wildcard ../data/DRAM-correctable-einj/*/*.data)
FIGSdetour = $(addprefix ${FIGS_DIR}/, $(notdir $(DATAdetour:.data=_dtr.eps)))
PATTERNdetour = $(subst selfish,%,${FIGSdetour})
SCRIPTdetour = ./detour.py 

print-%  : ; @echo $* = $($*)

all: ${FIGSdetour}

${PATTERNdetour}: ${DATAdetour} ${SCRIPTdetour}
	${SCRIPTdetour}

print-%  : ; @echo $* = $($*)

clean:
	-rm -f ${FIGSdetour}
	-rm -f ${FIGS_DIR}/*.pdf
